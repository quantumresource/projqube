"""
Registers a decomposition for a CNOT gate into a single multi qubit rotation
which is implemented using the TimeEvolution gate and additional single qubit rotations.
"""
import cmath
from projectq.types import Qureg
from projectq.cengines import DecompositionRule
from projectq.meta import Compute, get_control_count, Uncompute
from projectq.ops import Rx, Rz, X, QubitOperator, TimeEvolution
	

def _decompose_cnot_rotation(cmd):
    """ Decompose CNOT gates. """
    qureg = Qureg(cmd.control_qubits + cmd.qubits[0])
    H = QubitOperator("Z0 X1")
    T = TimeEvolution(-cmath.pi/4, H)
    T | qureg
    Rz(cmath.pi) | qureg[0]
    Rx(cmath.pi) | qureg[1]



def _recognize_cnot(cmd):
    return get_control_count(cmd) == 1


#: Decomposition rules
all_defined_decomposition_rules = [
    DecompositionRule(X.__class__, _decompose_cnot_rotation, _recognize_cnot)
]
