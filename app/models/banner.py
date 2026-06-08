from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime
)

from app.core.database import Base


class HeroSection(Base):
    __tablename__ = "hero_sections"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(500), nullable=False)

    description = Column(Text, nullable=False)

    primary_button_text = Column(String(100))
    primary_button_url = Column(String(1000))

    secondary_button_text = Column(String(100))
    secondary_button_url = Column(String(1000))

    card_title = Column(String(255))
    card_description = Column(Text)

    background_image = Column(String(1000))
    hero_image = Column(String(1000))

    is_active = Column(Boolean, default=True)

    display_order = Column(Integer, default=1)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    is_deleted = Column(
        Boolean,
        default=False,
        nullable=False,
        index=True
    )

    deleted_at = Column(
        DateTime,
        nullable=True
    )







# from datetime import datetime

# from sqlalchemy import (
#     Column,
#     Integer,
#     String,
#     Text,
#     Boolean,
#     DateTime,
#     CheckConstraint,
# )

# from app.core.database import Base


# # ==========================================================
# # BANNER
# # ==========================================================

# class Banner(Base):
#     __tablename__ = "banners"

#     id = Column(Integer,primary_key=True,index=True,)

#     title = Column(String(200),nullable=False,index=True,)

#     description = Column(Text,nullable=True,)

#     image_url = Column(String(1000),nullable=False,)

#     button_text = Column(String(100),nullable=True,)

#     button_link = Column(String(1000),nullable=True,)

#     is_active = Column(Boolean,default=True,nullable=False,index=True,)

#     display_order = Column(Integer,default=0,nullable=False,index=True,)

#     start_date = Column(DateTime,nullable=True,)

#     end_date = Column(DateTime,nullable=True,)

#     created_at = Column(DateTime,default=datetime.utcnow,nullable=False,)

#     updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False,)

#     __table_args__ = (
#         CheckConstraint(
#             "display_order >= 0",
#             name="ck_banner_display_order_positive",
#         ),
#     )

#     # ======================================================
#     # HELPER PROPERTIES
#     # ======================================================

#     @property
#     def is_expired(self) -> bool:
#         """
#         Banner expired check.
#         """

#         if not self.end_date:
#             return False

#         return datetime.utcnow() > self.end_date

#     @property
#     def is_started(self) -> bool:
#         """
#         Banner start date reached.
#         """

#         if not self.start_date:
#             return True

#         return datetime.utcnow() >= self.start_date

#     @property
#     def is_currently_active(self) -> bool:
#         """
#         Banner visible to customers.
#         """

#         return (
#             self.is_active
#             and self.is_started
#             and not self.is_expired
#         )

#     # ======================================================
#     # REPR
#     # ======================================================

#     def __repr__(self):

#         return (
#             f"<Banner("
#             f"id={self.id}, "
#             f"title='{self.title}', "
#             f"active={self.is_active}"
#             f")>"
#         )