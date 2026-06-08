import os
import uuid

from fastapi import UploadFile


class FileService:

    HERO_DIR = "uploads/heroes"

    @classmethod
    async def save_image(
        cls,
        file: UploadFile
    ) -> str | None:

        if not file:
            return None

        os.makedirs(
            cls.HERO_DIR,
            exist_ok=True
        )

        extension = file.filename.split(".")[-1]

        filename = (
            f"{uuid.uuid4()}.{extension}"
        )

        file_path = os.path.join(
            cls.HERO_DIR,
            filename
        )

        with open(
            file_path,
            "wb"
        ) as buffer:

            buffer.write(
                await file.read()
            )

        return (
            f"/uploads/heroes/{filename}"
        )