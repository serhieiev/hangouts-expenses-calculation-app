from fastapi import FastAPI
from src import database
from src.app.api.users import router as user_router
from src.app.api.hangouts import router as hangout_router
from src.app.api.expenses import router as expense_router


app = FastAPI(
    title="Hangouts Expenses Calculation App",
    description="Your App Description",
    version="1.0.0",
)


@app.on_event("startup")
async def startup():
    await database.engine.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.engine.disconnect()


app.include_router(user_router, prefix="/user", tags=["users"])
app.include_router(hangout_router, prefix="", tags=["hangout"])
app.include_router(expense_router, prefix="", tags=["expenses"])
