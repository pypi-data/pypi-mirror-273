from ..utils.apiConnection import apiConnection
from ..utils.checker import getURL
from ..objects.SolutionItem import SolutionItem
from ..objects.DeviceItem import DeviceItem
from ..objects.FlowItem import FlowItem
from ..objects.Application import Application
from ..objects.Execution import Execution

from matplotlib import pyplot as plt
from prettytable import PrettyTable
import collections
import time


# API ENDPOINTS
connectionPoints = {
    'getVersion': 'connectionPoint/getVersion/',
    'getLicenceInfo': 'connectionPoint/getLicenceInfo/',
    'getQuantumSolutions': 'connectionPoint/getQuantumSolutions/',
    'getQuantumSolutionsEx': 'connectionPoint/getQuantumSolutionsEx/',
    'getQuantumDevices': 'connectionPoint/getQuantumDevices/',
    'getQuantumDevicesEx': 'connectionPoint/getQuantumDevicesEx/',
    'getQuantumFlows': 'connectionPoint/getQuantumFlows/',
    'runQuantumApplication': 'connectionPoint/runQuantumApplication/',
    'getQuantumExecutionResponse': 'connectionPoint/getQuantumExecutionResponse/'
}


# PRIVATE METHODS
def __plotQuantumGatesCircuit(histogramData: dict, name: str): # __plotQuantumGatesCircuit. Returns a plot
    histogramTitle = name
    histogramValues = histogramData[name]

    histogramValues = collections.OrderedDict(sorted(histogramValues.items())) # sort values

    fig, ax = plt.subplots(1, 1)
    ax.bar([ str(i) for i in histogramValues.keys()], histogramValues.values(), color='g')

    ax.set_title(histogramTitle)

    rects = ax.patches
    labels = [list(histogramValues.values())[i] for i in range(len(rects))]

    for rect, label in zip(rects, labels):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height+0.01, label, ha='center', va='bottom')

    plt.show()

def __plotAnnealingCircuit(histogramData, name): # __plotAnnealingCircuit. Returns a String
    histogramTitle = name
    histogramValues = histogramData[name]

    histogramValues2 = histogramValues.copy()
    del histogramValues2['fullsample']

    tableResults =PrettyTable(['Name', 'Value'])

    for key, value in histogramValues['fullsample'].items():
        tableResults.add_row([key, value])

    tableInfo = PrettyTable()
    tableInfo.field_names = histogramValues2.keys()
    tableInfo.add_rows([histogramValues2.values()])

    return f'\n\n{histogramTitle}\n{tableInfo}\n{tableResults}'


##################_____STATIC METHODS_____##################

# GET VERSION
def getVersion(context) -> str:
    urlData = getURL(context)
    url = urlData[0] + connectionPoints['getVersion']
    validate = urlData[1]

    return apiConnection(url, context.getHeader(), 'string', validate=validate)
    
# GET LICENCE INFO
def getLicenceInfo(context) -> dict:
    urlData = getURL(context)
    url = urlData[0] + connectionPoints['getLicenceInfo']
    validate = urlData[1]

    return apiConnection(url, context.getHeader(), 'json', validate=validate)

# GET QUANTUM SOLUTION LIST
def getQuantumSolutionList(context) -> dict:
    urlData = getURL(context)
    url = urlData[0] + connectionPoints['getQuantumSolutions']
    validate = urlData[1]
 
    return apiConnection(url, context.getHeader(), 'json', validate=validate)

# GET QUANTUM SOLUTIONS
def getQuantumSolutions(context) -> list:
    urlData = getURL(context)
    url = urlData[0] + connectionPoints['getQuantumSolutionsEx']
    validate = urlData[1]

    solutions = []

    solutionsDict = apiConnection(url, context.getHeader(), 'json', validate=validate)

    for solution in solutionsDict:
        solutions.append(SolutionItem(solution))

    return solutions

# GET QUANTUM SOLUTION NAME
def getQuantumSolutionName(context, idSolution: int) -> str:
    urlData = getURL(context)
    url = urlData[0] + connectionPoints['getQuantumSolutions']
    validate = urlData[1]

    solutionsDict = apiConnection(url, context.getHeader(), 'json', validate=validate)
    
    if str(idSolution) in solutionsDict.keys():
        solutionName = solutionsDict[str(idSolution)]
    
    else:
        raise ValueError('Incorrect Solution ID')

    return solutionName

# GET QUANTUM DEVICE LIST
def getQuantumDeviceList(context, idSolution: int) -> dict:
    urlData = getURL(context)
    url = urlData[0] + connectionPoints['getQuantumDevices'] + str(idSolution)
    validate = urlData[1]

    return apiConnection(url, context.getHeader(), 'json', validate=validate)

# GET QUANTUM DEVICES
def getQuantumDevices(context, idSolution: int) -> list:
    urlData = getURL(context)
    url = urlData[0] + connectionPoints['getQuantumDevicesEx'] + str(idSolution)
    validate = urlData[1]

    devices = []

    devicesDict = apiConnection(url, context.getHeader(), 'json', validate=validate)

    for device in devicesDict:
        devices.append(DeviceItem(device))
    
    return devices

# GET QUANTUM DEVICE NAME
def getQuantumDeviceName(context, idSolution: int, idDevice: int) -> str:
    urlData = getURL(context)
    url = urlData[0] + connectionPoints['getQuantumDevices'] + str(idSolution)
    validate = urlData[1]

    devicesDict = apiConnection(url, context.getHeader(), 'json', validate=validate)
    
    if str(idDevice) in devicesDict.keys():
        deviceName = devicesDict[str(idDevice)]
    
    else:
        raise ValueError('Incorrect Device ID')

    return deviceName

# GET QUANTUM FLOW LIST
def getQuantumFlowList(context, idSolution: int) -> dict:
    urlData = getURL(context)
    url = urlData[0] + connectionPoints['getQuantumFlows'] + str(idSolution)
    validate = urlData[1]
    
    return apiConnection(url, context.getHeader(), 'json', validate=validate)

# GET QUANTUM FLOWS
def getQuantumFlows(context, idSolution: int) -> list:
    urlData = getURL(context)
    url = urlData[0] + connectionPoints['getQuantumFlows'] + str(idSolution)
    validate = urlData[1]

    flows = []

    flowsDict = apiConnection(url, context.getHeader(), 'json', validate=validate)

    for idFlow in flowsDict:
        flows.append(FlowItem(int(idFlow), flowsDict[idFlow]))
    
    return flows

# GET QUANTUM FLOW NAME
def getQuantumFlowName(context, idSolution: int, idFlow: int) -> str:
    urlData = getURL(context)
    url = urlData[0] + connectionPoints['getQuantumFlows'] + str(idSolution)
    validate = urlData[1]

    flowsDict = apiConnection(url, context.getHeader(), 'json', validate=validate)
    
    if str(idFlow) in flowsDict.keys():
        flowName = flowsDict[str(idFlow)]
    
    else:
        raise ValueError('Incorrect Flow ID')

    return flowName

# RUN QUANTUM APPLICATION
def runQuantumApplication(context, applicationName: str, idSolution: int, idFlow: int, idDevice: int) -> Application:
    urlData = getURL(context)
    url = urlData[0] + connectionPoints['runQuantumApplication'] + str(applicationName) + '/' + str(idSolution) + '/' + str(idFlow) + '/' + str(idDevice)
    validate = urlData[1]

    executionToken = apiConnection(url, context.getHeader(), 'string', validate=validate)

    return Application(applicationName, int(idSolution), int(idFlow), int(idDevice), executionToken)

# RUN QUANTUM APPLICATION SYNC
def runQuantumApplicationSync(context, applicationName: str, idSolution: int, idFlow: int, idDevice: int) -> Application:
    application = runQuantumApplication(context, applicationName, idSolution, idFlow, idDevice)

    execution = getQuantumExecutionResponse(context, application)

    while execution.getExitCode() == 'WAIT':
        time.sleep(1)
        execution = getQuantumExecutionResponse(context, application)
    
    return application

# GET QUANTUM EXECUTION RESPONSE
def getQuantumExecutionResponse(context, *args) -> Execution:
    if len(args) == 1:
        executionToken = args[0].getExecutionToken()
        idSolution = args[0].getIdSolution()
        idFlow = args[0].getIdFlow()
    
    elif len(args) == 3:
        executionToken = args[0]
        idSolution = args[1]
        idFlow = args[2]

    urlData = getURL(context)
    url = urlData[0] + connectionPoints['getQuantumExecutionResponse'] + str(executionToken) + '/' + str(idSolution) + '/' + str(idFlow)
    validate = urlData[1]

    executionDict = apiConnection(url, context.getHeader(), 'json', validate=validate)
    
    return Execution(executionDict)

# REPRESENT RESULTS
def representResults(context, execution: Execution, resultIndex: int = None):
    representation = None
    histogramData = execution.getHistogram()

    if 'number_of_samples' in (list(histogramData.values())[0]).keys(): # annealing
        if resultIndex == None:
            representation = ''

            for name in histogramData:
                representation = representation + __plotAnnealingCircuit(histogramData, name)
        
        else:
            if resultIndex > -1 and resultIndex < len(histogramData):
                representation = __plotAnnealingCircuit(histogramData, list(histogramData)[resultIndex])
            
            else:
                raise IndexError(f'Invalid resultIndex. It should be 0 to {len(histogramData) - 1}')

    else: # quantum gates
        if resultIndex == None:
            for name in histogramData:
                __plotQuantumGatesCircuit(histogramData, name)
        else:
            if resultIndex > -1 and resultIndex < len(histogramData):
                __plotQuantumGatesCircuit(histogramData, list(histogramData)[resultIndex])

            else:
                raise IndexError(f'Invalid resultIndex. It should be 0 to {len(histogramData) - 1}')

    return representation