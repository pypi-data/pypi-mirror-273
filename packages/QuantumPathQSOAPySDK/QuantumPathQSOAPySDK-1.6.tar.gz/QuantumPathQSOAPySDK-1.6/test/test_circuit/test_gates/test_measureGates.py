import unittest
from QuantumPathQSOAPySDK.circuit.gates.measureGates import (MeasureGate)

# MEASURE GATES:
#   MeasureGate

##################_____MeasureGate_____##################
class Test_MeasureGate(unittest.TestCase):

    # MeasureGate
    def test_MeasureGate(self):
        gate = MeasureGate(0)

        self.assertIsInstance(gate, MeasureGate)
        self.assertEqual(gate.getSymbol(), 'Measure')
        self.assertEqual(gate.getControllable(), False)
        self.assertEqual(gate.getPosition(), 0)

    # BAD ARGUMENT TYPE position
    def test_MeasureGate_badArgumentType_position(self):
        try:
            MeasureGate('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

if __name__ == '__main__':
    unittest.main()