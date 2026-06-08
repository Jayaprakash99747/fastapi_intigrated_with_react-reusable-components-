# from starlette.middleware.base import BaseHTTPMiddleware
# from starlette.requests import Request
# from starlette.responses import Response
# from jose import jwt, JWTError

# from app.core.config import settings
# from app.services.user_service import user_service


# class AuthMiddleware(BaseHTTPMiddleware):

#     def __init__(self, app):
#         super().__init__(app)

#     # =====================================================
#     # MAIN DISPATCH
#     # =====================================================

#     async def dispatch(self, request: Request, call_next):

#         request.state.user = None

#         token = self._extract_token(request)

#         if token:
#             payload = self._decode_token(token)

#             if payload:
#                 user_id = payload.get("sub")

#                 if user_id:
#                     request.state.user = await self._get_user(user_id)

#         response: Response = await call_next(request)

#         self._add_security_headers(response)

#         return response

#     # =====================================================
#     # EXTRACT TOKEN FROM HEADER
#     # =====================================================

#     def _extract_token(self, request: Request) -> str | None:

#         auth_header = request.headers.get("Authorization")

#         if not auth_header:
#             return None

#         if not auth_header.startswith("Bearer "):
#             return None

#         return auth_header.split(" ")[1]

#     # =====================================================
#     # DECODE JWT TOKEN
#     # =====================================================

#     def _decode_token(self, token: str) -> dict | None:

#         try:
#             return jwt.decode(
#                 token,
#                 settings.SECRET_KEY,
#                 algorithms=[settings.ALGORITHM],
#             )

#         except JWTError:
#             return None

#     # =====================================================
#     # FETCH USER (LIGHTWEIGHT)
#     # =====================================================

#     async def _get_user(self, user_id: str):

#         try:
#             return await user_service.get_user_by_id(
#                 None,  # NOTE: no DB session here intentionally
#                 int(user_id),
#             )
#         except Exception:
#             return None

#     # =====================================================
#     # SECURITY HEADERS
#     # =====================================================

#     def _add_security_headers(self, response: Response):

#         response.headers["X-Frame-Options"] = "DENY"
#         response.headers["X-Content-Type-Options"] = "nosniff"
#         response.headers["X-XSS-Protection"] = "1; mode=block"
#         response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
#         response.headers["Server"] = "Secure-FastAPI"



from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.core.security import decode_access_token


class AuthMiddleware(BaseHTTPMiddleware):

    def __init__(self, app):
        super().__init__(app)

        # ✅ PUBLIC ROUTES (NO AUTH REQUIRED)
        self.public_paths = {
            "/",
            "/health",

            # Swagger / docs
            "/docs",
            "/docs/",
            "/redoc",
            "/redoc/",
            "/openapi.json",

            # auth routes
            "/api/auth/login",
            "/api/auth/login/",
            "/api/auth/register",
            "/api/auth/register/",

            # favicon
            "/favicon.ico",
        }

    async def dispatch(self, request: Request, call_next):
        print("=" * 50)
        print("PATH:", request.url.path)
        print("METHOD:", request.method)

        path = request.url.path

        # ✅ allow public routes
        if path in self.public_paths:
            return await call_next(request)

        # ✅ get token
        auth_header = request.headers.get("Authorization")
        print("AUTH HEADER:", auth_header)
        if not auth_header:
            return JSONResponse(
                status_code=401,
                content={"detail": "Authorization header missing"}
            )

        try:
            scheme, token = auth_header.split()
            print("TOKEN:", token)

            payload = decode_access_token(token)

            print("PAYLOAD:", payload)
            print("TOKEN:", token)

            if scheme.lower() != "bearer":
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Invalid auth scheme"}
                )

            payload = decode_access_token(token)
            print("TOKEN:", token)
            print("PAYLOAD:", payload)
            if not payload:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Invalid or expired token"}
                )

            # attach user
            request.state.user = payload

        except Exception:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid authorization format"}
            )

        return await call_next(request)