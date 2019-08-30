#   Copyright 2018 ProjectQ-Framework (www.projectq.ch)
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
Registers a decomposition to for a CNOT gate in terms of CZ and Hadamard.
"""

from projectq.cengines import DecompositionRule
from projectq.meta import Compute, get_control_count, Uncompute
from projectq.ops import CNOT, H, Z, Y, S, Toffoli

def _decompose_cz(cmd):
    """ Decompose CNOT gates. """
    ctrl = cmd.control_qubits
    eng = cmd.engine
    with Compute(eng):
        H | cmd.qubits[0]
    CNOT | (ctrl[0], cmd.qubits[0][0])
    Uncompute(eng)

def _decompose_cy(cmd):
    """ Decompose CNOT gates. """
    ctrl = cmd.control_qubits
    eng = cmd.engine
    with Compute(eng):
        S | cmd.qubits[0]
    CNOT | (ctrl[0], cmd.qubits[0][0])
    Uncompute(eng)


def _recognize_cz(cmd):
    return get_control_count(cmd) == 1



def _decompose_ccz(cmd):
    """ Decompose CNOT gates. """
    ctrl = cmd.control_qubits
    eng = cmd.engine
    with Compute(eng):
        H | cmd.qubits[0]
    Toffoli | (ctrl[0], ctrl[1], cmd.qubits[0][0])
    Uncompute(eng)

def _decompose_ccy(cmd):
    """ Decompose CNOT gates. """
    ctrl = cmd.control_qubits
    eng = cmd.engine
    with Compute(eng):
        S | cmd.qubits[0]
    Toffoli | (ctrl[0], ctrl[1], cmd.qubits[0][0])
    Uncompute(eng)


def _recognize_ccz(cmd):
    return get_control_count(cmd) == 2

#: Decomposition rules
all_defined_decomposition_rules = [
    DecompositionRule(Z.__class__, _decompose_cz, _recognize_cz),
    DecompositionRule(Y.__class__, _decompose_cy, _recognize_cz),
    DecompositionRule(Z.__class__, _decompose_ccz, _recognize_ccz),
    DecompositionRule(Y.__class__, _decompose_ccy, _recognize_ccz)
]
