from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field
from enum import Enum

from models import OTPPurposeEnum, UserStatusEnum, UserTypeEnum

class UserAuth(BaseModel):
    email: str

class CreateIndividualUser(BaseModel):
    fullname: str
    email: str
    password: str

class CreateBusinessUser(BaseModel):
    company_name: str
    email: str
    password: str
    tax_number: str

class GetOTP(BaseModel):
    otp_code: int

class GetOTPResponse(BaseModel):
    data: GetOTP

class IndividualUserData(BaseModel):
    user_uuid: UUID
    email: str

class GetFullData(BaseModel):
    id: int
    uuid: UUID
    fullname: Optional[str]
    company_name: Optional[str]
    email: str
    tax_number: Optional[str]
    user_type: UserTypeEnum
    status: UserStatusEnum

class GetFullDataResponse(BaseModel):
    data: GetFullData

# class GetFullBusinessData(BaseModel):
#     id: int
#     uuid: UUID
#     company_name: str
#     email: str
#     tax_number: str
#     user_type: UserTypeEnum
#     status: UserStatusEnum

# class GetFullBusinessDataResponse(BaseModel):
#     data: GetFullBusinessData

class IndividualUserResponse(BaseModel):
    data: IndividualUserData

class BusinessUserData(BaseModel):
    user_uuid: UUID
    email: str

class BusinessUserResponse(BaseModel):
    data: BusinessUserData

# class VerifyOTP(BaseModel):
#     otp_code: int

# class VerifyOTPResponse(BaseModel):
#     data: VerifyOTP
