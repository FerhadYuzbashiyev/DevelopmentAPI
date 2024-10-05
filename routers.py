import random
from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import delete, insert, select, update
from database import AsyncSession, get_async_session
from auth import create_access_token, get_current_user, get_password_hash, verify_password
from models import OTP, OTPPurposeEnum, User, UserStatusEnum, UserTypeEnum
from schemas import (BusinessUserData, CreateBusinessUser, BusinessUserResponse,
                      CreateIndividualUser,
                      GetFullData, GetFullDataResponse, IndividualUserResponse,
                        GetOTP, GetOTPResponse, IndividualUserData)

router = APIRouter()

@router.post("/otp")
async def create_otp(email: str, session: AsyncSession = Depends(get_async_session)):
    stmt_user = select(User.c.id, User.c.email).where(email == User.c.email)
    result = await session.execute(stmt_user)
    row = result.fetchone()
    # print(row)
    if row[1] is None:
        raise HTTPException(status_code=400, detail="No such user")
    stmt = insert(OTP).values(
        purpose = OTPPurposeEnum.USER_REGISTER,
        otp_code = random.randint(1000,9999),
        user_id = row[0]
    )
    await session.execute(stmt)
    await session.commit()
    return {"status": 200, "details": "OTP Created"}

@router.get("/otp/get")
async def get_otp(user_uuid: UUID, email: str, purpose: OTPPurposeEnum, session: AsyncSession = Depends(get_async_session)):
    stmt_user = select(User.c.user_uuid, User.c.id, User.c.email, OTP.c.purpose).join(OTP, OTP.c.user_id == User.c.id).where(User.c.user_uuid == user_uuid, User.c.email == email, OTP.c.purpose == purpose)
    result_user = await session.execute(stmt_user)
    row_user = result_user.fetchone()
    if row_user is None:
        raise HTTPException(status_code=400, detail="No such user")
    stmt_otp = select(OTP.c.otp_code).where(row_user[1] == OTP.c.user_id).order_by(OTP.c.id.desc())
    result = await session.execute(stmt_otp)
    row_otp = result.fetchone()[0] # with [0] = otp_code only
    # print(row_otp)
    data = GetOTP(
        otp_code=row_otp
    )
    return GetOTPResponse(data=data)

@router.post("/account/setup")
async def verify_user(user_uuid: UUID, otp_code: int, session: AsyncSession = Depends(get_async_session)):
    stmt_verify = select(User.c.id, User.c.user_uuid, OTP.c.otp_code).join(OTP, User.c.id == OTP.c.user_id).where(user_uuid == User.c.user_uuid, otp_code == OTP.c.otp_code)
    result_verify = await session.execute(stmt_verify)
    row_verify = result_verify.fetchone()
    if row_verify is None:
        raise HTTPException(status_code=400, detail="Wrong UUID or OTP code")
    stmt_otp_code = select(OTP.c.otp_code).where(row_verify[0] == OTP.c.user_id).order_by(OTP.c.id.desc())
    result_otp_code = await session.execute(stmt_otp_code)
    row_otp_code = result_otp_code.fetchone()[0]
    if row_otp_code != otp_code:
        raise HTTPException(status_code=400, detail="Wrong OTP code")
    stmt_user = select(User.c.id, User.c.user_uuid, User.c.fullname, User.c.email, User.c.user_type, User.c.company_name, User.c.tax_number).where(User.c.user_uuid == user_uuid)
    result_user = await session.execute(stmt_user)
    row_user = result_user.fetchone()
    # for _ in row_user:
    #     print(_)
    stmt_check_status = select(User.c.status).where(user_uuid == User.c.user_uuid)
    data = GetFullData(
        id=row_user.id,
        uuid=row_user.user_uuid,
        fullname=row_user.fullname,
        company_name=row_user.company_name,
        email=row_user.email,
        tax_number=row_user.tax_number,
        user_type=row_user.user_type,
        status=UserStatusEnum.ACTIVE
    )
    # print(GetFullDataResponse(data=data))
    result_check_status = await session.execute(stmt_check_status)
    row_check_status = result_check_status.fetchone()[0]
    if row_check_status is UserStatusEnum.ACTIVE:
        raise HTTPException(status_code=400, detail="User status is already ACTIVE")
    stmt_update_status = update(User).where(user_uuid == User.c.user_uuid).values(status = UserStatusEnum.ACTIVE)
    await session.execute(stmt_update_status)
    await session.commit()
    return GetFullDataResponse(data=data)

@router.post("/register/individual")
async def create_individual_user(individual_user: CreateIndividualUser, session: AsyncSession = Depends(get_async_session)):
    hash_password = get_password_hash(individual_user.password)
    check = select(User).where(User.c.email == individual_user.email)
    result = await session.execute(check)
    row = result.fetchone()
    # print(some)
    if row is not None:
        raise HTTPException(status_code=400, detail="User already exists")
    stmt = insert(User).values(
        fullname = individual_user.fullname,
        email = individual_user.email,
        hashed_password = hash_password,
        user_type = UserTypeEnum.INDIVIDUAL,
        status = UserStatusEnum.CONTACT_VERIFICATION
    )
    await session.execute(stmt)
    await session.commit()
    stmt_uuid = select(User.c.user_uuid).where(individual_user.email == User.c.email)
    result_uuid = await session.execute(stmt_uuid)
    uuid = result_uuid.fetchone()[0]
    get_response = IndividualUserData(
        user_uuid=uuid,
        email=individual_user.email
    )
    return IndividualUserResponse(data=get_response)

@router.post("/register/business")
async def create_business_user(business_user: CreateBusinessUser, session: AsyncSession = Depends(get_async_session)):
    hash_password = get_password_hash(business_user.password)
    check = select(User).where(User.c.email == business_user.email)
    result = await session.execute(check)
    row = result.fetchone()
    if row is not None:
        raise HTTPException(status_code=400, detail="User already exists")
    stmt = insert(User).values(
        company_name = business_user.company_name,
        email = business_user.email,
        hashed_password = hash_password,
        tax_number = business_user.tax_number,
        user_type = UserTypeEnum.BUSINESS,
        status = UserStatusEnum.CONTACT_VERIFICATION
    )
    await session.execute(stmt)
    await session.commit()
    stmt_uuid = select(User.c.user_uuid).where(business_user.email == User.c.email)
    result_uuid = await session.execute(stmt_uuid)
    uuid = result_uuid.fetchone()[0]
    get_response = BusinessUserData(
        user_uuid=uuid,
        email=business_user.email
    )
    return BusinessUserResponse(data=get_response)

@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: AsyncSession = Depends(get_async_session)):
    stmt = select(User.c.id, User.c.email, User.c.hashed_password).where(User.c.email == form_data.username)
    result = await session.execute(stmt)
    user = result.fetchone()
    print(user)
    if user is None or not verify_password(form_data.password, user[2]):  # user[1] - hashed_password
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    
    access_token = create_access_token(data={"sub": user[0], "email": user[1]})  # user[0] - id
    return {"access_token": access_token, "token_type": "bearer"}

@router.delete("/")
async def deluser(id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = delete(User).where(User.c.id == id)
    await session.execute(stmt)
    await session.commit()
    return {"status": 200, "detail": "Successfully deleted"}

@router.get("/protected-route")
async def protected_route(current_user: Annotated[CreateIndividualUser, Depends(get_current_user)]):
    return {"message": f"Hello, {current_user.email}!"}