import unittest
from QuantumPathQSOAPySDK.circuit.gates.utilities import (Barrier, BeginRepeat, EndRepeat)

# UTILITIES:
#   Barrier
#   BeginRepeat
#   EndRepeat

##################_____Barrier_____##################
class Test_Barrier(unittest.TestCase):

    # Barrier
    def test_Barrier(self):
        gate = Barrier(0)

        self.assertIsInstance(gate, Barrier)
        self.assertEqual(gate.getSymbol(), 'SPACER')
        self.assertEqual(gate.getControllable(), False)
        self.assertEqual(gate.getPosition(), 0)

    # BAD ARGUMENT TYPE position
    def test_Barrier_badArgumentType_position(self):
        try:
            Barrier('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____BeginRepeat_____##################
class Test_BeginRepeat(unittest.TestCase):

    # BeginRepeat
    def test_BeginRepeat(self):
        gate = BeginRepeat(0, 2)

        self.assertIsInstance(gate, BeginRepeat)
        self.assertEqual(gate.getSymbol(), {'id': 'BEGIN_R', 'arg': '2'})
        self.assertEqual(gate.getControllable(), False)
        self.assertEqual(gate.getPosition(), 0)
        self.assertEqual(gate.getArgument(), 2)

    # BAD ARGUMENT TYPE position
    def test_BeginRepeat_badArgumentType_position(self):
        try:
            BeginRepeat('position', 2)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE repetitions
    def test_BeginRepeat_badArgumentType_repetitions(self):
        try:
            BeginRepeat(0, 'repetitions')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____EndRepeat_____##################
class Test_EndRepeat(unittest.TestCase):

    # EndRepeat
    def test_EndRepeat(self):
        gate = EndRepeat(0)

        self.assertIsInstance(gate, EndRepeat)
        self.assertEqual(gate.getSymbol(), 'END_R')
        self.assertEqual(gate.getControllable(), False)
        self.assertEqual(gate.getPosition(), 0)

    # BAD ARGUMENT TYPE position
    def test_EndRepeat_badArgumentType_position(self):
        try:
            EndRepeat('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


if __name__ == '__main__':
    unittest.main()