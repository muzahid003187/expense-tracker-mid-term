from fastapi import FastAPI

from database import engine, base
import models

from routers import auth
from routers import transactions

base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Expense Tracker API"
)

app.include_router(auth.router)
app.include_router(transactions.router)


@app.get("/")
def home():
    return {
        "message": "Expense Tracker API is running"
    }