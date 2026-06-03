from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)

from app.core.constants import (
    PaymentStatus,
    PaymentProvider,
)


# ==========================================================
# CREATE PAYMENT ORDER
# ==========================================================

class PaymentCreateRequest(BaseModel):

    order_id: int = Field(
        ...,
        gt=0,
    )

    provider: PaymentProvider


# ==========================================================
# RAZORPAY ORDER RESPONSE
# ==========================================================

class RazorpayOrderResponse(BaseModel):

    order_id: int

    razorpay_order_id: str

    amount: float

    currency: str

    key_id: str


# ==========================================================
# STRIPE PAYMENT INTENT RESPONSE
# ==========================================================

class StripePaymentIntentResponse(BaseModel):

    payment_intent_id: str

    client_secret: str

    amount: float

    currency: str


# ==========================================================
# VERIFY RAZORPAY PAYMENT
# ==========================================================

class RazorpayVerifyRequest(BaseModel):

    order_id: int

    razorpay_order_id: str

    razorpay_payment_id: str

    razorpay_signature: str


# ==========================================================
# VERIFY STRIPE PAYMENT
# ==========================================================

class StripeVerifyRequest(BaseModel):

    order_id: int

    payment_intent_id: str


# ==========================================================
# WEBHOOK
# ==========================================================

class PaymentWebhookPayload(BaseModel):

    event: str

    payload: dict


# ==========================================================
# PAYMENT RESPONSE
# ==========================================================

class PaymentResponse(BaseModel):

    id: int

    order_id: int

    provider: PaymentProvider

    amount: float

    currency: str

    status: PaymentStatus

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================================
# PAYMENT DETAIL
# ==========================================================

class PaymentDetailResponse(BaseModel):

    id: int

    order_id: int

    provider: PaymentProvider

    provider_order_id: Optional[str]

    provider_payment_id: Optional[str]

    amount: float

    currency: str

    status: PaymentStatus

    failure_reason: Optional[str]

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================================
# PAYMENT STATUS RESPONSE
# ==========================================================

class PaymentStatusResponse(BaseModel):

    payment_id: int

    order_id: int

    status: PaymentStatus


# ==========================================================
# REFUND REQUEST
# ==========================================================

class RefundRequest(BaseModel):

    payment_id: int

    reason: Optional[str] = None


# ==========================================================
# REFUND RESPONSE
# ==========================================================

class RefundResponse(BaseModel):

    payment_id: int

    status: PaymentStatus

    message: str


# ==========================================================
# PAYMENT SUMMARY
# ==========================================================

class PaymentSummaryResponse(BaseModel):

    total_payments: int

    success_payments: int

    failed_payments: int

    refunded_payments: int

    total_amount: float


# ==========================================================
# GENERIC RESPONSE
# ==========================================================

class PaymentMessageResponse(BaseModel):

    message: str