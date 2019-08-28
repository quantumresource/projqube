#
# Implementation of the commutation relation between a Hadamard gate and
# rotational gates.
#
import cmath
import projectq.ops as gates
from . import _helper_functions

def comm_rel_Hadamard_Rot(rot_info):
	"""
	Changes the basis of a rotation operation when it is commuted
	with a Hadamard operator.
	"""
	if(rot_info[0][0][1] == "X"):
		rot_info[0][0] = (rot_info[0][0][0],"Z")
	elif(rot_info[0][0][1] == "Z"):
		rot_info[0][0] = (rot_info[0][0][0],"X")
	else: # for Y rotations the angle gets flipped
		rot_info[2] = 4*cmath.pi - rot_info[2]
	return



_HADAMARD_GATE_TO_INFO={
		gates.HGate: lambda gate: [[(0,"H")],"H","H"]
}

_HADAMARD_GATE_FROM_INFO = {
	"H" : lambda angle: gates.HGate()
}

_HADAMARD_ROTATION_COMM_REL = {
	("H","pi2"): lambda left, right: comm_rel_Hadamard_Rot(right),
	("pi2","H"): lambda left, right: comm_rel_Hadamard_Rot(left),
	("pi4","H"): lambda left, right: comm_rel_Hadamard_Rot(left),
	("H","pi4"): lambda left, right: comm_rel_Hadamard_Rot(right),
	("pi","H"): lambda left, right: comm_rel_Hadamard_Rot(left),
	("H","pi"): lambda left, right:	comm_rel_Hadamard_Rot(right),
	("H", "H"): lambda left, right:	_helper_functions.do_nothing()
}