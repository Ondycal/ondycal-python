from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.db.models import Formula
from app.domains import FormulaModel
from app.utils.formula import create_expression_tree


def formula_create(db: Session, formula: FormulaModel) -> Formula:
    create_expression_tree(formula.tokens)
    request_data: dict = jsonable_encoder(formula)
    _ = request_data.pop("variables", [])
    request_data["tree"] = request_data.pop("tokens")
    formula_obj = Formula(**request_data)
    db.add(formula_obj)
    db.commit()
    db.refresh(formula_obj)
    return formula_obj
