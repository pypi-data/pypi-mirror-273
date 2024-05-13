import unittest
from QuantumPathQSOAPySDK import QSOAPlatform
from QuantumPathQSOAPySDK.circuit.gates.gates import ControlledGate
from QuantumPathQSOAPySDK.circuit.gates.basicGates import (HGate, XGate, YGate, ZGate, SwapGate, CHGate, CXGate, CCXGate)
from QuantumPathQSOAPySDK.circuit.gates.rotationGates import PGate
from QuantumPathQSOAPySDK.circuit.gates.utilities import Barrier

# BASIC GATES:
#   HGate
#   XGate
#   YGate
#   ZGate
#   SwapGate
#   CHGate
#   CXGate
#   CCXGate
#   Control
#   MCG

##################_____H_____##################
class Test_H(unittest.TestCase):

    # H position 0
    def test_h_position_0(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.h(0)

        self.assertIsInstance(gate, HGate)
        self.assertEqual(circuit.getCircuitBody(), [['H']])

    # H position 1
    def test_h_position_1(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.h(1)

        self.assertIsInstance(gate, HGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'H']])

    # H EXISTING CIRCUIT position NEW COLUMN
    def test_h_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.h(0)

        self.assertIsInstance(gate, HGate)
        self.assertEqual(circuit.getCircuitBody(), [['H'], ['H']])

    # H EXISTING CIRCUIT position SAME COLUMN
    def test_h_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.h(1)

        self.assertIsInstance(gate, HGate)
        self.assertEqual(circuit.getCircuitBody(), [['H', 'H']])

    # H EXISTING CIRCUIT position BETWEEN SWAP
    def test_h_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.h(1)

        self.assertIsInstance(gate, HGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'H']])

    # H EXISTING CIRCUIT position UNDER SWAP
    def test_h_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.h(2)

        self.assertIsInstance(gate, HGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'H']])

    # H position LIST
    def test_h_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.h([0, 1])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], HGate)
        self.assertEqual(circuit.getCircuitBody(), [['H', 'H']])
    
    # H position LIST EXISTING CIRCUIT
    def test_h_position_list_existingCircuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.h([1, 2])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], HGate)
        self.assertEqual(circuit.getCircuitBody(), [['H'], [1, 'H', 'H']])

    # H position ALL
    def test_h_position_all(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.h()

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], HGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'H'], ['H', 'H']])

    # BAD ARGUMENT position LIST
    def test_h_badArgument_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.h([])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT position LIST DUPLICATED
    def test_h_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.h([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_h_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.h('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_h_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.h([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # DEPRECATED add: when add is deprecated REMOVE FROM HERE
    # H add
    def test_h_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.h(0, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'H')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # H position LIST add
    def test_h_position_list_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.h([0, 1], False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'H'), (1, 'H')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT TYPE add
    def test_h_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.h(0, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
    # TO HERE


##################_____X_____##################
class Test_X(unittest.TestCase):

    # X position 0
    def test_x_position_0(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.x(0)

        self.assertIsInstance(gate, XGate)
        self.assertEqual(circuit.getCircuitBody(), [['X']])

    # X position 1
    def test_x_position_1(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.x(1)

        self.assertIsInstance(gate, XGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'X']])

    # X EXISTING CIRCUIT position NEW COLUMN
    def test_x_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.x(0)

        gate = circuit.x(0)

        self.assertIsInstance(gate, XGate)
        self.assertEqual(circuit.getCircuitBody(), [['X'], ['X']])

    # X EXISTING CIRCUIT position SAME COLUMN
    def test_x_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.x(0)

        gate = circuit.x(1)

        self.assertIsInstance(gate, XGate)
        self.assertEqual(circuit.getCircuitBody(), [['X', 'X']])

    # X EXISTING CIRCUIT position BETWEEN SWAP
    def test_x_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.x(1)

        self.assertIsInstance(gate, XGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'X']])

    # X EXISTING CIRCUIT position UNDER SWAP
    def test_x_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.x(2)

        self.assertIsInstance(gate, XGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'X']])

    # X position LIST
    def test_x_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.x([0, 1])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], XGate)
        self.assertEqual(circuit.getCircuitBody(), [['X', 'X']])
    
    # X position LIST EXISTING CIRCUIT
    def test_x_position_list_existingCircuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.x(0)

        gate = circuit.x([1, 2])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], XGate)
        self.assertEqual(circuit.getCircuitBody(), [['X'], [1, 'X', 'X']])

    # X position ALL
    def test_x_position_all(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.x(1)

        gate = circuit.x()

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], XGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'X'], ['X', 'X']])

    # BAD ARGUMENT position LIST
    def test_x_badArgument_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.x([])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT position LIST DUPLICATED
    def test_x_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.x([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_x_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.x('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_x_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.x([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # DEPRECATED add: when add is deprecated REMOVE FROM HERE
    # X add
    def test_x_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.x(0, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # X position LIST add
    def test_x_position_list_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.x([0, 1], False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'X'), (1, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT TYPE add
    def test_x_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.x(0, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
    # TO HERE


##################_____Y_____##################
class Test_Y(unittest.TestCase):

    # Y position 0
    def test_y_position_0(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.y(0)

        self.assertIsInstance(gate, YGate)
        self.assertEqual(circuit.getCircuitBody(), [['Y']])

    # Y position 1
    def test_y_position_1(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.y(1)

        self.assertIsInstance(gate, YGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'Y']])

    # Y EXISTING CIRCUIT position NEW COLUMN
    def test_y_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.y(0)

        gate = circuit.y(0)

        self.assertIsInstance(gate, YGate)
        self.assertEqual(circuit.getCircuitBody(), [['Y'], ['Y']])

    # Y EXISTING CIRCUIT position SAME COLUMN
    def test_y_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.y(0)

        gate = circuit.y(1)

        self.assertIsInstance(gate, YGate)
        self.assertEqual(circuit.getCircuitBody(), [['Y', 'Y']])

    # Y EXISTING CIRCUIT position BETWEEN SWAP
    def test_y_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.y(1)

        self.assertIsInstance(gate, YGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'Y']])

    # Y EXISTING CIRCUIT position UNDER SWAP
    def test_y_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.y(2)

        self.assertIsInstance(gate, YGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'Y']])

    # Y position LIST
    def test_y_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.y([0, 1])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], YGate)
        self.assertEqual(circuit.getCircuitBody(), [['Y', 'Y']])
    
    # Y position LIST EXISTING CIRCUIT
    def test_y_position_list_existingCircuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.y(0)

        gate = circuit.y([1, 2])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], YGate)
        self.assertEqual(circuit.getCircuitBody(), [['Y'], [1, 'Y', 'Y']])

    # Y position ALL
    def test_y_position_all(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.y(1)

        gate = circuit.y()

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], YGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'Y'], ['Y', 'Y']])

    # BAD ARGUMENT position LIST
    def test_y_badArgument_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.y([])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT position LIST DUPLICATED
    def test_y_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.y([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_y_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.y('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_y_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.y([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # DEPRECATED add: when add is deprecated REMOVE FROM HERE
    # Y add
    def test_y_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.y(0, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Y')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # Y position LIST add
    def test_y_position_list_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.y([0, 1], False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Y'), (1, 'Y')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT TYPE add
    def test_y_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.y(0, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
    # TO HERE


##################_____Z_____##################
class Test_Z(unittest.TestCase):

    # Z position 0
    def test_z_position_0(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.z(0)

        self.assertIsInstance(gate, ZGate)
        self.assertEqual(circuit.getCircuitBody(), [['Z']])

    # Z position 1
    def test_z_position_1(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.z(1)

        self.assertIsInstance(gate, ZGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'Z']])

    # Z EXISTING CIRCUIT position NEW COLUMN
    def test_z_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.z(0)

        gate = circuit.z(0)

        self.assertIsInstance(gate, ZGate)
        self.assertEqual(circuit.getCircuitBody(), [['Z'], ['Z']])

    # Z EXISTING CIRCUIT position SAME COLUMN
    def test_z_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.z(0)

        gate = circuit.z(1)

        self.assertIsInstance(gate, ZGate)
        self.assertEqual(circuit.getCircuitBody(), [['Z', 'Z']])

    # Z EXISTING CIRCUIT position BETWEEN SWAP
    def test_z_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.z(1)

        self.assertIsInstance(gate, ZGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'Z']])

    # Z EXISTING CIRCUIT position UNDER SWAP
    def test_z_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.z(2)

        self.assertIsInstance(gate, ZGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'Z']])

    # Z position LIST
    def test_z_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.z([0, 1])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], ZGate)
        self.assertEqual(circuit.getCircuitBody(), [['Z', 'Z']])
    
    # Z position LIST EXISTING CIRCUIT
    def test_z_position_list_existingCircuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.z(0)

        gate = circuit.z([1, 2])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], ZGate)
        self.assertEqual(circuit.getCircuitBody(), [['Z'], [1, 'Z', 'Z']])

    # Z position ALL
    def test_z_position_all(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.z(1)

        gate = circuit.z()

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], ZGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'Z'], ['Z', 'Z']])

    # BAD ARGUMENT position LIST
    def test_z_badArgument_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.z([])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT position LIST DUPLICATED
    def test_z_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.z([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_z_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.z('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_z_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.z([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # DEPRECATED add: when add is deprecated REMOVE FROM HERE
    # Z add
    def test_z_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.z(0, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Z')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # Z position LIST add
    def test_z_position_list_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.z([0, 1], False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Z'), (1, 'Z')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT TYPE add
    def test_z_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.z(0, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
    # TO HERE


##################_____SWAP_____##################
class Test_Swap(unittest.TestCase):

    # SWAP position 0, 1
    def test_swap_position_0_1(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.swap(0, 1)

        self.assertIsInstance(gate, SwapGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap']])

    # SWAP position 0, 2
    def test_swap_position_0_2(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.swap(0, 2)

        self.assertIsInstance(gate, SwapGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap']])

    # SWAP position 1, 2
    def test_swap_position_1_2(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.swap(1, 2)

        self.assertIsInstance(gate, SwapGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'Swap', 'Swap']])

    # SWAP EXISTING CIRCUIT
    def test_swap_existingCircuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.swap(1, 2)

        self.assertIsInstance(gate, SwapGate)
        self.assertEqual(circuit.getCircuitBody(), [['H'], [1, 'Swap', 'Swap']])

    # BAD ARGUMENT position DUPLICATED
    def test_swap_badArgument_position_duplicated(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.swap(0, 0)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position1
    def test_swap_badArgumentType_position1(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.swap('position', 1)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position2
    def test_swap_badArgumentType_position2(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.swap(0, 'position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # DEPRECATED add: when add is deprecated REMOVE FROM HERE
    # SWAP add
    def test_swap_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.swap(0, 1, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'Swap'), (1, 'Swap')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT TYPE add
    def test_swap_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.swap(0, 1, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
    # TO HERE


##################_____CH_____##################
class Test_CH(unittest.TestCase):

    # CH position 0, 1
    def test_ch_0_1(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.ch(0, 1)

        self.assertIsInstance(gate, CHGate)
        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 'H']])

    # CH position 1, 0
    def test_ch_1_0(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.ch(1, 0)

        self.assertIsInstance(gate, CHGate)
        self.assertEqual(circuit.getCircuitBody(), [['H', 'CTRL']])

    # CH position 0, 2
    def test_ch_position_0_2(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.ch(0, 2)

        self.assertIsInstance(gate, CHGate)
        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 1, 'H']])

    # CH position 1, 2
    def test_ch_position_1_2(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.ch(1, 2)

        self.assertIsInstance(gate, CHGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'CTRL', 'H']])

    # CH EXISTING CIRCUIT
    def test_ch_existingCircuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.ch(1, 2)

        self.assertIsInstance(gate, CHGate)
        self.assertEqual(circuit.getCircuitBody(), [['H'], [1, 'CTRL', 'H']])

    # BAD ARGUMENT position DUPLICATED
    def test_ch_badArgument_position_duplicated(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ch(0, 0)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position1
    def test_ch_badArgumentType_position1(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ch('position', 1)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position2
    def test_ch_badArgumentType_position2(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ch(0, 'position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # DEPRECATED add: when add is deprecated REMOVE FROM HERE
    # CH add
    def test_ch_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.ch(0, 1, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'CTRL'), (1, 'H')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT TYPE add
    def test_ch_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ch(0, 1, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
    # TO HERE


##################_____CX_____##################
class Test_CX(unittest.TestCase):

    # CX position 0, 1
    def test_cx_position_0_1(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.cx(0, 1)

        self.assertIsInstance(gate, CXGate)
        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 'X']])

    # CX position 1, 0
    def test_cx_position_1_0(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.cx(1, 0)

        self.assertIsInstance(gate, CXGate)
        self.assertEqual(circuit.getCircuitBody(), [['X', 'CTRL']])

    # CX position 0, 2
    def test_cx_position_0_2(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.cx(0, 2)

        self.assertIsInstance(gate, CXGate)
        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 1, 'X']])

    # CX position 1, 2
    def test_cx_position_1_2(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.cx(1, 2)

        self.assertIsInstance(gate, CXGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'CTRL', 'X']])

    # CX EXISTING CIRCUIT
    def test_cx_existingCircuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.cx(1, 2)

        self.assertIsInstance(gate, CXGate)
        self.assertEqual(circuit.getCircuitBody(), [['H'], [1, 'CTRL', 'X']])

    # BAD ARGUMENT position DUPLICATED
    def test_cx_badArgument_position_duplicated(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.cx(0, 0)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position1
    def test_cx_badArgumentType_position1(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.cx('position', 1)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position2
    def test_cx_badArgumentType_position2(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.cx(0, 'position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # DEPRECATED add: when add is deprecated REMOVE FROM HERE
    # CX add
    def test_cx_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.cx(0, 1, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'CTRL'), (1, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT TYPE add
    def test_cx_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.cx(0, 1, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
    # TO HERE


##################_____CCX_____##################
class Test_CCX(unittest.TestCase):

    # CCX position 0, 1, 2
    def test_ccx_position_0_1_2(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.ccx(0, 1, 2)

        self.assertIsInstance(gate, CCXGate)
        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 'CTRL', 'X']])

    # CCX position 0, 1, 3
    def test_ccx_position_0_1_3(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.ccx(0, 1, 3)

        self.assertIsInstance(gate, CCXGate)
        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 'CTRL', 1, 'X']])

    # CCX position 1, 2, 3
    def test_ccx_position_1_2_3(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.ccx(1, 2, 3)

        self.assertIsInstance(gate, CCXGate)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'CTRL', 'CTRL', 'X']])

    # CCX EXISTING CIRCUIT
    def test_ccx_existingCircuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.ccx(1, 2, 3)

        self.assertIsInstance(gate, CCXGate)
        self.assertEqual(circuit.getCircuitBody(), [['H'], [1, 'CTRL', 'CTRL', 'X']])

    # BAD ARGUMENT position DUPLICATED
    def test_ccx_badArgument_position_duplicated(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ccx(0, 0, 1)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position1
    def test_ccx_badArgumentType_position1(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ccx('position', 1, 2)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position2
    def test_ccx_badArgumentType_position2(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ccx(0, 'position', 2)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position3
    def test_ccx_badArgumentType_position3(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ccx(0, 1, 'position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # DEPRECATED add: when add is deprecated REMOVE FROM HERE
    # CCX add
    def test_ccx_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.ccx(0, 1, 2, False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(0, 'CTRL'), (1, 'CTRL'), (2, 'X')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT TYPE add
    def test_ccx_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.ccx(0, 1, 2, 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____CONTROL_____##################
class Test_Control(unittest.TestCase):

    # CONTROL position 0 gate SingleGate position 1
    def test_control_position_0_gate_SingleGate_position_1(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.control(0, HGate(1))

        self.assertIsInstance(gate, ControlledGate)
        self.assertEqual(gate.getSymbol(), 'H')
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getControlPositions(), [0])
        self.assertEqual(gate.getTargetPosition(), 1)
        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 'H']])

    # CONTROL position LIST gate SingleGate position 2
    def test_control_position_list_gate_SingleGate_position_2(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.control([0, 1], HGate(2))

        self.assertIsInstance(gate, ControlledGate)
        self.assertEqual(gate.getSymbol(), 'H')
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getControlPositions(), [0, 1])
        self.assertEqual(gate.getTargetPosition(), 2)
        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 'CTRL', 'H']])

    # CONTROL position 0 gate ArgumentGate position 1
    def test_control_position_0_gate_ArgumentGate_position_1(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.control(0, PGate(1))

        self.assertIsInstance(gate, ControlledGate)
        self.assertEqual(gate.getSymbol(), {'id': 'P', 'arg': 'pi'})
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getControlPositions(), [0])
        self.assertEqual(gate.getTargetPosition(), 1)
        self.assertEqual(circuit.getCircuitBody(), [['CTRL', {'id': 'P', 'arg': 'pi'}]])

    # CONTROL position LIST gate ArgumentGate position 2
    def test_control_position_list_gate_ArgumentGate_position_2(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.control([0, 1], PGate(2))

        self.assertIsInstance(gate, ControlledGate)
        self.assertEqual(gate.getSymbol(), {'id': 'P', 'arg': 'pi'})
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getControlPositions(), [0, 1])
        self.assertEqual(gate.getTargetPosition(), 2)
        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 'CTRL', {'id': 'P', 'arg': 'pi'}]])

    # CONTROL position 0 gate MultipleGate position 1, 2
    def test_control_position_0_gate_MultipleGate_position_1_2(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.control(0, SwapGate(1, 2))

        self.assertIsInstance(gate, ControlledGate)
        self.assertEqual(gate.getSymbol(), 'Swap')
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getControlPositions(), [0])
        self.assertEqual(gate.getTargetPosition(), [1, 2])
        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 'Swap', 'Swap']])

    # CONTROL position LIST gate MultipleGate position 2, 3
    def test_control_position_list_gate_MultipleGate_position_2_3(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.control([0, 1], SwapGate(2, 3))

        self.assertIsInstance(gate, ControlledGate)
        self.assertEqual(gate.getSymbol(), 'Swap')
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getControlPositions(), [0, 1])
        self.assertEqual(gate.getTargetPosition(), [2, 3])
        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 'CTRL', 'Swap', 'Swap']])

    # CONTROL position 0 gate ControlledGate position 1, 2
    def test_control_position_0_gate_ControlledGate_position_1_2(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.control(0, CHGate(1, 2))

        self.assertIsInstance(gate, ControlledGate)
        self.assertEqual(gate.getSymbol(), 'H')
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getControlPositions(), [0, 1])
        self.assertEqual(gate.getTargetPosition(), 2)
        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 'CTRL', 'H']])

    # CONTROL position LIST gate ControlledGate position 2, 3
    def test_control_position_list_gate_ControlledGate_position_2_3(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.control([0, 1], CHGate(2, 3))

        self.assertIsInstance(gate, ControlledGate)
        self.assertEqual(gate.getSymbol(), 'H')
        self.assertEqual(gate.getControllable(), True)
        self.assertEqual(gate.getControlPositions(), [0, 1, 2])
        self.assertEqual(gate.getTargetPosition(), 3)
        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 'CTRL', 'CTRL', 'H']])

    # BAD ARGUMENT position LIST
    def test_control_badArgument_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.control([], HGate(1))
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT position LIST DUPLICATED
    def test_control_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.control([0, 0], HGate(1))
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT gate NON CONTROLLABLE
    def test_control_badArgument_gate_nonControllable(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.control(0, Barrier(1))
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_control_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.control('position', HGate(1))
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE gate
    def test_control_badArgumentType_gate(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.control(0, 'gate')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # DEPRECATED oldGateStructure: when oldGateStructure is deprecated REMOVE FROM HERE
    # CONTROL position 0 oldGateStructure
    def test_control_position_0_oldGateStructure(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.control(0, circuit.h(1, False))

        self.assertEqual(gate, [(1, 'H'), (0, 'CTRL')])

    # BAD ARGUMENT TYPE position oldGateStructure
    def test_control_badArgumentType_position_oldGateStructure(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            cx = circuit.control('position', circuit.h(0, False))
            circuit.addCreatedGate(cx)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE circuit oldGateStructure
    def test_control_badArgumentType_circuit_oldGateStructure(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.control(0, 'circuit')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
    # TO HERE

# DEPRECATED mcg: when mcg is deprecated REMOVE FROM HERE
##################_____MULTI CONTROL GATE_____##################
class Test_MCG(unittest.TestCase):

    # MCG position 0
    def test_mcg_position_0(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.mcg(0, circuit.x(1, False))

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'X'), (0, 'CTRL')])
        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 'X']])

    # MCG EXISTING CIRCUIT position NEW COLUMN
    def test_mcg_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.mcg(0, circuit.x(1, False))

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(1, 'X'), (0, 'CTRL')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], ['CTRL', 'X']])

    # MCG EXISTING CIRCUIT position SAME COLUMN
    def test_mcg_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.mcg(1, circuit.x(2, False))

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, 'X'), (1, 'CTRL')])
        self.assertEqual(circuit.getCircuitBody(), [['H'], [1, 'CTRL', 'X']])

    # MCG EXISTING CIRCUIT position BETWEEN SWAP
    def test_mcg_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 3)

        gate = circuit.mcg(1, circuit.x(2, False))

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, 'X'), (1, 'CTRL')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 1, 'Swap'], [1, 'CTRL', 'X']])

    # MCG EXISTING CIRCUIT position UNDER SWAP
    def test_mcg_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.mcg(2, circuit.x(3, False))

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(3, 'X'), (2, 'CTRL')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'CTRL', 'X']])

    # MCG position LIST
    def test_mcg_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.mcg([0, 2], circuit.x(3, False))

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(3, 'X'), (0, 'CTRL'), (2, 'CTRL')])
        self.assertEqual(circuit.getCircuitBody(), [[1, 'H'], ['CTRL', 1, 'CTRL', 'X']])

    # MCG position LIST EXISTING CIRCUIT
    def test_mcg_position_list_existingCircuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.x(0)

        gate = circuit.mcg([0, 1], circuit.x(2, False))

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, 'X'), (0, 'CTRL'), (1, 'CTRL')])
        self.assertEqual(circuit.getCircuitBody(), [['X'], ['CTRL', 'CTRL', 'X']])

    # MCG position LIST EXISTING CIRCUIT WITH SWAP
    def test_mcg_position_list_existingCircuit_swap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.mcg([0, 1], circuit.x(2, False))

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(2, 'X'), (0, 'CTRL'), (1, 'CTRL')])
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], ['CTRL', 'CTRL', 'X']])

    # MCG add
    def test_mcg_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.mcg([0, 2], circuit.x(3, False), False)

        self.assertIsInstance(gate, list)
        self.assertEqual(gate, [(3, 'X'), (0, 'CTRL'), (2, 'CTRL')])
        self.assertEqual(circuit.getCircuitBody(), [[]])

    # BAD ARGUMENT position DUPLICATED CIRCUIT
    def test_mcg_badArgument_position_duplicated_circuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.mcg(0, circuit.x(0, False))
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT position LIST
    def test_mcg_badArgument_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.mcg([], circuit.x(3, False))
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT position LIST DUPLICATED
    def test_mcg_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.mcg([0, 0], circuit.x(3, False))
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT position LIST DUPLICATED CIRCUIT
    def test_mcg_badArgument_position_list_duplicated_circuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.mcg([0, 1], circuit.x(1, False))
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_mcg_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.mcg('position', circuit.x(3, False))
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_mcg_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.mcg([0, 'position'], circuit.x(3, False))
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE add
    def test_mcg_badArgumentType_add(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.mcg([0, 2], circuit.x(3, False), 'add')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
# TO HERE


if __name__ == '__main__':
    unittest.main()