import dataclasses
from typing import Any, Iterator, List, Mapping

from sympy import sympify

from classiq.interface.generator.control_state import ControlState
from classiq.interface.generator.synthesis_execution_parameter import PydanticPowerType

from classiq.exceptions import ClassiqValueError

ILLEGAL_NESTED_POWER_ERROR = "Nested power calls with a parametric power and an integer power are unsupported: {a}, {b}"


def _merge_power(a: PydanticPowerType, b: PydanticPowerType) -> PydanticPowerType:
    symbolic_res = sympify(a) * sympify(b)
    if symbolic_res.is_Integer:
        return int(symbolic_res)
    elif symbolic_res.is_symbol:
        return str(symbolic_res)
    else:
        raise ClassiqValueError(ILLEGAL_NESTED_POWER_ERROR.format(a=a, b=b))


@dataclasses.dataclass
class CallSynthesisData(Mapping):
    power: PydanticPowerType = 1
    is_inverse: bool = False
    control_states: List[ControlState] = dataclasses.field(default_factory=list)
    should_control: bool = True

    def merge(self, other: "CallSynthesisData") -> "CallSynthesisData":
        return CallSynthesisData(
            power=_merge_power(self.power, other.power),
            is_inverse=self.is_inverse != other.is_inverse,
            control_states=self.control_states + other.control_states,
            should_control=self.should_control and other.should_control,
        )

    def set_control(self, ctrl_name: str, ctrl_size: int, ctrl_state: str) -> None:
        self.control_states = [
            ControlState(
                name=ctrl_name, num_ctrl_qubits=ctrl_size, ctrl_state=ctrl_state
            )
        ]

    @property
    def has_control(self) -> bool:
        return bool(self.control_states)

    def __getitem__(self, key: str) -> Any:
        return dataclasses.asdict(self)[key]

    def __iter__(self) -> Iterator[str]:
        return iter(dataclasses.asdict(self))

    def __len__(self) -> int:
        return len(dataclasses.asdict(self))
