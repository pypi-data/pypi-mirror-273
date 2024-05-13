# QUANTUM GATES:
    # SINGLE GATE
    # ARGUMENT GATE
    # MULTIPLE GATE
    # CONTROLLED GATE

# QUANTUM GATE
class __QuantumGate:

    # CONSTRUCTOR
    def __init__(self, symbol, controllable: bool):
        """
        Create QuantumGate.
        """
        self.__symbol = symbol
        self.__controllable = controllable


    # GETTERS
    def getSymbol(self) -> str:
        """
        Get gate symbol.

        Prerequisites
        ----------
        - None.

        Output
        ----------
        str | dict
        """

        return self.__symbol

    def getControllable(self) -> bool:
        """
        Get if gate is controllable.

        Prerequisites
        ----------
        - None.

        Output
        ----------
        bool
        """

        return self.__controllable
    

# SINGLE GATE
class SingleGate(__QuantumGate):

    # CONSTRUCTOR
    def __init__(self, symbol: str, controllable: bool, position: int):
        """
        Create SingleGate.
        """
        super().__init__(symbol, controllable)
        self.__position = position


    # GETTERS
    def getPosition(self) -> int:
        """
        Get gate position.

        Prerequisites
        ----------
        - None.

        Output
        ----------
        int
        """

        return self.__position


# ARGUMENT GATE
class ArgumentGate(SingleGate):

    # CONSTRUCTOR
    def __init__(self, symbol: str, controllable: bool, position: int, argument):
        """
        Create SingleGate.
        """
        symbol = {'id': symbol, 'arg': str(argument)}

        super().__init__(symbol, controllable, position)
        self.__argument = argument


    # GETTERS
    def getArgument(self):
        """
        Get gate argument.

        Prerequisites
        ----------
        - None.

        Output
        ----------
        str | int | float
        """

        return self.__argument


# MULTIPLE GATE
class MultipleGate(__QuantumGate):

    # CONSTRUCTOR
    def __init__(self, symbol: str, controllable: bool, positions: int):
        """
        Create SingleGate.
        """
        super().__init__(symbol, controllable)
        self.__positions = sorted(positions)


    # GETTERS
    def getPositions(self) -> list:
        """
        Get gate positions.

        Prerequisites
        ----------
        - None.

        Output
        ----------
        list
        """

        return self.__positions


# CONTROLLED GATE
class ControlledGate(__QuantumGate):

    # CONSTRUCTOR
    def __init__(self, symbol: str, controllable: bool, controlPositions: list, targetPosition: int):
        """
        Create ControlledGate.
        """
        super().__init__(symbol, controllable)
        self.__controlSymbol = 'CTRL'
        self.__controlPositions = sorted(controlPositions)
        self.__targetPosition = targetPosition


    # GETTERS
    def getControlSymbol(self) -> str:
        """
        Get control symbol.

        Prerequisites
        ----------
        - None.

        Output
        ----------
        str
        """

        return self.__controlSymbol

    def getControlPositions(self) -> list:
        """
        Get control positions.

        Prerequisites
        ----------
        - None.

        Output
        ----------
        list
        """

        return self.__controlPositions
    
    def getTargetPosition(self) -> int:
        """
        Get target position or positions.

        Prerequisites
        ----------
        - None.

        Output
        ----------
        int | list
        """

        return self.__targetPosition