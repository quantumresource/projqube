import projectq.ops as gates
from projectq.cengines import BasicEngine, LastEngineException

import projqube
import projqube.projectq.ops
from projqube.projectq.cengines._permutation_engine._permutation_relations import _GATE_TO_INFO


class OpenSurgeryExporter(BasicEngine):
    """
    Simple exporter that writes OpenSurgery instructions
    """

    def __init__(self, output = "instructions"):
        BasicEngine.__init__(self)

        self._output = output
        self._command_buffer = []
        # self._Tgate_count = 0
        self._logical_qubit_count = 0
        self._remap = dict()

    def is_available(self, cmd):
        """
        Specialized implementation of is_available: Returns True if the
        CommandPrinter is the last engine (since it can print any command).

        Args:
            cmd (Command): Command of which to check availability (all
                Commands can be printed).
        Returns:
            availability (bool): True, unless the next engine cannot handle
                the Command (if there is a next engine).
        """
        try:
            return BasicEngine.is_available(self, cmd)
        except LastEngineException:
            return True

    def receive(self, command_list):
        """
        TODO
        """
        # Need to specialize the receive command to add Hadamards and S gates
        for cmd in command_list:
            # flush gate --> returns the current stabilizers as parity measurements
            if (isinstance(cmd.gate, gates.FlushGate)):
                # finished perform placement
                self.generate_layout()
            elif (isinstance(cmd.gate, gates.AllocateQubitGate)):
                self._remap[cmd.qubits[0][0].id] = self._logical_qubit_count
                self._logical_qubit_count += 1
                self._command_buffer.append(cmd)
            elif (isinstance(cmd.gate, projqube.projectq.ops.ParityMeasurementGate)):
                self._command_buffer.append(cmd)
            elif (isinstance(cmd.gate, gates.SGate)):
                self._command_buffer.append(cmd)
            elif (isinstance(cmd.gate, gates.HGate)):
                self._command_buffer.append(cmd)
            elif (isinstance(cmd.gate, gates.DaggeredGate) and isinstance(cmd.gate._gate, gates.SGate)):
                self._command_buffer.append(cmd)
            elif (isinstance(cmd.gate, gates.ClassicalInstructionGate)):
                continue
            # elif(_GATE_TO_INFO[type(cmd.gate)](cmd.gate)[1] == "pi4"):
            #     self._Tgate_count += 1
            #     self._command_buffer.append(cmd)
            elif(_GATE_TO_INFO[type(cmd.gate)](cmd.gate)[1] == "pi4"):
                # self._Tgate_count += 1
                self._command_buffer.append(cmd)
            else:
                raise TypeError("Non supported gate for the surface"
                    "layouting received: " + str(cmd.gate))
        return


    # def _basis_trafo(self, info, cmd, fout):
    #     """
    #     Instead of rotating the boundaries o a patch on the surgery map, a Hadamard gate is applied to the patch.
    #     This comes in pair with _basis_trafo_back
    #     :param info:
    #     :param cmd: the gate command
    #     :param fout: output stream
    #     :return:
    #     """
    #     for basis in info[0]:
    #         if(basis[1]) == "X":
    #             fout.write("H " + str(self._remap[cmd.qubits[0][basis[0]].id]) + "\n")
    #         if(basis[1]) == "Y":
    #             fout.write("H " + str(self._remap[cmd.qubits[0][basis[0]].id]) + "\n")
    #             fout.write("S " + str(self._remap[cmd.qubits[0][basis[0]].id]) + "\n")
    #
    # def _basis_trafo_back(self, info, cmd, fout):
    #     """
    #        Instead of rotating the boundaries o a patch on the surgery map, a Hadamard gate is applied to the patch.
    #        This comes in pair with _basis_trafo
    #        :param info:
    #        :param cmd: the gate command
    #        :param fout: output stream
    #        :return:
    #     """
    #     for basis in info[0]:
    #         if(basis[1]) == "X":
    #             fout.write("H " + str(self._remap[cmd.qubits[0][basis[0]].id]) + "\n")
    #         if(basis[1]) == "Y":
    #             fout.write("S " + str(self._remap[cmd.qubits[0][basis[0]].id]) + "\n")
    #             fout.write("H " + str(self._remap[cmd.qubits[0][basis[0]].id]) + "\n")


    def generate_layout(self):
        with open(self._output, "w") as fout:
            # write initialization (all have to be initialized at beginning)
            fout.write("INIT " + str(self._logical_qubit_count) + "\n")
            # perform gates
            for cmd in self._command_buffer:
                if (isinstance(cmd.gate, gates.AllocateQubitGate)):
                    # already done in the beginning
                    continue
                elif (isinstance(cmd.gate, projqube.projectq.ops.ParityMeasurementGate)):
                    qubits = ""
                    for basis in cmd.gate._bases:
                        qubits += " " + str(self._remap[cmd.qubits[0][basis[0]].id])

                    # transform to all Z measurements
                    # self._basis_trafo([cmd.gate._bases], cmd, fout)

                    if(len(cmd.gate._bases) == 1):
                        fout.write("MZ" + qubits + "\n")
                    else:
                        fout.write("MZZ" + qubits + "\n")

                    # TODO: transform back with trafo_back?
                    # self._basis_trafo_back([cmd.gate._bases], cmd, fout)

                    continue
                elif (isinstance(cmd.gate, gates.HGate)):
                    fout.write("H " + str(self._remap[cmd.qubits[0][0].id])+"\n")
                elif (isinstance(cmd.gate, gates.SGate)):
                    fout.write("S " + str(self._remap[cmd.qubits[0][0].id])+"\n")
                elif (isinstance(cmd.gate, gates.DaggeredGate) and isinstance(cmd.gate._gate, gates.SGate)):
                    # TODO: the S \dagger gate is (for the moment) treated like a normal S gate
                    fout.write("S " + str(self._remap[cmd.qubits[0][0].id])+"\n")
                elif(_GATE_TO_INFO[type(cmd.gate)](cmd.gate)[1] == "pi4"):
                    #
                    # This is a pi/4 gate, but its basis is not necessarily Z
                    #
                    info = _GATE_TO_INFO[type(cmd.gate)](cmd.gate)

                    # transform to all Z
                    # self._basis_trafo(info, cmd, fout)

                    # at this point it is a Z rotation of pi/4
                    fout.write("NEED A\n")
                    qubits = ""
                    for basis in info[0]:
                        qubits += " " + str(self._remap[cmd.qubits[0][basis[0]].id])
                    fout.write("MZZ A" + qubits + "\n")
                    fout.write("MX A\n")
                    fout.write("S ANCILLA\n") # TODO: add information for initialization
                    fout.write("MXX ANCILLA" + qubits + "\n")

                    # done with the T gate (Z pi/4)
                    # and back to whatever it was before the trafo
                    # self._basis_trafo_back(info, cmd, fout)

                else:
                    raise TypeError("Non supported gate for the surface"
                        "layouting received: " + str(cmd.gate))