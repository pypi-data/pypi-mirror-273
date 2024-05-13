import unittest
from QuantumPathQSOAPySDK.circuit.gates.rotationGates import (PGate, RXGate, RYGate, RZGate)

# ROTATION GATES:
#   PGate
#   RXGate
#   RYGate
#   RZGate

##################_____PGate_____##################
class Test_PGate(unittest.TestCase):

    # PGate argument INT
    def test_PGate_argument_int(self):
        gate = PGate(0, 1)

        self.assertIsInstance(gate, PGate)
        self.assertEqual(gate.getSymbol(), {'id': 'P', 'arg': '1'})
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getPosition(), 0)
        self.assertEqual(gate.getArgument(), 1)

    # PGate argument INT
    def test_PGate_argument_float(self):
        gate = PGate(0, 1.5)

        self.assertIsInstance(gate, PGate)
        self.assertEqual(gate.getSymbol(), {'id': 'P', 'arg': '1.5'})
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getPosition(), 0)
        self.assertEqual(gate.getArgument(), 1.5)

    # PGate argument STRING NUMBER
    def test_PGate_argument_string_number(self):
        gate = PGate(0, '1')

        self.assertIsInstance(gate, PGate)
        self.assertEqual(gate.getSymbol(), {'id': 'P', 'arg': '1'})
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getPosition(), 0)
        self.assertEqual(gate.getArgument(), '1')

    # PGate argument STRING EXPRESSION
    def test_PGate_argument_string_expression(self):
        gate = PGate(0, 'pi/2')

        self.assertIsInstance(gate, PGate)
        self.assertEqual(gate.getSymbol(), {'id': 'P', 'arg': 'pi/2'})
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getPosition(), 0)
        self.assertEqual(gate.getArgument(), 'pi/2')

    # BAD ARGUMENT argument
    def test_PGate_badArgument_argument(self):
        try:
            PGate(0, 'argument')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_PGate_badArgumentType_position(self):
        try:
            PGate('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE argument
    def test_PGate_badArgumentType_argument(self):
        try:
            PGate(0, True)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____RXGate_____##################
class Test_RXGate(unittest.TestCase):

    # RXGate argument INT
    def test_RXGate_argument_int(self):
        gate = RXGate(0, 1)

        self.assertIsInstance(gate, RXGate)
        self.assertEqual(gate.getSymbol(), {'id': 'RX', 'arg': '1'})
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getPosition(), 0)
        self.assertEqual(gate.getArgument(), 1)

    # RXGate argument INT
    def test_RXGate_argument_float(self):
        gate = RXGate(0, 1.5)

        self.assertIsInstance(gate, RXGate)
        self.assertEqual(gate.getSymbol(), {'id': 'RX', 'arg': '1.5'})
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getPosition(), 0)
        self.assertEqual(gate.getArgument(), 1.5)

    # RXGate argument STRING NUMBER
    def test_RXGate_argument_string_number(self):
        gate = RXGate(0, '1')

        self.assertIsInstance(gate, RXGate)
        self.assertEqual(gate.getSymbol(), {'id': 'RX', 'arg': '1'})
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getPosition(), 0)
        self.assertEqual(gate.getArgument(), '1')

    # RXGate argument STRING EXPRESSION
    def test_RXGate_argument_string_expression(self):
        gate = RXGate(0, 'pi/2')

        self.assertIsInstance(gate, RXGate)
        self.assertEqual(gate.getSymbol(), {'id': 'RX', 'arg': 'pi/2'})
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getPosition(), 0)
        self.assertEqual(gate.getArgument(), 'pi/2')

    # BAD ARGUMENT argument
    def test_RXGate_badArgument_argument(self):
        try:
            RXGate(0, 'argument')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_RXGate_badArgumentType_position(self):
        try:
            RXGate('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE argument
    def test_RXGate_badArgumentType_argument(self):
        try:
            RXGate(0, True)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____RYGate_____##################
class Test_RYGate(unittest.TestCase):

    # RYGate argument INT
    def test_RYGate_argument_int(self):
        gate = RYGate(0, 1)

        self.assertIsInstance(gate, RYGate)
        self.assertEqual(gate.getSymbol(), {'id': 'RY', 'arg': '1'})
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getPosition(), 0)
        self.assertEqual(gate.getArgument(), 1)

    # RYGate argument INT
    def test_RYGate_argument_float(self):
        gate = RYGate(0, 1.5)

        self.assertIsInstance(gate, RYGate)
        self.assertEqual(gate.getSymbol(), {'id': 'RY', 'arg': '1.5'})
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getPosition(), 0)
        self.assertEqual(gate.getArgument(), 1.5)

    # RYGate argument STRING NUMBER
    def test_RYGate_argument_string_number(self):
        gate = RYGate(0, '1')

        self.assertIsInstance(gate, RYGate)
        self.assertEqual(gate.getSymbol(), {'id': 'RY', 'arg': '1'})
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getPosition(), 0)
        self.assertEqual(gate.getArgument(), '1')

    # RYGate argument STRING EXPRESSION
    def test_RYGate_argument_string_expression(self):
        gate = RYGate(0, 'pi/2')

        self.assertIsInstance(gate, RYGate)
        self.assertEqual(gate.getSymbol(), {'id': 'RY', 'arg': 'pi/2'})
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getPosition(), 0)
        self.assertEqual(gate.getArgument(), 'pi/2')

    # BAD ARGUMENT argument
    def test_RYGate_badArgument_argument(self):
        try:
            RYGate(0, 'argument')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_RYGate_badArgumentType_position(self):
        try:
            RYGate('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE argument
    def test_RYGate_badArgumentType_argument(self):
        try:
            RYGate(0, True)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____RZGate_____##################
class Test_RZGate(unittest.TestCase):

    # RZGate argument INT
    def test_RZGate_argument_int(self):
        gate = RZGate(0, 1)

        self.assertIsInstance(gate, RZGate)
        self.assertEqual(gate.getSymbol(), {'id': 'RZ', 'arg': '1'})
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getPosition(), 0)
        self.assertEqual(gate.getArgument(), 1)

    # RZGate argument INT
    def test_RZGate_argument_float(self):
        gate = RZGate(0, 1.5)

        self.assertIsInstance(gate, RZGate)
        self.assertEqual(gate.getSymbol(), {'id': 'RZ', 'arg': '1.5'})
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getPosition(), 0)
        self.assertEqual(gate.getArgument(), 1.5)

    # RZGate argument STRING NUMBER
    def test_RZGate_argument_string_number(self):
        gate = RZGate(0, '1')

        self.assertIsInstance(gate, RZGate)
        self.assertEqual(gate.getSymbol(), {'id': 'RZ', 'arg': '1'})
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getPosition(), 0)
        self.assertEqual(gate.getArgument(), '1')

    # RZGate argument STRING EXPRESSION
    def test_RZGate_argument_string_expression(self):
        gate = RZGate(0, 'pi/2')

        self.assertIsInstance(gate, RZGate)
        self.assertEqual(gate.getSymbol(), {'id': 'RZ', 'arg': 'pi/2'})
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getPosition(), 0)
        self.assertEqual(gate.getArgument(), 'pi/2')

    # BAD ARGUMENT argument
    def test_RZGate_badArgument_argument(self):
        try:
            RZGate(0, 'argument')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_RZGate_badArgumentType_position(self):
        try:
            RZGate('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE argument
    def test_RZGate_badArgumentType_argument(self):
        try:
            RZGate(0, True)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


if __name__ == '__main__':
    unittest.main()