import asyncio
from email.message import EmailMessage
from typing import Optional

import aiosmtplib
from app.core.settings import settings


class EmailService:

    async def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        html: Optional[str] = None,
    ) -> bool:

        message = EmailMessage()
        message["From"] = settings.SMTP_FROM_EMAIL   # FIXED
        message["To"] = to_email
        message["Subject"] = subject

        message.set_content(body)

        if html:
            message.add_alternative(html, subtype="html")

        try:
            await aiosmtplib.send(
                message,
                hostname=settings.SMTP_HOST,
                port=settings.SMTP_PORT,
                username=settings.SMTP_USERNAME,
                password=settings.SMTP_PASSWORD,
                start_tls=settings.SMTP_TLS,
            )
            return True

        except Exception as e:
            print(f"[EMAIL ERROR] {e}")
            return False

    async def send_otp_email(self, to_email: str, otp: str) -> bool:
        return await self.send_email(
            to_email,
            "Your OTP Code",
            f"OTP: {otp}",
            f"<h1>{otp}</h1>",
        )

    async def send_password_reset_email(self, to_email: str, reset_code: str) -> bool:
        return await self.send_email(
            to_email,
            "Password Reset",
            f"Reset code: {reset_code}",
            f"<h1>{reset_code}</h1>",
        )

    async def send_welcome_email(self, to_email: str, username: str) -> bool:
        return await self.send_email(
            to_email,
            "Welcome!",
            f"Hi {username}",
            f"<h2>Welcome {username}</h2>",
        )


email_service = EmailService()








# import asyncio
# from email.message import EmailMessage
# from typing import Optional

# import aiosmtplib

# from app.core.config import settings


# class EmailService:

#     # =====================================================
#     # BASE EMAIL SENDER (ASYNC SMTP)
#     # =====================================================

#     async def send_email(
#         self,
#         to_email: str,
#         subject: str,
#         body: str,
#         html: Optional[str] = None,
#     ) -> bool:

#         message = EmailMessage()
#         message["From"] = settings.EMAIL_FROM
#         message["To"] = to_email
#         message["Subject"] = subject

#         # fallback plain text
#         message.set_content(body)

#         # HTML support (production-ready)
#         if html:
#             message.add_alternative(html, subtype="html")

#         try:
#             await aiosmtplib.send(
#                 message,
#                 hostname=settings.SMTP_HOST,
#                 port=settings.SMTP_PORT,
#                 username=settings.SMTP_USER,
#                 password=settings.SMTP_PASSWORD,
#                 start_tls=True,
#             )
#             return True

#         except Exception as e:
#             # In production → replace with structured logger
#             print(f"[EMAIL ERROR] {e}")
#             return False

#     # =====================================================
#     # OTP EMAIL
#     # =====================================================

#     async def send_otp_email(
#         self,
#         to_email: str,
#         otp: str,
#     ) -> bool:

#         subject = "Your OTP Verification Code"

#         body = f"""
#         Your OTP Code is: {otp}
#         This code will expire soon. Do not share it with anyone.
#         """

#         html = f"""
#         <html>
#             <body>
#                 <h2>OTP Verification</h2>
#                 <p>Your OTP code is:</p>
#                 <h1 style="color:#2d89ef;">{otp}</h1>
#                 <p>This code will expire soon. Do not share it.</p>
#             </body>
#         </html>
#         """

#         return await self.send_email(
#             to_email=to_email,
#             subject=subject,
#             body=body,
#             html=html,
#         )

#     # =====================================================
#     # PASSWORD RESET EMAIL
#     # =====================================================

#     async def send_password_reset_email(
#         self,
#         to_email: str,
#         reset_code: str,
#     ) -> bool:

#         subject = "Password Reset Request"

#         body = f"""
#         You requested a password reset.
#         Your reset code is: {reset_code}
#         """

#         html = f"""
#         <html>
#             <body>
#                 <h2>Password Reset</h2>
#                 <p>Use the following code to reset your password:</p>
#                 <h1 style="color:red;">{reset_code}</h1>
#                 <p>This code will expire soon.</p>
#             </body>
#         </html>
#         """

#         return await self.send_email(
#             to_email=to_email,
#             subject=subject,
#             body=body,
#             html=html,
#         )

#     # =====================================================
#     # WELCOME EMAIL
#     # =====================================================

#     async def send_welcome_email(
#         self,
#         to_email: str,
#         username: str,
#     ) -> bool:

#         subject = "Welcome to Our Platform 🎉"

#         body = f"""
#         Hi {username},
#         Welcome to our platform. We are happy to have you onboard.
#         """

#         html = f"""
#         <html>
#             <body>
#                 <h2>Welcome {username} 🎉</h2>
#                 <p>Thanks for registering with us.</p>
#             </body>
#         </html>
#         """

#         return await self.send_email(
#             to_email=to_email,
#             subject=subject,
#             body=body,
#             html=html,
#         )

#     # =====================================================
#     # NOTIFICATION EMAIL
#     # =====================================================

#     async def send_notification_email(
#         self,
#         to_email: str,
#         title: str,
#         message: str,
#     ) -> bool:

#         return await self.send_email(
#             to_email=to_email,
#             subject=title,
#             body=message,
#         )


# email_service = EmailService()