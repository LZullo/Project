import sys
sys.path.append('../')
from fastapi import FastAPI
from app.router.user_router import router as user_router
from app.router.salaries_router import router as salaries_router


app = FastAPI()

app.include_router(user_router)
app.include_router(salaries_router)