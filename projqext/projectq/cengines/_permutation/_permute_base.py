
from projectq.cengines import BasicEngine
from projectq.ops import ClassicalInstructionGate, FlushGate, FastForwardingGate, NotMergeable, MeasureGate, AllocateQubitGate, AllocateDirtyQubitGate

from projqext.projectq.cengines._permutation._linkedlist import DoubleLinkedList
from projqext.projectq.cengines._permutation._permutation_rules import BasePermutationRules

class PermuteBase(BasicEngine):
    """
    Permutes all gates of a certain type to the front. For this the whole
    circuit needs to be read into memory and acted upon. Thus, it breaks the
    streaming operators after its application.

    All commands are stored in a linked lists. This allows O(1) inserts and
    deletion operations. Easy swaps between gates are also possible.
    """
    def __init__(self, permutation_rule):
        """
        Initialize the Permutation Base Engine.
        To use the permutation engine please use a derived class.
        """
        BasicEngine.__init__(self)
        self._dllist = DoubleLinkedList()  # dict of lists containing operations for each qubit
        self._perm = permutation_rule(self._dllist)


    def _send_qubit_pipeline(self):
        """
        Send the first gates that are already in the proper location
        """
        for node in self._dllist:
            self.send([node.data])
        # now remove all elements from it
        del self._dllist
        self._dllist = DoubleLinkedList()  # dict of lists containing operations for each qubit
        return


    def _permute(self):
        """
        This function needs to be overwritten by the derived class.
        It should perform the Permutation.
        """
        return



    def receive(self, command_list):
        """
        Receive commands from the previous engine and cache them.
        If a flush gate arrives, this engine assumes the circuit is
        finished and sends the permuted circuit to the next engine.
        """
        for cmd in command_list:
            if (isinstance(cmd.gate, FlushGate)):  # flush gate --> permute and flush
                #print("Warning: received a flush gate. For the permutation engine to work a flush can only be performed at the very end.")
                self.permute() # perform permutations
                self._send_qubit_pipeline() # send the new commands onwards and delete the stored list of commands
                self.send([cmd]) # send the flush command
            else: # new command
                # push back command into linked list
                self._dllist.push_back(cmd)



