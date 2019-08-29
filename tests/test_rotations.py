
import cmath
import pytest
import projectq.ops as gates

from projqext.projectq.cengines._permutation_engine._permutation_relations._permutation_error import PermutationRuleDoesNotExist
from projqext.projectq.cengines._permutation_engine._permutation_relations import _rotations

_PRECISION = 10**-5

def test_modify_pi4_left():
	# left: rotation(pi/4) #actually any rotation
	# right: rotation(pi/2)

	comm = ("pi4","pi2")

	#test 1: same basis
	left = [[(0,"X")],"pi4", cmath.pi/4]
	right = [[(0,"X")],"pi2", cmath.pi/2]
	_rotations._ROT_COMM_REL[comm](left, right)
	print(left)
	assert( left[0][0][1] == "X")
	assert(left[2] == cmath.pi/4)

	#test 2: minus
	left = [[(0,"Z")], "pi4", cmath.pi/4]
	right = [[(0,"X")],"pi2", cmath.pi/2]
	_rotations._ROT_COMM_REL[comm](left, right)
	print(left)
	assert(left[0][0][1] == "Y")
	assert(left[2] == 4*cmath.pi - cmath.pi/4)

	#test 3: plus
	left = [[(0,"X")], "pi4", cmath.pi/4]
	right = [[(0,"Z")],"pi2", cmath.pi/2]
	_rotations._ROT_COMM_REL[comm](left, right)
	print(left)
	assert(left[0][0][1] == "Y")
	assert(left[2] == cmath.pi/4)

	#test 4: plus
	left = [[(0,"Y")], "pi4", cmath.pi/4]
	right = [[(0,"X")],"pi2", cmath.pi/2]
	_rotations._ROT_COMM_REL[comm](left, right)
	print(left)
	assert(left[0][0][1] == "Z")
	assert(left[2] == cmath.pi/4)



def test_modify_pi4_right():
	# left: rotation(pi/2)
	# right: rotation(pi/4) #actually any rotation
	comm = ("pi2","pi4")
	#test 1: same basis -> commuting no change
	left = [[(0,"X")],"pi2", cmath.pi/2]
	right = [[(0,"X")],"pi4", cmath.pi/4]
	_rotations._ROT_COMM_REL[comm](left, right)
	print(right)
	assert(right[0][0][1] == "X")
	assert(right[2] == cmath.pi/4)

	#test 2: plus
	left = [[(0,"X")],"pi2", cmath.pi/2]
	right = [[(0,"Z")], "pi4", cmath.pi/4]
	_rotations._ROT_COMM_REL[comm](left, right)
	print(right)
	assert(right[0][0][1] == "Y")
	assert(right[2] == cmath.pi/4)

	#test 3: -sign
	left = [[(0,"Z")],"pi2", cmath.pi/2]
	right = [[(0,"X")], "pi4", cmath.pi/4]
	_rotations._ROT_COMM_REL[comm](left, right)
	print(right)
	assert(right[0][0][1] == "Y")
	assert(right[2] == 4*cmath.pi - cmath.pi/4)

	#test 4: -sign Y basis
	left = [[(0,"X")],"pi2", cmath.pi/2]
	right = [[(0,"Y")], "pi4", cmath.pi/4]
	_rotations._ROT_COMM_REL[comm](left, right)
	print(right)
	assert(right[0][0][1] == "Z")
	assert(right[2] == 4*cmath.pi - cmath.pi/4)



def test_time_evolution_info():
	# standard example
	gate = gates.TimeEvolution(-cmath.pi/8, gates.QubitOperator("X0 X1 Y2"))
	gate_info = _rotations.time_evolution_info(gate)
	print(gate_info)
	assert(len(gate_info[0]) == 3)
	assert(gate_info[1] == "pi4" and gate_info[2] == cmath.pi/4)

	# example with -angle
	gate = gates.TimeEvolution(-(2*cmath.pi-cmath.pi/4), gates.QubitOperator("X0 X1 Y2"))
	gate_info = _rotations.time_evolution_info(gate)
	assert(gate_info[1] == "pi2" and gate_info[2] == 4*cmath.pi - cmath.pi/2)


	# does it throw errors as it is supposed to
	with pytest.raises(PermutationRuleDoesNotExist) as e:
	 	gate = gates.TimeEvolution(-cmath.pi/16, gates.QubitOperator("X0 X1 Y2"))
	 	gate_info = _rotations.time_evolution_info(gate)
	return



def test_determine_rotation():
	g = gates.Rx(cmath.pi/4)
	out = _rotations.determine_rotation(g)
	assert(out[0] == "pi4" and abs(out[1]-(cmath.pi/4)) < _PRECISION)

	g = gates.Rx(-cmath.pi/4)
	out = _rotations.determine_rotation(g)
	assert(out[0] == "pi4" and abs(out[1]-(4*cmath.pi - cmath.pi/4)) < _PRECISION)

	g = gates.Rx(cmath.pi/2)
	out = _rotations.determine_rotation(g)
	assert(out[0] == "pi2" and abs(out[1]-(cmath.pi/2)) < _PRECISION)


	g = gates.Rx(-cmath.pi/2)
	out = _rotations.determine_rotation(g)
	assert(out[0] == "pi2" and abs(out[1]-(4*cmath.pi - cmath.pi/2)) < _PRECISION)

	g = gates.Rx(-cmath.pi)
	out = _rotations.determine_rotation(g)
	assert(out[0] == "pi" and abs(out[1]-(3*cmath.pi)) < _PRECISION)

	g = gates.Rx(cmath.pi)
	out = _rotations.determine_rotation(g)
	assert(out[0] == "pi" and abs(out[1]-cmath.pi) < _PRECISION)
	return

def test_comm_rel():

	comm = ("pi2","pi2")
	# without negative sign
	left = [[(0,"X")], "pi2", cmath.pi/2]
	right = [[(0,"X")],"pi2", cmath.pi/2]
	_rotations._ROT_COMM_REL[comm](left,right)
	assert(right[0][0][1] == "X")
	assert(right[2] == cmath.pi/2)


	comm = ("pi2","pi2")
	# without negative sign
	left = [[(0,"X")], "pi2", cmath.pi/2]
	right = [[(0,"Z")],"pi2", cmath.pi/2]
	_rotations._ROT_COMM_REL[comm](left,right)
	assert(right[0][0][1] == "Y")
	assert(right[2] == cmath.pi/2)

	# with sign
	left = [[(0,"Z")], "pi2", cmath.pi/2]
	right = [[(0,"X")],"pi2", cmath.pi/2]
	_rotations._ROT_COMM_REL[comm](left,right)
	assert(right[0][0][1] == "Y")
	assert(right[2] == 4*cmath.pi - cmath.pi/2)

	#("pi4","pi2")
	#("pi2","pi4")
	# see test_modify_pi4_left and test_modify_pi4_right

	#("pi","pi") does nothing

	#("pi","pi2")
	comm = ("pi","pi2")
	left = [[(0,"Z")], "pi", cmath.pi]
	right = [[(0,"Z")],"pi2", cmath.pi/2]
	_rotations._ROT_COMM_REL[comm](left,right)
	assert(right[0][0][1] == "Z")
	assert(right[2] == cmath.pi/2)

	left = [[(0,"Z")], "pi", cmath.pi]
	right = [[(0,"X")],"pi2", cmath.pi/2]
	_rotations._ROT_COMM_REL[comm](left,right)
	assert(right[0][0][1] == "X")
	assert(right[2] == 4*cmath.pi - cmath.pi/2)

	#("pi2","pi")
	comm = ("pi2","pi")
	left = [[(0,"Z")], "pi2", cmath.pi/2]
	right = [[(0,"Z")],"pi", cmath.pi]
	_rotations._ROT_COMM_REL[comm](left,right)
	assert(left[0][0][1] == "Z")
	assert(left[2] == cmath.pi/2)

	left = [[(0,"Z")], "pi2", cmath.pi/2]
	right = [[(0,"X")],"pi", cmath.pi]
	_rotations._ROT_COMM_REL[comm](left,right)
	assert(left[0][0][1] == "Z")
	assert(left[2] == 4*cmath.pi - cmath.pi/2)

	#("pi","pi4") # same as before
	#("pi4","pi") # same as before
	comm = ("pi4","pi")
	left = [[(0,"Z")], "pi2", cmath.pi/4]
	right = [[(0,"Z")],"pi", cmath.pi]
	_rotations._ROT_COMM_REL[comm](left,right)
	assert(left[0][0][1] == "Z")
	assert(left[2] == cmath.pi/4)

	left = [[(0,"Z")], "pi2", cmath.pi/4]
	right = [[(0,"X")],"pi", cmath.pi]
	_rotations._ROT_COMM_REL[comm](left,right)
	assert(left[0][0][1] == "Z")
	assert(left[2] == 4*cmath.pi - cmath.pi/4)
	return

def test_gate_to_info():
	gate = gates.Rx(cmath.pi/4)
	info = _rotations._ROTATION_GATE_TO_INFO[type(gate)](gate)
	assert(info[:2] == [[(0,"X")], "pi4"])
	assert(abs(info[2]-(cmath.pi/4)) < _PRECISION)

	gate = gates.Ry(cmath.pi/2)
	info = _rotations._ROTATION_GATE_TO_INFO[type(gate)](gate)
	assert(info[:2] == [[(0,"Y")], "pi2"])
	assert(abs(info[2]-(cmath.pi/2)) < _PRECISION)

	gate = gates.Rz(cmath.pi)
	info = _rotations._ROTATION_GATE_TO_INFO[type(gate)](gate)
	assert(info[:2] == [[(0,"Z")], "pi"])
	assert(abs(info[2]-(cmath.pi)) < _PRECISION)

	gate = gates.TimeEvolution(-cmath.pi/8, gates.QubitOperator("X0 X1 Y2"))
	info = _rotations._ROTATION_GATE_TO_INFO[type(gate)](gate)
	assert(info[:2] == [[(0,"X"),(1,"X"),(2, "Y")], "pi4"])
	assert(abs(info[2]-(cmath.pi/4)) < _PRECISION)
	return

def test_gate_from_info():
	assert(_rotations._ROTATION_GATE_FROM_INFO["X"](cmath.pi/4) == gates.Rx(cmath.pi/4))
	assert(_rotations._ROTATION_GATE_FROM_INFO["Y"](cmath.pi/2) == gates.Ry(cmath.pi/2))
	assert(_rotations._ROTATION_GATE_FROM_INFO["Z"](cmath.pi) == gates.Rz(cmath.pi))
	return