import pytest
import projectq
from projectq.backends import CommandPrinter
from projectq.cengines import BasicEngine
from projectq.cengines import AutoReplacer, DecompositionRuleSet, InstructionFilter

from projqube.projectq.ops import ParityMeasurementGate
import projqube.projectq.setups.decompositions

class Debugger(BasicEngine):
	def __init__(self):
		super(BasicEngine, self).__init__()
		self.commands = []

	def receive(self, cmd):
		self.commands += cmd
		self.send(cmd)


def test_Parity_generation():
	gate = ParityMeasurementGate("X1 X4 X3 Z2")
	print(gate._bases)
	assert(len(gate._bases)==4)

def test_or():
	a = Debugger()
	engine_list = [a]
	eng = projectq.MainEngine(engine_list = engine_list, backend = CommandPrinter())
	q1 = eng.allocate_qubit()
	q2 = eng.allocate_qubit()

	ParityMeasurementGate("Z0 X1") | q1+q2

	assert(a.commands[-1].gate._bases[0][0] == 0)
	assert(a.commands[-1].gate._bases[0][1] == "Z")


def is_supported(eng, cmd):
	if (isinstance(cmd.gate,ParityMeasurementGate)):
		return False
	return True

def test_decomposition():
	a = Debugger()
	decomp = DecompositionRuleSet(modules=[projqube.projectq.setups.decompositions.parity_measurement])

	engine_list = [AutoReplacer(decomp), InstructionFilter(is_supported), a]

	eng = projectq.MainEngine(engine_list = engine_list, backend = CommandPrinter(accept_input=False))
	q1 = eng.allocate_qubit()
	q2 = eng.allocate_qubit()

	ParityMeasurementGate("Z0 X1") | q1+q2

	print(a.commands)
	#TODO
	#assert(a.commands[-1].gate._bases[0][0] == 0)
	#assert(a.commands[-1].gate._bases[0][1] == "Z")
	assert(False)


