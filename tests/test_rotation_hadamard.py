import cmath
from projqext.projectq.cengines._permutation_engine._permutation_relations import _rotation_hadamard


def test_rotation_hadamard():
	comm = ("H","pi2")
	left = [[(0,"H")],"H","H"]
	right =[[(0,"X")],"pi2", cmath.pi/2]
	_rotation_hadamard._HADAMARD_ROTATION_COMM_REL[comm](left, right)
	assert(right == [[(0,"Z")],"pi2",cmath.pi/2])

	comm = ("H","pi4")
	left = [[(0,"H")],"H","H"]
	right =[[(0,"Y")],"pi4", cmath.pi/4]
	_rotation_hadamard._HADAMARD_ROTATION_COMM_REL[comm](left, right)
	assert(right == [[(0,"Y")],"pi4",4*cmath.pi-cmath.pi/4])

	comm = ("H","H")
	left = [[(0,"H")],"H","H"]
	right =[[(0,"H")],"H", "H"]
	_rotation_hadamard._HADAMARD_ROTATION_COMM_REL[comm](left, right)
	assert(right == [[(0,"H")],"H", "H"])
	return