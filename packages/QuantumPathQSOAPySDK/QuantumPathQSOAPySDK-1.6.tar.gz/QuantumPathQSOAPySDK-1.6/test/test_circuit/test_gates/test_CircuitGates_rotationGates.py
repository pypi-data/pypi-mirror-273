import unittest
from QuantumPathQSOAPySDK import QSOAPlatform
from QuantumPathQSOAPySDK.circuit.gates.rotationGates import (PGate, RXGate, RYGate, RZGate)

# ROTATION GATES:
#   PGate
#   RXGate
#   RYGate
#   RZGate

##################_____P_____##################
class Test_P(unittest.TestCase):

    # P position 0
    def test_p_position_0(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.p(0)

        self.assertIsInstance(gate, PGate)
        self.assertEqual(circuit.getCircuitBody(), [[{'id': 'P', 'arg': 'pi'}]])

    # P position 1
    def test_p_position_1(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.p(1)

        self.assertIsInstance(gate, PGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, {'id': 'P', 'arg': 'pi'}]])

    # P argument INT
    def test_p_argument_int(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.p(0, 1)

        self.assertIsInstance(gate, PGate)
        self.assertEqual(circuit.getCircuitBody(), [[{'id': 'P', 'arg': '1'}]])

    # P argument FLOAT
    def test_p_argument_float(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.p(0, 1.5)

        self.assertIsInstance(gate, PGate)
        self.assertEqual(circuit.getCircuitBody(), [[{'id': 'P', 'arg': '1.5'}]])

    # P argument STRING NUMBER
    def test_p_argument_string_number(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.p(0, '1')

        self.assertIsInstance(gate, PGate)
        self.assertEqual(circuit.getCircuitBody(), [[{'id': 'P', 'arg': '1'}]])

    # P argument STRING EXPRESSION
    def test_p_argument_string_expression(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.p(0, 'pi/2')

        self.assertIsInstance(gate, PGate)
        self.assertEqual(circuit.getCircuitBody(), [[{'id': 'P', 'arg': 'pi/2'}]])

    # P EXISTING CIRCUIT position NEW COLUMN
    def test_p_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.p(0)

        self.assertIsInstance(gate, PGate)
        self.assertEqual(circuit.getCircuitBody(), [['H'], [{'id': 'P', 'arg': 'pi'}]])

    # P EXISTING CIRCUIT position SAME COLUMN
    def test_p_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.p(1)

        self.assertIsInstance(gate, PGate)
        self.assertEqual(circuit.getCircuitBody(), [['H', {'id': 'P', 'arg': 'pi'}]])

    # P EXISTING CIRCUIT position BETWEEN SWAP
    def test_p_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.p(1)

        self.assertIsInstance(gate, PGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, {'id': 'P', 'arg': 'pi'}]])

    # P EXISTING CIRCUIT position UNDER SWAP
    def test_p_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.p(2)

        self.assertIsInstance(gate, PGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, {'id': 'P', 'arg': 'pi'}]])

    # P position LIST
    def test_p_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.p([0, 1])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], PGate)
        self.assertEqual(circuit.getCircuitBody(), [[{'id': 'P', 'arg': 'pi'}, {'id': 'P', 'arg': 'pi'}]])
    
    # P position LIST EXISTING CIRCUIT
    def test_p_position_list_existingCircuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.p([1, 2])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], PGate)
        self.assertEqual(circuit.getCircuitBody(), [['H'], [1, {'id': 'P', 'arg': 'pi'}, {'id': 'P', 'arg': 'pi'}]])

    # P position ALL
    def test_p_position_all(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.p()

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], PGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'H'], [{'id': 'P', 'arg': 'pi'}, {'id': 'P', 'arg': 'pi'}]])

    # BAD ARGUMENT position LIST
    def test_p_badArgument_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.p([])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT position LIST DUPLICATED
    def test_p_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.p([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT argument
    def test_p_badArgument_argument(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.p(1, 'argument')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_p_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.p('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_p_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.p([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE argument
    def test_p_badArgumentType_argument(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.p(0, True)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # DEPRECATED add: when add is deprecated REMOVE FROM HERE
    # P add
    def test_p_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.p(0, add=False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'P', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT TYPE add
    def test_p_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.p(0, add='add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
    # TO HERE


##################_____RX_____##################
class Test_RX(unittest.TestCase):

    # RX position 0
    def test_rx_position_0(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.rx(0)

        self.assertIsInstance(gate, RXGate)
        self.assertEqual(circuit.getCircuitBody(), [[{'id': 'RX', 'arg': 'pi'}]])

    # RX position 1
    def test_rx_position_1(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.rx(1)

        self.assertIsInstance(gate, RXGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, {'id': 'RX', 'arg': 'pi'}]])

    # RX argument INT
    def test_rx_argument_int(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.rx(0, 1)

        self.assertIsInstance(gate, RXGate)
        self.assertEqual(circuit.getCircuitBody(), [[{'id': 'RX', 'arg': '1'}]])

    # RX argument FLOAT
    def test_rx_argument_float(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.rx(0, 1.5)

        self.assertIsInstance(gate, RXGate)
        self.assertEqual(circuit.getCircuitBody(), [[{'id': 'RX', 'arg': '1.5'}]])

    # RX argument STRING NUMBER
    def test_rx_argument_string_number(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.rx(0, '1')

        self.assertIsInstance(gate, RXGate)
        self.assertEqual(circuit.getCircuitBody(), [[{'id': 'RX', 'arg': '1'}]])

    # RX argument STRING EXPRESSION
    def test_rx_argument_string_expression(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.rx(0, 'pi/2')

        self.assertIsInstance(gate, RXGate)
        self.assertEqual(circuit.getCircuitBody(), [[{'id': 'RX', 'arg': 'pi/2'}]])

    # RX EXISTING CIRCUIT position NEW COLUMN
    def test_rx_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.rx(0)

        self.assertIsInstance(gate, RXGate)
        self.assertEqual(circuit.getCircuitBody(), [['H'], [{'id': 'RX', 'arg': 'pi'}]])

    # RX EXISTING CIRCUIT position SAME COLUMN
    def test_rx_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.rx(1)

        self.assertIsInstance(gate, RXGate)
        self.assertEqual(circuit.getCircuitBody(), [['H', {'id': 'RX', 'arg': 'pi'}]])

    # RX EXISTING CIRCUIT position BETWEEN SWAP
    def test_rx_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.rx(1)

        self.assertIsInstance(gate, RXGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, {'id': 'RX', 'arg': 'pi'}]])

    # RX EXISTING CIRCUIT position UNDER SWAP
    def test_rx_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.rx(2)

        self.assertIsInstance(gate, RXGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, {'id': 'RX', 'arg': 'pi'}]])

    # RX position LIST
    def test_rx_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.rx([0, 1])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], RXGate)
        self.assertEqual(circuit.getCircuitBody(), [[{'id': 'RX', 'arg': 'pi'}, {'id': 'RX', 'arg': 'pi'}]])
    
    # RX position LIST EXISTING CIRCUIT
    def test_rx_position_list_existingCircuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.rx([1, 2])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], RXGate)
        self.assertEqual(circuit.getCircuitBody(), [['H'], [1, {'id': 'RX', 'arg': 'pi'}, {'id': 'RX', 'arg': 'pi'}]])

    # RX position ALL
    def test_rx_position_all(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.rx()

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], RXGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'H'], [{'id': 'RX', 'arg': 'pi'}, {'id': 'RX', 'arg': 'pi'}]])

    # BAD ARGUMENT position LIST
    def test_rx_badArgument_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.rx([])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT position LIST DUPLICATED
    def test_rx_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.rx([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT argument
    def test_rx_badArgument_argument(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.rx(1, 'argument')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_rx_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.rx('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_rx_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.rx([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE argument
    def test_rx_badArgumentType_argument(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.rx(0, True)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # DEPRECATED add: when add is deprecated REMOVE FROM HERE
    # RX add
    def test_rx_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.rx(0, add=False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'RX', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT TYPE add
    def test_rx_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.rx(0, add='add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
    # TO HERE


##################_____RY_____##################
class Test_RY(unittest.TestCase):

    # RY position 0
    def test_ry_position_0(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.ry(0)

        self.assertIsInstance(gate, RYGate)
        self.assertEqual(circuit.getCircuitBody(), [[{'id': 'RY', 'arg': 'pi'}]])

    # RY position 1
    def test_ry_position_1(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.ry(1)

        self.assertIsInstance(gate, RYGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, {'id': 'RY', 'arg': 'pi'}]])

    # RY argument INT
    def test_ry_argument_int(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.ry(0, 1)

        self.assertIsInstance(gate, RYGate)
        self.assertEqual(circuit.getCircuitBody(), [[{'id': 'RY', 'arg': '1'}]])

    # RY argument FLOAT
    def test_ry_argument_float(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.ry(0, 1.5)

        self.assertIsInstance(gate, RYGate)
        self.assertEqual(circuit.getCircuitBody(), [[{'id': 'RY', 'arg': '1.5'}]])

    # RY argument STRING NUMBER
    def test_ry_argument_string_number(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.ry(0, '1')

        self.assertIsInstance(gate, RYGate)
        self.assertEqual(circuit.getCircuitBody(), [[{'id': 'RY', 'arg': '1'}]])

    # RY argument STRING EXPRESSION
    def test_ry_argument_string_expression(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.ry(0, 'pi/2')

        self.assertIsInstance(gate, RYGate)
        self.assertEqual(circuit.getCircuitBody(), [[{'id': 'RY', 'arg': 'pi/2'}]])

    # RY EXISTING CIRCUIT position NEW COLUMN
    def test_ry_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.ry(0)

        self.assertIsInstance(gate, RYGate)
        self.assertEqual(circuit.getCircuitBody(), [['H'], [{'id': 'RY', 'arg': 'pi'}]])

    # RY EXISTING CIRCUIT position SAME COLUMN
    def test_ry_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.ry(1)

        self.assertIsInstance(gate, RYGate)
        self.assertEqual(circuit.getCircuitBody(), [['H', {'id': 'RY', 'arg': 'pi'}]])

    # RY EXISTING CIRCUIT position BETWEEN SWAP
    def test_ry_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.ry(1)

        self.assertIsInstance(gate, RYGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, {'id': 'RY', 'arg': 'pi'}]])

    # RY EXISTING CIRCUIT position UNDER SWAP
    def test_ry_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.ry(2)

        self.assertIsInstance(gate, RYGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, {'id': 'RY', 'arg': 'pi'}]])

    # RY position LIST
    def test_ry_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.ry([0, 1])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], RYGate)
        self.assertEqual(circuit.getCircuitBody(), [[{'id': 'RY', 'arg': 'pi'}, {'id': 'RY', 'arg': 'pi'}]])
    
    # RY position LIST EXISTING CIRCUIT
    def test_ry_position_list_existingCircuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.ry([1, 2])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], RYGate)
        self.assertEqual(circuit.getCircuitBody(), [['H'], [1, {'id': 'RY', 'arg': 'pi'}, {'id': 'RY', 'arg': 'pi'}]])

    # RY position ALL
    def test_ry_position_all(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.ry()

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], RYGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'H'], [{'id': 'RY', 'arg': 'pi'}, {'id': 'RY', 'arg': 'pi'}]])

    # BAD ARGUMENT position LIST
    def test_ry_badArgument_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ry([])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT position LIST DUPLICATED
    def test_ry_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ry([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT argument
    def test_ry_badArgument_argument(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ry(1, 'argument')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_ry_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ry('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_ry_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ry([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE argument
    def test_ry_badArgumentType_argument(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ry(0, True)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # DEPRECATED add: when add is deprecated REMOVE FROM HERE
    # RY add
    def test_ry_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.ry(0, add=False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'RY', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT TYPE add
    def test_ry_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ry(0, add='add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
    # TO HERE


##################_____RZ_____##################
class Test_RZ(unittest.TestCase):

    # RZ position 0
    def test_rz_position_0(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.rz(0)

        self.assertIsInstance(gate, RZGate)
        self.assertEqual(circuit.getCircuitBody(), [[{'id': 'RZ', 'arg': 'pi'}]])

    # RZ position 1
    def test_rz_position_1(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.rz(1)

        self.assertIsInstance(gate, RZGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, {'id': 'RZ', 'arg': 'pi'}]])

    # RZ argument INT
    def test_rz_argument_int(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.rz(0, 1)

        self.assertIsInstance(gate, RZGate)
        self.assertEqual(circuit.getCircuitBody(), [[{'id': 'RZ', 'arg': '1'}]])

    # RZ argument FLOAT
    def test_rz_argument_float(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.rz(0, 1.5)

        self.assertIsInstance(gate, RZGate)
        self.assertEqual(circuit.getCircuitBody(), [[{'id': 'RZ', 'arg': '1.5'}]])

    # RZ argument STRING NUMBER
    def test_rz_argument_string_number(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.rz(0, '1')

        self.assertIsInstance(gate, RZGate)
        self.assertEqual(circuit.getCircuitBody(), [[{'id': 'RZ', 'arg': '1'}]])

    # RZ argument STRING EXPRESSION
    def test_rz_argument_string_expression(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.rz(0, 'pi/2')

        self.assertIsInstance(gate, RZGate)
        self.assertEqual(circuit.getCircuitBody(), [[{'id': 'RZ', 'arg': 'pi/2'}]])

    # RZ EXISTING CIRCUIT position NEW COLUMN
    def test_rz_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.rz(0)

        self.assertIsInstance(gate, RZGate)
        self.assertEqual(circuit.getCircuitBody(), [['H'], [{'id': 'RZ', 'arg': 'pi'}]])

    # RZ EXISTING CIRCUIT position SAME COLUMN
    def test_rz_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.rz(1)

        self.assertIsInstance(gate, RZGate)
        self.assertEqual(circuit.getCircuitBody(), [['H', {'id': 'RZ', 'arg': 'pi'}]])

    # RZ EXISTING CIRCUIT position BETWEEN SWAP
    def test_rz_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.rz(1)

        self.assertIsInstance(gate, RZGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, {'id': 'RZ', 'arg': 'pi'}]])

    # RZ EXISTING CIRCUIT position UNDER SWAP
    def test_rz_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.rz(2)

        self.assertIsInstance(gate, RZGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, {'id': 'RZ', 'arg': 'pi'}]])

    # RZ position LIST
    def test_rz_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.rz([0, 1])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], RZGate)
        self.assertEqual(circuit.getCircuitBody(), [[{'id': 'RZ', 'arg': 'pi'}, {'id': 'RZ', 'arg': 'pi'}]])
    
    # RZ position LIST EXISTING CIRCUIT
    def test_rz_position_list_existingCircuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.rz([1, 2])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], RZGate)
        self.assertEqual(circuit.getCircuitBody(), [['H'], [1, {'id': 'RZ', 'arg': 'pi'}, {'id': 'RZ', 'arg': 'pi'}]])

    # RZ position ALL
    def test_rz_position_all(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.rz()

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], RZGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'H'], [{'id': 'RZ', 'arg': 'pi'}, {'id': 'RZ', 'arg': 'pi'}]])

    # BAD ARGUMENT position LIST
    def test_rz_badArgument_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.rz([])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT position LIST DUPLICATED
    def test_rz_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.rz([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT argument
    def test_rz_badArgument_argument(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.rz(1, 'argument')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_rz_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.rz('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_rz_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.rz([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE argument
    def test_rz_badArgumentType_argument(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.rz(0, True)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # DEPRECATED add: when add is deprecated REMOVE FROM HERE
    # P add
    def test_rz_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.rz(0, add=False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, {'id': 'RZ', 'arg': 'pi'})])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT TYPE add
    def test_rz_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.rz(0, add='add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
    # TO HERE


if __name__ == '__main__':
    unittest.main()