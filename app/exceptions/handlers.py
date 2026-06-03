# from fastapi import Request, status,FastAPI
# from fastapi.responses import JSONResponse
# from fastapi.exceptions import RequestValidationError
# from sqlalchemy.exc import IntegrityError
# from app.utils.logger import logger
# from sqlalchemy.exc import SQLAlchemyError


# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     errors = []
#     for error in exc.errors():
#         field = " -> ".join(str(e) for e in error["loc"])
#         errors.append({"field": field, "message": error["msg"]})
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content={"detail": "Validation error", "errors": errors},
#     )


# async def integrity_error_handler(request: Request, exc: IntegrityError):
#     logger.error(f"DB IntegrityError: {exc}")
#     detail = "A record with this data already exists"
#     return JSONResponse(
#         status_code=status.HTTP_409_CONFLICT,
#         content={"detail": detail},
#     )


# async def general_exception_handler(request: Request, exc: Exception):
#     logger.exception(f"Unhandled exception: {exc}")
#     return JSONResponse(
#         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#         content={"detail": "An internal server error occurred"},
#     )

# async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
#     return JSONResponse(status_code=500, content={"detail": "Database error"})

# def add_exception_handlers(app: FastAPI):
#     app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)









import logging
import traceback

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


logger = logging.getLogger("app_logger")


# =====================================================
# STANDARD API ERROR RESPONSE FORMAT
# =====================================================

def error_response(
    status_code: int,
    message: str,
    details=None,
    trace_id: str = None,
):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "details": details,
            "trace_id": trace_id,
        },
    )


# =====================================================
# HTTP EXCEPTION HANDLER
# =====================================================

async def http_exception_handler(request: Request, exc: StarletteHTTPException):

    trace_id = getattr(request.state, "trace_id", None)

    logger.warning(
        f"[HTTP EXCEPTION] {exc.status_code} | {exc.detail} | trace_id={trace_id}"
    )

    return error_response(
        status_code=exc.status_code,
        message=exc.detail,
        trace_id=trace_id,
    )


# =====================================================
# VALIDATION ERROR HANDLER (Pydantic)
# =====================================================

async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):

    trace_id = getattr(request.state, "trace_id", None)

    errors = []

    for err in exc.errors():
        errors.append({
            "field": ".".join(str(x) for x in err["loc"]),
            "message": err["msg"],
            "type": err["type"],
        })

    logger.warning(
        f"[VALIDATION ERROR] trace_id={trace_id} | errors={errors}"
    )

    return error_response(
        status_code=422,
        message="Validation error",
        details=errors,
        trace_id=trace_id,
    )


# =====================================================
# GLOBAL UNHANDLED EXCEPTION HANDLER
# =====================================================

async def global_exception_handler(request: Request, exc: Exception):

    trace_id = getattr(request.state, "trace_id", None)

    error_trace = traceback.format_exc()

    logger.error(
        f"[UNHANDLED EXCEPTION] trace_id={trace_id} | error={str(exc)}"
    )

    logger.error(error_trace)

    return error_response(
        status_code=500,
        message="Internal server error",
        details=str(exc),
        trace_id=trace_id,
    )