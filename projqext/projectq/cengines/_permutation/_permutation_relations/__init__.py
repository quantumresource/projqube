from . import _rotation_hadamard
from . import _rotations
from . import _permutation_error
from ._controlled_gate import permute_cnot

PermutationRuleDoesNotExist = _permutation_error.PermutationRuleDoesNotExist
#
# The following dictionary implements a mapping to the abstract format used in
# this engine to calculate the permutation relations. The keys are class names
# of gates.
#
_GATE_TO_INFO = {**_rotation_hadamard._HADAMARD_GATE_TO_INFO,
				**_rotations._ROTATION_GATE_TO_INFO}

#
# The following dictionary implements the inverse mapping of the previous
# dictionary. The abstract format that is used to calculate the commutation
# relations is translated back to a projectq.gate object
#
_GATE_FROM_INFO = {**_rotation_hadamard._HADAMARD_GATE_FROM_INFO,
				**_rotations._ROTATION_GATE_FROM_INFO}

#
# The following dictionary implements the commutation relation given the
# abstract gate information.
#
_COMM_REL = {**_rotation_hadamard._HADAMARD_ROTATION_COMM_REL,
			**_rotations._ROT_COMM_REL}


# controlled gates need to be handled differently (unfortunately)
