from QuantumPathQSOAPySDK import QSOAPlatform
from QuantumPathQSOAPySDK.circuit.gates.basicGates import *
qsoa = QSOAPlatform(configFile=True)

circuit = qsoa.CircuitGates()

print(circuit.getCircuitBody())