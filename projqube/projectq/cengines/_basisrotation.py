from projectq.cengines import BasicEngine
import projectq.ops as gates

import projqube.projectq.ops

class BasisRotation(BasicEngine):
    """
    This engine transforms the Basis of TimeEvolution and ParityMeasurementGate operators
    to the Z basis, by inserting appropriate basis transformation operations
    """
    def __init__(self):
        BasicEngine.__init__(self)

    
    def send_time_evolution(self, cmd):
        """
        Handles the basis transformation for TimeEvolution operators
        """
        assert(isinstance(cmd.gate.hamiltonian, gates.QubitOperator))

        # rotate the existing bases
        bases = list(cmd.gate.hamiltonian.terms.keys())[0]
        self.send_rotation(bases, cmd)

        # transform all the basis in Z
        new_bases = tuple(((basis[0],"Z") for basis in bases))
        new_cmd = gates.TimeEvolution(cmd.gate.time, gates.QubitOperator(new_bases)).generate_command(cmd.qubits[0])
        self.send([new_cmd])

        # rotate back to original bases
        self.send_dagger_rotation(bases, cmd)


    def send_parity_measurement_gate(self, cmd):
        """
        Handles the basis transformation for ParityMeasurementGates
        """
        # rotate the existing bases
        self.send_rotation(cmd.gate._bases, cmd)

        # transform all the basis in Z
        new_bases = list((basis[0], "Z") for basis in cmd.gate._bases)
        new_cmd = projqube.projectq.ops.ParityMeasurementGate(new_bases).generate_command(cmd.qubits[0])
        self.send([new_cmd])

        # rotate back to original bases
        self.send_dagger_rotation(cmd.gate._bases, cmd)


    def send_rotation(self, bases, cmd):
        """
        Handles general basis rotations using a list of bases
        """
        for basis in bases:
            if(basis[1]) == "X":
                self.send([gates.H.generate_command(cmd.qubits[0][basis[0]])])
            if(basis[1]) == "Y":
                self.send([gates.S.generate_command(cmd.qubits[0][basis[0]])])
                self.send([gates.H.generate_command(cmd.qubits[0][basis[0]])])


    def send_dagger_rotation(self, bases, cmd):
        """
        Handles general basis rotations using a list of bases
        """
        for basis in bases:
            if(basis[1]) == "X":
                self.send([gates.H.generate_command(cmd.qubits[0][basis[0]])])
            if(basis[1]) == "Y":
                self.send([gates.H.generate_command(cmd.qubits[0][basis[0]])])
                self.send([gates.Sdag.generate_command(cmd.qubits[0][basis[0]])])



    def receive(self, command_list):
        for cmd in command_list:

            if(isinstance(cmd.gate, gates.TimeEvolution)):
                self.send_time_evolution(cmd)

            elif(isinstance(cmd.gate, projqube.projectq.ops.ParityMeasurementGate)):
                self.send_parity_measurement_gate(cmd)

            else:
                #just send the command along
                self.send([cmd])