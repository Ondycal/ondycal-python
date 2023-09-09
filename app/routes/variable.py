from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.domains import VariableInDB
from app.modules import variable
from . import deps


router = APIRouter(
    prefix="/formulas/variables",
    tags=["variables"],
)


@router.get("/", response_model=list[VariableInDB])
async def variable_list_api(db: Session = Depends(deps.get_db)):
    return variable.get_multi(db)
