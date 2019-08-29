#
# Helper functions for the computation of commutation relations between
# different rotations
#
import cmath

from . import _helper_functions

import projectq.ops as gates
from projectq.ops._qubit_operator import _PAULI_OPERATOR_PRODUCTS


from . import _permutation_error

#needed for the comparison of angles
_PRECISION = 10**-5


def modify_pi4_left(left, right):
	"""
	Changes the angle and basis when the left pi4 gate is commuted with a pi2
	gate (right). Depending on the prefactor the angle needs to be inverted.
	Commutation relations are used to determine the basis.
	"""
	factor, basis = _PAULI_OPERATOR_PRODUCTS[(left[0][0][1],right[0][0][1])]
	if (basis == "I"): # commuting operators -> do nothing
		return

	# update basis
	left[0][0] = (left[0][0][0], basis)
	# update angle
	factor *= 1.j
	if(abs(factor + 1)< _PRECISION):
		left[2] = 4*cmath.pi - left[2]
	return

def modify_pi4_right(left, right):
	"""
	Changes the angle and basis when the right pi4 gate is commuted with a pi2
	gate (left). Depending on the prefactor the angle needs to be inverted.
	Commutation relations are used to determine the basis.
	"""
	factor, basis = _PAULI_OPERATOR_PRODUCTS[(left[0][0][1],right[0][0][1])]
	if (basis == "I"): # commuting operators -> do nothing
		return

	# update basis
	right[0][0] = (right[0][0][0], basis)
	# update angle
	factor *= 1.j
	if(abs(factor + 1)< _PRECISION):
		right[2] = 4*cmath.pi - right[2]
	return

def get_left_angle(left,right):
	factor, basis = _PAULI_OPERATOR_PRODUCTS[(left[0][0][1],right[0][0][1])]
	if basis == "I":
		return left[2]
	return 4*cmath.pi - left[2]


def get_right_angle(left,right):
	factor, basis = _PAULI_OPERATOR_PRODUCTS[(left[0][0][1],right[0][0][1])]
	if basis == "I":
		return right[2]
	return 4*cmath.pi - right[2]


def time_evolution_info(gate):
	if (isinstance(gate.hamiltonian, gates.QubitOperator)):
		# the hamiltonian should only have one term with 1
		assert(len(gate.hamiltonian.terms) == 1)
		assert(abs(gate.time) <= 2*cmath.pi)
		assert(gate.time < 0)
		#gate.time = 2*cmath.pi + gate.time

		# There are differences in the prefactors from rotational gates and
		# the time evolution operator. Namely a missing factor of 1/2 and a minus
		# sign.

		bases = list(list(gate.hamiltonian.terms.keys())[0])
		#only allow prefactor of 1 (the angle is given by the time)
		assert(list(gate.hamiltonian.terms.values())[0] == 1)
		# time in TimeEvolution operator gives rotation angle
		if(abs((-1*gate.time)-cmath.pi/4) < _PRECISION or
				abs((-1*gate.time)-(cmath.pi*2-cmath.pi/4)) < _PRECISION):
			return [bases, "pi2", -gate.time*2] # time evolution is missing the 1/2 of rotational gates
		elif(abs((-1*gate.time)-cmath.pi/8) < _PRECISION or
				abs((-1*gate.time)-(cmath.pi*2-cmath.pi/8)) < _PRECISION):
			return [bases, "pi4", -gate.time*2] # time evolution is missing the factor 1/2 of rotational gates
	raise _permutation_error.PermutationRuleDoesNotExist("""To be able to use
		arbitrary rotations (Time evolutions) they first have to be decomposed.
		Into pi/2 and pi/4 rotations.""")



def determine_rotation(gate):
	if(abs(abs(gate.angle)-cmath.pi) < _PRECISION or abs(abs(gate.angle)-3*cmath.pi) < _PRECISION):
		return ["pi", gate.angle]
	elif(abs(abs(gate.angle)-cmath.pi/2) < _PRECISION or abs(abs(gate.angle)-cmath.pi*(3.5)) < _PRECISION):
		return ["pi2", gate.angle]
	elif(abs(abs(gate.angle)-cmath.pi/4) < _PRECISION or abs(abs(gate.angle)-cmath.pi*(3.75)) < _PRECISION):
		return ["pi4", gate.angle]
	raise _permutation_error.PermutationRuleDoesNotExist("""This is not a valid gate for the 
		permutation rules. Allowed gatesets are currently: Pauli-rotations
		and controlled Pauli-rotations. Any other gate is currently 
		unsupported. Be sure to use the predefined decomposition rules.""")


_ROTATION_GATE_TO_INFO = {
	gates.XGate: lambda gate: [[(0,"X")], "pi", cmath.pi],
	gates.YGate: lambda gate: [[(0,"Y")], "pi", cmath.pi],
	gates.ZGate: lambda gate: [[(0,"Z")], "pi", cmath.pi],
	gates.SGate: lambda gate: [[(0,"Z")], "pi2", cmath.pi/2],
	gates.TGate: lambda gate: [[(0,"Z")], "pi4", cmath.pi/4],
	gates.Rx: lambda gate: [[(0,"X")]] + determine_rotation(gate),
	gates.Ry: lambda gate: [[(0,"Y")]] + determine_rotation(gate),
	gates.Rz: lambda gate: [[(0,"Z")]] + determine_rotation(gate),
	gates.TimeEvolution: lambda gate: time_evolution_info(gate),
}

_ROTATION_GATE_FROM_INFO = {
	"X" : lambda angle: gates.Rx(angle),
	"Y" : lambda angle: gates.Ry(angle),
	"Z" : lambda angle: gates.Rz(angle)
}



#
# This lookup table implemets the following commutation relations relation
# (1) P * P'(phi) = P'(phi) * P
# (2) P'(phi) * P = P * P'(-phi)
# (3) P(pi/2) * P'(phi) = (i P P')(phi) * P(pi/2)
# (4) P'(phi) * P(pi/2) = P(pi/2) * (i P P')(-phi)
# 
# Here, P and P' are bases for one of the Pauli-rotations (Rx, Ry, Rz).
# The angle pi/2 indicates S gates, phi is arbitrary and if the angle is omitted,
# a standard Pauli operator (angle = pi) is used.
#
_ROT_COMM_REL = {
	("pi2","pi2"): lambda left, right: modify_pi4_right(left, right),
	("pi4","pi2"): lambda left, right: modify_pi4_left(left, right),
	("pi2","pi4"): lambda left, right: modify_pi4_right(left, right),
	("pi","pi"): lambda left, right: helper_functions.do_nothing(),
	("pi","pi2"): lambda left, right:
				_helper_functions.modify_gate(right, right[0][0][1], get_right_angle(left, right)),
	("pi2","pi"): lambda left, right:
				_helper_functions.modify_gate(left, left[0][0][1], get_left_angle(left, right)),
	("pi","pi4"): lambda left, right:
				_helper_functions.modify_gate(right, right[0][0][1], get_right_angle(left, right)),
	("pi4","pi"): lambda left, right:
				_helper_functions.modify_gate(left, left[0][0][1], get_left_angle(left, right))
}