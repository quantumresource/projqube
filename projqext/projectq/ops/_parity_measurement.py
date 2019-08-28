import projectq

class ParityMeasurementGate(projectq.ops.MeasureGate):
    def __init__(self, bases, is_inverted = False):
        """
        
        """
        super(projectq.ops.MeasureGate, self).__init__()
        self._bases = []
        self._is_inverted = is_inverted

        if(isinstance(bases, str)):
            for el in bases.split():
                if len(el) < 2:
                    raise ValueError('term specified incorrectly.')
                self._bases.append((int(el[1:]), el[0]))
        
        elif(isinstance(bases, list)):
            for el in bases:
                assert(isinstance(el, tuple))
                assert(isinstance(el[0], int))
                assert(isinstance(el[1], str) and el[1] in ["X","Y","Z"])
                self._bases.append(el)

        # Test that _bases has correct format of tuples
        for local_operator in self._bases:
            qubit_num, action = local_operator
            if not isinstance(action, str) or action not in 'XYZ':
                raise ValueError("Invalid action provided: must be "
                    "string 'X', 'Y', or 'Z'.")
                if not (isinstance(qubit_num, int) and qubit_num >= 0):
                    raise QubitOperatorError("Invalid qubit number "
                        "provided to QubitTerm: "
                        "must be a non-negative "
                        "int.")

        self._bases.sort(key=lambda loc_operator: loc_operator[0])
        return

    def __str__(self):
        name = "Parity Measurement " 
        for element in self._bases:
            name += str(element[1]) + str(element[0]) + " "
        return name


    def __or__(self, qubits):
        """
        Only accepts a 
        """
        qubits = self.make_tuple_of_qureg(qubits)
        if len(qubits) != 1:
            raise TypeError("Only one qubit or qureg allowed.")
        
        # Check that Qureg has enough qubits:
        num_qubits = len(qubits[0])
        non_trivial_qubits = set()
        for index, action in self._bases:
            non_trivial_qubits.add(index)
        if max(non_trivial_qubits) >= num_qubits:
            raise ValueError("QubitOperator acts on more qubits than the qureg "
                             "is applied to.")
        
        # Perform X,Y,Z measurement if ParityMeasurement acts only on one qubit
        if len(self._bases) == 1:
            if self._bases[0][1] == "X":
                projectq.ops.H | qubits[0][self._bases[0][0]]
                projectq.ops.Measure | qubits[0][self._bases[0][0]]
            elif self._bases[0][1] == "Y":
                projectq.ops.S * projectq.ops.H | qubits[0][self._bases[0][0]]
                projectq.ops.Measure | qubits[0][self._bases[0][0]]
            elif self._bases[0][1] == "Z":
                projectq.ops.Measure | qubits[0][self._bases[0][0]]
            return

        # Create new ParityMeasurement gate with rescaled qubit indices in
        # 0,..., len(non_trivial_qubits) - 1
        new_index = dict()
        non_trivial_qubits = sorted(list(non_trivial_qubits))
        for i in range(len(non_trivial_qubits)):
            new_index[non_trivial_qubits[i]] = i
        new_bases = [(new_index[index], action) for index, action in self._bases]
        new_qubits = [qubits[0][i] for i in non_trivial_qubits]
        new_paritymeasurement = ParityMeasurementGate(new_bases, self._is_inverted)
        # Apply new gate
        cmd = new_paritymeasurement.generate_command(new_qubits)
        projectq.ops.apply_command(cmd)
