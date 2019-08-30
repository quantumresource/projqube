
import cmath
import pytest
import projectq
import projectq.ops as gates
from projectq.ops import ClassicalInstructionGate
from projectq.types import Qureg
from projectq.cengines import BasicEngine

from projqube.projectq.cengines._permutation_engine._permutation_relations._controlled_gate import permute_cnot

_PRECISION = 10**-5

class GetCommand(BasicEngine):
	def __init__(self):
		BasicEngine.__init__(self)
		self.commands = []

	def receive(self, command_list):
		for command in command_list:
			if not isinstance(command.gate,ClassicalInstructionGate):
				self.commands += command_list
			self.send(command_list)


def test_single_rotation():
	commands = GetCommand()
	eng = projectq.MainEngine(engine_list=[commands])
	qubit1 = eng.allocate_qubit()
	qubit2 = eng.allocate_qubit()

	gates.CNOT | (qubit1, qubit2)
	gates.Rx(1) | qubit1
	cmd2_info = [[(0,"X")], "pi4", 1]

	permute_cnot(commands.commands[0], commands.commands[1], cmd2_info)

	print(cmd2_info)
	assert(len(cmd2_info[0])==2)
	assert(cmd2_info[0][1][1] == "X")


def test_single_rotation2():
	commands = GetCommand()
	eng = projectq.MainEngine(engine_list=[commands])
	qubit1 = eng.allocate_qubit()
	qubit2 = eng.allocate_qubit()

	gates.CNOT | (qubit1, qubit2)
	gates.Rz(1) | qubit2
	cmd2_info = [[(0,"Z")], "pi4", 1]

	permute_cnot(commands.commands[0], commands.commands[1], cmd2_info)

	print(cmd2_info)
	assert(len(cmd2_info[0])==2)
	assert(cmd2_info[0][1][1] == "Z")


def test_multirotation():
	commands = GetCommand()
	eng = projectq.MainEngine(engine_list=[commands])
	qubit1 = eng.allocate_qubit()
	qubit2 = eng.allocate_qubit()

	gates.CNOT | (qubit1, qubit2)
	gates.TimeEvolution(-1, gates.QubitOperator("X0 Z1")) | Qureg(qubit1 + qubit2)
	cmd2_info = [[(0,"X"), (1,"Z")], "pi4", 1]

	permute_cnot(commands.commands[0], commands.commands[1], cmd2_info)

	print(cmd2_info)
	assert(len(cmd2_info[0])==2)
	assert(cmd2_info[0][0][1] == "Y" and cmd2_info[0][1][1] == "Y")