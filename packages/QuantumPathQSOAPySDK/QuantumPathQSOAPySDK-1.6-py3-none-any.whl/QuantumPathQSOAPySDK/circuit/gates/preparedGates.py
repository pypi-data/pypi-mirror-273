from ...utils.checker import checkInputTypes
from .gates import (
    SingleGate as __SingleGate
)

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

# SQUARE ROOT OF Z, S GATE
class SGate(__SingleGate):

    # CONSTRUCTOR
    def __init__(self, position: int):
        """
        Create square root of Z, S Gate obj.

        Prerequisites
        ----------
        - None.

        Parameters
        ----------
        position : int
           Qubit position to add the gate.

        Output
        ----------
        SGate obj
        """
        # CHECK INPUTS
        checkInputTypes(
            ('position', position, (int,))
        )

        super().__init__('S', True, position)


# ADJOINT SQUARE ROOT Z, I_S GATE
class I_SGate(__SingleGate):

    # CONSTRUCTOR
    def __init__(self, position: int):
        """
        Create adjoint square root Z, I_S Gate obj.

        Prerequisites
        ----------
        - None.

        Parameters
        ----------
        position : int
           Qubit position to add the gate.

        Output
        ----------
        I_SGate obj
        """
        # CHECK INPUTS
        checkInputTypes(
            ('position', position, (int,))
        )

        super().__init__('I_S', True, position)


# SQUARE ROOT OF X, SX GATE
class SXGate(__SingleGate):

    # CONSTRUCTOR
    def __init__(self, position: int):
        """
        Create square root of X, SX Gate obj.

        Prerequisites
        ----------
        - None.

        Parameters
        ----------
        position : int
           Qubit position to add the gate.

        Output
        ----------
        SXGate obj
        """
        # CHECK INPUTS
        checkInputTypes(
            ('position', position, (int,))
        )

        super().__init__('SX', True, position)


# ADJOINT SQUARE ROOT Z, I_SX GATE
class I_SXGate(__SingleGate):

    # CONSTRUCTOR
    def __init__(self, position: int):
        """
        Create adjoint square root X, I_SX Gate obj.

        Prerequisites
        ----------
        - None.

        Parameters
        ----------
        position : int
           Qubit position to add the gate.

        Output
        ----------
        I_SXGate obj
        """
        # CHECK INPUTS
        checkInputTypes(
            ('position', position, (int,))
        )

        super().__init__('I_SX', True, position)


# SQUARE ROOT OF Y, SY GATE
class SYGate(__SingleGate):

    # CONSTRUCTOR
    def __init__(self, position: int):
        """
        Create square root of Y, SY Gate obj.

        Prerequisites
        ----------
        - None.

        Parameters
        ----------
        position : int
           Qubit position to add the gate.

        Output
        ----------
        SYGate obj
        """
        # CHECK INPUTS
        checkInputTypes(
            ('position', position, (int,))
        )

        super().__init__('SY', True, position)


# ADJOINT SQUARE ROOT Y, I_SY GATE
class I_SYGate(__SingleGate):

    # CONSTRUCTOR
    def __init__(self, position: int):
        """
        Create adjoint square root Y, I_SY Gate obj.

        Prerequisites
        ----------
        - None.

        Parameters
        ----------
        position : int
           Qubit position to add the gate.

        Output
        ----------
        I_SYGate obj
        """
        # CHECK INPUTS
        checkInputTypes(
            ('position', position, (int,))
        )

        super().__init__('I_SY', True, position)


# FOUR ROOT OF Z, T GATE
class TGate(__SingleGate):

    # CONSTRUCTOR
    def __init__(self, position: int):
        """
        Create four root of Z, T Gate obj.

        Prerequisites
        ----------
        - None.

        Parameters
        ----------
        position : int
           Qubit position to add the gate.

        Output
        ----------
        TGate obj
        """
        # CHECK INPUTS
        checkInputTypes(
            ('position', position, (int,))
        )

        super().__init__('T', True, position)


# ADJOINT FOUR ROOT Z, I_T GATE
class I_TGate(__SingleGate):

    # CONSTRUCTOR
    def __init__(self, position: int):
        """
        Create adjoint four root Z, I_T Gate obj.

        Prerequisites
        ----------
        - None.

        Parameters
        ----------
        position : int
           Qubit position to add the gate.

        Output
        ----------
        I_TGate obj
        """
        # CHECK INPUTS
        checkInputTypes(
            ('position', position, (int,))
        )

        super().__init__('I_T', True, position)


# FOUR ROOT OF X, TX GATE
class TXGate(__SingleGate):

    # CONSTRUCTOR
    def __init__(self, position: int):
        """
        Create four root of X, TX Gate obj.

        Prerequisites
        ----------
        - None.

        Parameters
        ----------
        position : int
           Qubit position to add the gate.

        Output
        ----------
        TXGate obj
        """
        # CHECK INPUTS
        checkInputTypes(
            ('position', position, (int,))
        )

        super().__init__('TX', True, position)


# ADJOINT FOUR ROOT X, I_TX GATE
class I_TXGate(__SingleGate):

    # CONSTRUCTOR
    def __init__(self, position: int):
        """
        Create adjoint four root X, I_TX Gate obj.

        Prerequisites
        ----------
        - None.

        Parameters
        ----------
        position : int
           Qubit position to add the gate.

        Output
        ----------
        I_TXGate obj
        """
        # CHECK INPUTS
        checkInputTypes(
            ('position', position, (int,))
        )

        super().__init__('I_TX', True, position)


# FOUR ROOT OF Y, TY GATE
class TYGate(__SingleGate):

    # CONSTRUCTOR
    def __init__(self, position: int):
        """
        Create four root of Y, TY Gate obj.

        Prerequisites
        ----------
        - None.

        Parameters
        ----------
        position : int
           Qubit position to add the gate.

        Output
        ----------
        TYGate obj
        """
        # CHECK INPUTS
        checkInputTypes(
            ('position', position, (int,))
        )

        super().__init__('TY', True, position)


# ADJOINT FLOUR ROOT Y, I_TY GATE
class I_TYGate(__SingleGate):

    # CONSTRUCTOR
    def __init__(self, position: int):
        """
        Create adjoint four root Y, I_TY Gate obj.

        Prerequisites
        ----------
        - None.

        Parameters
        ----------
        position : int
           Qubit position to add the gate.

        Output
        ----------
        I_TYGate obj
        """
        # CHECK INPUTS
        checkInputTypes(
            ('position', position, (int,))
        )

        super().__init__('I_TY', True, position)