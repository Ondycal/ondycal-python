from fastapi import FastAPI

from app.routes import formula_router


app = FastAPI()

app.include_router(formula_router)
