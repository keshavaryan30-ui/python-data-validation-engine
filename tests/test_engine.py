import pandas as pd
import pytest

from validator.engine import CircularDependencyError, ValidationEngine
from validator.rules import Severity, ValidationRule


class AlwaysPassRule(ValidationRule):
    name = "AlwaysPass"
    severity = Severity.LOW
    depends_on = []

    def validate(self, df):
        return True


class AlwaysFailRule(ValidationRule):
    name = "AlwaysFail"
    severity = Severity.HIGH
    depends_on = []

    def validate(self, df):
        return False


def test_rule_execution_order():
    rule1 = AlwaysPassRule()
    rule2 = AlwaysFailRule()

    engine = ValidationEngine([rule1, rule2])
    results = engine.run(pd.DataFrame())

    assert results == {
        "AlwaysPass": True,
        "AlwaysFail": False,
    }


def test_circular_dependency_detection():
    class RuleA(ValidationRule):
        name = "A"
        severity = Severity.LOW
        depends_on = ["B"]

        def validate(self, df):
            return True

    class RuleB(ValidationRule):
        name = "B"
        severity = Severity.MEDIUM
        depends_on = ["A"]

        def validate(self, df):
            return True

    engine = ValidationEngine([RuleA(), RuleB()])
    with pytest.raises(CircularDependencyError):
        engine.run(pd.DataFrame())
