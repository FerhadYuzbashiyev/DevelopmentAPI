from fastapi import FastAPI, Depends
from sqlalchemy import insert, select, update, delete
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import CreateIndividualUser, CreateIndividualUserResponse
from models import UserIndividual as userind

app = FastAPI()

@app.post("/")
async def create_user(create_ind_user: CreateIndividualUser, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(userind).values(
        id = create_ind_user.id,
        fullname = create_ind_user.fullname,
        email = create_ind_user.email,
        hashed_password = create_ind_user.hashed_password
    )
    await session.execute(stmt)
    await session.commit()
    return CreateIndividualUserResponse(data=create_ind_user)