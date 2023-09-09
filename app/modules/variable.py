from sqlalchemy.orm import Session

from app.db.models import Variable
from app.domains import VariableModel
from .common import CRUDBase


class VariableModule(CRUDBase[Variable, VariableModel, VariableModel]):
    def create_multi(
        self, db: Session, variable_list: list[VariableModel], formula_id: int
    ):
        for variable in variable_list:
            constraint = variable.pop("constraint")
            if constraint:
                pass  # TODO: save constraint
            variable_obj = Variable(**variable, formula_id=formula_id)
            db.add(variable_obj)
        db.commit()


variable = VariableModule(Variable)
