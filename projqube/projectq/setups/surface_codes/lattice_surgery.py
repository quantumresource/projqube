import projectq.ops as gates
import projectq.setups.decompositions
import projectq.libs.math

from projectq.setups import restrictedgateset
from projectq.cengines import AutoReplacer, DecompositionRuleSet

import projqube.projectq.setups.decompositions
from projqube.projectq.cengines import BasisRotation, PermutePi4Front, MultiqubitMeasurementCliffordEngine

def expand_rule_set_of_autoreplacer(engines):
	"""
	The ProjectQ AutoReplacer initialises a ruleset of known decompositions from the original namespace
	However, the ProjQUBE extension has its own decompositions in projqube.project.setups.decompositions
	Assume that AutoReplacer is the first in the list
	:return:
	"""

	larger_rule_set = DecompositionRuleSet(modules=[projectq.libs.math,
                                             		projectq.setups.decompositions,
													projqube.projectq.setups.decompositions])
	list_with_modified_autoreplacer = []
	#copy the other engines

	for engine in engines:
		if isinstance(engine, AutoReplacer):
			list_with_modified_autoreplacer.append(AutoReplacer(larger_rule_set))
		else:
			list_with_modified_autoreplacer.append(engine)

	return list_with_modified_autoreplacer

def get_engine_list():
	# lets start from a circuit that has CNOT, Pauli, S and T and time evolution
	engines = restrictedgateset.get_engine_list(one_qubit_gates=(gates.HGate,
				gates.XGate, gates.YGate, gates.ZGate, gates.TGate, gates.Tdag, gates.SGate, gates.Sdag),
                two_qubit_gates=(gates.CNOT,),
                other_gates=(gates.TimeEvolution,))

	engines = expand_rule_set_of_autoreplacer(engines) + [PermutePi4Front(), MultiqubitMeasurementCliffordEngine()]

	return engines

def OpenSurgeryExporterEngineList():
	# lets start from a circuit that has CNOT, Pauli, S and T and time evolution
	engines = restrictedgateset.get_engine_list(one_qubit_gates=(gates.HGate,
				gates.XGate, gates.YGate, gates.ZGate, gates.TGate, gates.Tdag, gates.SGate, gates.Sdag),
                two_qubit_gates=(gates.CNOT,),
                other_gates=())

	engines = expand_rule_set_of_autoreplacer(engines) + [PermutePi4Front(), MultiqubitMeasurementCliffordEngine(), BasisRotation()]
	return engines