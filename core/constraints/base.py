from ortools.sat.python import cp_model


class BaseConstraint:
    name: str

    def apply(self, model: cp_model.CpModel, variables, params: dict):
        raise NotImplementedError
