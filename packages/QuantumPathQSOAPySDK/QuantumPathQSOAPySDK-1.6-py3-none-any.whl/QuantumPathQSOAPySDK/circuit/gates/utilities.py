from ...utils.checker import checkInputTypes
from .gates import (
    SingleGate as __SingleGate,
    ArgumentGate as __ArgumentGate
)

# UTILITIES:
#   Barrier
#   BeginRepeat
#   EndRepeat

# BARRIER
class Barrier(__SingleGate):

    # CONSTRUCTOR
    def __init__(self, position: int):
        """
        Create Barrier obj.

        Prerequisites
        ----------
        - None.

        Parameters
        ----------
        position : int
            Qubit position to add the gate.

        Output
        ----------
        Barrier obj
        """
        # CHECK INPUTS
        checkInputTypes(
            ('position', position, (int,))
        )

        super().__init__('SPACER', False, position)


# BEGIN REPEAT
class BeginRepeat(__ArgumentGate):

    # CONSTRUCTOR
    def __init__(self, position: int, repetitions: int):
        """
        Create Begin Repeat obj.

        Prerequisites
        ----------
        - None.

        Parameters
        ----------
        position : int
            Qubit position to add the begin repetition.
        repetitions: int
            Number of repetitions.
            
        Output
        ----------
        BeginRepeat obj
        """
        # CHECK INPUTS
        checkInputTypes(
            ('position', position, (int,)),
            ('repetitions', repetitions, (int,))
        )

        super().__init__('BEGIN_R', False, position, repetitions)


# END REPEAT
class EndRepeat(__SingleGate):

    # CONSTRUCTOR
    def __init__(self, position: int):
        """
        Create Barrier obj.

        Prerequisites
        ----------
        - None.

        Parameters
        ----------
        position : int
            Qubit position to add the end repetition.
        
        Output
        ----------
        EndRepeat obj
        """
        # CHECK INPUTS
        checkInputTypes(
            ('position', position, (int,))
        )

        super().__init__('END_R', False, position)