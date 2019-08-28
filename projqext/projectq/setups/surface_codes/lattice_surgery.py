from projectq.setups import restrictedgateset
import projectq.ops as gates
from projectq.cengines import LocalOptimizer, TagRemover

from projqext.projectq.cengines import BasisRotation, PermutePi4Front, MultiqubitMeasurementCliffordEngine

def get_engine_list():
	# lets start from a circuit that has CNOT, Pauli, S and T and time evolution
	engines = restrictedgateset.get_engine_list(one_qubit_gates=(gates.HGate,
				gates.XGate, gates.YGate, gates.ZGate, gates.TGate, gates.Tdag, gates.SGate, gates.Sdag),
                two_qubit_gates=(gates.CNOT,),
                other_gates=(gates.TimeEvolution,))

	engines = engines + [PermutePi4Front(), MultiqubitMeasurementCliffordEngine()]
	return engines

def SimpleExporterEngineList():
	# lets start from a circuit that has CNOT, Pauli, S and T and time evolution
	engines = restrictedgateset.get_engine_list(one_qubit_gates=(gates.HGate,
				gates.XGate, gates.YGate, gates.ZGate, gates.TGate, gates.Tdag, gates.SGate, gates.Sdag),
                two_qubit_gates=(gates.CNOT,),
                other_gates=())

	engines = engines + [PermutePi4Front(), MultiqubitMeasurementCliffordEngine(), BasisRotation()]
	return engines