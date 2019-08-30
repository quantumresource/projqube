import pytest
import projectq

from projqube.projectq.cengines import CliffordSimulator, MultiqubitMeasurementCliffordEngine


class A:
	def __init__(self):
		self.commands = []
	
	def receive(self, cmd):
		self.commands += cmd



def test_qubit_initialization():
	eng = projectq.MainEngine()
	init = [(eng.allocate_qubit(), "Z")]
	sim = CliffordSimulator()

	sim.add_stabilizer(init)
	assert(len(sim._stabilizers) == 1)
	assert(len(sim._stabilizers[0][0])==1)

	# does the commutation check work?
	init2 = [(init[0][0], "X")]
	with pytest.raises(ValueError):
		sim.add_stabilizer(init2)
	assert(len(sim._stabilizers) == 1)
	assert(len(sim._stabilizers[0][0])==1)
	
	init += [(eng.allocate_qubit(), "X")]
	print(init)
	sim.add_stabilizer(init)
	print(sim._stabilizers)
	assert(len(sim._stabilizers) == 2)
	assert(len(sim._stabilizers[0][0])==1)
	assert(len(sim._stabilizers[1][0])==2)


def test_operation():
	eng = projectq.MainEngine()
	qubit1 = eng.allocate_qubit()
	qubit2 = eng.allocate_qubit()
	init1 = [(qubit1, "Z")]
	init2 = [(qubit2, "Z")]

	sim = CliffordSimulator()
	sim.add_stabilizer(init1)
	sim.add_stabilizer(init2)

	cmd1 = projectq.ops.H.generate_command(qubit1)

	sim.apply_operation(cmd1)

	print(sim._stabilizers)
	assert(len(sim._stabilizers) == 2)
	assert(len(sim._stabilizers[0][0])==1)

	assert(sim._stabilizers[0][0][qubit1[0].id]=="X")
	assert(sim._stabilizers[1][0][qubit2[0].id]=="Z")


def test_MultiqubitMeasurementCliffordEngine():
	debugger = A()
	engine_list = [MultiqubitMeasurementCliffordEngine()]
	eng = projectq.MainEngine(engine_list=engine_list)
	engine_list[0].next_engine = debugger
	qubit1 = eng.allocate_qubit()
	qubit2 = eng.allocate_qubit()
	projectq.ops.H | qubit1
	projectq.ops.CNOT | (qubit1[0], qubit2[0])
	projectq.ops.Measure | qubit1
	projectq.ops.Measure | qubit2
	eng.flush()

	print(debugger.commands[2].gate._bases)
	print(debugger.commands[3].gate._bases)
	assert(False)




def test_CNOT():
	pass