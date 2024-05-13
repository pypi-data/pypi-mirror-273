from ...utils.checker import checkInputTypes
from .gates import (
    SingleGate as __SingleGate,
    MultipleGate as __MultipleGate,
    ControlledGate as __ControlledGate
)

# BASIC GATES:
#   HGate
#   XGate
#   YGate
#   ZGate
#   SwapGate
#   CHGate
#   CXGate
#   CCXGate

# HADAMARD GATE
class HGate(__SingleGate):

    # CONSTRUCTOR
    def __init__(self, position: int):
        """
        Create Hadamard Gate obj.

        Prerequisites
        ----------
        - None.

        Parameters
        ----------
        position : int
           Qubit position to add the gate.

        Output
        ----------
        HGate obj
        """
        # CHECK INPUTS
        checkInputTypes(
            ('position', position, (int,))
        )

        super().__init__('H', True, position)


# NOT GATE
class XGate(__SingleGate):

    # CONSTRUCTOR
    def __init__(self, position: int):
        """
        Create Not Gate obj.

        Prerequisites
        ----------
        - None.

        Parameters
        ----------
        position : int
            Qubit position to add the gate.

        Output
        ----------
        XGate obj
        """
        # CHECK INPUTS
        checkInputTypes(
            ('position', position, (int,))
        )

        super().__init__('X', True, position)


# PAULI Y GATE
class YGate(__SingleGate):

    # CONSTRUCTOR
    def __init__(self, position: int):
        """
        Create Pauli Y Gate obj.

        Prerequisites
        ----------
        - None.

        Parameters
        ----------
        position : int
            Qubit position to add the gate.

        Output
        ----------
        YGate obj
        """
        # CHECK INPUTS
        checkInputTypes(
            ('position', position, (int,))
        )

        super().__init__('Y', True, position)


# PAULI Z GATE
class ZGate(__SingleGate):

    # CONSTRUCTOR
    def __init__(self, position: int):
        """
        Create Pauli Z Gate obj.

        Prerequisites
        ----------
        - None.

        Parameters
        ----------
        position : int
            Qubit position to add the gate.

        Output
        ----------
        ZGate obj
        """
        # CHECK INPUTS
        checkInputTypes(
            ('position', position, (int,))
        )

        super().__init__('Z', True, position)


# SWAP GATE
class SwapGate(__MultipleGate):

    # CONSTRUCTOR
    def __init__(self, position1: int, position2: int):
        """
        Create Swap Gate obj.

        Prerequisites
        ----------
        - None.

        Parameters
        ----------
        position1 : int
            First qubit position to add the swap.
        position2 : int
            Second qubit position to add the swap.

        Output
        ----------
        SwapGate obj
        """
        # CHECK INPUTS
        checkInputTypes(
            ('position1', position1, (int,)),
            ('position2', position2, (int,))
        )

        super().__init__('Swap', True, [position1, position2])


# CONTROLLED HADAMARD GATE
class CHGate(__ControlledGate):

    # CONSTRUCTOR
    def __init__(self, position1: int, position2: int):
        """
        Create Controlled Hadamard Gate obj.

        Prerequisites
        ----------
        - None.

        Parameters
        ----------
        position1 : int
            First qubit position to add the control.
        position2 : int
            Second qubit position to add the hadamard gate.

        Output
        ----------
        CHGate obj
        """
        # CHECK INPUTS
        checkInputTypes(
            ('position1', position1, (int,)),
            ('position2', position2, (int,))
        )

        super().__init__('H', True, [position1], position2)


# CONTROLLED X GATE
class CXGate(__ControlledGate):

    # CONSTRUCTOR
    def __init__(self, position1: int, position2: int):
        """
        Create Controlled X Gate obj.

        Prerequisites
        ----------
        - None.

        Parameters
        ----------
        position1 : int
            First qubit position to add the control.
        position2 : int
            Second qubit position to add the X gate.

        Output
        ----------
        CXGate obj
        """
        # CHECK INPUTS
        checkInputTypes(
            ('position1', position1, (int,)),
            ('position2', position2, (int,))
        )

        super().__init__('X', True, [position1], position2)


# TOFFOLI GATE
class CCXGate(__ControlledGate):

    # CONSTRUCTOR
    def __init__(self, position1: int, position2: int, position3: int):
        """
        Create Toffoli Gate obj.

        Prerequisites
        ----------
        - None.

        Parameters
        ----------
        position1 : int
            First qubit position to add the control.
        position2 : int
            Second qubit position to add the control.
        position3 : int
            Third qubit position to add the X gate.

        Output
        ----------
        CCXGate obj
        """
        # CHECK INPUTS
        checkInputTypes(
            ('position1', position1, (int,)),
            ('position2', position2, (int,)),
            ('position3', position2, (int,))
        )

        super().__init__('X', True, [position1, position2], position3)