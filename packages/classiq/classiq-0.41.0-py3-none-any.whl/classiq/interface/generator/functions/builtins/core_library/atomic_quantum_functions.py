from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.classical_type import (
    ClassicalList,
    Integer,
    Real,
)
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.quantum_function_declaration import (
    QuantumFunctionDeclaration,
)

DEFAULT_TARGET_NAME = "target"

H_FUNCTION = QuantumFunctionDeclaration(
    name="H",
    port_declarations={
        DEFAULT_TARGET_NAME: PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)


X_FUNCTION = QuantumFunctionDeclaration(
    name="X",
    port_declarations={
        DEFAULT_TARGET_NAME: PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)


Y_FUNCTION = QuantumFunctionDeclaration(
    name="Y",
    port_declarations={
        DEFAULT_TARGET_NAME: PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)

Z_FUNCTION = QuantumFunctionDeclaration(
    name="Z",
    port_declarations={
        DEFAULT_TARGET_NAME: PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)


I_FUNCTION = QuantumFunctionDeclaration(
    name="I",
    port_declarations={
        DEFAULT_TARGET_NAME: PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)


S_FUNCTION = QuantumFunctionDeclaration(
    name="S",
    port_declarations={
        DEFAULT_TARGET_NAME: PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)


T_FUNCTION = QuantumFunctionDeclaration(
    name="T",
    port_declarations={
        DEFAULT_TARGET_NAME: PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)


SDG_FUNCTION = QuantumFunctionDeclaration(
    name="SDG",
    port_declarations={
        DEFAULT_TARGET_NAME: PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)


TDG_FUNCTION = QuantumFunctionDeclaration(
    name="TDG",
    port_declarations={
        DEFAULT_TARGET_NAME: PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)


PHASE_FUNCTION = QuantumFunctionDeclaration(
    name="PHASE",
    param_decls={"theta": Real()},
    port_declarations={
        DEFAULT_TARGET_NAME: PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)


RX_FUNCTION = QuantumFunctionDeclaration(
    name="RX",
    param_decls={
        "theta": Real(),
    },
    port_declarations={
        DEFAULT_TARGET_NAME: PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        )
    },
)


RY_FUNCTION = QuantumFunctionDeclaration(
    name="RY",
    param_decls={
        "theta": Real(),
    },
    port_declarations={
        DEFAULT_TARGET_NAME: PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        )
    },
)


RZ_FUNCTION = QuantumFunctionDeclaration(
    name="RZ",
    param_decls={
        "theta": Real(),
    },
    port_declarations={
        DEFAULT_TARGET_NAME: PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        )
    },
)

R_FUNCTION = QuantumFunctionDeclaration(
    name="R",
    param_decls={
        "theta": Real(),
        "phi": Real(),
    },
    port_declarations={
        DEFAULT_TARGET_NAME: PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        )
    },
)


RXX_FUNCTION = QuantumFunctionDeclaration(
    name="RXX",
    param_decls={
        "theta": Real(),
    },
    port_declarations={
        DEFAULT_TARGET_NAME: PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="2"),
        )
    },
)


RYY_FUNCTION = QuantumFunctionDeclaration(
    name="RYY",
    param_decls={
        "theta": Real(),
    },
    port_declarations={
        DEFAULT_TARGET_NAME: PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="2"),
        )
    },
)


RZZ_FUNCTION = QuantumFunctionDeclaration(
    name="RZZ",
    param_decls={
        "theta": Real(),
    },
    port_declarations={
        DEFAULT_TARGET_NAME: PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="2"),
        )
    },
)


CH_FUNCTION = QuantumFunctionDeclaration(
    name="CH",
    port_declarations={
        "control": PortDeclaration(
            name="control",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
        DEFAULT_TARGET_NAME: PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)


CX_FUNCTION = QuantumFunctionDeclaration(
    name="CX",
    port_declarations={
        "control": PortDeclaration(
            name="control",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
        DEFAULT_TARGET_NAME: PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)


CY_FUNCTION = QuantumFunctionDeclaration(
    name="CY",
    port_declarations={
        "control": PortDeclaration(
            name="control",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
        DEFAULT_TARGET_NAME: PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)


CZ_FUNCTION = QuantumFunctionDeclaration(
    name="CZ",
    port_declarations={
        "control": PortDeclaration(
            name="control",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
        DEFAULT_TARGET_NAME: PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)


CRX_FUNCTION = QuantumFunctionDeclaration(
    name="CRX",
    param_decls={
        "theta": Real(),
    },
    port_declarations={
        "control": PortDeclaration(
            name="control",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
        DEFAULT_TARGET_NAME: PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)


CRY_FUNCTION = QuantumFunctionDeclaration(
    name="CRY",
    param_decls={
        "theta": Real(),
    },
    port_declarations={
        "control": PortDeclaration(
            name="control",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
        DEFAULT_TARGET_NAME: PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)


CRZ_FUNCTION = QuantumFunctionDeclaration(
    name="CRZ",
    param_decls={
        "theta": Real(),
    },
    port_declarations={
        "control": PortDeclaration(
            name="control",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
        DEFAULT_TARGET_NAME: PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)


CPHASE_FUNCTION = QuantumFunctionDeclaration(
    name="CPHASE",
    param_decls={
        "theta": Real(),
    },
    port_declarations={
        "control": PortDeclaration(
            name="control",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
        DEFAULT_TARGET_NAME: PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)


SWAP_FUNCTION = QuantumFunctionDeclaration(
    name="SWAP",
    port_declarations={
        "qbit0": PortDeclaration(
            name="qbit0",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
        "qbit1": PortDeclaration(
            name="qbit1",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)


IDENTITY_FUNCTION = QuantumFunctionDeclaration(
    name="IDENTITY",
    port_declarations={
        DEFAULT_TARGET_NAME: PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
        )
    },
)

UNITARY_FUNCTION = QuantumFunctionDeclaration(
    name="unitary",
    param_decls={
        "elements": ClassicalList(element_type=ClassicalList(element_type=Real()))
    },
    port_declarations={
        DEFAULT_TARGET_NAME: PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="log(get_field(elements[0], 'len'), 2)"),
        )
    },
)


PREPARE_STATE_FUNCTION = QuantumFunctionDeclaration(
    name="prepare_state",
    param_decls={"probabilities": ClassicalList(element_type=Real()), "bound": Real()},
    port_declarations={
        "out": PortDeclaration(
            name="out",
            direction=PortDeclarationDirection.Output,
            size=Expression(expr="log(get_field(probabilities, 'len'), 2)"),
        )
    },
)

PREPARE_AMPLITUDES_FUNCTION = QuantumFunctionDeclaration(
    name="prepare_amplitudes",
    param_decls={"amplitudes": ClassicalList(element_type=Real()), "bound": Real()},
    port_declarations={
        "out": PortDeclaration(
            name="out",
            direction=PortDeclarationDirection.Output,
            size=Expression(expr="log(get_field(amplitudes, 'len'), 2)"),
        )
    },
)

ADD_FUNCTION = QuantumFunctionDeclaration(
    name="add",
    port_declarations={
        "left": PortDeclaration(
            name="left",
            direction=PortDeclarationDirection.Inout,
        ),
        "right": PortDeclaration(
            name="right",
            direction=PortDeclarationDirection.Inout,
        ),
        "result": PortDeclaration(
            name="result",
            direction=PortDeclarationDirection.Output,
            size=Expression(
                expr="Max(get_field(left, 'len'), get_field(right, 'len')) + 1"
            ),
        ),
    },
)


MODULAR_ADD_FUNCTION = QuantumFunctionDeclaration(
    name="modular_add",
    port_declarations={
        "left": PortDeclaration(
            name="left",
            direction=PortDeclarationDirection.Inout,
        ),
        "right": PortDeclaration(
            name="right",
            direction=PortDeclarationDirection.Inout,
        ),
    },
)


INTEGER_XOR_FUNCTION = QuantumFunctionDeclaration(
    name="integer_xor",
    port_declarations={
        "left": PortDeclaration(
            name="left",
            direction=PortDeclarationDirection.Inout,
        ),
        "right": PortDeclaration(
            name="right",
            direction=PortDeclarationDirection.Inout,
        ),
    },
)


U_FUNCTION = QuantumFunctionDeclaration(
    name="U",
    param_decls={"theta": Real(), "phi": Real(), "lam": Real(), "gam": Real()},
    port_declarations={
        DEFAULT_TARGET_NAME: PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        )
    },
)


CCX_FUNCTION = QuantumFunctionDeclaration(
    name="CCX",
    port_declarations={
        "control": PortDeclaration(
            name="control",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="2"),
        ),
        DEFAULT_TARGET_NAME: PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)


ALLOCATE_FUNCTION = QuantumFunctionDeclaration(
    name="allocate",
    param_decls={"num_qubits": Integer()},
    port_declarations={
        "out": PortDeclaration(
            name="out",
            direction=PortDeclarationDirection.Output,
            size=Expression(expr="num_qubits"),
        )
    },
)


FREE_FUNCTION = QuantumFunctionDeclaration(
    name="free",
    port_declarations={
        "in": PortDeclaration(
            name="in",
            direction=PortDeclarationDirection.Input,
        )
    },
)


RANDOMIZED_BENCHMARKING = QuantumFunctionDeclaration(
    name="randomized_benchmarking",
    port_declarations={
        DEFAULT_TARGET_NAME: PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
        ),
    },
    param_decls={
        "num_of_cliffords": Integer(),
    },
)


INPLACE_PREPARE_STATE = QuantumFunctionDeclaration(
    name="inplace_prepare_state",
    param_decls={"probabilities": ClassicalList(element_type=Real()), "bound": Real()},
    port_declarations={
        "target": PortDeclaration(
            name="target",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="log(get_field(probabilities, 'len'), 2)"),
        )
    },
)


INPLACE_PREPARE_AMPLITUDES = QuantumFunctionDeclaration(
    name="inplace_prepare_amplitudes",
    param_decls={"amplitudes": ClassicalList(element_type=Real()), "bound": Real()},
    port_declarations={
        "target": PortDeclaration(
            name="target",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="log(get_field(amplitudes, 'len'), 2)"),
        )
    },
)


__all__ = [
    "H_FUNCTION",
    "X_FUNCTION",
    "Y_FUNCTION",
    "Z_FUNCTION",
    "I_FUNCTION",
    "S_FUNCTION",
    "T_FUNCTION",
    "SDG_FUNCTION",
    "TDG_FUNCTION",
    "PHASE_FUNCTION",
    "RX_FUNCTION",
    "RY_FUNCTION",
    "RZ_FUNCTION",
    "R_FUNCTION",
    "RXX_FUNCTION",
    "RYY_FUNCTION",
    "RZZ_FUNCTION",
    "CH_FUNCTION",
    "CX_FUNCTION",
    "CY_FUNCTION",
    "CZ_FUNCTION",
    "CRX_FUNCTION",
    "CRY_FUNCTION",
    "CRZ_FUNCTION",
    "CPHASE_FUNCTION",
    "SWAP_FUNCTION",
    "IDENTITY_FUNCTION",
    "PREPARE_STATE_FUNCTION",
    "PREPARE_AMPLITUDES_FUNCTION",
    "UNITARY_FUNCTION",
    "ADD_FUNCTION",
    "MODULAR_ADD_FUNCTION",
    "INTEGER_XOR_FUNCTION",
    "U_FUNCTION",
    "CCX_FUNCTION",
    "ALLOCATE_FUNCTION",
    "FREE_FUNCTION",
    "RANDOMIZED_BENCHMARKING",
    "INPLACE_PREPARE_STATE",
    "INPLACE_PREPARE_AMPLITUDES",
]
