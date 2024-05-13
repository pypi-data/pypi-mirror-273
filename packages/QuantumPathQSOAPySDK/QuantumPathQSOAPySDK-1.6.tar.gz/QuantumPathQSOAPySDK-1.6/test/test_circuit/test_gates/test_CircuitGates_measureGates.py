import unittest
from QuantumPathQSOAPySDK import QSOAPlatform
from QuantumPathQSOAPySDK.circuit.gates.measureGates import (MeasureGate)

# MEASURE GATES:
#   MeasureGate

##################_____MEASURE_____##################
class Test_Measure(unittest.TestCase):

    # MEASURE position 0
    def test_measure_position_0(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.measure(0)

        self.assertIsInstance(gate, MeasureGate)
        self.assertEqual(circuit.getCircuitBody(), [['Measure']])

    # MEASURE position 1
    def test_measure_position_1(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.measure(1)

        self.assertIsInstance(gate, MeasureGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'Measure']])

    # MEASURE EXISTING CIRCUIT position NEW COLUMN
    def test_measure_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.measure(0)

        self.assertIsInstance(gate, MeasureGate)
        self.assertEqual(circuit.getCircuitBody(), [['H'], ['Measure']])

    # MEASURE EXISTING CIRCUIT position SAME COLUMN
    def test_measure_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.measure(1)

        self.assertIsInstance(gate, MeasureGate)
        self.assertEqual(circuit.getCircuitBody(), [['H', 'Measure']])

    # MEASURE EXISTING CIRCUIT position BETWEEN SWAP
    def test_measure_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.measure(1)

        self.assertIsInstance(gate, MeasureGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'Measure']])

    # MEASURE EXISTING CIRCUIT position UNDER SWAP
    def test_measure_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.measure(2)

        self.assertIsInstance(gate, MeasureGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'Measure']])

    # MEASURE position LIST
    def test_measure_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.measure([0, 1])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], MeasureGate)
        self.assertEqual(circuit.getCircuitBody(), [['Measure', 'Measure']])
    
    # MEASURE position LIST EXISTING CIRCUIT
    def test_measure_position_list_existingCircuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.measure([1, 2])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], MeasureGate)
        self.assertEqual(circuit.getCircuitBody(), [['H'], [1, 'Measure', 'Measure']])

    # MEASURE position ALL
    def test_measure_position_all(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.measure()

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], MeasureGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'H'], ['Measure', 'Measure']])
    
    # BAD ARGUMENT position LIST
    def test_measure_badArgument_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.measure([])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT position LIST DUPLICATED
    def test_measure_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.measure([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_measure_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.measure('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_measure_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.measure([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


if __name__ == '__main__':
    unittest.main()