from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.domains import FormulaModel, FormulaInDB
from app.modules import formula
from . import deps


router = APIRouter(
    prefix="/formulas",
    tags=["formulas"],
)


@router.get("/", response_model=list[FormulaInDB])
async def formula_list_api(db: Session = Depends(deps.get_db)):
    return formula.get_multi(db)


@router.get("/{formula_id}", response_model=FormulaInDB)
async def formula_detail_api(formula_id: int, db: Session = Depends(deps.get_db)):
    return formula.get(db, formula_id)


@router.post("/", response_model=FormulaInDB)
def formula_create_api(formulaCreate: FormulaModel, db: Session = Depends(deps.get_db)):
    return formula.create_with_tree(db, formulaCreate)


@router.delete("/{formula_id}")
async def formula_delete_api(formula_id: int, db: Session = Depends(deps.get_db)):
    return formula.remove(db, id=formula_id)


@router.post("/{formula_id}/run")
def formula_run_api(formula_id: int):
    pass
