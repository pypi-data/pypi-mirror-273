from ...utils.checker import (checkInputTypes, checkListTypes, checkValues, checkMathExpression, checkDifferentPosition)
from .gates import (SingleGate, ArgumentGate, MultipleGate, ControlledGate)
from .measureGates import MeasureGate
from .basicGates import (HGate, XGate, YGate, ZGate, SwapGate, CHGate, CXGate, CCXGate)
from .preparedGates import (SGate, I_SGate, SXGate, I_SXGate, SYGate, I_SYGate, TGate, I_TGate, TXGate, I_TXGate, TYGate, I_TYGate)
from .rotationGates import (PGate, RXGate, RYGate, RZGate)
from .utilities import (Barrier, BeginRepeat, EndRepeat)

import warnings
import sys

def deprecation_warning_add(func):
    warnings.formatwarning = lambda message, category, filename, lineno, file, line=None: f'{category.__name__}: using "{func}" function. {message}\n'
    warnings.simplefilter('always', DeprecationWarning)
    warnings.warn(f'"add" argument is deprecated and will be removed in future versions. For further information please visit the user guide', DeprecationWarning)

def deprecation_warning_oldGateStructure(func):
    warnings.formatwarning = lambda message, category, filename, lineno, file, line=None: f'{category.__name__}: using "{func}" function. {message}\n'
    warnings.simplefilter('always', DeprecationWarning)
    warnings.warn(f'Old gate structure is deprecated. Instead use a gate object. For further information please visit the user guide', DeprecationWarning)

def deprecation_warning_mcg(func):
    warnings.formatwarning = lambda message, category, filename, lineno, file, line=None: f'{category.__name__}: using "{func}" function. {message}\n'
    warnings.simplefilter('always', DeprecationWarning)
    warnings.warn(f'"mcg" method is deprecated. Instead use the new behaviour of "control" method . For further information please visit the user guide', DeprecationWarning)

class CircuitGates:

    # CONSTRUCTOR
    def __init__(self):
        self.__circuitBody = [[]]
        self.__qubitStates = []
        self.__numerOfQubits = 0
        self.__defaultQubitState = '0'

        self.__circuitVLStructure = {
            'cols': self.__circuitBody,
            'init': self.__qubitStates
        }

    # GETTERS
    def getCircuitBody(self) -> list:
        """
        Get Circuit Body.

        Prerequisites
        ----------
        - Created circuit.

        Output
        ----------
        list
        """

        return self.__circuitBody

    def getParsedBody(self) -> str:
        """
        Get Circuit Body VL.

        Prerequisites
        ----------
        - Created circuit.

        Output
        ----------
        str
        """

        parsedtBody = 'circuit=' +  str(self.__circuitVLStructure).replace("'", '"')

        return parsedtBody

    def getQubitStates(self) -> list:
        """
        Get Circuit Qubit states.

        Prerequisites
        ----------
        - Created circuit.

        Output
        ----------
        list
        """

        return self.__qubitStates

    def getNumberOfQubits(self) -> int:
        """
        Get number of qubits used in circuit.

        Prerequisites
        ----------
        - Created circuit.

        Output
        ----------
        int
        """

        return self.__numerOfQubits

    def getDefaultQubitState(self) -> str:
        """
        Get Default Qubit state.

        Prerequisites
        ----------
        - Created circuit.
        
        Output
        ----------
        str
        """
        
        return self.__defaultQubitState

    def setDefaultQubitState(self, qubitState: str) -> str:
        """
        Set Default Qubit state.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        qubitState : str
            Set default qubit state. It can be 0, 1, +, -, i or -i.

        Output
        ----------
        str
        """

        # CHECK INPUTS
        checkInputTypes(
            ('qubitState', qubitState, (str,))
        )
        checkValues(('qubitStates', qubitState, ['0', '1', '+', '-', 'i', '-i']))

        # set new default qubit state
        self.__defaultQubitState = qubitState

        return self.__qubitStates

    def initializeQubitStates(self, qubitStates: list):
        """
        Initialize Qubit states.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        qbitStates : list
            List of strings setting up the qubit states. It must be equal than number of qubits. There can be 0, 1, +, -, i or -i.
        """
        # CHECK INPUTS
        checkInputTypes(
            ('qubitStates', qubitStates, (list,))
        )
        for qubitState in qubitStates:
            checkInputTypes(('qubitStates', qubitState, (str,)))
            checkValues(('qubitStates', qubitState, ['0', '1', '+', '-', 'i', '-i']))

        self.__qubitStates = qubitStates


    # PRIVATE METHODS
    def __addGateInNewColumn(self, gate):
        '''
        Add a gate or multiple gates in a new column.
        '''
        # SEARCH LAST COLUMN WITH GATE
        if self.__circuitBody[0] == []: # circuit is empty
            lastColumn = 0
        
        else: # if circuit is not empty
            self.__circuitBody.append([]) # add a new column
            lastColumn = -1

        # CREATE GATES LIST TO ADD
        gatesList = []

        if isinstance(gate, list): # list of gates
            for g in gate:
                gatesList.append((g.getPosition(), g.getSymbol()))
        
        elif isinstance(gate, MultipleGate): # multiple gate
            for position in gate.getPositions():
                gatesList.append((position, gate.getSymbol()))

        elif isinstance(gate, ControlledGate): # controlled gate
            if isinstance(gate.getTargetPosition(), int):
                gatesList.append((gate.getTargetPosition(), gate.getSymbol()))
            else:
                for position in gate.getTargetPosition():
                    gatesList.append((position, gate.getSymbol()))

            for position in gate.getControlPositions():
                gatesList.append((position, gate.getControlSymbol()))

        gatesList = sorted(gatesList, key=lambda g: g[0])

        # ADD GATE
        for gate in gatesList:
            while len(self.__circuitBody[lastColumn]) != gate[0]: # fill with 1 the positions until the gate position
                self.__circuitBody[lastColumn].append(1)
            
            self.__circuitBody[lastColumn].append(gate[1]) # add the gate

    def __addGateInExistingColumn(self, gate):
        '''
        Add a gate in an existing column.
        '''
        gatesList = gate if isinstance(gate, list) else [gate] # gate to gateList

        for gate in gatesList:
            # SEARCH LAST COLUMN WITH GATE
            lastColumn = self.__searchLastColumnWithGate(gate.getPosition()) # last column with gate in a specific row

            # ADD GATE
            if lastColumn != -1: # add the gate in an existing column

                if len(self.__circuitBody[lastColumn]) - 1 < gate.getPosition(): # column is smaller than the gate position

                    while len(self.__circuitBody[lastColumn]) != gate.getPosition(): # fill with 1 the positions until the gate position
                        self.__circuitBody[lastColumn].append(1)
                    
                    self.__circuitBody[lastColumn].append(gate.getSymbol()) # add the gate
                
                else: # column is larger than the gate position
                    self.__circuitBody[lastColumn][gate.getPosition()] = gate.getSymbol() # replace 1 by the gate
            
            else: # add a new column
                self.__circuitBody.append([])

                while len(self.__circuitBody[lastColumn]) != gate.getPosition(): # fill with 1 the positions until the gate position
                    self.__circuitBody[-1].append(1)
                    
                self.__circuitBody[-1].append(gate.getSymbol()) # add the gate

    def __searchLastColumnWithGate(self, position: int) -> int:
        '''
        Search last column with gate.
        '''
        numColumn = len(self.__circuitBody) - 1 # column index
        lastColumn = -1 # last column with gate

        # SEARCH LAST COLUMN
        while numColumn >= 0: # while there are columns

            if 'CTRL' in self.__circuitBody[numColumn] or 'Swap' in self.__circuitBody[numColumn]: # column have a multiple gate
                break

            elif len(self.__circuitBody[numColumn]) - 1 < position: # column is smaller than the gate position
                lastColumn = numColumn # column available to add the gate
            
            else: # column is greater than the gate position

                if self.__circuitBody[numColumn][position] == 1: # position is 1
                    lastColumn = numColumn # column available to add the gate
                
                else: # column have a gate, so is not available to add the gate
                    break

            numColumn -= 1 # check previous column

        return lastColumn

    def __addMultipleGate(self, positions, circuitBody):
        positions = sorted(positions)

        # SEARCH LAST COLUMN TO ADD
        if circuitBody[0] == []: # circuit is empty
            lastColumn = 0

        else: # if circuit is not empty
            lastColumn = -1
            circuitBody.append([])
        
        # ADD GATE
        for position in positions:

            while len(circuitBody[lastColumn]) != position[0]: # fill with 1 the positions until the gate position
                circuitBody[lastColumn].append(1)
            
            circuitBody[lastColumn].append(position[1]) # add the gate

    def __updateQubits(self):
        new_numerOfQubits = max(len(x) for x in self.__circuitBody) # new number of qubits

        if new_numerOfQubits > self.__numerOfQubits: # if new number of qubits
            while len(self.__qubitStates) < new_numerOfQubits:
                self.__qubitStates.append(self.__defaultQubitState) # add new qubit states
        
        self.__numerOfQubits = new_numerOfQubits
    
    # DEPRECATED add: when add is deprecated REMOVE FROM HERE
    def __definePositions(self, gate) -> list:
        positions = list()

        if isinstance(gate, list):
            for g in gate:
                positions.append((g.getPosition(), g.getSymbol()))

        else: 
            positionList = [gate.getPosition()]

            for position in positionList:
                positions.append((position, gate.getSymbol()))
        
        return positions
    # TO HERE


    # MEASURE GATES
    def measure(self, position = None) -> MeasureGate: # measure
        """
        Add Measure gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the measure. In the case that the position is not indicated, the measure will be added in all qubits. It can also be a list of positions.
        
        Output
        ----------
        MeasureGate obj | MeasureGate obj list
        """
        # CHECK INPUTS
        if position or isinstance(position, list):
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                checkListTypes(('position', position, (int,)))
                checkDifferentPosition(position)

        if isinstance(position, int):
            gate = MeasureGate(position)
        
        elif isinstance(position, list):
            gate = [MeasureGate(p) for p in position]
        
        elif position == None:
            gate = [MeasureGate(p) for p in range(0, self.__numerOfQubits)]

        return self.add(gate) # add to circuit


    # BASIC GATES
    def h(self, position = None, add: bool = True) -> HGate: # hadamard gate
        """
        Add Hadamard gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. It can also be a list of positions.
        add : bool
            [DEPRECATED] "add" argument is deprecated and will be removed in future versions. For more information visit the user guide.
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        HGate obj | HGate obj list | tuple list [DEPRECATED]
        """
        # CHECK INPUTS
        if position or isinstance(position, list):
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                checkListTypes(('position', position, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('add', add, (bool,))
        )

        if isinstance(position, int):
            gate = HGate(position)
        
        elif isinstance(position, list):
            gate = [HGate(p) for p in position]
        
        elif position == None:
            gate = [HGate(p) for p in range(0, self.__numerOfQubits)]

        if not add:
            deprecation_warning_add(sys._getframe().f_code.co_name)
            return self.__definePositions(gate)

        else:
            return self.add(gate) # add to circuit

        # DEPRECATED add: when add is deprecated REPLACE THE CODE ABOVE WITH THE FOLLOWING
        # # CHECK INPUTS
        # if position or isinstance(position, list):
        #     checkInputTypes(
        #         ('position', position, (int, list))
        #     )
        #     if isinstance(position, list):
        #         checkListTypes(('position', position, (int,)))
        #         checkDifferentPosition(position)

        # if isinstance(position, int):
        #     gate = HGate(position)
        
        # elif isinstance(position, list):
        #     gate = [HGate(p) for p in position]
        
        # elif position == None:
        #     gate = [HGate(p) for p in range(0, self.__numerOfQubits)]

        # return self.add(gate) # add to circuit

    
    def x(self, position = None, add: bool = True) -> XGate: # not gate
        """
        Add Pauli X gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. It can also be a list of positions.
        add : bool
            [DEPRECATED] "add" argument is deprecated and will be removed in future versions. For more information visit the user guide.
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        XGate obj | XGate obj list | tuple list [DEPRECATED]
        """
        # CHECK INPUTS
        if position or isinstance(position, list):
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                checkListTypes(('position', position, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('add', add, (bool,))
        )

        if isinstance(position, int):
            gate = XGate(position)
        
        elif isinstance(position, list):
            gate = [XGate(p) for p in position]
        
        elif position == None:
            gate = [XGate(p) for p in range(0, self.__numerOfQubits)]

        if not add:
            deprecation_warning_add(sys._getframe().f_code.co_name)
            return self.__definePositions(gate)

        else:
            return self.add(gate) # add to circuit

        # DEPRECATED add: when add is deprecated REPLACE THE CODE ABOVE WITH THE FOLLOWING
        # # CHECK INPUTS
        # if position or isinstance(position, list):
        #     checkInputTypes(
        #         ('position', position, (int, list))
        #     )
        #     if isinstance(position, list):
        #         checkListTypes(('position', position, (int,)))
        #         checkDifferentPosition(position)

        # if isinstance(position, int):
        #     gate = XGate(position)
        
        # elif isinstance(position, list):
        #     gate = [XGate(p) for p in position]
        
        # elif position == None:
        #     gate = [XGate(p) for p in range(0, self.__numerOfQubits)]

        # return self.add(gate) # add to circuit
    
    def y(self, position = None, add: bool = True) -> YGate: # pauli y gate
        """
        Add Pauli Y gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. It can also be a list of positions.
        add : bool
            [DEPRECATED] "add" argument is deprecated and will be removed in future versions. For more information visit the user guide.
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        YGate obj | YGate obj list | tuple list [DEPRECATED]
        """
        # CHECK INPUTS
        if position or isinstance(position, list):
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                checkListTypes(('position', position, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('add', add, (bool,))
        )

        if isinstance(position, int):
            gate = YGate(position)
        
        elif isinstance(position, list):
            gate = [YGate(p) for p in position]
        
        elif position == None:
            gate = [YGate(p) for p in range(0, self.__numerOfQubits)]

        if not add:
            deprecation_warning_add(sys._getframe().f_code.co_name)
            return self.__definePositions(gate)

        else:
            return self.add(gate) # add to circuit

        # DEPRECATED add: when add is deprecated REPLACE THE CODE ABOVE WITH THE FOLLOWING
        # # CHECK INPUTS
        # if position or isinstance(position, list):
        #     checkInputTypes(
        #         ('position', position, (int, list))
        #     )
        #     if isinstance(position, list):
        #         checkListTypes(('position', position, (int,)))
        #         checkDifferentPosition(position)

        # if isinstance(position, int):
        #     gate = YGate(position)
        
        # elif isinstance(position, list):
        #     gate = [YGate(p) for p in position]
        
        # elif position == None:
        #     gate = [YGate(p) for p in range(0, self.__numerOfQubits)]

        # return self.add(gate) # add to circuit

    def z(self, position = None, add: bool = True) -> ZGate: # pauli z gate
        """
        Add Pauli Z gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. It can also be a list of positions.
        add : bool
            [DEPRECATED] "add" argument is deprecated and will be removed in future versions. For more information visit the user guide.
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        ZGate obj | ZGate obj list | tuple list [DEPRECATED]
        """
        # CHECK INPUTS
        if position or isinstance(position, list):
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                checkListTypes(('position', position, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('add', add, (bool,))
        )

        if isinstance(position, int):
            gate = ZGate(position)
        
        elif isinstance(position, list):
            gate = [ZGate(p) for p in position]
        
        elif position == None:
            gate = [ZGate(p) for p in range(0, self.__numerOfQubits)]

        if not add:
            deprecation_warning_add(sys._getframe().f_code.co_name)
            return self.__definePositions(gate)

        else:
            return self.add(gate) # add to circuit

        # DEPRECATED add: when add is deprecated REPLACE THE CODE ABOVE WITH THE FOLLOWING
        # # CHECK INPUTS
        # if position or isinstance(position, list):
        #     checkInputTypes(
        #         ('position', position, (int, list))
        #     )
        #     if isinstance(position, list):
        #         checkListTypes(('position', position, (int,)))
        #         checkDifferentPosition(position)

        # if isinstance(position, int):
        #     gate = ZGate(position)
        
        # elif isinstance(position, list):
        #     gate = [ZGate(p) for p in position]
        
        # elif position == None:
        #     gate = [ZGate(p) for p in range(0, self.__numerOfQubits)]

        # return self.add(gate) # add to circuit

    def swap(self, position1: int, position2: int, add: bool = True) -> SwapGate: # swap gate
        """
        Add Swap gates.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position1 : int
            Mandatory argument. First qubit position to add the swap.
        position2 : int
            Mandatory argument. Second qubit position to add the swap.
        add : bool
            [DEPRECATED] "add" argument is deprecated and will be removed in future versions. For more information visit the user guide.
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        SwapGate obj
        """
        # CHECK INPUTS
        checkInputTypes(
            ('position1', position1, (int,)),
            ('position2', position2, (int,)),
            ('add', add, (bool,))
        )
        checkDifferentPosition([position1, position2])

        if not add:
            deprecation_warning_add(sys._getframe().f_code.co_name)
            return [(position1, 'Swap'), (position2, 'Swap')]

        else:
            return self.add(SwapGate(position1, position2)) # add to circuit

        # DEPRECATED add: when add is deprecated REPLACE THE CODE ABOVE WITH THE FOLLOWING
        # # CHECK INPUTS
        # checkInputTypes(
        #     ('position1', position1, (int,)),
        #     ('position2', position2, (int,)),
        # )
        # checkDifferentPosition([position1, position2])

        # return self.add(SwapGate(position1, position2)) # add to circuit

    def ch(self, position1: int, position2: int, add: bool = True) -> CHGate: # controlled hadamard gate
        """
        Add Controlled Hadamard gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position1 : int
            Mandatory argument. First qubit position to add the control.
        position2 : int
            Mandatory argument. Second qubit position to add the hadamard gate.
        add : bool
            [DEPRECATED] "add" argument is deprecated and will be removed in future versions. For more information visit the user guide.
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
            
        Output
        ----------
        CHGate obj | tuple list [DEPRECATED]
        """
        # CHECK INPUTS
        checkInputTypes(
            ('position1', position1, (int,)),
            ('position2', position2, (int,)),
            ('add', add, (bool,))
        )
        checkDifferentPosition([position1, position2])

        # DEPRECATED add
        if not add:
            deprecation_warning_add(sys._getframe().f_code.co_name)
            return [(position1, 'CTRL'), (position2, 'H')]

        else:
            return self.add(CHGate(position1, position2)) # add to circuit

        # DEPRECATED add: when add is deprecated REPLACE THE CODE ABOVE WITH THE FOLLOWING
        # # CHECK INPUTS
        # checkInputTypes(
        #     ('position1', position1, (int,)),
        #     ('position2', position2, (int,))
        # )
        # checkDifferentPosition([position1, position2])

        # return self.add(CHGate(position1, position2)) # add to circuit

    def cx(self, position1: int, position2: int, add: bool = True) -> CXGate: # control x gate
        """
        Add Controlled X gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position1 : int
            Mandatory argument. First qubit position to add the control.
        position2 : int
            Mandatory argument. Second qubit position to add the X gate.
        add : bool
            [DEPRECATED] "add" argument is deprecated and will be removed in future versions. For more information visit the user guide.
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        CXGate obj | tuple list [DEPRECATED]
        """
        # CHECK INPUTS
        checkInputTypes(
            ('position1', position1, (int,)),
            ('position2', position2, (int,)),
            ('add', add, (bool,))
        )
        checkDifferentPosition([position1, position2])

        # DEPRECATED add
        if not add:
            deprecation_warning_add(sys._getframe().f_code.co_name)
            return [(position1, 'CTRL'), (position2, 'X')]

        else:
            return self.add(CXGate(position1, position2)) # add to circuit
        
        # DEPRECATED add: when add is deprecated REPLACE THE CODE ABOVE WITH THE FOLLOWING
        # # CHECK INPUTS
        # checkInputTypes(
        #     ('position1', position1, (int,)),
        #     ('position2', position2, (int,))
        # )
        # checkDifferentPosition([position1, position2])

        # return self.add(CXGate(position1, position2)) # add to circuit

    def ccx(self, position1: int, position2: int, position3: int, add = True) -> CCXGate: # toffoli gate
        """
        Add Toffoli gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position1 : int
            Mandatory argument. First qubit position to add the control.
        position2 : int
            Mandatory argument. Second qubit position to add the control.
        position3 : int
            Mandatory argument. Third qubit position to add the X gate.
        add : bool
            [DEPRECATED] "add" argument is deprecated and will be removed in future versions. For more information visit the user guide.
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        CCXGate obj | tuple list [DEPRECATED]
        """
        # CHECK INPUTS
        checkInputTypes(
            ('position1', position1, (int,)),
            ('position2', position2, (int,)),
            ('position3', position3, (int,)),
            ('add', add, (bool,))
        )
        checkDifferentPosition([position1, position2, position3])

        # DEPRECATED add
        if not add:
            deprecation_warning_add(sys._getframe().f_code.co_name)
            return [(position1, 'CTRL'), (position2, 'CTRL'), (position3, 'X')]

        else:
            return self.add(CCXGate(position1, position2, position3)) # add to circuit

        # DEPRECATED add: when add is deprecated REPLACE THE CODE ABOVE WITH THE FOLLOWING
        # # CHECK INPUTS
        # checkInputTypes(
        #     ('position1', position1, (int,)),
        #     ('position2', position2, (int,)),
        #     ('position3', position3, (int,))
        # )
        # checkDifferentPosition([position1, position2, position3])

        # return self.add(CCXGate(position1, position2, position3)) # add to circuit

    def control(self, position, gate) -> ControlledGate: # control
        """
        Create and add custom controlled gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Mandatory argument. Qubit position to add the control. It can also be a list of positions.
        gate : Gate obj | list [DEPRECATED]
            Gate obj to be controlled.
        
        Output
        ----------
        ControlledGate obj | tuple list [DEPRECATED]
        """
        # CHECK INPUTS
        checkInputTypes(
            ('position', position, (int, list)),
            ('gate', gate, (SingleGate, ArgumentGate, MultipleGate, ControlledGate, list))
        )
        if isinstance(position, list):
            checkListTypes(('position', position, (int,)))
            checkDifferentPosition(position)
        if not isinstance(gate, list):
            if not gate.getControllable():
                raise ValueError('Gate object should be a controllable gate')

        if isinstance(gate, list):
            deprecation_warning_oldGateStructure(sys._getframe().f_code.co_name)

            circuit = gate
            correctPosition = True

            for gate in circuit:
                if position in gate:
                    correctPosition = False
                    break

            if correctPosition:
                circuit.append((position, 'CTRL'))

            return circuit

        else:
            controlPositions = position if isinstance(position, list) else [position]

            if isinstance(gate, SingleGate) or isinstance(gate, ArgumentGate):
                targetPosition = gate.getPosition()
            
            elif isinstance(gate, MultipleGate):
                targetPosition = gate.getPositions()

            elif isinstance(gate, ControlledGate):
                controlPositions.extend(gate.getControlPositions())
                targetPosition = gate.getTargetPosition()

            return self.add(ControlledGate(gate.getSymbol(), True, controlPositions, targetPosition))

        # DEPRECATED oldGateStructure: when oldGateStructure is deprecated REPLACE THE CODE ABOVE WITH THE FOLLOWING
        # # CHECK INPUTS
        # checkInputTypes(
        #     ('position', position, (int, list)),
        #     ('gate', gate, (SingleGate, ArgumentGate, MultipleGate, ControlledGate))
        # )
        # if isinstance(position, list):
        #     checkListTypes(('position', position, (int,)))
        #     checkDifferentPosition(position)
        # if not gate.getControllable():
        #     raise ValueError('Gate object should be a controllable gate')

        # controlPositions = position if isinstance(position, list) else [position]

        # if isinstance(gate, SingleGate) or isinstance(gate, ArgumentGate):
        #     targetPosition = gate.getPosition()
        
        # elif isinstance(gate, MultipleGate):
        #     targetPosition = gate.getPositions()

        # elif isinstance(gate, ControlledGate):
        #     controlPositions.extend(gate.getControlPositions())
        #     targetPosition = gate.getTargetPosition()

        # return ControlledGate(gate.getSymbol(), True, controlPositions, targetPosition)

    # DEPRECATED mcg: when mcg is deprecated REMOVE FROM HERE
    def mcg(self, position, circuit: list, add: bool = True) -> list: # multi control gate
        """
        [DEPRECATED METHOD] Use "control" method instead.
        Add Multi Controlled gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Qubit position or list of positions to add the control. It can also be a list of positions.
        circuit : list
            Gate or set of elements to add a control.
        add : bool
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        list
        """
        # CHECK INPUTS
        checkInputTypes(
            ('position', position, (int, list)),
            ('circuit', circuit, (list,)),
            ('add', add, (bool,)),
        )
        if isinstance(position, list):
            checkListTypes(('position', position, (int,)))
        
        deprecation_warning_mcg(sys._getframe().f_code.co_name)

        # DEPRECATED add
        if not add:
            deprecation_warning_add(sys._getframe().f_code.co_name)

        circuitPositions = []
        for gate in circuit:
            circuitPositions.append(gate[0])

        if isinstance(position, int):
            circuitPositions.append(position)
            checkDifferentPosition(circuitPositions)
        else:
            checkDifferentPosition(position + circuitPositions)

        gateSymbol = 'CTRL'

        if isinstance(position, int): # one postion
            circuit.append((position, gateSymbol))

        elif isinstance(position, list): # multiple positions
            for i in position:
                circuit.append((i, gateSymbol)) # add all controls

        if add:
            self.__addMultipleGate(circuit, self.__circuitBody) # add to circuit
        
        self.__updateQubits()
        
        return circuit
    # TO HERE

    # PREPARED GATES
    def s(self, position = None, add: bool = True) -> SGate: # square root of z, s gate
        """
        Add square root of Z, S gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. It can also be a list of positions.
        add : bool
            [DEPRECATED] "add" argument is deprecated and will be removed in future versions. For more information visit the user guide.
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        SGate obj | SGate obj list | tuple list [DEPRECATED]
        """
        # CHECK INPUTS
        if position or isinstance(position, list):
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                checkListTypes(('position', position, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('add', add, (bool,))
        )

        if isinstance(position, int):
            gate = SGate(position)
        
        elif isinstance(position, list):
            gate = [SGate(p) for p in position]
        
        elif position == None:
            gate = [SGate(p) for p in range(0, self.__numerOfQubits)]

        if not add:
            deprecation_warning_add(sys._getframe().f_code.co_name)
            return self.__definePositions(gate)

        else:
            return self.add(gate) # add to circuit

        # DEPRECATED add: when add is deprecated REPLACE THE CODE ABOVE WITH THE FOLLOWING
        # # CHECK INPUTS
        # if position or isinstance(position, list):
        #     checkInputTypes(
        #         ('position', position, (int, list))
        #     )
        #     if isinstance(position, list):
        #         checkListTypes(('position', position, (int,)))
        #         checkDifferentPosition(position)

        # if isinstance(position, int):
        #     gate = SGate(position)
        
        # elif isinstance(position, list):
        #     gate = [SGate(p) for p in position]
        
        # elif position == None:
        #     gate = [SGate(p) for p in range(0, self.__numerOfQubits)]

        # return self.add(gate) # add to circuit

    def i_s(self, position = None, add: bool = True) -> I_SGate: # adjoint square root z, i_s gate
        """
        Add adjoint square root Z, I_S gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. It can also be a list of positions.
        add : bool
            [DEPRECATED] "add" argument is deprecated and will be removed in future versions. For more information visit the user guide.
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        I_SGate obj | I_SGate obj list | tuple list [DEPRECATED]
        """
        # CHECK INPUTS
        if position or isinstance(position, list):
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                checkListTypes(('position', position, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('add', add, (bool,))
        )

        if isinstance(position, int):
            gate = I_SGate(position)
        
        elif isinstance(position, list):
            gate = [I_SGate(p) for p in position]
        
        elif position == None:
            gate = [I_SGate(p) for p in range(0, self.__numerOfQubits)]

        if not add:
            deprecation_warning_add(sys._getframe().f_code.co_name)
            return self.__definePositions(gate)

        else:
            return self.add(gate) # add to circuit

        # DEPRECATED add: when add is deprecated REPLACE THE CODE ABOVE WITH THE FOLLOWING
        # # CHECK INPUTS
        # if position or isinstance(position, list):
        #     checkInputTypes(
        #         ('position', position, (int, list))
        #     )
        #     if isinstance(position, list):
        #         checkListTypes(('position', position, (int,)))
        #         checkDifferentPosition(position)

        # if isinstance(position, int):
        #     gate = I_SGate(position)
        
        # elif isinstance(position, list):
        #     gate = [I_SGate(p) for p in position]
        
        # elif position == None:
        #     gate = [I_SGate(p) for p in range(0, self.__numerOfQubits)]

        # return self.add(gate) # add to circuit

    def sx(self, position = None, add: bool = True) -> SXGate: # square root of x, sx gate
        """
        Add square root of X, SX gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. It can also be a list of positions.
        add : bool
            [DEPRECATED] "add" argument is deprecated and will be removed in future versions. For more information visit the user guide.
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        SXGate obj | SXGate obj list | tuple list [DEPRECATED]
        """
        # CHECK INPUTS
        if position or isinstance(position, list):
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                checkListTypes(('position', position, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('add', add, (bool,))
        )

        if isinstance(position, int):
            gate = SXGate(position)
        
        elif isinstance(position, list):
            gate = [SXGate(p) for p in position]
        
        elif position == None:
            gate = [SXGate(p) for p in range(0, self.__numerOfQubits)]

        if not add:
            deprecation_warning_add(sys._getframe().f_code.co_name)
            return self.__definePositions(gate)

        else:
            return self.add(gate) # add to circuit

        # DEPRECATED add: when add is deprecated REPLACE THE CODE ABOVE WITH THE FOLLOWING
        # # CHECK INPUTS
        # if position or isinstance(position, list):
        #     checkInputTypes(
        #         ('position', position, (int, list))
        #     )
        #     if isinstance(position, list):
        #         checkListTypes(('position', position, (int,)))
        #         checkDifferentPosition(position)

        # if isinstance(position, int):
        #     gate = SXGate(position)
        
        # elif isinstance(position, list):
        #     gate = [SXGate(p) for p in position]
        
        # elif position == None:
        #     gate = [SXGate(p) for p in range(0, self.__numerOfQubits)]

        # return self.add(gate) # add to circuit

    def i_sx(self, position = None, add: bool = True) -> I_SXGate: # adjoint square root x, i_sx gate
        """
        Add adjoint square root X, I_SX gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. It can also be a list of positions.
        add : bool
            [DEPRECATED] "add" argument is deprecated and will be removed in future versions. For more information visit the user guide.
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        I_SXGate obj | I_SXGate obj list | tuple list [DEPRECATED]
        """
        # CHECK INPUTS
        if position or isinstance(position, list):
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                checkListTypes(('position', position, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('add', add, (bool,))
        )

        if isinstance(position, int):
            gate = I_SXGate(position)
        
        elif isinstance(position, list):
            gate = [I_SXGate(p) for p in position]
        
        elif position == None:
            gate = [I_SXGate(p) for p in range(0, self.__numerOfQubits)]

        if not add:
            deprecation_warning_add(sys._getframe().f_code.co_name)
            return self.__definePositions(gate)

        else:
            return self.add(gate) # add to circuit

        # DEPRECATED add: when add is deprecated REPLACE THE CODE ABOVE WITH THE FOLLOWING
        # # CHECK INPUTS
        # if position or isinstance(position, list):
        #     checkInputTypes(
        #         ('position', position, (int, list))
        #     )
        #     if isinstance(position, list):
        #         checkListTypes(('position', position, (int,)))
        #         checkDifferentPosition(position)

        # if isinstance(position, int):
        #     gate = I_SXGate(position)
        
        # elif isinstance(position, list):
        #     gate = [I_SXGate(p) for p in position]
        
        # elif position == None:
        #     gate = [I_SXGate(p) for p in range(0, self.__numerOfQubits)]

        # return self.add(gate) # add to circuit

    def sy(self, position = None, add: bool = True) -> SYGate: # square root of y, sy gate
        """
        Add square root of Y, SY gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. It can also be a list of positions.
        add : bool
            [DEPRECATED] "add" argument is deprecated and will be removed in future versions. For more information visit the user guide.
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        SYGate obj | SYGate obj list | tuple list [DEPRECATED]
        """
        # CHECK INPUTS
        if position or isinstance(position, list):
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                checkListTypes(('position', position, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('add', add, (bool,))
        )

        if isinstance(position, int):
            gate = SYGate(position)
        
        elif isinstance(position, list):
            gate = [SYGate(p) for p in position]
        
        elif position == None:
            gate = [SYGate(p) for p in range(0, self.__numerOfQubits)]

        if not add:
            deprecation_warning_add(sys._getframe().f_code.co_name)
            return self.__definePositions(gate)

        else:
            return self.add(gate) # add to circuit

        # DEPRECATED add: when add is deprecated REPLACE THE CODE ABOVE WITH THE FOLLOWING
        # # CHECK INPUTS
        # if position or isinstance(position, list):
        #     checkInputTypes(
        #         ('position', position, (int, list))
        #     )
        #     if isinstance(position, list):
        #         checkListTypes(('position', position, (int,)))
        #         checkDifferentPosition(position)

        # if isinstance(position, int):
        #     gate = SYGate(position)
        
        # elif isinstance(position, list):
        #     gate = [SYGate(p) for p in position]
        
        # elif position == None:
        #     gate = [SYGate(p) for p in range(0, self.__numerOfQubits)]

        # return self.add(gate) # add to circuit

    def i_sy(self, position = None, add: bool = True) -> I_SYGate: # adjoint square root y, i_sy gate
        """
        Add adjoint square root Y, I_SY gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. It can also be a list of positions.
        add : bool
            [DEPRECATED] "add" argument is deprecated and will be removed in future versions. For more information visit the user guide.
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        I_SYGate obj | I_SYGate obj list | tuple list [DEPRECATED]
        """
        # CHECK INPUTS
        if position or isinstance(position, list):
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                checkListTypes(('position', position, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('add', add, (bool,))
        )

        if isinstance(position, int):
            gate = I_SYGate(position)
        
        elif isinstance(position, list):
            gate = [I_SYGate(p) for p in position]
        
        elif position == None:
            gate = [I_SYGate(p) for p in range(0, self.__numerOfQubits)]

        if not add:
            deprecation_warning_add(sys._getframe().f_code.co_name)
            return self.__definePositions(gate)

        else:
            return self.add(gate) # add to circuit

        # DEPRECATED add: when add is deprecated REPLACE THE CODE ABOVE WITH THE FOLLOWING
        # # CHECK INPUTS
        # if position or isinstance(position, list):
        #     checkInputTypes(
        #         ('position', position, (int, list))
        #     )
        #     if isinstance(position, list):
        #         checkListTypes(('position', position, (int,)))
        #         checkDifferentPosition(position)

        # if isinstance(position, int):
        #     gate = I_SYGate(position)
        
        # elif isinstance(position, list):
        #     gate = [I_SYGate(p) for p in position]
        
        # elif position == None:
        #     gate = [I_SYGate(p) for p in range(0, self.__numerOfQubits)]

        # return self.add(gate) # add to circuit

    def t(self, position = None, add: bool = True) -> TGate: # four root of z, t gate
        """
        Add four root of Z, T gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. It can also be a list of positions.
        add : bool
            [DEPRECATED] "add" argument is deprecated and will be removed in future versions. For more information visit the user guide.
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        TGate obj | TGate obj list | tuple list [DEPRECATED]
        """
        # CHECK INPUTS
        if position or isinstance(position, list):
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                checkListTypes(('position', position, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('add', add, (bool,))
        )

        if isinstance(position, int):
            gate = TGate(position)
        
        elif isinstance(position, list):
            gate = [TGate(p) for p in position]
        
        elif position == None:
            gate = [TGate(p) for p in range(0, self.__numerOfQubits)]

        if not add:
            deprecation_warning_add(sys._getframe().f_code.co_name)
            return self.__definePositions(gate)

        else:
            return self.add(gate) # add to circuit

        # DEPRECATED add: when add is deprecated REPLACE THE CODE ABOVE WITH THE FOLLOWING
        # # CHECK INPUTS
        # if position or isinstance(position, list):
        #     checkInputTypes(
        #         ('position', position, (int, list))
        #     )
        #     if isinstance(position, list):
        #         checkListTypes(('position', position, (int,)))
        #         checkDifferentPosition(position)

        # if isinstance(position, int):
        #     gate = TGate(position)
        
        # elif isinstance(position, list):
        #     gate = [TGate(p) for p in position]
        
        # elif position == None:
        #     gate = [TGate(p) for p in range(0, self.__numerOfQubits)]

        # return self.add(gate) # add to circuit

    def i_t(self, position = None, add: bool = True) -> I_TGate: # adjoint four root z, i_t gate
        """
        Add adjoint four root Z, I_T gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. It can also be a list of positions.
        add : bool
            [DEPRECATED] "add" argument is deprecated and will be removed in future versions. For more information visit the user guide.
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        I_TGate obj | I_TGate obj list | tuple list [DEPRECATED]
        """
        # CHECK INPUTS
        if position or isinstance(position, list):
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                checkListTypes(('position', position, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('add', add, (bool,))
        )

        if isinstance(position, int):
            gate = I_TGate(position)
        
        elif isinstance(position, list):
            gate = [I_TGate(p) for p in position]
        
        elif position == None:
            gate = [I_TGate(p) for p in range(0, self.__numerOfQubits)]

        if not add:
            deprecation_warning_add(sys._getframe().f_code.co_name)
            return self.__definePositions(gate)

        else:
            return self.add(gate) # add to circuit

        # DEPRECATED add: when add is deprecated REPLACE THE CODE ABOVE WITH THE FOLLOWING
        # # CHECK INPUTS
        # if position or isinstance(position, list):
        #     checkInputTypes(
        #         ('position', position, (int, list))
        #     )
        #     if isinstance(position, list):
        #         checkListTypes(('position', position, (int,)))
        #         checkDifferentPosition(position)

        # if isinstance(position, int):
        #     gate = I_TGate(position)
        
        # elif isinstance(position, list):
        #     gate = [I_TGate(p) for p in position]
        
        # elif position == None:
        #     gate = [I_TGate(p) for p in range(0, self.__numerOfQubits)]

        # return self.add(gate) # add to circuit

    def tx(self, position = None, add: bool = True) -> TXGate: # four root of x, tx gate
        """
        Add four root of X, TX gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. It can also be a list of positions.
        add : bool
            [DEPRECATED] "add" argument is deprecated and will be removed in future versions. For more information visit the user guide.
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        TXGate obj | TXGate obj list | tuple list [DEPRECATED]
        """
        # CHECK INPUTS
        if position or isinstance(position, list):
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                checkListTypes(('position', position, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('add', add, (bool,))
        )

        if isinstance(position, int):
            gate = TXGate(position)
        
        elif isinstance(position, list):
            gate = [TXGate(p) for p in position]
        
        elif position == None:
            gate = [TXGate(p) for p in range(0, self.__numerOfQubits)]

        if not add:
            deprecation_warning_add(sys._getframe().f_code.co_name)
            return self.__definePositions(gate)

        else:
            return self.add(gate) # add to circuit

        # DEPRECATED add: when add is deprecated REPLACE THE CODE ABOVE WITH THE FOLLOWING
        # # CHECK INPUTS
        # if position or isinstance(position, list):
        #     checkInputTypes(
        #         ('position', position, (int, list))
        #     )
        #     if isinstance(position, list):
        #         checkListTypes(('position', position, (int,)))
        #         checkDifferentPosition(position)

        # if isinstance(position, int):
        #     gate = TXGate(position)
        
        # elif isinstance(position, list):
        #     gate = [TXGate(p) for p in position]
        
        # elif position == None:
        #     gate = [TXGate(p) for p in range(0, self.__numerOfQubits)]

        # return self.add(gate) # add to circuit

    def i_tx(self, position = None, add: bool = True) -> I_TXGate: # adjoint four root x, i_tx gate
        """
        Add adjoint four root X, I_TX gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. It can also be a list of positions.
        add : bool
            [DEPRECATED] "add" argument is deprecated and will be removed in future versions. For more information visit the user guide.
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        I_TXGate obj | I_TXGate obj list | tuple list [DEPRECATED]
        """
        # CHECK INPUTS
        if position or isinstance(position, list):
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                checkListTypes(('position', position, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('add', add, (bool,))
        )

        if isinstance(position, int):
            gate = I_TXGate(position)
        
        elif isinstance(position, list):
            gate = [I_TXGate(p) for p in position]
        
        elif position == None:
            gate = [I_TXGate(p) for p in range(0, self.__numerOfQubits)]

        if not add:
            deprecation_warning_add(sys._getframe().f_code.co_name)
            return self.__definePositions(gate)

        else:
            return self.add(gate) # add to circuit

        # DEPRECATED add: when add is deprecated REPLACE THE CODE ABOVE WITH THE FOLLOWING
        # # CHECK INPUTS
        # if position or isinstance(position, list):
        #     checkInputTypes(
        #         ('position', position, (int, list))
        #     )
        #     if isinstance(position, list):
        #         checkListTypes(('position', position, (int,)))
        #         checkDifferentPosition(position)

        # if isinstance(position, int):
        #     gate = I_TXGate(position)
        
        # elif isinstance(position, list):
        #     gate = [I_TXGate(p) for p in position]
        
        # elif position == None:
        #     gate = [I_TXGate(p) for p in range(0, self.__numerOfQubits)]

        # return self.add(gate) # add to circuit

    def ty(self, position = None, add: bool = True) -> TYGate: # four root of y, ty gate
        """
        Add four root of Y, TY gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. It can also be a list of positions.
        add : bool
            [DEPRECATED] "add" argument is deprecated and will be removed in future versions. For more information visit the user guide.
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        TYGate obj | TYGate obj list | tuple list [DEPRECATED]
        """
        # CHECK INPUTS
        if position or isinstance(position, list):
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                checkListTypes(('position', position, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('add', add, (bool,))
        )

        if isinstance(position, int):
            gate = TYGate(position)
        
        elif isinstance(position, list):
            gate = [TYGate(p) for p in position]
        
        elif position == None:
            gate = [TYGate(p) for p in range(0, self.__numerOfQubits)]

        if not add:
            deprecation_warning_add(sys._getframe().f_code.co_name)
            return self.__definePositions(gate)

        else:
            return self.add(gate) # add to circuit

        # DEPRECATED add: when add is deprecated REPLACE THE CODE ABOVE WITH THE FOLLOWING
        # # CHECK INPUTS
        # if position or isinstance(position, list):
        #     checkInputTypes(
        #         ('position', position, (int, list))
        #     )
        #     if isinstance(position, list):
        #         checkListTypes(('position', position, (int,)))
        #         checkDifferentPosition(position)

        # if isinstance(position, int):
        #     gate = TYGate(position)
        
        # elif isinstance(position, list):
        #     gate = [TYGate(p) for p in position]
        
        # elif position == None:
        #     gate = [TYGate(p) for p in range(0, self.__numerOfQubits)]

        # return self.add(gate) # add to circuit

    def i_ty(self, position = None, add: bool = True) -> I_TYGate: # adjoint four root y, i_ty gate
        """
        Add adjoint four root Y, I_TY gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. It can also be a list of positions.
        add : bool
            [DEPRECATED] "add" argument is deprecated and will be removed in future versions. For more information visit the user guide.
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        I_TYGate obj | I_TYGate obj list | tuple list [DEPRECATED]
        """
        # CHECK INPUTS
        if position or isinstance(position, list):
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                checkListTypes(('position', position, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('add', add, (bool,))
        )

        if isinstance(position, int):
            gate = I_TYGate(position)
        
        elif isinstance(position, list):
            gate = [I_TYGate(p) for p in position]
        
        elif position == None:
            gate = [I_TYGate(p) for p in range(0, self.__numerOfQubits)]

        if not add:
            deprecation_warning_add(sys._getframe().f_code.co_name)
            return self.__definePositions(gate)

        else:
            return self.add(gate) # add to circuit

        # DEPRECATED add: when add is deprecated REPLACE THE CODE ABOVE WITH THE FOLLOWING
        # # CHECK INPUTS
        # if position or isinstance(position, list):
        #     checkInputTypes(
        #         ('position', position, (int, list))
        #     )
        #     if isinstance(position, list):
        #         checkListTypes(('position', position, (int,)))
        #         checkDifferentPosition(position)

        # if isinstance(position, int):
        #     gate = I_TYGate(position)
        
        # elif isinstance(position, list):
        #     gate = [I_TYGate(p) for p in position]
        
        # elif position == None:
        #     gate = [I_TYGate(p) for p in range(0, self.__numerOfQubits)]

        # return self.add(gate) # add to circuit


    # ROTATION GATES
    def p(self, position = None, argument = 'pi', add: bool = True) -> PGate: # phase gate
        """
        Add Phase gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. It can also be a list of positions.
        argument: str | int | float
            Optional argument. Gate angle value. In the case that it is not indicated, it will be pi by default.
        add : bool
            [DEPRECATED] "add" argument is deprecated and will be removed in future versions. For more information visit the user guide.
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        PGate obj | PGate obj list | tuple list [DEPRECATED]
        """
        # CHECK INPUTS
        if position or isinstance(position, list):
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                checkListTypes(('position', position, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('argument', argument, (str, int, float)),
            ('add', add, (bool,))
        )
        if isinstance(argument, str):
            checkMathExpression('argument', argument)

        if isinstance(position, int):
            gate = PGate(position, argument)
        
        elif isinstance(position, list):
            gate = [PGate(p, argument) for p in position]
        
        elif position == None:
            gate = [PGate(p, argument) for p in range(0, self.__numerOfQubits)]

        if not add:
            deprecation_warning_add(sys._getframe().f_code.co_name)
            return self.__definePositions(gate)

        else:
            return self.add(gate) # add to circuit

        # DEPRECATED add: when add is deprecated REPLACE THE CODE ABOVE WITH THE FOLLOWING
        # # CHECK INPUTS
        # if position or isinstance(position, list):
        #     checkInputTypes(
        #         ('position', position, (int, list))
        #     )
        #     if isinstance(position, list):
        #         checkListTypes(('position', position, (int,)))
        #         checkDifferentPosition(position)
        # checkInputTypes(
        #     ('argument', argument, (str, int, float))
        # )
        # if isinstance(argument, str):
        #     checkMathExpression('argument', argument)

        # if isinstance(position, int):
        #     gate = PGate(position, argument)
        
        # elif isinstance(position, list):
        #     gate = [PGate(p, argument) for p in position]
        
        # elif position == None:
        #     gate = [PGate(p, argument) for p in range(0, self.__numerOfQubits)]

        # return self.add(gate) # add to circuit

    def rx(self, position = None, argument = 'pi', add: bool = True) -> RXGate: # rotation x gate
        """
        Add Rotation X gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. It can also be a list of positions.
        argument: str | int | float
            Optional argument. Gate angle value. In the case that it is not indicated, it will be pi by default.
        add : bool
            [DEPRECATED] "add" argument is deprecated and will be removed in future versions. For more information visit the user guide.
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        RXGate obj | RXGate obj list | tuple list [DEPRECATED]
        """
        # CHECK INPUTS
        if position or isinstance(position, list):
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                checkListTypes(('position', position, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('argument', argument, (str, int, float)),
            ('add', add, (bool,))
        )
        if isinstance(argument, str):
            checkMathExpression('argument', argument)

        if isinstance(position, int):
            gate = RXGate(position, argument)
        
        elif isinstance(position, list):
            gate = [RXGate(p, argument) for p in position]
        
        elif position == None:
            gate = [RXGate(p, argument) for p in range(0, self.__numerOfQubits)]

        if not add:
            deprecation_warning_add(sys._getframe().f_code.co_name)
            return self.__definePositions(gate)

        else:
            return self.add(gate) # add to circuit

        # DEPRECATED add: when add is deprecated REPLACE THE CODE ABOVE WITH THE FOLLOWING
        # # CHECK INPUTS
        # if position or isinstance(position, list):
        #     checkInputTypes(
        #         ('position', position, (int, list))
        #     )
        #     if isinstance(position, list):
        #         checkListTypes(('position', position, (int,)))
        #         checkDifferentPosition(position)
        # checkInputTypes(
        #     ('argument', argument, (str, int, float))
        # )
        # if isinstance(argument, str):
        #     checkMathExpression('argument', argument)

        # if isinstance(position, int):
        #     gate = RXGate(position, argument)
        
        # elif isinstance(position, list):
        #     gate = [RXGate(p, argument) for p in position]
        
        # elif position == None:
        #     gate = [RXGate(p, argument) for p in range(0, self.__numerOfQubits)]

        # return self.add(gate) # add to circuit

    def ry(self, position = None, argument = 'pi', add: bool = True) -> RYGate: # rotation y gate
        """
        Add Rotation Y gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. It can also be a list of positions.
        argument: str | int | float
            Optional argument. Gate angle value. In the case that it is not indicated, it will be pi by default.
        add : bool
            [DEPRECATED] "add" argument is deprecated and will be removed in future versions. For more information visit the user guide.
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        RYGate obj | RYGate obj list | tuple list [DEPRECATED]
        """
        # CHECK INPUTS
        if position or isinstance(position, list):
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                checkListTypes(('position', position, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('argument', argument, (str, int, float)),
            ('add', add, (bool,))
        )
        if isinstance(argument, str):
            checkMathExpression('argument', argument)

        if isinstance(position, int):
            gate = RYGate(position, argument)
        
        elif isinstance(position, list):
            gate = [RYGate(p, argument) for p in position]
        
        elif position == None:
            gate = [RYGate(p, argument) for p in range(0, self.__numerOfQubits)]

        if not add:
            deprecation_warning_add(sys._getframe().f_code.co_name)
            return self.__definePositions(gate)

        else:
            return self.add(gate) # add to circuit

        # DEPRECATED add: when add is deprecated REPLACE THE CODE ABOVE WITH THE FOLLOWING
        # # CHECK INPUTS
        # if position or isinstance(position, list):
        #     checkInputTypes(
        #         ('position', position, (int, list))
        #     )
        #     if isinstance(position, list):
        #         checkListTypes(('position', position, (int,)))
        #         checkDifferentPosition(position)
        # checkInputTypes(
        #     ('argument', argument, (str, int, float))
        # )
        # if isinstance(argument, str):
        #     checkMathExpression('argument', argument)

        # if isinstance(position, int):
        #     gate = RYGate(position, argument)
        
        # elif isinstance(position, list):
        #     gate = [RYGate(p, argument) for p in position]
        
        # elif position == None:
        #     gate = [RYGate(p, argument) for p in range(0, self.__numerOfQubits)]

        # return self.add(gate) # add to circuit

    def rz(self, position = None, argument = 'pi', add: bool = True) -> RZGate: # rotation z gate
        """
        Add Rotation Z gate.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the gate. If no position are indicated, gate will be added in all qubits. It can also be a list of positions.
        argument: str | int | float
            Optional argument. Gate angle value. In the case that it is not indicated, it will be pi by default.
        add : bool
            [DEPRECATED] "add" argument is deprecated and will be removed in future versions. For more information visit the user guide.
            Optional argument. True by default. Indicates whether the gate should be added to the circuit or not. In the case of wanting to add it, it is not necessary to introduce that argument. If you want to create a new gate, you must enter False.
        
        Output
        ----------
        RZGate obj | RZGate obj list | tuple list [DEPRECATED]
        """
        # CHECK INPUTS
        if position or isinstance(position, list):
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                checkListTypes(('position', position, (int,)))
                checkDifferentPosition(position)
        checkInputTypes(
            ('argument', argument, (str, int, float)),
            ('add', add, (bool,))
        )
        if isinstance(argument, str):
            checkMathExpression('argument', argument)

        if isinstance(position, int):
            gate = RZGate(position, argument)
        
        elif isinstance(position, list):
            gate = [RZGate(p, argument) for p in position]
        
        elif position == None:
            gate = [RZGate(p, argument) for p in range(0, self.__numerOfQubits)]

        if not add:
            deprecation_warning_add(sys._getframe().f_code.co_name)
            return self.__definePositions(gate)

        else:
            return self.add(gate) # add to circuit

        # DEPRECATED add: when add is deprecated REPLACE THE CODE ABOVE WITH THE FOLLOWING
        # # CHECK INPUTS
        # if position or isinstance(position, list):
        #     checkInputTypes(
        #         ('position', position, (int, list))
        #     )
        #     if isinstance(position, list):
        #         checkListTypes(('position', position, (int,)))
        #         checkDifferentPosition(position)
        # checkInputTypes(
        #     ('argument', argument, (str, int, float))
        # )
        # if isinstance(argument, str):
        #     checkMathExpression('argument', argument)

        # if isinstance(position, int):
        #     gate = RZGate(position, argument)
        
        # elif isinstance(position, list):
        #     gate = [RZGate(p, argument) for p in position]
        
        # elif position == None:
        #     gate = [RZGate(p, argument) for p in range(0, self.__numerOfQubits)]

        # return self.add(gate) # add to circuit


    # UTILITIES
    def barrier(self, position = None) -> Barrier: # barrier
        """
        Add Barrier.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Optional argument. Qubit position to add the barrier. In the case that the position is not indicated, the barrier will be added in all qubits. It can also be a list of positions.
        
        Output
        ----------
        Barrier obj | Barrier obj list
        """
        # CHECK INPUTS
        if position or isinstance(position, list):
            checkInputTypes(
                ('position', position, (int, list))
            )
            if isinstance(position, list):
                checkListTypes(('position', position, (int,)))
                checkDifferentPosition(position)

        if isinstance(position, int):
            gate = Barrier(position)
        
        elif isinstance(position, list):
            gate = [Barrier(p) for p in position]
        
        elif position == None:
            gate = [Barrier(p) for p in range(0, self.__numerOfQubits)]

        return self.add(gate) # add to circuit

    def beginRepeat(self, position, repetitions: int) -> BeginRepeat: # begin repeat
        """
        Add Begin Repeat.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Qubit position to add the begin repetition. It can also be a list of positions.
        repetitions: int
            Number of repetitions.
        
        Output
        ----------
        BeginRepeat obj | BeginRepeat obj list
        """
        # CHECK INPUTS
        checkInputTypes(
            ('position', position, (int, list))
        )
        if isinstance(position, list):
            checkListTypes(('position', position, (int,)))
            checkDifferentPosition(position)
        checkInputTypes(
            ('repetitions', repetitions, (int,))
        )

        if isinstance(position, int):
            gate = BeginRepeat(position, repetitions)
        
        elif isinstance(position, list):
            gate = [BeginRepeat(p, repetitions) for p in position]
        
        elif position == None:
            gate = [BeginRepeat(p, repetitions) for p in range(0, self.__numerOfQubits)]

        return self.add(gate) # add to circuit

    def endRepeat(self, position) -> EndRepeat: # begin repeat
        """
        Add End Repeat.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        position : int | list
            Qubit position to add the end repetition. It can also be a list of positions.
        
        Output
        ----------
        EndRepeat obj | EndRepeat obj list
        """
        # CHECK INPUTS
        checkInputTypes(
            ('position', position, (int, list))
        )
        if isinstance(position, list):
            checkListTypes(('position', position, (int,)))
            checkDifferentPosition(position)

        if isinstance(position, int):
            gate = EndRepeat(position)
        
        elif isinstance(position, list):
            gate = [EndRepeat(p) for p in position]
        
        elif position == None:
            gate = [EndRepeat(p) for p in range(0, self.__numerOfQubits)]

        return self.add(gate) # add to circuit

    def add(self, gate): # add gate
        """
        Add gate or list of gates to circuit.

        Prerequisites
        ----------
        - Created circuit.

        Parameters
        ----------
        gate : gate obj | gate obj list
            Gate object or list of gates to add to the circuit.
        
        Output
        ----------
        gate obj | gate obj list
        """
        # CHECK INPUTS
        checkInputTypes(
            ('gate', gate, (SingleGate, ArgumentGate, MultipleGate, ControlledGate, list))
        )
        if isinstance(gate, list):
            checkListTypes(('gate', gate, (SingleGate, ArgumentGate, MultipleGate, ControlledGate)))

        addInNewColumn = False
        if isinstance(gate, list):
            if all(type(g) == type(gate[0]) for g in gate): # all gates are the same type
                addInNewColumn = True
        elif isinstance(gate, (MultipleGate, ControlledGate)):
            addInNewColumn = True

        if addInNewColumn:
            self.__addGateInNewColumn(gate)
        
        else:
            self.__addGateInExistingColumn(gate)
        
        self.__updateQubits()
        
        return gate
    
        # CHECK INPUTS
        # checkInputTypes(
        #     ('gate', gate, (HGate, XGate, YGate, ZGate, SwapGate)) añadir los que faltan
        # )
        
        # positions = gate.getPositions() if gate.getPositions() != None else list(range(self.getNumberOfQubits())) # getPositions or a list of all qubit positions

        # if gate.getType() == 'SINGLE_GATE': # add one gate by one
        #     for position in positions:
        #         self.__addSingleGateVL(gate.getSymbol(), position)
        
        # elif gate.getType() == 'MULTIPLE_GATE':
        #     self.__addMultipleGateVL(gate)

        # self.__updateQubits()

        # return gate


        # CHECK INPUTS
        # checkInputTypes(
        #     ('gate', gate, (HGate, XGate, YGate, ZGate, SwapGate)) añadir los que faltan
        # )

        # positions = gate.getPositions() if gate.getPositions() != None else list(range(self.getNumberOfQubits())) # getPositions or a list of all qubit positions
        
        # if gate.getType() == 'SINGLE_GATE': # add one gate by one
        #     for position in positions:
        #         self.__addSingleGateVL(gate.getSymbol(), position)
        
        # elif gate.getType() == 'MULTIPLE_GATE': # add all gates at once
        #     self.__addMultipleGateVL(gate)

        # self.__updateQubits()

        # return gate

    # DEPRECATED addCreatedGate: when addCreatedGate is deprecated REMOVE FROM HERE
    def addCreatedGate(self, gate: list): # add created gate
        """
        Add Created gate.

        Prerequisites
        ----------
        - Created circuit.
        - Created gate.

        Parameters
        ----------
        gate : list
            Created gate to add to the circuit.
        """
        # CHECK INPUTS
        checkInputTypes(
            ('gate', gate, (list,))
        )

        self.__addMultipleGate(gate, self.__circuitBody) # add to circuit

        self.__updateQubits()
    # TO HERE