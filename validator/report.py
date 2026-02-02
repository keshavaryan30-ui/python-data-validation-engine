from typing import Dict

from validator.rules import Severity


def generate_validation_score(
    results: Dict[str, bool],
    rules: Dict[str, object],
) -> float:
    total_weight = 0
    failed_weight = 0

    for rule_name, passed in results.items():
        severity: Severity = rules[rule_name].severity
        weight = severity.value

        total_weight += weight
        if not passed:
            failed_weight += weight

    if total_weight == 0:
        return 100.0

    score = 100 - (failed_weight / total_weight) * 100
    return round(score, 2)
