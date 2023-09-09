from fastapi import FastAPI

from app.routes import formula_router, variable_router


app = FastAPI()

app.include_router(formula_router)
app.include_router(variable_router)
