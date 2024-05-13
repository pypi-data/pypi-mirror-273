from ...utils.checker import checkInputTypes
from .gates import (SingleGate as __SingleGate)

# MEASURE GATES:
#   MeasureGate

# MEASURE GATE
class MeasureGate(__SingleGate):

    # CONSTRUCTOR
    def __init__(self, position: int):
        """
        Create Measure Gate obj.

        Prerequisites
        ----------
        - None.

        Parameters
        ----------
        position : int
            Qubit position to add the measure.

        Output
        ----------
        MeasureGate obj
        """
        # CHECK INPUTS
        checkInputTypes(
            ('position', position, (int,))
        )

        super().__init__('Measure', False, position)