from fastapi import APIRouter

from app.domains import FormulaModel


router = APIRouter(
    prefix="/formulas",
    tags=["formulas"],
)


@router.get("/")
async def formula_list():
    return {}


@router.get("/{formula_id}")
async def formula_detail(formula_id: int):
    return {"id": formula_id}


@router.post("/")
def formula_create(formula: FormulaModel):
    return {}


@router.post("/{formula_id}/run")
def formula_run(formula_id: int):
    pass
