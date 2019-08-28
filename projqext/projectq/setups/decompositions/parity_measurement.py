#   Copyright 2017 ProjectQ-Framework (www.projectq.ch)
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
Registers a decomposition rule for Parity Measurements.
"""
from projectq.types import Qureg
from projectq.cengines import DecompositionRule
from projectq.meta import Control
from projectq.ops import ParityMeasurementGate, CNOT, S, X, H, get_inverse, Measure


def _decompose_parity_measurement(cmd):
    ancilla = cmd.engine.allocate_qubit()
    for pos, action in cmd.gate._bases:
        qureg = Qureg([cmd.qubits[0][pos]])
        if action == "X":
            H | cmd.qubits[0][pos]
            with Control(cmd.engine, qureg):
                X | ancilla
            H | cmd.qubits[0][pos]

        elif action == "Y":
            H | cmd.qubits[0][pos]
            S | cmd.qubits[0][pos]
            with Control(cmd.engine, qureg):
                X | ancilla
            get_inverse(S) | cmd.qubits[0][pos]
            H | cmd.qubits[0][pos]
        elif action == "Z":
            with Control(cmd.engine, qureg):
              X | ancilla


    # if there is a minus sign
    if(cmd.gate._is_inverted):
        X | ancilla

    # at last measure the parity:
    Measure | ancilla

def _recognize_paritymeasurement(cmd):
    """ Recognize all ParityMeasurements. """
    return True


#: Decomposition rules
all_defined_decomposition_rules = [
    DecompositionRule(ParityMeasurementGate, _decompose_parity_measurement, _recognize_paritymeasurement)
]
