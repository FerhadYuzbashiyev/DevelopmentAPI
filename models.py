from datetime import datetime

from sqlalchemy import Enum, MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean
from enum import Enum as PyEnum

# Define the enums
class VoucherType(PyEnum):
    FirstPrice = "FirstPrice"
    SecondPrice = "SecondPrice"
    ThirdPrice = "ThirdPrice"

class UserType(PyEnum):
    Individual = "Individual"
    Business = "Business"

class SubscriptionType(PyEnum):
    Basic = "Basic"
    Standart = "Standart"
    Premium = "Premium"

metadata = MetaData()

UserBusiness = Table(
    "UserRegistrationBusiness",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("company_name", String, nullable=False),
    Column("email", String, nullable=False),
    Column("tax_number", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow),
    Column("hashed_password", String, nullable=False)
)

UserIndividual = Table(
    "UserRegisterIndividual",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("fullname", String, nullable=False),
    Column("email", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow),
    Column("hashed_password", String, nullable=False)
)

Vouchers = Table(
    "Vouchers",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("voucher_type", Enum(VoucherType), nullable=False),
    Column("voucher_count", Integer, nullable=False),
    Column("is_activate", Boolean, nullable=False),
    Column("begins_at", TIMESTAMP, default=datetime.utcnow),
    Column("expires_at", TIMESTAMP, nullable=False),
    Column("user_individual_id", Integer, ForeignKey(UserIndividual.c.id)),
    Column("user_company_id", Integer, ForeignKey(UserBusiness.c.id))
)

UserLogin = Table(
    "UserLogin",
    metadata,
    Column("email", String, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("is_exists", Boolean, nullable=False),
    Column("user_type", Enum(UserType), nullable=False),
    Column("user_individual_id", Integer, ForeignKey(UserIndividual.c.id), nullable=True),
    Column("user_company_id", Integer, ForeignKey(UserBusiness.c.id), nullable=True)
)

Subscriptions = Table(
    "Subscriptions",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("sub_type", Enum(SubscriptionType), nullable=False),
    Column("sub_count", Integer, nullable=False),
    Column("begins_at", TIMESTAMP, default=datetime.utcnow),
    Column("expries_at", TIMESTAMP, nullable=False),
    Column("is_activate", Boolean, nullable=False),
    Column("user_individual_id", Integer, ForeignKey(UserIndividual.c.id)),
    Column("user_company_id", Integer, ForeignKey(UserBusiness.c.id))
)

