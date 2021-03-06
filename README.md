<img src="projqube.png" alt="projqube" height="100px"></img>

# ProjQUBE_alpha is a collection of extensions to ProjectQ

It was developed by [Daniel Herr](https://github.com/herr-d)and includes:
* Clifford circuit simulator
* Engine for gate permutations through the circuit
* Exporter into [OpenSurgery](https://github.com/alexandrupaler/opensurgery/) instructions


The original repository (QC_benchmark) included ProjectQ code. This repository separated the extensions from ProjectQ, reorganised the code into packages and, where needed, extended it.

The namespace projqube is organised similarly to the ``projectq`` namespace from the original codebase.
For example, if the OpenSurgery exporter is needed, then ``projqube.projectq.cengines`` is the package for the ``OpenSurgeryExporter``

More documentation: TODO

The original CHP circuits are simulated in ``tests/chp_circuits_simulator.py``