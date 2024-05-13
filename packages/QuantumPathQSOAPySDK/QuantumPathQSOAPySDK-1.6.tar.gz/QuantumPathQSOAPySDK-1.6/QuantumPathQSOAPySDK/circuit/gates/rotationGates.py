from ...utils.checker import (checkInputTypes, checkMathExpression)
from .gates import ArgumentGate as __ArgumentGate

# ROTATION GATES:
#   PGate
#   RXGate
#   RYGate
#   RZGate

# PHASE GATE
class PGate(__ArgumentGate):

    # CONSTRUCTOR
    def __init__(self, position: int, argument = 'pi'):
        """
        Create Phase Gate obj.

        Prerequisites
        ----------
        - None.

        Parameters
        ----------
        position : int
            Mandatory argument. Qubit position to add the gate.
        argument: str | int | float
            Optional argument. Gate angle value. In the case that it is not indicated, it will be pi by default.
            
        Output
        ----------
        PGate obj
        """
        # CHECK INPUTS
        checkInputTypes(
            ('position', position, (int,)),
            ('argument', argument, (str, int, float))
        )
        if isinstance(argument, str):
            checkMathExpression('argument', argument)

        super().__init__('P', True, position, argument)


# ROTATION X GATE
class RXGate(__ArgumentGate):

    # CONSTRUCTOR
    def __init__(self, position: int, argument = 'pi'):
        """
        Create Rotation X Gate obj.

        Prerequisites
        ----------
        - None.

        Parameters
        ----------
        position : int
            Mandatory argument. Qubit position to add the gate.
        argument: str | int | float
            Optional argument. Gate angle value. In the case that it is not indicated, it will be pi by default.
            
        Output
        ----------
        RXGate obj
        """
       # CHECK INPUTS
        checkInputTypes(
            ('position', position, (int,)),
            ('argument', argument, (str, int, float))
        )
        if isinstance(argument, str):
            checkMathExpression('argument', argument)

        super().__init__('RX', True, position, argument)


# ROTATION Y GATE
class RYGate(__ArgumentGate):

    # CONSTRUCTOR
    def __init__(self, position: int, argument = 'pi'):
        """
        Create Rotation Y Gate obj.

        Prerequisites
        ----------
        - None.

        Parameters
        ----------
        position : int
            Mandatory argument. Qubit position to add the gate.
        argument: str | int | float
            Optional argument. Gate angle value. In the case that it is not indicated, it will be pi by default.
            
        Output
        ----------
        RYGate obj
        """
       # CHECK INPUTS
        checkInputTypes(
            ('position', position, (int,)),
            ('argument', argument, (str, int, float))
        )
        if isinstance(argument, str):
            checkMathExpression('argument', argument)

        super().__init__('RY', True, position, argument)


# ROTATION Z GATE
class RZGate(__ArgumentGate):

    # CONSTRUCTOR
    def __init__(self, position: int, argument = 'pi'):
        """
        Create Rotation Z Gate obj.

        Prerequisites
        ----------
        - None.

        Parameters
        ----------
        position : int
            Mandatory argument. Qubit position to add the gate.
        argument: str | int | float
            Optional argument. Gate angle value. In the case that it is not indicated, it will be pi by default.
            
        Output
        ----------
        RZGate obj
        """
       # CHECK INPUTS
        checkInputTypes(
            ('position', position, (int,)),
            ('argument', argument, (str, int, float))
        )
        if isinstance(argument, str):
            checkMathExpression('argument', argument)

        super().__init__('RZ', True, position, argument)