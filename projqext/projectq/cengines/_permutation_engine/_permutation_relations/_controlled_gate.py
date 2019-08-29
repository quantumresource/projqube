from projectq.ops._qubit_operator import _PAULI_OPERATOR_PRODUCTS
import cmath

_PRECISION = 10**-5

def permute_cnot(control_gate, rotation, rotation_info):
	contributions=[]
	for basis_element in rotation_info[0]:
		# does it anti-commute with control?
		if(rotation.qubits[0][basis_element[0]] in control_gate.control_qubits):
			if(basis_element[1] != "Z"):
				# add X contribution to target
				for qubit in control_gate.qubits[0]:
					contributions.append((qubit, "X"))

		# does it anti-commute with the target?
		if(rotation.qubits[0][basis_element[0]] in control_gate.qubits[0]):
			if(basis_element[1] != "X"):
				for qubit in control_gate.control_qubits:
					contributions.append((qubit, "Z"))

	# update the basis contributions
	_add_basis_contribution(rotation, rotation_info, contributions)
	return

# Helper functions

def _add_basis_contribution(rotation, rotation_info, contributions):
	# first check if qubit is already in multi qubit rotation gate
	total_factor = 1
	for contrib in contributions:
		if (contrib[0] in rotation.qubits[0]):
			pos = rotation.qubits[0].index(contrib[0])
		else:
			pos = len(rotation.qubits[0])
			rotation.qubits[0].append(contrib[0])

		# pos is now defined and points to the qubit that needs to be modified
		modified = False
		for i in range(len(rotation_info[0])):
			if(rotation_info[0][i][0] == pos):
				modified = True
				f, b = _PAULI_OPERATOR_PRODUCTS[(rotation_info[0][i][1], contrib[1])]
				rotation_info[0][i] = (rotation_info[0][i][0], b)
				total_factor *= f
		if(not modified):
			rotation_info[0].append((pos,contrib[1]))
	if(abs(total_factor + 1)< _PRECISION):
		rotation_info[2] = 4*cmath.pi - rotation_info[2]
		return
	elif(abs(total_factor - 1) < _PRECISION):
		return
	raise("Total factor is imaginary! This is not unitary!")