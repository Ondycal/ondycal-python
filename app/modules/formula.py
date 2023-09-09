from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.db.models import Formula
from app.domains import FormulaModel
from app.utils.formula import create_expression_tree
from .common import CRUDBase
from .variable import variable as variable_module


class FormulaModule(CRUDBase[Formula, FormulaModel, FormulaModel]):
    def create_with_tree(self, db: Session, obj_in: FormulaModel):
        create_expression_tree(obj_in.tokens)
        request_data: dict = jsonable_encoder(obj_in)
        variables = request_data.pop("variables", [])
        request_data["tree"] = request_data.pop("tokens")
        formula_obj = Formula(**request_data)
        db.add(formula_obj)
        db.commit()
        db.refresh(formula_obj)
        variable_module.create_multi(db, variables, formula_obj.id)
        return formula_obj


formula = FormulaModule(Formula)
