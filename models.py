from datetime import datetime, timedelta
import uuid

from sqlalchemy import UUID, MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, Enum
from enum import Enum as PyEnum

class UserTypeEnum(str, PyEnum):
    BUSINESS = "business"
    INDIVIDUAL = "individual"

class UserStatusEnum(str, PyEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    CONTACT_VERIFICATION = "contact_verification"
    
class StatusEnum(str, PyEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class OTPPurposeEnum(str, PyEnum):
    USER_REGISTER = "user_register"

metadata = MetaData()

User = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_uuid", UUID(as_uuid=True), default=uuid.uuid4),
    Column("fullname", String, nullable=True, unique=False),
    Column("company_name", String, nullable=True, unique=True),
    Column("email", String, nullable=False, unique=True),
    Column("tax_number", String, nullable=True),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow),
    Column("hashed_password", String, nullable=False),
    Column("user_type", Enum(UserTypeEnum), nullable=False),
    Column("status", Enum(UserStatusEnum), nullable=False),
)

OTP = Table(
    "otp",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("purpose", Enum(OTPPurposeEnum), nullable=False),
    Column("otp_code", Integer, nullable=False),
    Column("user_id", Integer, ForeignKey(User.c.id), nullable=False),
    Column("expiration_time", TIMESTAMP, default=lambda: datetime.utcnow() + timedelta(minutes=2)),
)

Voucher = Table(
    "voucher",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("voucher_type", String, nullable=False),
    Column("voucher_count", Integer, nullable=False),
    Column("is_activate", Boolean, nullable=False),
    Column("begins_at", TIMESTAMP, default=datetime.utcnow),
    Column("expires_at", TIMESTAMP, nullable=False),
    Column("user_id", Integer, ForeignKey(User.c.id)),
    Column("status", Enum(StatusEnum), nullable=False),
)

Subscription = Table(
    "subscription",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("subscription_type", String, nullable=False),
    Column("begins_at", TIMESTAMP, default=datetime.utcnow),
    Column("expries_at", TIMESTAMP, nullable=False),
    Column("is_activate", Boolean, nullable=False),
    Column("user_id", Integer, ForeignKey(User.c.id)),
    Column("status", Enum(StatusEnum), nullable=False),
)

UserVoucher = Table(
    "user_voucher",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("begins_at", TIMESTAMP, default=datetime.utcnow),
    Column("expires_at", TIMESTAMP, nullable=False),
    Column("status", Enum(StatusEnum), nullable=False),
    Column("user_id", Integer, ForeignKey(User.c.id)),
    Column("voucher_id", Integer, ForeignKey(Voucher.c.id)),
)

UserSubscription = Table(
    "user_subscription",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("begins_at", TIMESTAMP, default=datetime.utcnow),
    Column("expires_at", TIMESTAMP, nullable=False),
    Column("status", Enum(StatusEnum), nullable=False),
    Column("user_id", Integer, ForeignKey(User.c.id)),
    Column("subscription_id", Integer, ForeignKey(Subscription.c.id)),
)
