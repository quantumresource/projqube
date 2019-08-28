from projqext.projectq.backends import OpenSurgeryExporter
import projectq
import projectq.ops as gates
import cmath
import os


def test_simple():
    eng = projectq.MainEngine(engine_list = [], backend=OpenSurgeryExporter(output="test_simple_case1"))
    qubit1 = eng.allocate_qubit()
    qubit2 = eng.allocate_qubit()
    gates.T | qubit2
    gates.ParityMeasurementGate("Z0 X1") | qubit1+qubit2
    eng.flush()
    del qubit1
    del qubit2

    #assert(False)
    #now check output
    with open("test_simple_case1") as fin:
        line = fin.readline()
        line = line.strip()
        assert(line == "INIT 2")
        
        line = fin.readline()
        line = line.strip()
        assert(line == "NEED A")

        line = fin.readline()
        line = line.strip()
        assert(line == "MZZ A 1")

        line = fin.readline()
        line = line.strip()
        assert(line == "MX A")

        line = fin.readline()
        line = line.strip()
        assert(line == "S ANCILLA")

        line = fin.readline()
        line = line.strip()
        assert(line == "MXX ANCILLA 1")

        line = fin.readline()
        line = line.strip()
        assert(line == "H 1")

        line = fin.readline()
        line = line.strip()
        assert(line == "MZZ 0 1")

    os.remove("test_simple_case1")



def test_simple2():
    eng = projectq.MainEngine(engine_list = [], backend=OpenSurgeryExporter(output="test_simple_case2"))
    qubit1 = eng.allocate_qubit()
    qubit2 = eng.allocate_qubit()
    gates.TimeEvolution(- cmath.pi/8, gates.QubitOperator("Y0 X1")) | qubit1 + qubit2

    eng.flush()
    del qubit1
    del qubit2

    with open("test_simple_case2") as fin:
        line = fin.readline()
        line = line.strip()
        assert(line == "INIT 2")
        
        line = fin.readline()
        line = line.strip()
        assert(line == "H 0")

        line = fin.readline()
        line = line.strip()
        assert(line == "S 0")

        line = fin.readline()
        line = line.strip()
        assert(line == "H 1")

        line = fin.readline()
        line = line.strip()
        assert(line == "NEED A")

        line = fin.readline()
        line = line.strip()
        assert(line == "MZZ A 0 1")

        
        line = fin.readline()
        line = line.strip()
        assert(line == "MX A")


        line = fin.readline()
        line = line.strip()
        assert(line == "S ANCILLA")

        line = fin.readline()
        line = line.strip()
        assert(line == "MXX ANCILLA 0 1")

        line = fin.readline()
        line = line.strip()
        assert(line == "S 0")

        line = fin.readline()
        line = line.strip()
        assert(line == "H 0")

        line = fin.readline()
        line = line.strip()
        assert(line == "H 1")

    os.remove("test_simple_case2")