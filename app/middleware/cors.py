from fastapi.middleware.cors import CORSMiddleware
from app.core.settings import settings

def add_cors_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS or ["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )