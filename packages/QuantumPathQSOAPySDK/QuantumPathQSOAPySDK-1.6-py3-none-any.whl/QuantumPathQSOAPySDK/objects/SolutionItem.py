class SolutionItem:

    # CONSTRUCTOR
    def __init__(self, solution: dict):
        self.__id = solution['SolutionID']
        self.__name = solution['SolutionName']
        self.__quantumType = solution['QuantumType']
    
    
    # GETTERS
    def getId(self) -> int:
        return self.__id

    def getName(self) -> str:
        return self.__name
    
    def getQuantumType(self) -> str:
        return self.__quantumType