import projectq
from projectq.ops import *

from projqube.projectq.cengines import OpenSurgeryExporter
from projqube.projectq.setups.surface_codes import lattice_surgery


def generate_instructions():
	engines = lattice_surgery.SimpleExporterEngineList() # This is the same as before but only using multi-qu:bit Z rotations
	eng = projectq.MainEngine(backend=OpenSurgeryExporter(output = "perceptron_instructions"), engine_list=engines, verbose=True)


	# Fig2 of arxiv:1811.02266 perceptron
	qreg = eng.allocate_qureg(4)
	ancilla = eng.allocate_qubit()

	# U_i
	# currently tensor doesn't work
	Tensor(H) | qreg
	Tensor(Z) | qreg[:3]

	CZ | (qreg[1], qreg[2])
	CZ | (qreg[0], qreg[2])
	CZ | (qreg[0], qreg[1])
	ControlledGate(Z,2)	| (qreg[0], qreg[1], qreg[2])

	# U_w
	Tensor(Z) | [qreg[1],qreg[2]]
	CZ | (qreg[1], qreg[3])
	CZ | (qreg[0], qreg[2])
	CZ | (qreg[0], qreg[1])
	ControlledGate(Z,2)	| (qreg[1], qreg[2], qreg[3])
	ControlledGate(Z,2)	| (qreg[0], qreg[1], qreg[3])
	ControlledGate(Z,3)	| (qreg[0], qreg[1], qreg[2], qreg[3])

	Tensor(H) | qreg
	Tensor(X) | qreg

	# perform measurement
	ControlledGate(X,4) | (qreg, ancilla)

	Measure | ancilla
	Tensor(Measure) | qreg
	eng.flush()
	return

if __name__ == '__main__':
	generate_instructions()