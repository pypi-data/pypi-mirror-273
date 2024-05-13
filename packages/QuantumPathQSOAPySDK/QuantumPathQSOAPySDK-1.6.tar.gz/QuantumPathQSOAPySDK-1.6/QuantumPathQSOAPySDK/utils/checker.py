from ..utils.apiConnection import apiConnection
from .Exception import AuthenticationError

import math

def getURL(context) -> tuple:
    if context.getActiveEnvironment()[0] == 'default-environments':
        url = (context.getEnvironments()[context.getActiveEnvironment()[0]][context.getActiveEnvironment()[1]], True)

    elif context.getActiveEnvironment()[0] == 'custom-environments':
        url = context.getEnvironments()[context.getActiveEnvironment()[0]][context.getActiveEnvironment()[1]]

    return url

def depth(inputList):
    if isinstance(inputList, list):
        return 1 + max(depth(item) for item in inputList)
    else:
        return 0

def checkUserSession(context):
    urlData = getURL(context)
    url = urlData[0] + 'login/echostatus'
    validate = urlData[1]

    if not apiConnection(url, context.getHeader(), 'boolean', validate=validate):
        raise AuthenticationError('User not authenticated')

def checkInputTypes(*args):
    for arg in args:
        name = arg[0]
        variable = arg[1]
        types = arg[2]

        expectedTypes = str([i.__name__ for i in types]).replace("['", "<").replace(" '", " <").replace("']", ">").replace("',", ">,")

        if bool in types and isinstance(variable, bool):
            return
        else:
            if isinstance(variable, bool):
                raise TypeError(f'Argument "{name}" expected to be {expectedTypes}, not <{type(variable).__name__}>')

        if not isinstance(variable, types):
            raise TypeError(f'Argument "{name}" expected to be {expectedTypes}, not <{type(variable).__name__}>')

def checkListTypes(*args):
    for arg in args:
        name = arg[0]
        inputList = arg[1]
        types = arg[2]

        expextedTypes = str([i.__name__ for i in types]).replace("['", "<").replace(" '", " <").replace("']", ">").replace("',", ">,")
        
        if not inputList:
            raise ValueError(f'{inputList} list should not be empty')
        
        if list in types:
            listDepth = depth(inputList)

            if listDepth == 1:
                for elem in inputList:
                    checkInputTypes((name, elem, types))
            
            elif listDepth == 2:
                if not all(isinstance(elem, list) for elem in inputList):
                    raise TypeError(f'All elements of inside of argument "{name}" list, expected to be <list>, or a combination of {expextedTypes}'.replace(", <list>", ""))
                
                for elem in inputList:
                    checkInputTypes((name, elem, types))

            else:
                raise ValueError(f'Argument "{name}" list expected to be maximum depth 2, not depth {listDepth}')

        else:
            for elem in inputList:
                checkInputTypes((name, elem, types))

def checkValues(*args):
    for arg in args:
        name = arg[0]
        variable = arg[1]
        types = arg[2]

        expectedValues = str([i for i in types]).replace('[', '').replace(']', '')
        
        if variable not in types:
            raise ValueError(f'Argument "{name}" expected to be {expectedValues}, not "{variable}"')

def checkMathExpression(arg: str, expression: str):
    try:
        eval(expression)

    except Exception:
        try:
            expression = expression.replace('pi', 'math.pi')
            expression = expression.replace('e', 'math.e')
            expression = expression.replace('tau', 'math.tau')
            eval(expression)

        except Exception:
            raise ValueError(f'{arg} is not a mathematical expression')

def checkDifferentPosition(positions: list):
    if len(positions) != len(set(positions)):
        raise ValueError('Duplicated positions')