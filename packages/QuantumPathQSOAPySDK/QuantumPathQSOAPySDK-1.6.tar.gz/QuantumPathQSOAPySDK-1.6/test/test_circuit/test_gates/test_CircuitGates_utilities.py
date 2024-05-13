import unittest
from QuantumPathQSOAPySDK import QSOAPlatform
from QuantumPathQSOAPySDK.circuit.gates.basicGates import (HGate, SwapGate, CHGate)
from QuantumPathQSOAPySDK.circuit.gates.rotationGates import PGate
from QuantumPathQSOAPySDK.circuit.gates.utilities import (Barrier, BeginRepeat, EndRepeat)

# UTILITIES:
#   Barrier
#   BeginRepeat
#   EndRepeat
#   Add
#   AddCreatedGate

##################_____BARRIER_____##################
class Test_Barrier(unittest.TestCase):

    # BARRIER position 0
    def test_barrier_position_0(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.barrier(0)

        self.assertIsInstance(gate, Barrier)
        self.assertEqual(circuit.getCircuitBody(), [['SPACER']])

    # BARRIER position 1
    def test_barrier_position_1(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.barrier(1)

        self.assertIsInstance(gate, Barrier)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'SPACER']])

    # BARRIER EXISTING CIRCUIT position NEW COLUMN
    def test_barrier_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.barrier(0)

        self.assertIsInstance(gate, Barrier)
        self.assertEqual(circuit.getCircuitBody(), [['H'], ['SPACER']])

    # BARRIER EXISTING CIRCUIT position SAME COLUMN
    def test_barrier_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.barrier(1)

        self.assertIsInstance(gate, Barrier)
        self.assertEqual(circuit.getCircuitBody(), [['H', 'SPACER']])

    # BARRIER EXISTING CIRCUIT position BETWEEN SWAP
    def test_barrier_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.barrier(1)

        self.assertIsInstance(gate, Barrier)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'SPACER']])

    # BARRIER EXISTING CIRCUIT position UNDER SWAP
    def test_barrier_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.barrier(2)

        self.assertIsInstance(gate, Barrier)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'SPACER']])

    # BARRIER position LIST
    def test_barrier_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.barrier([0, 1])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], Barrier)
        self.assertEqual(circuit.getCircuitBody(), [['SPACER', 'SPACER']])
    
    # BARRIER position LIST EXISTING CIRCUIT
    def test_barrier_position_list_existingCircuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.barrier([1, 2])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], Barrier)
        self.assertEqual(circuit.getCircuitBody(), [['H'], [1, 'SPACER', 'SPACER']])

    # BARRIER position ALL
    def test_barrier_position_all(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(1)

        gate = circuit.barrier()

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], Barrier)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'H'], ['SPACER', 'SPACER']])

    # BAD ARGUMENT position LIST
    def test_barrier_badArgument_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.barrier([])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT position LIST DUPLICATED
    def test_barrier_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.barrier([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_barrier_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.barrier('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_barrier_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.barrier([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____BEGIN REPEAT_____##################
class Test_BeginRepeat(unittest.TestCase):

    # BEGIN REPEAT position 0
    def test_beginRepeat_position_0(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.beginRepeat(0, 2)

        self.assertIsInstance(gate, BeginRepeat)
        self.assertEqual(circuit.getCircuitBody(), [[{'id': 'BEGIN_R', 'arg': '2'}]])

    # BEGIN REPEAT EXISTING CIRCUIT position NEW COLUMN
    def test_beginRepeat_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.beginRepeat(0, 2)

        self.assertIsInstance(gate, BeginRepeat)
        self.assertEqual(circuit.getCircuitBody(), [['H'], [{'id': 'BEGIN_R', 'arg': '2'}]])

    # BEGIN REPEAT EXISTING CIRCUIT position SAME COLUMN
    def test_beginRepeat_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.beginRepeat(1, 2)

        self.assertIsInstance(gate, BeginRepeat)
        self.assertEqual(circuit.getCircuitBody(), [['H', {'id': 'BEGIN_R', 'arg': '2'}]])

    # BEGIN REPEAT EXISTING CIRCUIT position BETWEEN SWAP
    def test_beginRepeat_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.beginRepeat(1, 2)

        self.assertIsInstance(gate, BeginRepeat)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, {'id': 'BEGIN_R', 'arg': '2'}]])

    # BEGIN REPEAT EXISTING CIRCUIT position UNDER SWAP
    def test_beginRepeat_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.beginRepeat(2, 2)

        self.assertIsInstance(gate, BeginRepeat)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, {'id': 'BEGIN_R', 'arg': '2'}]])

    # BEGIN REPEAT position LIST
    def test_beginRepeat_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.beginRepeat([0, 1], 2)

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], BeginRepeat)
        self.assertEqual(circuit.getCircuitBody(), [[{'id': 'BEGIN_R', 'arg': '2'}, {'id': 'BEGIN_R', 'arg': '2'}]])

    # BEGIN REPEAT position LIST EXISTING CIRCUIT
    def test_beginRepeat_position_list_existingCircuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.beginRepeat([1, 2], 2)

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], BeginRepeat)
        self.assertEqual(circuit.getCircuitBody(), [['H'], [1, {'id': 'BEGIN_R', 'arg': '2'}, {'id': 'BEGIN_R', 'arg': '2'}]])

    # BAD ARGUMENT position LIST
    def test_beginRepeat_badArgument_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.beginRepeat([], 2)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT position LIST DUPLICATED
    def test_beginRepeat_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.beginRepeat([0, 0], 2)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_beginRepeat_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.beginRepeat('position', 2)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_beginRepeat_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.beginRepeat([0, 'position'], 2)
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE repetitions
    def test_beginRepeat_badArgumentType_argument(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.beginRepeat(0, 'repetitions')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____END REPEAT_____##################
class Test_EndRepeat(unittest.TestCase):

    # END REPEAT position 0
    def test_endRepeat_position_0(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.endRepeat(0)

        self.assertIsInstance(gate, EndRepeat)
        self.assertEqual(circuit.getCircuitBody(), [['END_R']])

    # END REPEAT position 1
    def test_endRepeat_position_1(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.endRepeat(1)

        self.assertIsInstance(gate, EndRepeat)
        self.assertEqual(circuit.getCircuitBody(), [[1, 'END_R']])

    # END REPEAT EXISTING CIRCUIT position NEW COLUMN
    def test_endRepeat_existingCircuit_position_newColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.endRepeat(0)

        self.assertIsInstance(gate, EndRepeat)
        self.assertEqual(circuit.getCircuitBody(), [['H'], ['END_R']])

    # END REPEAT EXISTING CIRCUIT position SAME COLUMN
    def test_endRepeat_existingCircuit_position_sameColumn(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.h(0)

        gate = circuit.endRepeat(1)

        self.assertIsInstance(gate, EndRepeat)
        self.assertEqual(circuit.getCircuitBody(), [['H', 'END_R']])

    # END REPEAT EXISTING CIRCUIT position BETWEEN SWAP
    def test_endRepeat_existingCircuit_position_betweenSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 2)

        gate = circuit.endRepeat(1)

        self.assertIsInstance(gate, EndRepeat)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 1, 'Swap'], [1, 'END_R']])

    # END REPEAT EXISTING CIRCUIT position UNDER SWAP
    def test_endRepeat_existingCircuit_position_underSwap(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.swap(0, 1)

        gate = circuit.endRepeat(2)

        self.assertIsInstance(gate, EndRepeat)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap'], [1, 1, 'END_R']])

    # END REPEAT position LIST
    def test_endRepeat_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.endRepeat([0, 1])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], EndRepeat)
        self.assertEqual(circuit.getCircuitBody(), [['END_R', 'END_R']])

    # END REPEAT position LIST EXISTING CIRCUIT
    def test_endRepeat_position_list_existingCircuit(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()
        circuit.x(0)

        gate = circuit.endRepeat([1, 2])

        self.assertIsInstance(gate, list)
        self.assertIsInstance(gate[0], EndRepeat)
        self.assertEqual(circuit.getCircuitBody(), [['X'], [1, 'END_R', 'END_R']])

    # BAD ARGUMENT position LIST
    def test_endRepeat_badArgument_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.endRepeat([])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT position LIST DUPLICATED
    def test_endRepeat_badArgument_position_list_duplicated(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.endRepeat([0, 0])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_endRepeat_badArgumentType_position(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.endRepeat('position')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE position LIST
    def test_endRepeat_badArgumentType_position_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.endRepeat([0, 'position'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


##################_____ADD_____##################
class Test_Add(unittest.TestCase):

    # ADD gate SingleGate
    def test_add_gate_SingleGate(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.add(HGate(0))

        self.assertIsInstance(gate, HGate)
        self.assertEqual(circuit.getCircuitBody(), [['H']])

    # ADD gate ArgumentGate
    def test_add_gate_ArgumentGate(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.add(PGate(0))

        self.assertIsInstance(gate, PGate)
        self.assertEqual(circuit.getCircuitBody(), [[{'id': 'P', 'arg': 'pi'}]])

    # ADD gate MultipleGate
    def test_add_gate_MultipleGate(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.add(SwapGate(0, 1))

        self.assertIsInstance(gate, SwapGate)
        self.assertEqual(circuit.getCircuitBody(), [['Swap', 'Swap']])

    # ADD gate ControlledGate
    def test_add_gate_ControlledGate(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.add(CHGate(0, 1))

        self.assertIsInstance(gate, CHGate)
        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 'H']])

    # ADD gate LIST
    def test_add_gate_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        gate = circuit.add([HGate(0), PGate(0)])

        self.assertIsInstance(gate, list)
        self.assertEqual(circuit.getCircuitBody(), [['H'], [{'id': 'P', 'arg': 'pi'}]])

    # BAD ARGUMENT gate LIST
    def test_add_badArgument_gate_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.add([])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, ValueError)

    # BAD ARGUMENT TYPE position
    def test_add_badArgumentType_gate(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.add('gate')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)

    # BAD ARGUMENT TYPE gate LIST
    def test_add_badArgumentType_gate_list(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.add([HGate(0), 'gate'])
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)


# DEPRECATED addCreatedGate: when addCreatedGate is deprecated REMOVE FROM HERE
class Test_AddCreatedGate(unittest.TestCase):

    # ADD CREATED GATE position 0
    def test_addCreatedGate_position_0(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        cx = circuit.control(0, circuit.x(1, False))
        circuit.addCreatedGate(cx)

        self.assertEqual(circuit.getCircuitBody(), [['CTRL', 'X']])

    # BAD ARGUMENT TYPE gate
    def test_addCreatedGate_badArgumentType_gate(self):
        qsoa = QSOAPlatform(configFile=True)
        circuit = qsoa.CircuitGates()

        try:
            circuit.addCreatedGate('gate')
            raise Exception

        except Exception as e:
            self.assertIsInstance(e, TypeError)
# TO HERE

if __name__ == '__main__':
    unittest.main()