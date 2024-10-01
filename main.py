from fastapi import FastAPI
from routers import router

app = FastAPI(title="Paypresso")

app.include_router(router)