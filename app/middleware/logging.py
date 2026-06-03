import time
import uuid
import json
import logging

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


# =====================================================
# STRUCTURED LOGGER SETUP
# =====================================================

logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()

formatter = logging.Formatter(
    "%(message)s"
)

handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(handler)


# =====================================================
# SENSITIVE FIELDS FILTER
# =====================================================

SENSITIVE_KEYS = {
    "password",
    "token",
    "authorization",
    "access_token",
    "refresh_token",
}


def sanitize(data: dict) -> dict:
    """
    Remove sensitive fields from logs
    """
    if not isinstance(data, dict):
        return data

    cleaned = {}

    for k, v in data.items():
        if k.lower() in SENSITIVE_KEYS:
            cleaned[k] = "***REDACTED***"
        else:
            cleaned[k] = v

    return cleaned


# =====================================================
# MIDDLEWARE
# =====================================================

class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        start_time = time.time()

        # -------------------------------------------------
        # TRACE ID (CORRELATION ID)
        # -------------------------------------------------
        trace_id = request.headers.get("X-Trace-Id", str(uuid.uuid4()))
        request.state.trace_id = trace_id

        # -------------------------------------------------
        # REQUEST BODY (SAFE READ)
        # -------------------------------------------------
        body = await self._get_body(request)

        log_data = {
            "event": "request_start",
            "trace_id": trace_id,
            "method": request.method,
            "url": str(request.url),
            "headers": dict(request.headers),
            "body": body,
        }

        logger.info(json.dumps(sanitize(log_data)))

        # -------------------------------------------------
        # PROCESS REQUEST
        # -------------------------------------------------
        try:
            response: Response = await call_next(request)

        except Exception as e:

            error_log = {
                "event": "request_error",
                "trace_id": trace_id,
                "error": str(e),
            }

            logger.error(json.dumps(error_log))
            raise

        # -------------------------------------------------
        # RESPONSE TIME
        # -------------------------------------------------
        process_time = time.time() - start_time

        # -------------------------------------------------
        # RESPONSE LOG
        # -------------------------------------------------
        response_log = {
            "event": "request_end",
            "trace_id": trace_id,
            "status_code": response.status_code,
            "process_time_ms": round(process_time * 1000, 2),
            "url": str(request.url),
        }

        logger.info(json.dumps(response_log))

        # -------------------------------------------------
        # ADD TRACE HEADER TO RESPONSE
        # -------------------------------------------------
        response.headers["X-Trace-Id"] = trace_id
        response.headers["X-Response-Time"] = str(process_time)

        return response

    # =====================================================
    # SAFE BODY READER
    # =====================================================

    async def _get_body(self, request: Request):

        try:
            body = await request.body()

            if not body:
                return None

            return json.loads(body.decode("utf-8"))

        except Exception:
            return None