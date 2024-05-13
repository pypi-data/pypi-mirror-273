import unittest
from QuantumPathQSOAPySDK.circuit.gates.preparedGates import (SGate, I_SGate, SXGate, I_SXGate, SYGate, I_SYGate, TGate, I_TGate, TXGate, I_TXGate, TYGate, I_TYGate)

# PREPARED GATES:
#   SGate
#   I_SGate
#   SXGate
#   I_SXGate
#   SYGate
#   I_SYGate
#   TGate
#   I_TGate
#   TXGate
#   I_TXGate
#   TYGate
#   I_TYGate

##################_____SGate_____##################
class Test_SGate(unittest.TestCase):

    # SGate
    def test_SGate(self):
        gate = SGate(0)

        self.assertIsInstance(gate, SGate)
        self.assertEqual(gate.getSymbol(), 'S')
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getPosition(), 0)

    # BAD ARGUMENT TYPE position
    def test_SGate_badArgumentType_position(self):
        try:
            SGate('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____I_SGate_____##################
class Test_I_SGate(unittest.TestCase):

    # I_SGate
    def test_I_SGate(self):
        gate = I_SGate(0)

        self.assertIsInstance(gate, I_SGate)
        self.assertEqual(gate.getSymbol(), 'I_S')
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getPosition(), 0)

    # BAD ARGUMENT TYPE position
    def test_I_SGate_badArgumentType_position(self):
        try:
            I_SGate('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____SXGate_____##################
class Test_SXGate(unittest.TestCase):

    # SXGate
    def test_SXGate(self):
        gate = SXGate(0)

        self.assertIsInstance(gate, SXGate)
        self.assertEqual(gate.getSymbol(), 'SX')
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getPosition(), 0)

    # BAD ARGUMENT TYPE position
    def test_SXGate_badArgumentType_position(self):
        try:
            SXGate('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____I_SXGate_____##################
class Test_I_SXGate(unittest.TestCase):

    # I_SXGate
    def test_I_SXGate(self):
        gate = I_SXGate(0)

        self.assertIsInstance(gate, I_SXGate)
        self.assertEqual(gate.getSymbol(), 'I_SX')
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getPosition(), 0)

    # BAD ARGUMENT TYPE position
    def test_I_SXGate_badArgumentType_position(self):
        try:
            I_SXGate('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____SYGate_____##################
class Test_SYGate(unittest.TestCase):

    # SYGate
    def test_SYGate(self):
        gate = SYGate(0)

        self.assertIsInstance(gate, SYGate)
        self.assertEqual(gate.getSymbol(), 'SY')
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getPosition(), 0)

    # BAD ARGUMENT TYPE position
    def test_SYGate_badArgumentType_position(self):
        try:
            SYGate('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____I_SYGate_____##################
class Test_I_SYGate(unittest.TestCase):

    # I_SYGate
    def test_I_SYGate(self):
        gate = I_SYGate(0)

        self.assertIsInstance(gate, I_SYGate)
        self.assertEqual(gate.getSymbol(), 'I_SY')
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getPosition(), 0)

    # BAD ARGUMENT TYPE position
    def test_I_SYGate_badArgumentType_position(self):
        try:
            I_SYGate('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____TGate_____##################
class Test_TGate(unittest.TestCase):

    # TGate
    def test_TGate(self):
        gate = TGate(0)

        self.assertIsInstance(gate, TGate)
        self.assertEqual(gate.getSymbol(), 'T')
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getPosition(), 0)

    # BAD ARGUMENT TYPE position
    def test_TGate_badArgumentType_position(self):
        try:
            TGate('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____I_TGate_____##################
class Test_I_TGate(unittest.TestCase):

    # I_TGate
    def test_I_TGate(self):
        gate = I_TGate(0)

        self.assertIsInstance(gate, I_TGate)
        self.assertEqual(gate.getSymbol(), 'I_T')
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getPosition(), 0)

    # BAD ARGUMENT TYPE position
    def test_I_TGate_badArgumentType_position(self):
        try:
            I_TGate('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____TXGate_____##################
class Test_TXGate(unittest.TestCase):

    # TXGate
    def test_TXGate(self):
        gate = TXGate(0)

        self.assertIsInstance(gate, TXGate)
        self.assertEqual(gate.getSymbol(), 'TX')
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getPosition(), 0)

    # BAD ARGUMENT TYPE position
    def test_TXGate_badArgumentType_position(self):
        try:
            TXGate('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____I_TXGate_____##################
class Test_I_TXGate(unittest.TestCase):

    # I_TXGate
    def test_I_TXGate(self):
        gate = I_TXGate(0)

        self.assertIsInstance(gate, I_TXGate)
        self.assertEqual(gate.getSymbol(), 'I_TX')
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getPosition(), 0)

    # BAD ARGUMENT TYPE position
    def test_I_TXGate_badArgumentType_position(self):
        try:
            I_TXGate('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____TYGate_____##################
class Test_TYGate(unittest.TestCase):

    # TYGate
    def test_TYGate(self):
        gate = TYGate(0)

        self.assertIsInstance(gate, TYGate)
        self.assertEqual(gate.getSymbol(), 'TY')
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getPosition(), 0)

    # BAD ARGUMENT TYPE position
    def test_TYGate_badArgumentType_position(self):
        try:
            TYGate('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____I_TYGate_____##################
class Test_I_TYGate(unittest.TestCase):

    # I_TYGate
    def test_I_TYGate(self):
        gate = I_TYGate(0)

        self.assertIsInstance(gate, I_TYGate)
        self.assertEqual(gate.getSymbol(), 'I_TY')
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getPosition(), 0)

    # BAD ARGUMENT TYPE position
    def test_I_TYGate_badArgumentType_position(self):
        try:
            I_TYGate('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


if __name__ == '__main__':
    unittest.main()