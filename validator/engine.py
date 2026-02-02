from collections import defaultdict, deque
from typing import Dict, List

from validator.rules import ValidationRule


class CircularDependencyError(Exception):
    """Raised when rule dependencies form a cycle."""


class ValidationEngine:
    def __init__(self, rules: List[ValidationRule]):
        self.rules: Dict[str, ValidationRule] = {r.name: r for r in rules}

    def _resolve_execution_order(self) -> List[str]:
        graph = defaultdict(list)
        indegree = defaultdict(int)

        for rule in self.rules.values():
            for dep in getattr(rule, "depends_on", []):
                graph[dep].append(rule.name)
                indegree[rule.name] += 1

        queue = deque([name for name in self.rules if indegree[name] == 0])
        execution_order = []

        while queue:
            current = queue.popleft()
            execution_order.append(current)

            for dependent in graph[current]:
                indegree[dependent] -= 1
                if indegree[dependent] == 0:
                    queue.append(dependent)

        if len(execution_order) != len(self.rules):
            raise CircularDependencyError(
                "Circular dependency detected among validation rules"
            )

        return execution_order

    def run(self, df) -> Dict[str, bool]:
        execution_order = self._resolve_execution_order()
        results: Dict[str, bool] = {}

        for rule_name in execution_order:
            rule = self.rules[rule_name]
            results[rule_name] = rule.validate(df)

        return results
