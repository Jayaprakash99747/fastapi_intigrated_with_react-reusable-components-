from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    ConfigDict,
    field_validator,
)

import re


# ==========================================================
# REGISTER
# ==========================================================

class RegisterSchema(BaseModel):

    username: str = Field(
        ...,
        min_length=3,
        max_length=100,
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=6,
        max_length=128,
    )

    phone: str | None = Field(
        default=None,
        max_length=20,
    )

    @field_validator("password")
    @classmethod
    def validate_password(
        cls,
        value: str,
    ):

        if not re.search(r"[A-Z]", value):
            raise ValueError(
                "Password must contain uppercase letter"
            )

        if not re.search(r"[a-z]", value):
            raise ValueError(
                "Password must contain lowercase letter"
            )

        if not re.search(r"\d", value):
            raise ValueError(
                "Password must contain a number"
            )

        if not re.search(
            r"[!@#$%^&*(),.?\":{}|<>]",
            value,
        ):
            raise ValueError(
                "Password must contain special character"
            )

        return value


# ==========================================================
# LOGIN
# ==========================================================

class LoginSchema(BaseModel):

    email: EmailStr

    password: str = Field(
        ...,
        min_length=6,
        max_length=128,
    )


# ==========================================================
# TOKEN Schema
# ==========================================================

class TokenSchema(BaseModel):

    access_token: str

    refresh_token: str

    token_type: str = "bearer"

    expires_in: int


# ==========================================================
# REFRESH TOKEN
# ==========================================================

class RefreshTokenSchema(BaseModel):

    refresh_token: str


# ==========================================================
# LOGOUT
# ==========================================================

class LogoutSchema(BaseModel):

    refresh_token: str


# ==========================================================
# FORGOT PASSWORD
# ==========================================================

class ForgotPasswordSchema(BaseModel):

    email: EmailStr


# ==========================================================
# VERIFY RESET CODE
# ==========================================================

class VerifyResetCodeSchema(BaseModel):

    email: EmailStr

    reset_code: str = Field(
        ...,
        min_length=4,
        max_length=20,
    )


# ==========================================================
# RESET PASSWORD
# ==========================================================

class ResetPasswordSchema(BaseModel):

    email: EmailStr

    reset_code: str

    new_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
    )

    @field_validator("new_password")
    @classmethod
    def validate_password(
        cls,
        value: str,
    ):

        if not re.search(r"[A-Z]", value):
            raise ValueError(
                "Password must contain uppercase letter"
            )

        if not re.search(r"[a-z]", value):
            raise ValueError(
                "Password must contain lowercase letter"
            )

        if not re.search(r"\d", value):
            raise ValueError(
                "Password must contain number"
            )

        if not re.search(
            r"[!@#$%^&*(),.?\":{}|<>]",
            value,
        ):
            raise ValueError(
                "Password must contain special character"
            )

        return value


# ==========================================================
# MESSAGE Schema
# ==========================================================

class MessageSchema(BaseModel):

    message: str


# ==========================================================
# AUTH Schema
# ==========================================================

class AuthSchema(BaseModel):

    success: bool

    message: str

    data: TokenSchema | None = None


# ==========================================================
# TOKEN PAYLOAD
# ==========================================================

class TokenPayloadSchema(BaseModel):

    sub: str

    user_id: int

    role: str

    exp: int

    jti: str | None = None


# ==========================================================
# EMAIL VERIFICATION
# ==========================================================

class EmailVerificationSchema(BaseModel):

    email: EmailStr

    code: str


# ==========================================================
# RESEND VERIFICATION
# ==========================================================

class ResendVerificationSchema(BaseModel):

    email: EmailStr


# ==========================================================
# CHANGE EMAIL
# ==========================================================

class ChangeEmailSchema(BaseModel):

    new_email: EmailStr

    password: str


# ==========================================================
# SESSION Schema
# ==========================================================

class SessionSchema(BaseModel):

    id: int

    created_at: str

    expires_at: str

    is_revoked: bool

    model_config = ConfigDict(
        from_attributes=True
    )