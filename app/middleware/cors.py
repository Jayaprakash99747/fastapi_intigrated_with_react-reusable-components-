from fastapi.middleware.cors import CORSMiddleware
from app.core.settings import settings

def add_cors_middleware(app):
    # Merge settings origins with dev defaults — no silent fallback
    origins = list(settings.BACKEND_CORS_ORIGINS) if settings.BACKEND_CORS_ORIGINS else []

    # Always include local dev origins
    dev_origins = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

    allowed = list(set(origins + dev_origins))

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )