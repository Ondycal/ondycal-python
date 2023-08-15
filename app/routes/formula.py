from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.domains import FormulaModel, FormulaInDB
from app.modules.formula import formula_create
from . import deps


router = APIRouter(
    prefix="/formulas",
    tags=["formulas"],
)


@router.get("/", response_model=list[FormulaInDB])
async def formula_list_api(db: Session = Depends(deps.get_db)):
    return {}


@router.get("/{formula_id}", response_model=FormulaInDB)
async def formula_detail_api(formula_id: int):
    return {"id": formula_id}


@router.post("/", response_model=FormulaInDB)
def formula_create_api(*, db: Session = Depends(deps.get_db), formula: FormulaModel):
    return formula_create(db, formula)


@router.post("/{formula_id}/run")
def formula_run_api(formula_id: int):
    pass
