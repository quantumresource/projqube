import projectq
from projectq.ops import *

from projectq.cengines import LocalOptimizer

from projqext.projectq.cengines import PermutePi4Front, MultiqubitMeasurementCliffordEngine
from projqext.projectq.backends import OpenSurgeryExporter

def generate_instructions():
	engines3 = [projectq.cengines.TagRemover(),PermutePi4Front(), MultiqubitMeasurementCliffordEngine()]
	eng3 = projectq.MainEngine(backend=OpenSurgeryExporter(), engine_list=engines3, verbose=True)

	qubit1 = eng3.allocate_qubit()
	qubit2 = eng3.allocate_qubit()
	qubit3 = eng3.allocate_qubit()
	qubit4 = eng3.allocate_qubit()

	T | qubit1
	CNOT | (qubit3, qubit2)
	Rx(-cmath.pi/2) | qubit4

	CNOT | (qubit2, qubit1)
	Rx(cmath.pi/2) | qubit3
	Rz(cmath.pi/4) | qubit4

	CNOT | (qubit4, qubit1)

	Rz(cmath.pi/4) | qubit1
	Rz(cmath.pi/2) | qubit2
	Rz(cmath.pi/4) | qubit3
	Rz(cmath.pi/2) | qubit4

	Rx(-cmath.pi/2) | qubit1
	Rx(cmath.pi/2) | qubit2
	Rx(cmath.pi/2) | qubit3
	Rx(cmath.pi/2) | qubit4

	Measure | qubit1
	Measure | qubit2
	Measure | qubit3
	Measure | qubit4

	return

if __name__ == '__main__':
	generate_instructions()