import cmath

import projectq.ops as gates
from projectq.types import BasicQubit


from projqext.projectq.cengines._permutation_engine._permutation_relations import _GATE_TO_INFO

_CONTROLLED_GATE_ = [("XI","XX",1), ("XX","XI",1), ("XY", "YZ", 1), ("XZ", "YY", -1),
					("II","II",1), ("IX","IX",1), ("IY","ZY",1), ("IZ","ZZ",1),
					("ZI","ZI",1), ("ZX", "ZX", 1), ("ZY", "IY", 1), ("ZZ", "IZ", 1),
				 	("YI","YX",1), ("YX", "YI", 1), ("YY", "XZ", -1), ("YZ", "YY", 1)]

_ACTION = {
		gates.HGate:[("X","Z",1), ("Z","X",1), ("Y","Y",-1), ("I","I",1)],
		gates.SGate:[("X","Y",1), ("Z","Z",1), ("Y","X",-1), ("I","I",1)],
		gates.XGate:[("Z","Z",-1), ("X","X",1), ("Y","Y",-1), ("I","I",1)],
		gates.YGate:[("X","X",-1), ("Y","Y",1), ("Z","Z",-1), ("I","I",1)],
		gates.ZGate:[("Z","Z",1), ("X","X",-1), ("Y","Y",-1), ("I","I",1)]
}


_ROTATION_POS = {
		gates.Rx:[("Z","Y",-1), ("X","X",1), ("Y","Z",1), ("I","I",1)],
		gates.Ry:[("Z","X",1), ("X","Z",-1), ("Y","Y",-1), ("I","I",1)],
		gates.Rz:[("Z","Z",1), ("X","Y",1), ("Y","X",-1), ("I","I",1)]
		}


_ROTATION_NEG = {
		gates.Rx:[("Z","Y",1), ("X","X",1), ("Y","Z",-1), ("I","I",1)],
		gates.Ry:[("Z","X",-1), ("Y","Y",1), ("X","Z",1), ("I","I",1)],
		gates.Rz:[("Z","Z",1), ("Y","X",1), ("X","Y",-1), ("I","I",1)]
		}


class CliffordSimulator(object):
	def __init__(self):
		self._stabilizers = []
		self._qubit_dict = dict()

	def add_stabilizer(self, stabilizer_list):
		"""
		Adds a new stabilizer to the list of stabilizers that describe the system.
		Args:
            stabilizer_list: A list of tuples in the following format:
            		[(Qureg1, "X"), (Qureg2, "Y"), ...]
            		Each Qureg object has to contain only 1 BasicQubit. 
            		The second element of the tuple has to be a string of length 1
            		indicating the basis either X Y or Z.
		"""
		# check if valid format
		try:
			for qubit, basis in stabilizer_list:
				assert(len(qubit)==1)
				qubit = qubit[0]
				assert(isinstance(basis, str) and isinstance(qubit, BasicQubit))
		except:
			raise TypeError("The stabilizer_list needs to be of the format [(Qureg, str),...]"
					"The string needs to indicate one of these bases: X Y Z")

		# check if the new stabilizer commutes with the existing stabilizers
		if(not self._is_commuting(stabilizer_list)):
			raise ValueError("The new stabilizer doesn't commute with"
				"the existing stabilizers. ")

		# it passed all the checks? -> add it to the stabilizers
		self._stabilizers.append((dict(),1))
		for qubit, basis in stabilizer_list:
			self.add_qubit_to_dict(qubit)
			self._stabilizers[-1][0][qubit[0].id] = basis


	def add_qubit_to_dict(self, qubit):
		if not qubit[0].id in self._qubit_dict:
			self._qubit_dict[qubit[0].id] = qubit


	def apply_operation(self, cmd):
		"""
		Applies a gate to all of the registered stabilizers.
		Clifford gates are the only gates supported in this version.
		"""
		# first determine the gate
		# CNOT
		if (len(cmd.control_qubits) > 0):

			if(isinstance(cmd.gate, gates.YGate)):
				self.apply_rules(_ACTION[gates.SGate], cmd.qubits[0])
				self.apply_rules(_CONTROLLED_GATE_, cmd.control_qubits + cmd.qubits[0])
				self.apply_rules(_ACTION[gates.ZGate], cmd.qubits[0])
				self.apply_rules(_ACTION[gates.SGate], cmd.qubits[0])
			elif(isinstance(cmd.gate, gates.ZGate)):
				self.apply_rules(_ACTION[gates.HGate], cmd.qubits[0])
				self.apply_rules(_CONTROLLED_GATE_, cmd.control_qubits + cmd.qubits[0])
				self.apply_rules(_ACTION[gates.HGate], cmd.qubits[0])
			else:
				assert(isinstance(cmd.gate, gates.XGate))
				self.apply_rules(_CONTROLLED_GATE_, cmd.control_qubits + cmd.qubits[0])
			return
		if(isinstance(cmd.gate, gates.BasicRotationGate)):
			if(self._get_sign_of_angle(cmd.gate)==1):
				self.apply_rules(_ROTATION_POS[type(cmd.gate)], cmd.qubits[0])
			else:
				self.apply_rules(_ROTATION_NEG[type(cmd.gate)], cmd.qubits[0])
			return

		# otherwise single qubit rule defined in _ACTION
		self.apply_rules(_ACTION[type(cmd.gate)], cmd.qubits[0])



	def apply_rules(self, rules, qubits):
		for i in range(len(self._stabilizers)):
			subset = ""
			for qubit in qubits:
				if(qubit.id in self._stabilizers[i][0]):
					subset += self._stabilizers[i][0][qubit.id]
				else:
					subset += "I"

			# find the new basis
			for rule in rules:
				if(rule[0] == subset):
					subset = rule[1]
					self._stabilizers[i] = (self._stabilizers[i][0], self._stabilizers[i][1]*rule[2])
					break

			# update the self._stabilizers
			for qubit in qubits:
				self._stabilizers[i][0][qubit.id] = subset[0]
				subset = subset[1:]
				if (self._stabilizers[i][0][qubit.id] == "I"):
					#not needed removing
					del self._stabilizers[i][0][qubit.id]
		return


	def _get_sign_of_angle(self, gate):
		info = _GATE_TO_INFO[type(gate)](gate)
		if not info[1] in ["pi2","pi"]:
			raise ValueError("Value of the angle (" +str(gate.angle)+
				") not supported in the Clifford Simulator")
		if (gate.angle > 2*cmath.pi):
			return -1
		return 1

	def _is_commuting(self, new_stabilizer):
		for stabilizer in self._stabilizers:
			parity = 1
			for qubit, basis in new_stabilizer:
				if(qubit[0].id in stabilizer[0] and stabilizer[0][qubit[0].id] != basis):
					parity *= -1
			if (parity == -1):
				return False
		return True

	def return_stabilizers(self):
		total = []
		for stabilizer in self._stabilizers:
			# ids for the qubits
			ids = sorted(list(stabilizer[0].keys()))
			qubits = []
			for qid in ids:
				qubits.append(self._qubit_dict[qid][0])
			bases = []
			for i in range(len(ids)):
				bases.append((i, stabilizer[0][ids[i]]))
			total.append((bases, qubits, stabilizer[1]))

		return total