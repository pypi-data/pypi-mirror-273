import unittest
from QuantumPathQSOAPySDK import QSOAPlatform
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

##################_____S_____##################
class Test_S(unittest.TestCase):

    # S position 0
    def test_s_position_0(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.s(0)

        self.assertIsInstance(gate, SGate)
        self.assertEqual(circuit.getCircuitBody(), [['S']])

    # S position 1
    def test_s_position_1(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.s(1)

        self.assertIsInstance(gate, SGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'S']])

    # S EXISTING CIRCUIT position NEW COLUMN
    def test_s_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.s(0)

        gate = circuit.s(0)

        self.assertIsInstance(gate, SGate)
        self.assertEqual(circuit.getCircuitBody(), [['S'], ['S']])

    # S EXISTING CIRCUIT position SAME COLUMN
    def test_s_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.s(0)

        gate = circuit.s(1)

        self.assertIsInstance(gate, SGate)
        self.assertEqual(circuit.getCircuitBody(), [['S', 'S']])

    # S EXISTING CIRCUIT position BETWEEN SWAP
    def test_s_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.s(1)

        self.assertIsInstance(gate, SGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'S']])

    # S EXISTING CIRCUIT position UNDER SWAP
    def test_s_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.s(2)

        self.assertIsInstance(gate, SGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'S']])

    # S position LIST
    def test_s_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.s([0, 1])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], SGate)
        self.assertEqual(circuit.getCircuitBody(), [['S', 'S']])
    
    # S position LIST EXISTING CIRCUIT
    def test_s_position_list_existingCircuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.s(0)

        gate = circuit.s([1, 2])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], SGate)
        self.assertEqual(circuit.getCircuitBody(), [['S'], [1, 'S', 'S']])

    # S position ALL
    def test_s_position_all(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.s(1)

        gate = circuit.s()

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], SGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'S'], ['S', 'S']])

    # BAD ARGUMENT position LIST
    def test_s_badArgument_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.s([])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT position LIST DUPLICATED
    def test_s_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.s([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_s_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.s('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_s_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.s([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # DEPRECATED add: when add is deprecated REMOVE FROM HERE
    # S add
    def test_s_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.s(0, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'S')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # S position LIST add
    def test_s_position_list_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.s([0, 1], False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'S'), (1, 'S')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT TYPE add
    def test_s_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.s(0, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
    # TO HERE


##################_____I_S_____##################
class Test_I_S(unittest.TestCase):

    # I_S position 0
    def test_i_s_position_0(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.i_s(0)

        self.assertIsInstance(gate, I_SGate)
        self.assertEqual(circuit.getCircuitBody(), [['I_S']])

    # I_S position 1
    def test_i_s_position_1(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.i_s(1)

        self.assertIsInstance(gate, I_SGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'I_S']])

    # I_S EXISTING CIRCUIT position NEW COLUMN
    def test_i_s_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.i_s(0)

        gate = circuit.i_s(0)

        self.assertIsInstance(gate, I_SGate)
        self.assertEqual(circuit.getCircuitBody(), [['I_S'], ['I_S']])

    # I_S EXISTING CIRCUIT position SAME COLUMN
    def test_i_s_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.i_s(0)

        gate = circuit.i_s(1)

        self.assertIsInstance(gate, I_SGate)
        self.assertEqual(circuit.getCircuitBody(), [['I_S', 'I_S']])

    # I_S EXISTING CIRCUIT position BETWEEN SWAP
    def test_i_s_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.i_s(1)

        self.assertIsInstance(gate, I_SGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'I_S']])

    # I_S EXISTING CIRCUIT position UNDER SWAP
    def test_i_s_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.i_s(2)

        self.assertIsInstance(gate, I_SGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'I_S']])

    # I_S position LIST
    def test_i_s_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.i_s([0, 1])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], I_SGate)
        self.assertEqual(circuit.getCircuitBody(), [['I_S', 'I_S']])
    
    # I_S position LIST EXISTING CIRCUIT
    def test_i_s_position_list_existingCircuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.i_s(0)

        gate = circuit.i_s([1, 2])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], I_SGate)
        self.assertEqual(circuit.getCircuitBody(), [['I_S'], [1, 'I_S', 'I_S']])

    # I_S position ALL
    def test_i_s_position_all(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.i_s(1)

        gate = circuit.i_s()

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], I_SGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'I_S'], ['I_S', 'I_S']])

    # BAD ARGUMENT position LIST
    def test_i_s_badArgument_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_s([])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT position LIST DUPLICATED
    def test_i_s_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_s([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_i_s_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_s('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_i_s_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_s([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # DEPRECATED add: when add is deprecated REMOVE FROM HERE
    # I_S add
    def test_i_s_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.i_s(0, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_S')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # I_S position LIST add
    def test_i_s_position_list_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.i_s([0, 1], False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_S'), (1, 'I_S')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT TYPE add
    def test_i_s_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_s(0, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
    # TO HERE


##################_____SX_____##################
class Test_SX(unittest.TestCase):

    # SX position 0
    def test_sx_position_0(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.sx(0)

        self.assertIsInstance(gate, SXGate)
        self.assertEqual(circuit.getCircuitBody(), [['SX']])

    # SX position 1
    def test_sx_position_1(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.sx(1)

        self.assertIsInstance(gate, SXGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'SX']])

    # SX EXISTING CIRCUIT position NEW COLUMN
    def test_sx_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.sx(0)

        gate = circuit.sx(0)

        self.assertIsInstance(gate, SXGate)
        self.assertEqual(circuit.getCircuitBody(), [['SX'], ['SX']])

    # SX EXISTING CIRCUIT position SAME COLUMN
    def test_sx_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.sx(0)

        gate = circuit.sx(1)

        self.assertIsInstance(gate, SXGate)
        self.assertEqual(circuit.getCircuitBody(), [['SX', 'SX']])

    # SX EXISTING CIRCUIT position BETWEEN SWAP
    def test_sx_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.sx(1)

        self.assertIsInstance(gate, SXGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'SX']])

    # SX EXISTING CIRCUIT position UNDER SWAP
    def test_sx_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.sx(2)

        self.assertIsInstance(gate, SXGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'SX']])

    # SX position LIST
    def test_sx_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.sx([0, 1])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], SXGate)
        self.assertEqual(circuit.getCircuitBody(), [['SX', 'SX']])
    
    # SX position LIST EXISTING CIRCUIT
    def test_sx_position_list_existingCircuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.sx(0)

        gate = circuit.sx([1, 2])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], SXGate)
        self.assertEqual(circuit.getCircuitBody(), [['SX'], [1, 'SX', 'SX']])

    # SX position ALL
    def test_sx_position_all(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.sx(1)

        gate = circuit.sx()

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], SXGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'SX'], ['SX', 'SX']])

    # BAD ARGUMENT position LIST
    def test_sx_badArgument_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.sx([])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT position LIST DUPLICATED
    def test_sx_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.sx([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_sx_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.sx('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_sx_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.sx([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # DEPRECATED add: when add is deprecated REMOVE FROM HERE
    # SX add
    def test_sx_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.sx(0, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'SX')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # SX position LIST add
    def test_sx_position_list_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.sx([0, 1], False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'SX'), (1, 'SX')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT TYPE add
    def test_sx_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.sx(0, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
    # TO HERE


##################_____I_SX_____##################
class Test_I_SX(unittest.TestCase):

    # I_SX position 0
    def test_i_sx_position_0(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.i_sx(0)

        self.assertIsInstance(gate, I_SXGate)
        self.assertEqual(circuit.getCircuitBody(), [['I_SX']])

    # I_SX position 1
    def test_i_sx_position_1(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.i_sx(1)

        self.assertIsInstance(gate, I_SXGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'I_SX']])

    # I_SX EXISTING CIRCUIT position NEW COLUMN
    def test_i_sx_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.i_sx(0)

        gate = circuit.i_sx(0)

        self.assertIsInstance(gate, I_SXGate)
        self.assertEqual(circuit.getCircuitBody(), [['I_SX'], ['I_SX']])

    # I_SX EXISTING CIRCUIT position SAME COLUMN
    def test_i_sx_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.i_sx(0)

        gate = circuit.i_sx(1)

        self.assertIsInstance(gate, I_SXGate)
        self.assertEqual(circuit.getCircuitBody(), [['I_SX', 'I_SX']])

    # I_SX EXISTING CIRCUIT position BETWEEN SWAP
    def test_i_sx_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.i_sx(1)

        self.assertIsInstance(gate, I_SXGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'I_SX']])

    # I_SX EXISTING CIRCUIT position UNDER SWAP
    def test_i_sx_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.i_sx(2)

        self.assertIsInstance(gate, I_SXGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'I_SX']])

    # I_SX position LIST
    def test_i_sx_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.i_sx([0, 1])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], I_SXGate)
        self.assertEqual(circuit.getCircuitBody(), [['I_SX', 'I_SX']])
    
    # I_SX position LIST EXISTING CIRCUIT
    def test_i_sx_position_list_existingCircuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.i_sx(0)

        gate = circuit.i_sx([1, 2])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], I_SXGate)
        self.assertEqual(circuit.getCircuitBody(), [['I_SX'], [1, 'I_SX', 'I_SX']])

    # I_SX position ALL
    def test_i_sx_position_all(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.i_sx(1)

        gate = circuit.i_sx()

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], I_SXGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'I_SX'], ['I_SX', 'I_SX']])

    # BAD ARGUMENT position LIST
    def test_i_sx_badArgument_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_sx([])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT position LIST DUPLICATED
    def test_i_sx_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_sx([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_i_sx_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_sx('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_i_sx_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_sx([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # DEPRECATED add: when add is deprecated REMOVE FROM HERE
    # I_SX add
    def test_i_sx_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.i_sx(0, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_SX')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # I_SX position LIST add
    def test_i_sx_position_list_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.i_sx([0, 1], False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_SX'), (1, 'I_SX')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT TYPE add
    def test_i_sx_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_sx(0, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
    # TO HERE


##################_____SY_____##################
class Test_SY(unittest.TestCase):

    # SY position 0
    def test_sy_position_0(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.sy(0)

        self.assertIsInstance(gate, SYGate)
        self.assertEqual(circuit.getCircuitBody(), [['SY']])

    # SY position 1
    def test_sy_position_1(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.sy(1)

        self.assertIsInstance(gate, SYGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'SY']])

    # SY EXISTING CIRCUIT position NEW COLUMN
    def test_sy_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.sy(0)

        gate = circuit.sy(0)

        self.assertIsInstance(gate, SYGate)
        self.assertEqual(circuit.getCircuitBody(), [['SY'], ['SY']])

    # SY EXISTING CIRCUIT position SAME COLUMN
    def test_sy_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.sy(0)

        gate = circuit.sy(1)

        self.assertIsInstance(gate, SYGate)
        self.assertEqual(circuit.getCircuitBody(), [['SY', 'SY']])

    # SY EXISTING CIRCUIT position BETWEEN SWAP
    def test_sy_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.sy(1)

        self.assertIsInstance(gate, SYGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'SY']])

    # SY EXISTING CIRCUIT position UNDER SWAP
    def test_sy_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.sy(2)

        self.assertIsInstance(gate, SYGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'SY']])

    # SY position LIST
    def test_sy_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.sy([0, 1])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], SYGate)
        self.assertEqual(circuit.getCircuitBody(), [['SY', 'SY']])
    
    # SY position LIST EXISTING CIRCUIT
    def test_sy_position_list_existingCircuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.sy(0)

        gate = circuit.sy([1, 2])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], SYGate)
        self.assertEqual(circuit.getCircuitBody(), [['SY'], [1, 'SY', 'SY']])

    # SY position ALL
    def test_sy_position_all(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.sy(1)

        gate = circuit.sy()

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], SYGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'SY'], ['SY', 'SY']])

    # BAD ARGUMENT position LIST
    def test_sy_badArgument_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.sy([])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT position LIST DUPLICATED
    def test_sy_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.sy([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_sy_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.sy('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_sy_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.sy([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # DEPRECATED add: when add is deprecated REMOVE FROM HERE
    # SY add
    def test_sy_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.sy(0, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'SY')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # SY position LIST add
    def test_sy_position_list_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.sy([0, 1], False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'SY'), (1, 'SY')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT TYPE add
    def test_sy_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.sy(0, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
    # TO HERE


##################_____I_SY_____##################
class Test_I_SY(unittest.TestCase):

    # I_SY position 0
    def test_i_sy_position_0(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.i_sy(0)

        self.assertIsInstance(gate, I_SYGate)
        self.assertEqual(circuit.getCircuitBody(), [['I_SY']])

    # I_SY position 1
    def test_i_sy_position_1(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.i_sy(1)

        self.assertIsInstance(gate, I_SYGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'I_SY']])

    # I_SY EXISTING CIRCUIT position NEW COLUMN
    def test_i_sy_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.i_sy(0)

        gate = circuit.i_sy(0)

        self.assertIsInstance(gate, I_SYGate)
        self.assertEqual(circuit.getCircuitBody(), [['I_SY'], ['I_SY']])

    # I_SY EXISTING CIRCUIT position SAME COLUMN
    def test_i_sy_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.i_sy(0)

        gate = circuit.i_sy(1)

        self.assertIsInstance(gate, I_SYGate)
        self.assertEqual(circuit.getCircuitBody(), [['I_SY', 'I_SY']])

    # I_SY EXISTING CIRCUIT position BETWEEN SWAP
    def test_i_sy_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.i_sy(1)

        self.assertIsInstance(gate, I_SYGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'I_SY']])

    # I_SY EXISTING CIRCUIT position UNDER SWAP
    def test_i_sy_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.i_sy(2)

        self.assertIsInstance(gate, I_SYGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'I_SY']])

    # I_SY position LIST
    def test_i_sy_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.i_sy([0, 1])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], I_SYGate)
        self.assertEqual(circuit.getCircuitBody(), [['I_SY', 'I_SY']])
    
    # I_SY position LIST EXISTING CIRCUIT
    def test_i_sy_position_list_existingCircuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.i_sy(0)

        gate = circuit.i_sy([1, 2])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], I_SYGate)
        self.assertEqual(circuit.getCircuitBody(), [['I_SY'], [1, 'I_SY', 'I_SY']])

    # I_SY position ALL
    def test_i_sy_position_all(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.i_sy(1)

        gate = circuit.i_sy()

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], I_SYGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'I_SY'], ['I_SY', 'I_SY']])

    # BAD ARGUMENT position LIST
    def test_i_sy_badArgument_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_sy([])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT position LIST DUPLICATED
    def test_i_sy_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_sy([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_i_sy_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_sy('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_i_sy_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_sy([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # DEPRECATED add: when add is deprecated REMOVE FROM HERE
    # I_SY add
    def test_i_sy_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.i_sy(0, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_SY')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # I_SY position LIST add
    def test_i_sy_position_list_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.i_sy([0, 1], False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_SY'), (1, 'I_SY')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT TYPE add
    def test_i_sy_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_sy(0, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
    # TO HERE


##################_____T_____##################
class Test_T(unittest.TestCase):

    # T position 0
    def test_t_position_0(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.t(0)

        self.assertIsInstance(gate, TGate)
        self.assertEqual(circuit.getCircuitBody(), [['T']])

    # T position 1
    def test_t_position_1(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.t(1)

        self.assertIsInstance(gate, TGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'T']])

    # T EXISTING CIRCUIT position NEW COLUMN
    def test_t_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.t(0)

        gate = circuit.t(0)

        self.assertIsInstance(gate, TGate)
        self.assertEqual(circuit.getCircuitBody(), [['T'], ['T']])

    # T EXISTING CIRCUIT position SAME COLUMN
    def test_t_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.t(0)

        gate = circuit.t(1)

        self.assertIsInstance(gate, TGate)
        self.assertEqual(circuit.getCircuitBody(), [['T', 'T']])

    # T EXISTING CIRCUIT position BETWEEN SWAP
    def test_t_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.t(1)

        self.assertIsInstance(gate, TGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'T']])

    # T EXISTING CIRCUIT position UNDER SWAP
    def test_t_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.t(2)

        self.assertIsInstance(gate, TGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'T']])

    # T position LIST
    def test_t_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.t([0, 1])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], TGate)
        self.assertEqual(circuit.getCircuitBody(), [['T', 'T']])
    
    # T position LIST EXISTING CIRCUIT
    def test_t_position_list_existingCircuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.t(0)

        gate = circuit.t([1, 2])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], TGate)
        self.assertEqual(circuit.getCircuitBody(), [['T'], [1, 'T', 'T']])

    # T position ALL
    def test_t_position_all(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.t(1)

        gate = circuit.t()

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], TGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'T'], ['T', 'T']])

    # BAD ARGUMENT position LIST
    def test_t_badArgument_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.t([])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT position LIST DUPLICATED
    def test_t_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.t([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_t_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.t('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_t_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.t([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # DEPRECATED add: when add is deprecated REMOVE FROM HERE
    # T add
    def test_t_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.t(0, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'T')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # T position LIST add
    def test_t_position_list_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.t([0, 1], False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'T'), (1, 'T')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT TYPE add
    def test_t_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.t(0, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
    # TO HERE


##################_____I_T_____##################
class Test_I_T(unittest.TestCase):

    # I_T position 0
    def test_i_t_position_0(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.i_t(0)

        self.assertIsInstance(gate, I_TGate)
        self.assertEqual(circuit.getCircuitBody(), [['I_T']])

    # I_T position 1
    def test_i_t_position_1(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.i_t(1)

        self.assertIsInstance(gate, I_TGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'I_T']])

    # I_T EXISTING CIRCUIT position NEW COLUMN
    def test_i_t_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.i_t(0)

        gate = circuit.i_t(0)

        self.assertIsInstance(gate, I_TGate)
        self.assertEqual(circuit.getCircuitBody(), [['I_T'], ['I_T']])

    # I_T EXISTING CIRCUIT position SAME COLUMN
    def test_i_t_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.i_t(0)

        gate = circuit.i_t(1)

        self.assertIsInstance(gate, I_TGate)
        self.assertEqual(circuit.getCircuitBody(), [['I_T', 'I_T']])

    # I_T EXISTING CIRCUIT position BETWEEN SWAP
    def test_i_t_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.i_t(1)

        self.assertIsInstance(gate, I_TGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'I_T']])

    # I_T EXISTING CIRCUIT position UNDER SWAP
    def test_i_t_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.i_t(2)

        self.assertIsInstance(gate, I_TGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'I_T']])

    # I_T position LIST
    def test_i_t_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.i_t([0, 1])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], I_TGate)
        self.assertEqual(circuit.getCircuitBody(), [['I_T', 'I_T']])
    
    # I_T position LIST EXISTING CIRCUIT
    def test_i_t_position_list_existingCircuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.i_t(0)

        gate = circuit.i_t([1, 2])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], I_TGate)
        self.assertEqual(circuit.getCircuitBody(), [['I_T'], [1, 'I_T', 'I_T']])

    # I_T position ALL
    def test_i_t_position_all(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.i_t(1)

        gate = circuit.i_t()

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], I_TGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'I_T'], ['I_T', 'I_T']])

    # BAD ARGUMENT position LIST
    def test_i_t_badArgument_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_t([])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT position LIST DUPLICATED
    def test_i_t_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_t([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_i_t_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_t('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_i_t_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_t([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # DEPRECATED add: when add is deprecated REMOVE FROM HERE
    # I_T add
    def test_i_t_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.i_t(0, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_T')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # I_T position LIST add
    def test_i_t_position_list_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.i_t([0, 1], False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_T'), (1, 'I_T')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT TYPE add
    def test_i_t_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_t(0, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
    # TO HERE


##################_____TX_____##################
class Test_TX(unittest.TestCase):

    # TX position 0
    def test_tx_position_0(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.tx(0)

        self.assertIsInstance(gate, TXGate)
        self.assertEqual(circuit.getCircuitBody(), [['TX']])

    # TX position 1
    def test_tx_position_1(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.tx(1)

        self.assertIsInstance(gate, TXGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'TX']])

    # TX EXISTING CIRCUIT position NEW COLUMN
    def test_tx_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.tx(0)

        gate = circuit.tx(0)

        self.assertIsInstance(gate, TXGate)
        self.assertEqual(circuit.getCircuitBody(), [['TX'], ['TX']])

    # TX EXISTING CIRCUIT position SAME COLUMN
    def test_tx_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.tx(0)

        gate = circuit.tx(1)

        self.assertIsInstance(gate, TXGate)
        self.assertEqual(circuit.getCircuitBody(), [['TX', 'TX']])

    # TX EXISTING CIRCUIT position BETWEEN SWAP
    def test_tx_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.tx(1)

        self.assertIsInstance(gate, TXGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'TX']])

    # TX EXISTING CIRCUIT position UNDER SWAP
    def test_tx_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.tx(2)

        self.assertIsInstance(gate, TXGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'TX']])

    # TX position LIST
    def test_tx_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.tx([0, 1])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], TXGate)
        self.assertEqual(circuit.getCircuitBody(), [['TX', 'TX']])
    
    # TX position LIST EXISTING CIRCUIT
    def test_tx_position_list_existingCircuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.tx(0)

        gate = circuit.tx([1, 2])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], TXGate)
        self.assertEqual(circuit.getCircuitBody(), [['TX'], [1, 'TX', 'TX']])

    # TX position ALL
    def test_tx_position_all(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.tx(1)

        gate = circuit.tx()

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], TXGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'TX'], ['TX', 'TX']])

    # BAD ARGUMENT position LIST
    def test_tx_badArgument_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.tx([])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT position LIST DUPLICATED
    def test_tx_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.tx([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_tx_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.tx('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_tx_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.tx([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # DEPRECATED add: when add is deprecated REMOVE FROM HERE
    # TX add
    def test_tx_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.tx(0, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'TX')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # TX position LIST add
    def test_tx_position_list_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.tx([0, 1], False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'TX'), (1, 'TX')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT TYPE add
    def test_tx_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.tx(0, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
    # TO HERE


##################_____I_TX_____##################
class Test_I_TX(unittest.TestCase):

    # I_TX position 0
    def test_i_tx_position_0(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.i_tx(0)

        self.assertIsInstance(gate, I_TXGate)
        self.assertEqual(circuit.getCircuitBody(), [['I_TX']])

    # I_TX position 1
    def test_i_tx_position_1(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.i_tx(1)

        self.assertIsInstance(gate, I_TXGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'I_TX']])

    # I_TX EXISTING CIRCUIT position NEW COLUMN
    def test_i_tx_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.i_tx(0)

        gate = circuit.i_tx(0)

        self.assertIsInstance(gate, I_TXGate)
        self.assertEqual(circuit.getCircuitBody(), [['I_TX'], ['I_TX']])

    # I_TX EXISTING CIRCUIT position SAME COLUMN
    def test_i_tx_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.i_tx(0)

        gate = circuit.i_tx(1)

        self.assertIsInstance(gate, I_TXGate)
        self.assertEqual(circuit.getCircuitBody(), [['I_TX', 'I_TX']])

    # I_TX EXISTING CIRCUIT position BETWEEN SWAP
    def test_i_tx_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.i_tx(1)

        self.assertIsInstance(gate, I_TXGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'I_TX']])

    # I_TX EXISTING CIRCUIT position UNDER SWAP
    def test_i_tx_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.i_tx(2)

        self.assertIsInstance(gate, I_TXGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'I_TX']])

    # I_TX position LIST
    def test_i_tx_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.i_tx([0, 1])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], I_TXGate)
        self.assertEqual(circuit.getCircuitBody(), [['I_TX', 'I_TX']])
    
    # I_TX position LIST EXISTING CIRCUIT
    def test_i_tx_position_list_existingCircuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.i_tx(0)

        gate = circuit.i_tx([1, 2])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], I_TXGate)
        self.assertEqual(circuit.getCircuitBody(), [['I_TX'], [1, 'I_TX', 'I_TX']])

    # I_TX position ALL
    def test_i_tx_position_all(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.i_tx(1)

        gate = circuit.i_tx()

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], I_TXGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'I_TX'], ['I_TX', 'I_TX']])

    # BAD ARGUMENT position LIST
    def test_i_tx_badArgument_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_tx([])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT position LIST DUPLICATED
    def test_i_tx_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_tx([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_i_tx_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_tx('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_i_tx_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_tx([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # DEPRECATED add: when add is deprecated REMOVE FROM HERE
    # I_TX add
    def test_i_tx_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.i_tx(0, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_TX')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # I_TX position LIST add
    def test_i_tx_position_list_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.i_tx([0, 1], False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_TX'), (1, 'I_TX')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT TYPE add
    def test_i_tx_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_tx(0, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
    # TO HERE


##################_____TY_____##################
class Test_TY(unittest.TestCase):

    # TY position 0
    def test_ty_position_0(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.ty(0)

        self.assertIsInstance(gate, TYGate)
        self.assertEqual(circuit.getCircuitBody(), [['TY']])

    # TY position 1
    def test_ty_position_1(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.ty(1)

        self.assertIsInstance(gate, TYGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'TY']])

    # TY EXISTING CIRCUIT position NEW COLUMN
    def test_ty_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.ty(0)

        gate = circuit.ty(0)

        self.assertIsInstance(gate, TYGate)
        self.assertEqual(circuit.getCircuitBody(), [['TY'], ['TY']])

    # TY EXISTING CIRCUIT position SAME COLUMN
    def test_ty_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.ty(0)

        gate = circuit.ty(1)

        self.assertIsInstance(gate, TYGate)
        self.assertEqual(circuit.getCircuitBody(), [['TY', 'TY']])

    # TY EXISTING CIRCUIT position BETWEEN SWAP
    def test_ty_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.ty(1)

        self.assertIsInstance(gate, TYGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'TY']])

    # TY EXISTING CIRCUIT position UNDER SWAP
    def test_ty_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.ty(2)

        self.assertIsInstance(gate, TYGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'TY']])

    # TY position LIST
    def test_ty_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.ty([0, 1])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], TYGate)
        self.assertEqual(circuit.getCircuitBody(), [['TY', 'TY']])
    
    # TY position LIST EXISTING CIRCUIT
    def test_ty_position_list_existingCircuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.ty(0)

        gate = circuit.ty([1, 2])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], TYGate)
        self.assertEqual(circuit.getCircuitBody(), [['TY'], [1, 'TY', 'TY']])

    # TY position ALL
    def test_ty_position_all(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.ty(1)

        gate = circuit.ty()

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], TYGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'TY'], ['TY', 'TY']])

    # BAD ARGUMENT position LIST
    def test_ty_badArgument_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ty([])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT position LIST DUPLICATED
    def test_ty_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ty([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_ty_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ty('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_ty_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ty([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # DEPRECATED add: when add is deprecated REMOVE FROM HERE
    # TY add
    def test_ty_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.ty(0, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'TY')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # TY position LIST add
    def test_ty_position_list_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.ty([0, 1], False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'TY'), (1, 'TY')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT TYPE add
    def test_ty_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ty(0, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
    # TO HERE


##################_____I_TY_____##################
class Test_I_TY(unittest.TestCase):

    # I_TY position 0
    def test_i_ty_position_0(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.i_ty(0)

        self.assertIsInstance(gate, I_TYGate)
        self.assertEqual(circuit.getCircuitBody(), [['I_TY']])

    # I_TY position 1
    def test_i_ty_position_1(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.i_ty(1)

        self.assertIsInstance(gate, I_TYGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'I_TY']])

    # I_TY EXISTING CIRCUIT position NEW COLUMN
    def test_i_ty_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.i_ty(0)

        gate = circuit.i_ty(0)

        self.assertIsInstance(gate, I_TYGate)
        self.assertEqual(circuit.getCircuitBody(), [['I_TY'], ['I_TY']])

    # I_TY EXISTING CIRCUIT position SAME COLUMN
    def test_i_ty_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.i_ty(0)

        gate = circuit.i_ty(1)

        self.assertIsInstance(gate, I_TYGate)
        self.assertEqual(circuit.getCircuitBody(), [['I_TY', 'I_TY']])

    # I_TY EXISTING CIRCUIT position BETWEEN SWAP
    def test_i_ty_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.i_ty(1)

        self.assertIsInstance(gate, I_TYGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'I_TY']])

    # I_TY EXISTING CIRCUIT position UNDER SWAP
    def test_i_ty_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.i_ty(2)

        self.assertIsInstance(gate, I_TYGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'I_TY']])

    # I_TY position LIST
    def test_i_ty_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.i_ty([0, 1])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], I_TYGate)
        self.assertEqual(circuit.getCircuitBody(), [['I_TY', 'I_TY']])
    
    # I_TY position LIST EXISTING CIRCUIT
    def test_i_ty_position_list_existingCircuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.i_ty(0)

        gate = circuit.i_ty([1, 2])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], I_TYGate)
        self.assertEqual(circuit.getCircuitBody(), [['I_TY'], [1, 'I_TY', 'I_TY']])

    # I_TY position ALL
    def test_i_ty_position_all(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.i_ty(1)

        gate = circuit.i_ty()

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], I_TYGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'I_TY'], ['I_TY', 'I_TY']])

    # BAD ARGUMENT position LIST
    def test_i_ty_badArgument_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_ty([])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT position LIST DUPLICATED
    def test_i_ty_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_ty([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_i_ty_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_ty('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_i_ty_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_ty([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # DEPRECATED add: when add is deprecated REMOVE FROM HERE
    # I_TY add
    def test_i_ty_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.i_ty(0, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_TY')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # I_TY position LIST add
    def test_i_ty_position_list_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.i_ty([0, 1], False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'I_TY'), (1, 'I_TY')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT TYPE add
    def test_i_ty_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.i_ty(0, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
    # TO HERE