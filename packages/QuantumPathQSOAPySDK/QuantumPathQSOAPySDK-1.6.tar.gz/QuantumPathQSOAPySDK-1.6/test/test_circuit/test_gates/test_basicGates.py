import unittest
from QuantumPathQSOAPySDK.circuit.gates.basicGates import (HGate, XGate, YGate, ZGate, SwapGate, CHGate, CXGate, CCXGate)

# BASIC GATES:
#   HGate
#   XGate
#   YGate
#   ZGate
#   SwapGate
#   CHGate
#   CXGate
#   CCXGate

##################_____HGate_____##################
class Test_HGate(unittest.TestCase):

    # HGate
    def test_HGate(self):
        gate = HGate(0)

        self.assertIsInstance(gate, HGate)
        self.assertEqual(gate.getSymbol(), 'H')
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getPosition(), 0)

    # BAD ARGUMENT TYPE position
    def test_HGate_badArgumentType_position(self):
        try:
            HGate('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____XGate_____##################
class Test_XGate(unittest.TestCase):

    # XGate
    def test_XGate(self):
        gate = XGate(0)

        self.assertIsInstance(gate, XGate)
        self.assertEqual(gate.getSymbol(), 'X')
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getPosition(), 0)

    # BAD ARGUMENT TYPE position
    def test_XGate_badArgumentType_position(self):
        try:
            XGate('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____YGate_____##################
class Test_YGate(unittest.TestCase):

    # YGate
    def test_YGate(self):
        gate = YGate(0)

        self.assertIsInstance(gate, YGate)
        self.assertEqual(gate.getSymbol(), 'Y')
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getPosition(), 0)

    # BAD ARGUMENT TYPE position
    def test_YGate_badArgumentType_position(self):
        try:
            YGate('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____ZGate_____##################
class Test_ZGate(unittest.TestCase):

    # ZGate
    def test_ZGate(self):
        gate = ZGate(0)

        self.assertIsInstance(gate, ZGate)
        self.assertEqual(gate.getSymbol(), 'Z')
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getPosition(), 0)

    # BAD ARGUMENT TYPE position
    def test_ZGate_badArgumentType_position(self):
        try:
            ZGate('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____SwapGate_____##################
class Test_SwapGate(unittest.TestCase):

    # SwapGate
    def test_SwapGate(self):
        gate = SwapGate(0, 1)

        self.assertIsInstance(gate, SwapGate)
        self.assertEqual(gate.getSymbol(), 'Swap')
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getPositions(), [0, 1])

    # BAD ARGUMENT TYPE position1
    def test_SwapGate_badArgumentType_position1(self):
        try:
            SwapGate('position1', 1)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position2
    def test_SwapGate_badArgumentType_position2(self):
        try:
            SwapGate(0, 'position2')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____CHGate_____##################
class Test_CHGate(unittest.TestCase):

    # CHGate
    def test_CHGate(self):
        gate = CHGate(0, 1)

        self.assertIsInstance(gate, CHGate)
        self.assertEqual(gate.getSymbol(), 'H')
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getControlSymbol(), 'CTRL')
        self.assertEqual(gate.getControlPositions(), [0])
        self.assertEqual(gate.getTargetPosition(), 1)

    # BAD ARGUMENT TYPE position1
    def test_CHGate_badArgumentType_position1(self):
        try:
            CHGate('position1', 1)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position2
    def test_CHGate_badArgumentType_position2(self):
        try:
            CHGate(0, 'position2')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____CXGate_____##################
class Test_CXGate(unittest.TestCase):

    # CXGate
    def test_CXGate(self):
        gate = CXGate(0, 1)

        self.assertIsInstance(gate, CXGate)
        self.assertEqual(gate.getSymbol(), 'X')
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getControlSymbol(), 'CTRL')
        self.assertEqual(gate.getControlPositions(), [0])
        self.assertEqual(gate.getTargetPosition(), 1)

    # BAD ARGUMENT TYPE position1
    def test_CXGate_badArgumentType_position1(self):
        try:
            CXGate('position1', 1)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position2
    def test_CXGate_badArgumentType_position2(self):
        try:
            CXGate(0, 'position2')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____CCXGate_____##################
class Test_CCXGate(unittest.TestCase):

    # CCXGate
    def test_CCXGate(self):
        gate = CCXGate(0, 1, 2)

        self.assertIsInstance(gate, CCXGate)
        self.assertEqual(gate.getSymbol(), 'X')
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getControlSymbol(), 'CTRL')
        self.assertEqual(gate.getControlPositions(), [0, 1])
        self.assertEqual(gate.getTargetPosition(), 2)

    # BAD ARGUMENT TYPE position1
    def test_CCXGate_badArgumentType_position1(self):
        try:
            CXGate('position1', 1, 2)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position2
    def test_CCXGate_badArgumentType_position2(self):
        try:
            CXGate(0, 'position2', 2)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position3
    def test_CCXGate_badArgumentType_position3(self):
        try:
            CXGate(0, 1, 'position3')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


if __name__ == '__main__':
    unittest.main()