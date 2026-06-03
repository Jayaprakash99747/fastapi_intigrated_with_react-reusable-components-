import uuid
import random
from datetime import datetime
import os
from fastapi import UploadFile

class Helpers:

    # -----------------------------
    # GENERATE UUID
    # -----------------------------
    @staticmethod
    def generate_uuid() -> str:
        return str(uuid.uuid4())

    # -----------------------------
    # GENERATE ORDER NUMBER
    # -----------------------------
    @staticmethod
    def generate_order_number() -> str:
        return f"ORD-{int(datetime.utcnow().timestamp())}-{random.randint(1000,9999)}"

    # -----------------------------
    # GENERATE OTP
    # -----------------------------
    @staticmethod
    def generate_otp() -> str:
        return str(random.randint(100000, 999999))

    # -----------------------------
    # PAGINATION HELPER
    # -----------------------------
    @staticmethod
    def paginate(skip: int, limit: int):
        return {
            "skip": skip,
            "limit": limit
        }

class FileHandler:

    UPLOAD_DIR = "static/uploads"

    # -----------------------------
    # SAVE FILE
    # -----------------------------
    @staticmethod
    async def save_file(file: UploadFile) -> str:

        if not os.path.exists(FileHandler.UPLOAD_DIR):
            os.makedirs(FileHandler.UPLOAD_DIR)

        file_ext = file.filename.split(".")[-1]
        file_name = f"{uuid.uuid4()}.{file_ext}"
        file_path = os.path.join(FileHandler.UPLOAD_DIR, file_name)

        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        return file_path

    # -----------------------------
    # DELETE FILE
    # -----------------------------
    @staticmethod
    def delete_file(file_path: str) -> bool:

        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False

        except Exception:
            return False