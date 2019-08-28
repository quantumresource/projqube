from projectq.ops import ClassicalInstructionGate, FlushGate, FastForwardingGate, NotMergeable, MeasureGate, \
    AllocateQubitGate, AllocateDirtyQubitGate

from projqext.projectq.cengines import BasePermutationRules, PermuteBase


class PermutePi4Front(PermuteBase):
    def __init__(self):
        super(PermutePi4Front, self).__init__(BasePermutationRules)


    def permute(self):
        for node in self._dllist:
            if(self._gate_of_interest(node)):
                while(self._permutation_required(node.prev)):
                    self._perm.permute(node.prev, node)
        return


    def _gate_of_interest(self, node):
        if(isinstance(node.data.gate, ClassicalInstructionGate) and not isinstance(node.data.gate, FastForwardingGate)):
            return True
        if(BasePermutationRules.is_clifford(node.data.gate)):
            return False
        return True


    def _permutation_required(self, left):
        if (left == None or isinstance(left.data.gate,AllocateQubitGate) or isinstance(left.data.gate, AllocateDirtyQubitGate)):
            return False
        return BasePermutationRules.is_clifford(left.data.gate)