from constraints.coverage import CoverageConstraint
from constraints.fairness import FairnessConstraint


def load_constraints():
    return {
        "coverage": CoverageConstraint,
        "fairness": FairnessConstraint,
    }
