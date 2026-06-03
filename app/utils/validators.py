import re
from typing import Optional


class Validators:

    EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    PHONE_REGEX = r"^[0-9]{10,15}$"

    # -----------------------------
    # EMAIL VALIDATION
    # -----------------------------
    @staticmethod
    def is_valid_email(email: str) -> bool:
        return bool(re.match(Validators.EMAIL_REGEX, email))

    # -----------------------------
    # PHONE VALIDATION
    # -----------------------------
    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        return bool(re.match(Validators.PHONE_REGEX, phone))

    # -----------------------------
    # PASSWORD STRENGTH CHECK
    # -----------------------------
    @staticmethod
    def is_strong_password(password: str) -> bool:
        if len(password) < 8:
            return False

        if not re.search(r"[A-Z]", password):
            return False

        if not re.search(r"[a-z]", password):
            return False

        if not re.search(r"[0-9]", password):
            return False

        return True