from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy import Enum

class VoucherType(str, Enum):
    FirstPrice = "FirstPrice"
    SecondPrice = "SecondPrice"
    ThirdPrice = "ThirdPrice"

class UserType(str, Enum):
    Individual = "Individual"
    Business = "Business"

class SubscriptionType(str, Enum):
    Basic = "Basic"
    Standart = "Standart"
    Premium = "Premium"

class CreateIndividualUser(BaseModel):
    id: int
    fullname: str
    email: str
    hashed_password: str

class CreateIndividualUserResponse(BaseModel):
    data: CreateIndividualUser