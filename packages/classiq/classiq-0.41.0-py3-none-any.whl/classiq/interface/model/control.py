from typing import TYPE_CHECKING, Literal

from classiq.interface.model.quantum_expressions.quantum_expression import (
    QuantumExpressionOperation,
)

if TYPE_CHECKING:
    from classiq.interface.model.statement_block import StatementBlock


class Control(QuantumExpressionOperation):
    kind: Literal["Control"]

    body: "StatementBlock"
