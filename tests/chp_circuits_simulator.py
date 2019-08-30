import urllib  # the lib that handles the url stuff

import projectq
import projectq.ops

from projqube.projectq.cengines import MultiqubitMeasurementCliffordEngine

# a dictionary of files from the Aaronson site
list_of_chp_remote_files = {
    "epr" : "https://www.scottaaronson.com/chp/epr.chp",
    "ghz" : "https://www.scottaaronson.com/chp/ghz.chp"
    # add the other ones if needed
}

list_of_local_files = {
    "epr" : "../epr.chp",
    "ghz" : "../ghz.chp"
    # add the other ones if needed
}

def load_remote_file(target_url):
    response = urllib.request.urlopen(target_url)  # it's a file like object and works just like a file
    data = response.readlines()  # a `bytes` object

    text = []
    for line in data:
        strline = line.decode("utf-8").strip()
        text.append(strline)

    return text


def load_local_file(target_path):
    text = []
    with open(target_path, "r") as f:
        for line in f:
            text.append(line.strip())

    return text

def get_only_chp_instructions(circuit_lines):
    """
    The single character line "#" is marking the beginning of the CHP instructions
    :param circuit_lines:
    :return:
    """
    filtered = []

    add_next_line = False
    for line in circuit_lines:
        if line == "#":
            add_next_line = True
            continue
        if not add_next_line:
            continue
        filtered.append(line)

    return filtered


def get_number_of_qubits(filtered_lines):
    """
    Split the CHP instructions to find out maximum qubit index
    :param filtered_lines:
    :return:
    """
    nr_qubits = -1

    for line in filtered_lines:
        parts = line.split(" ")
        for qub in parts[1:]:
            nr_qubits = max(int(qub), nr_qubits)

    return nr_qubits + 1


class A:
    def __init__(self):
        self.commands = []

    def receive(self, cmd):
        self.commands += cmd

def simulate_chp_files():
    # Initialize the Clifford simulator
    engine_list = [MultiqubitMeasurementCliffordEngine()]
    engine = projectq.MainEngine(engine_list = engine_list)
    engine_list[0].next_engine = A()

    # the id of the file from the dictionary
    file_id = "epr"
    file_url = list_of_local_files[file_id]

    # load and return the file as list of strings
    lines = get_only_chp_instructions(load_local_file(file_url))

    # How many qubits does the circuit have?
    nrq = get_number_of_qubits(lines)
    print("number of qubits in CHP file", nrq)

    # Allocate the qubits and initialize them into the Z basis
    qubits = []
    for qi in range(nrq):
        qubit = engine.allocate_qubit()
        qubits.append(qubit)


    # Transform CHP instructions into ProjectQ commands
    simulator_commands = []
    for line in lines:
        parts_line = line.split(" ")
        chp_instr_type = parts_line[0]
        #
        qb_tuple = (qubits[int(parts_line[1])])
        if len(parts_line) == 3:
            # cnot has two qubits
            qb_tuple = (qubits[int(parts_line[1])],
                        qubits[int(parts_line[2])])

        # Dummy value
        cmd = None
        # Translation between strings and gate types
        if chp_instr_type == "h":
            projectq.ops.H | qb_tuple
        elif chp_instr_type == "p":
            projectq.ops.S | qb_tuple
        elif chp_instr_type == "m":
            projectq.ops.Measure | qb_tuple
        elif chp_instr_type == "c":
            projectq.ops.CNOT | qb_tuple

    print(engine_list[0]._simulator._stabilizers)

    engine.flush()

    return

if __name__ == '__main__':
    simulate_chp_files()



