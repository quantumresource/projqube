from projectq.ops import ClassicalInstructionGate, FastForwardingGate

from projqube.projectq.cengines import BasePermutationRules, PermuteBase


class PermuteCliffordBack(PermuteBase):
    def __init__(self):
        super(PermuteCliffordBack, self).__init__(BasePermutationRules)


    def permute(self):
        for node in reversed(self._dllist):
            if(self._gate_of_interest(node) and not isinstance(node.data.gate,ClassicalInstructionGate)):
                while(self._permutation_required(node.next)):
                    self._perm.permute(node, node.next)
        return


    def _gate_of_interest(self, node):
        if(BasePermutationRules.is_clifford(node.data.gate)):
            return True
        return False


    def _permutation_required(self, right):
        if (right == None or isinstance(right.data.gate, FastForwardingGate)):
            return False
        if(self._gate_of_interest(right)):
            return False
        return True