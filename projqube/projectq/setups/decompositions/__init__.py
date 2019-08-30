from . import parity_measurement, cnot2rotations, cnu2toffoliandcu, cz2cnot

all_defined_decomposition_rules = [
    rule
    for module in [cz2cnot,
                   cnu2toffoliandcu,
                   parity_measurement
                   ]
    for rule in module.all_defined_decomposition_rules
]
