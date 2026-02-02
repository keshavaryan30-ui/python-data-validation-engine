from enum import Enum
from typing import List


class Severity(Enum):
    LOW = 1
    MEDIUM = 3
    HIGH = 5


class ValidationRule:
    """
    Base class for all validation rules.
    """

    name: str
    severity: Severity
    depends_on: List[str] = []

    def validate(self, df) -> bool:
        """
        Execute validation logic on a dataset.
        Must return True (pass) or False (fail).
        """
        raise NotImplementedError("validate() must be implemented by rule subclasses")
