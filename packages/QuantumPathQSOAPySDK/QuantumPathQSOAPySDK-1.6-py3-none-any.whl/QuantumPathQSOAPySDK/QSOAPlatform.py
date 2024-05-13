from .utils.checker import (checkUserSession, checkInputTypes, checkValues)
from .utils.Exception import ExecutionObjectError
from .objects.Application import Application
from .objects.Asset import Asset
from .objects.AssetManagementData import AssetManagementData
from .objects.AssetManagementResult import AssetManagementResult
from .objects.Execution import Execution
from .objects.QuantumExecutionHistoryEntry import QuantumExecutionHistoryEntry

from .utils.Context import Context
from .qsoa.securityConnectionPoints import (
    encodePassword,
    encryptPassword,
    authenticate,
    authenticateEx,
    authenticateBasic,
    echoping,
    echostatus,
    echouser
)
from .qsoa.connectionPoints import (
    getVersion,
    getLicenceInfo,
    getQuantumSolutionList,
    getQuantumSolutions,
    getQuantumSolutionName,
    getQuantumDeviceList,
    getQuantumDevices,
    getQuantumDeviceName,
    getQuantumFlowList,
    getQuantumFlows,
    getQuantumFlowName,
    runQuantumApplication,
    runQuantumApplicationSync,
    getQuantumExecutionResponse,
    representResults
)
from .qsoa.dynamicConnectionPoints import (
    getAssetCatalog,
    getAsset,
    createAsset,
    createAssetSync,
    createAssetFlow,
    createAssetFlowSync,
    publishFlow,
    updateAsset,
    updateAssetSync,
    getAssetManagementResult,
    deleteAsset,
    getQuantumExecutionHistoric,
    getQuantumExecutionHistoricResult
)
from .circuit.annealing.CircuitAnnealing import CircuitAnnealing
from .circuit.flow.CircuitFlow import CircuitFlow
from .circuit.gates.CircuitGates import CircuitGates


class QSOAPlatform:

    # CONSTRUCTOR
    def __init__(self, username: str = None, password: str = None, configFile: bool = False):
        """
        QSOAPlatform object constructor.

        Prerequisites
        ----------
        - User created in QPath.

        Parameters
        ----------
        username : str
            QPath account username to authenticate.
        password : str
            QPath account password to authenticate. (SHA-256)
        
        Prerequisites
        ----------
        - User created in QPath.
        - .qpath file created in home path.

        Parameters
        ----------
        authenticate : str
            True to authenticate using .qpath config file.

        Output
        ----------
        QSOAPlatform obj
        """
        # CHECK INPUTS
        if username and password:
            checkInputTypes(
                ('username', username, (str,)),
                ('password', password, (str,)),
            )
        if configFile:
            checkInputTypes(('configFile', configFile, (bool,)))

        self.__context = Context()

        if configFile:
            authenticateEx(self.__context)
        
        elif username and password:
            authenticateEx(self.__context, username, password)


    ##################_____CONTEXT METHODS_____##################

    # GET ENVIRONMENTS
    def getEnvironments(self) -> dict:
        """
        Show QuantumPath available environments.

        Prerequisites
        ----------
        None.

        Output
        ----------
        dict
        """
        return self.__context.getEnvironments()

    # GET ACTIVE ENVIRONMENT
    def getActiveEnvironment(self) -> tuple:
        """
        Show active QuantumPath environment.

        Prerequisites
        ----------
        None.

        Output
        ----------
        tuple
        """
        return self.__context.getActiveEnvironment()

    # SET ACTIVE ENVIRONMENT
    def setActiveEnvironment(self, environmentName: str, qSOATargetURL: str = None, validateCert: bool = True) -> tuple:
        """
        Set active QuantumPath environment.

        Prerequisites
        ----------
        Existing QuantumPath environment.

        Parameters
        ----------
        environmentName : str
            QuantumPath environment name to set as active.
        qSOATargetURL : str
            Optional argument. New qSOA target URL to add to existing environments and set as active.
        validate : Optional argument. Check URL certificate for custom environment.

        Output
        ----------
        tuple
        """
        # CHECK INPUTS
        checkInputTypes(
            ('environmentName', environmentName, (str,)),
            ('validateCert', validateCert, (bool,))
        )
        if qSOATargetURL:
            checkInputTypes(
                ('qSOATargetURL', qSOATargetURL, (str,))
            )

        return self.__context.setActiveEnvironment(environmentName, qSOATargetURL, validateCert)


    ##################_____SECURITY METHODS_____##################

    # ENCODE PASSWORD
    def encodePassword(self, password: str):
        """
        Encode password in Base64.
        
        Prerequisites
        ----------
        - None.

        Parameters
        ----------
        password : str
            QPath account password to encode.

        Output
        ----------
        str
        """
        # CHECK INPUTS
        checkInputTypes(
            ('password', password, (str,))
        )

        return encodePassword(password)

    # ENCRYPT PASSWORD
    def encryptPassword(self, password: str):
        """
        Encrypt password in SHA-256.
        
        Prerequisites
        ----------
        - None.

        Parameters
        ----------
        password : str
            QPath account password to encrypt.

        Output
        ----------
        str
        """
        # CHECK INPUTS
        checkInputTypes(
            ('password', password, (str,))
        )

        return encryptPassword(password)

    # AUTHENTICATE BASIC
    def authenticateBasic(self, username: str = None, password: str = None) -> bool:
        """
        Performs the user authentication process.
        
        Prerequisites
        ----------
        - User created in QPath.

        Parameters
        ----------
        username : str
            QPath account username to authenticate.
        password : str
            QPath account password to authenticate.

        Output
        ----------
        bool
        """
        # CHECK INPUTS
        if username and password:
            checkInputTypes(
                ('username', username, (str,)),
                ('password', password, (str,))
            )

        return authenticateBasic(self.__context, username, password)

    # AUTHENTICATE
    def authenticate(self, username: str = None, password: str = None) -> bool:
        """
        Performs the user authentication process. With Base64 password.
        
        Prerequisites
        ----------
        - User created in QPath.

        Parameters
        ----------
        username : str
            QPath account username to authenticate.
        password : str
            QPath account password to authenticate. (Base64)
        
        Prerequisites
        ----------
        - User created in QPath.
        - .qpath file created in home path.

        Parameters
        ----------
        None if .qpath file in home path contains the credentials.

        Output
        ----------
        bool
        """
        # CHECK INPUTS
        if username and password:
            checkInputTypes(
                ('username', username, (str,)),
                ('password', password, (str,))
            )

        return authenticate(self.__context, username, password)

    # AUTHENTICATE EX
    def authenticateEx(self, username: str = None, password: str = None) -> bool:
        """
        Performs the user authentication process. With SHA-256 password.
        
        Prerequisites
        ----------
        - User created in QPath.

        Parameters
        ----------
        username : str
            QPath account username to authenticate.
        password : str
            QPath account password to authenticate. (SHA-256)
        
        Prerequisites
        ----------
        - User created in QPath.
        - .qpath file created in home path.

        Parameters
        ----------
        None if .qpath file in home path contains the credentials.

        Output
        ----------
        bool
        """
        # CHECK INPUTS
        if username and password:
            checkInputTypes(
                ('username', username, (str,)),
                ('password', password, (str,))
            )

        return authenticateEx(self.__context, username, password)

    # ECHOPING
    def echoping(self) -> bool:
        """
        Test to validate if the security service is enabled.

        Prerequisites
        ----------
        None.

        Output
        ----------
        bool
        """
        return echoping(self.__context)

    # ECHOSTATUS
    def echostatus(self) -> bool:
        """
        Check if user session is active.

        Prerequisites
        ----------
        None.

        Output
        ----------
        bool
        """
        return echostatus(self.__context)

    # ECHOUSER
    def echouser(self) -> str:
        """
        Check user login status.

        Prerequisites
        ----------
        None.

        Output
        ----------
        str
        """
        return echouser(self.__context)


    ##################_____STATIC METHODS_____##################

    # GET VERSION
    def getVersion(self) -> str:
        """
        Check the ConnectionPoint service version.

        Prerequisites
        ----------
        - User already authenticated.

        Output
        ----------
        str
        """
        checkUserSession(self.__context)

        return getVersion(self.__context)

    # GET LICENCE INFO
    def getLicenceInfo(self) -> dict:
        """
        Returns QuantumPath account licence.

        Prerequisites
        ----------
        - User already authenticated.

        Output
        ----------
        dict
        """
        checkUserSession(self.__context)

        return getLicenceInfo(self.__context)

    # GET QUANTUM SOLUTION LIST
    def getQuantumSolutionList(self) -> dict:
        """
        Show the list of solutions available to the user along with their IDs.

        Prerequisites
        ----------
        - User already authenticated.
        - Solution created.

        Output
        ----------
        dict
        """
        checkUserSession(self.__context)

        return getQuantumSolutionList(self.__context)

    # GET QUANTUM SOLUTIONS
    def getQuantumSolutions(self) -> list:
        """
        Get the solutions available from the user as an object.

        Prerequisites
        ----------
        - User already authenticated.

        Output
        ----------
        SolutionItem obj list
        """
        checkUserSession(self.__context)

        return getQuantumSolutions(self.__context)

    # GET QUANTUM SOLUTION NAME
    def getQuantumSolutionName(self, idSolution: int) -> str:
        """
        Get the name of a solution.

        Prerequisites
        ----------
        - User already authenticated.
        
        Parameters
        ----------
        idSolution : int
            Solution ID to show their name.

        Output
        ----------
        str
        """
        checkUserSession(self.__context)

        # CHECK INPUTS
        checkInputTypes(
            ('idSolution', idSolution, (int,))
        )

        return getQuantumSolutionName(self.__context, idSolution)

    # GET QUANTUM DEVIDE LIST
    def getQuantumDeviceList(self, idSolution: int) -> dict:
        """
        Show the list of devices available in a solution along with their IDs.

        Prerequisites
        ----------
        - User already authenticated.
        - Solution created.
        
        Parameters
        ----------
        idSolution : int
            Solution ID to show their devices.

        Output
        ----------
        dict
        """
        checkUserSession(self.__context)

        # CHECK INPUTS
        checkInputTypes(
            ('idSolution', idSolution, (int,))
        )

        return getQuantumDeviceList(self.__context, idSolution)

    # GET QUANTUM DEVICES
    def getQuantumDevices(self, idSolution: int) -> list:
        """
        Get the available devices in a solution as an object.

        Prerequisites
        ----------
        - User already authenticated.
        - Solution created.
        
        Parameters
        ----------
        idSolution : int
            Solution ID to show their devices.
        
        Output
        ----------
        DeviceItem obj list
        """
        checkUserSession(self.__context)

        # CHECK INPUTS
        checkInputTypes(
            ('idSolution', idSolution, (int,))
        )

        return getQuantumDevices(self.__context, idSolution)

    # GET QUANTUM DEVICE NAME
    def getQuantumDeviceName(self, idSolution: int, idDevice: int) -> str:
        """
        Get the name of a device.

        Prerequisites
        ----------
        - User already authenticated.
        - Solution created.
        
        Parameters
        ----------
        idSolution : int
            Solution ID to wich the device belongs.
        idDevice : int
            Device ID to show their name.
        
        Output
        ----------
        str
        """
        checkUserSession(self.__context)

        # CHECK INPUTS
        checkInputTypes(
            ('idSolution', idSolution, (int,)),
            ('idDevice', idDevice, (int,))
        )

        return getQuantumDeviceName(self.__context, idSolution, idDevice)

    # GET QUANTUM FLOW LIST
    def getQuantumFlowList(self, idSolution: int) -> dict:
        """
        Show the list of flows available in a solution along with their IDs.

        Prerequisites
        ----------
        - User already authenticated.
        - Solution created.
        
        Parameters
        ----------
        idSolution : int
            Solution ID to show their flows.
        
        Output
        ----------
        dict
        """
        checkUserSession(self.__context)

        # CHECK INPUTS
        checkInputTypes(
            ('idSolution', idSolution, (int,))
        )

        return getQuantumFlowList(self.__context, idSolution)

    # GET QUANTUM FLOWS
    def getQuantumFlows(self, idSolution: int) -> list:
        """
        Get the flows available in a solution as an object.
        
        Prerequisites
        ----------
        - User already authenticated.
        - Solution created.

        Parameters
        ----------
        idSolution : int
            Solution ID to show their flows.

        Output
        ----------
        FlowItem obj list
        """
        checkUserSession(self.__context)

        # CHECK INPUTS
        checkInputTypes(
            ('idSolution', idSolution, (int,))
        )

        return getQuantumFlows(self.__context, idSolution)

    # GET QUANTUM FLOW NAME
    def getQuantumFlowName(self, idSolution: int, idFlow: int) -> str:
        """
        Get the name of a flow.

        Prerequisites
        ----------
        - User already authenticated.
        - Solution created.
        
        Parameters
        ----------
        idSolution : int
            Solution ID to wich the flow belongs.
        idFlow : int
            Flow ID to show their name.

        Output
        ----------
        str
        """
        checkUserSession(self.__context)

        # CHECK INPUTS
        checkInputTypes(
            ('idSolution', idSolution, (int,)),
            ('idFlow', idFlow, (int,))
        )

        return getQuantumFlowName(self.__context, idSolution, idFlow)

    # RUN QUANTUM APPLICATION
    def runQuantumApplication(self, applicationName: str, idSolution: int, idFlow: int, idDevice: int):
        """
        Run a created quantum solution.

        Prerequisites
        ----------
        - User already authenticated.
        - Solution created.
        
        Parameters
        ----------
        applicationName : str
            Nametag to identify the execution.
        idSolution : int
            Solution ID to run.
        idFlow : int
            Specific Flow ID to run.
        idDevice : int
            Specific Device ID to run the solution.
        
        Output
        ----------
        Application obj
        """
        checkUserSession(self.__context)

        # CHECK INPUTS
        checkInputTypes(
            ('applicationName', applicationName, (str,)),
            ('idSolution', idSolution, (int,)),
            ('idFlow', idFlow, (int,)),
            ('idDevice', idDevice, (int,))
        )

        return runQuantumApplication(self.__context, applicationName, idSolution, idFlow, idDevice)

    # RUN QUANTUM APPLICATION SYNC
    def runQuantumApplicationSync(self, applicationName: str, idSolution: int, idFlow: int, idDevice: int) -> Application:
        """
        Run a created quantum solution synchronous.

        Prerequisites
        ----------
        - User already authenticated.
        - Solution created.
        
        Parameters
        ----------
        applicationName : str
            Nametag to identify the execution.
        idSolution : int
            Solution ID to run.
        idFlow : int
            Specific Flow ID to run.
        idDevice : int
            Specific Device ID to run the solution.
        
        Output
        ----------
        Application obj
        """
        checkUserSession(self.__context)

        # CHECK INPUTS
        checkInputTypes(
            ('applicationName', applicationName, (str,)),
            ('idSolution', idSolution, (int,)),
            ('idFlow', idFlow, (int,)),
            ('idDevice', idDevice, (int,))
        )

        return runQuantumApplicationSync(self.__context, applicationName, idSolution, idFlow, idDevice)

    # GET QUANTUM EXECUTION RESPONSE
    def getQuantumExecutionResponse(self, *args):
        """
        Get the response of a quantum solution execution.

        Prerequisites
        ----------
        - User already authenticated.
        - Solution run.
        - Application object generated.
        
        Parameters
        ----------
        application : Application obj
            Application object generated in running a quantum solution.
        
        Prerequisites
        ----------
        - User already authenticated.
        - Solution run.

        Parameters
        ----------
        executionToken : str
            Solution ID of the application already run.
        idSolution : int
            Solution ID of the solution already run.
        idFlow : int
            Specific Flow ID of the flow already run.
        
        Output
        ----------
        Execution obj
        """
        checkUserSession(self.__context)

        # CHECK INPUTS
        if len(args) == 1:
            checkInputTypes(
                ('application', args[0], (Application,))
            )
        
        elif len(args) == 3:
            checkInputTypes(
                ('executionToken', args[0], (str,)),
                ('idSolution', args[1], (int,)),
                ('idFlow', args[2], (int,))
            )
        
        else:
            raise ValueError('QSOAPlatform.authenticate() takes from 1 to 4 positional arguments')

        return getQuantumExecutionResponse(self.__context, *args)

    # REPRESENT RESULTS
    def representResults(self, execution, resultIndex: int = None):
        """
        Results visual representation.

        Prerequisites
        ----------
        - User already authenticated.
        - Execution completed.
        
        Parameters
        ----------
        execution : Execution obj
            Execution object generated by execution response method.
        resultIndex : int
            Optional argument. Value to just show that result by index.
        
        Output
        ----------
        png | string
        """
        checkUserSession(self.__context)

        # CHECK INPUTS
        checkInputTypes(
            ('execution', execution, (Execution,))
        )
        if resultIndex:
            checkInputTypes(
                ('resultIndex', resultIndex, (int,))
            )
        if execution.getExitCode() != 'OK':
            raise ExecutionObjectError('Execution status code is not "OK"')
        
        return representResults(self.__context, execution, resultIndex)


    ##################_____DYNAMIC METHODS_____##################

    # GET ASSET CATALOG
    def getAssetCatalog(self, idSolution: int, assetType: str, assetLevel: str) -> list:
        """
        Get asset information from a solution.

        Prerequisites
        ----------
        - User already authenticated.
        - Solution created.
        
        Parameters
        ----------
        idSolution : int
            Solution ID to show their information.
        assetType : str
            Type of the asset required. It can be CIRCUIT or FLOW.
        assetLevel : str
            Level of the Language specificated. It can be VL (Visual Language) or IL (Intermediate Language).
        
        Output
        ----------
        Asset obj list
        """
        checkUserSession(self.__context)

        # CHECK INPUTS
        checkInputTypes(
            ('idSolution', idSolution, (int,)),
            ('assetType', assetType, (str,)),
            ('assetLevel', assetLevel, (str,))
        )
        checkValues(
            ('assetType', assetType, ['CIRCUIT', 'FLOW']),
            ('assetLevel', assetLevel, ['VL', 'IL'])
        )

        return getAssetCatalog(self.__context, idSolution, assetType, assetLevel)

    # GET ASSET
    def getAsset(self, idAsset: int, assetType: str, assetLevel: str) -> Asset:
        """
        Get specific asset information.

        Prerequisites
        ----------
        - User already authenticated.
        - Asset created.
        
        Parameters
        ----------
        idAsset : int
            Asset ID to show their information.
        assetType : str
            Type of the asset required. It can be CIRCUIT or FLOW.
        assetLevel : str
            Level of the Language specificated. It can be VL (Visual Language) or IL (Intermediate Language).
        
        Output
        ----------
        Asset obj
        """
        checkUserSession(self.__context)

        # CHECK INPUTS
        checkInputTypes(
            ('idAsset', idAsset, (int,)),
            ('assetType', assetType, (str,)),
            ('assetLevel', assetLevel, (str,))
        )
        checkValues(
            ('assetType', assetType, ['CIRCUIT', 'FLOW']),
            ('assetLevel', assetLevel, ['VL', 'IL'])
        )

        return getAsset(self.__context, idAsset, assetType, assetLevel)
    
    # CREATE ASSET
    def createAsset(self, idSolution: int, assetName: str, assetNamespace: str, assetDescription: str, assetBody, assetType: str,
                    assetLevel: str) -> AssetManagementData:
        """
        Create asset.

        Prerequisites
        ----------
        - User already authenticated.
        - Solution created.
        
        Parameters
        ----------
        idSolution : int
            Solution to create the asset.
        assetName : str
            New asset name.
        assetNamespace : str
            New asset namespace.
        assetDescription : str
            New asset description.
        assetBody : str | CircuitGates obj | CircuitAnnealing obj | CircuitFlow obj
            New asset body as string or as a circtuit obj.
        assetType : str
            New asset type. It can be GATES, ANNEAL or FLOW.
        assetLevel : str
            New asset level. It can be VL (Visual Language) or IL (Intermediate Language).
        
        Output
        ----------
        AssetManagementData obj
        """
        checkUserSession(self.__context)

        # CHECK INPUTS
        checkInputTypes(
            ('idSolution', idSolution, (int,)),
            ('assetName', assetName, (str,)),
            ('assetNamespace', assetNamespace, (str,)),
            ('assetDescription', assetDescription, (str,)),
            ('assetBody', assetBody, (str, CircuitGates, CircuitAnnealing, CircuitFlow)),
            ('assetType', assetType, (str,)),
            ('assetLevel', assetLevel, (str,))
        )
        checkValues(
            ('assetType', assetType, ['GATES', 'ANNEAL', 'FLOW']),
            ('assetLevel', assetLevel, ['VL', 'IL'])
        )

        return createAsset(self.__context, idSolution, assetName, assetNamespace, assetDescription, assetBody, assetType, assetLevel)
    
    # CREATE ASSET SYNC
    def createAssetSync(self, idSolution: int, assetName: str, assetNamespace: str, assetDescription: str, assetBody, assetType: str,
                        assetLevel: str) -> AssetManagementResult:
        """
        Create asset and get result.

        Prerequisites
        ----------
        - User already authenticated.
        - Solution created.
        
        Parameters
        ----------
        idSolution : int
            Solution to create the asset.
        assetName : str
            New asset name.
        assetNamespace : str
            New asset namespace.
        assetDescription : str
            New asset description.
        assetBody : str | CircuitGates obj | CircuitAnnealing obj | CircuitFlow obj
            New asset body as string or as a circtuit obj.
        assetType : str
            New asset type. It can be GATES, ANNEAL or FLOW.
        assetLevel : str
            New asset level. It can be VL (Visual Language) or IL (Intermediate Language).
        
        Output
        ----------
        AssetManagementResult obj
        """
        checkUserSession(self.__context)

        # CHECK INPUTS
        checkInputTypes(
            ('idSolution', idSolution, (int,)),
            ('assetName', assetName, (str,)),
            ('assetNamespace', assetNamespace, (str,)),
            ('assetDescription', assetDescription, (str,)),
            ('assetBody', assetBody, (str, CircuitGates, CircuitAnnealing, CircuitFlow)),
            ('assetType', assetType, (str,)),
            ('assetLevel', assetLevel, (str,))
        )
        checkValues(
            ('assetType', assetType, ['GATES', 'ANNEAL', 'FLOW']),
            ('assetLevel', assetLevel, ['VL', 'IL'])
        )

        return createAssetSync(self.__context, idSolution, assetName, assetNamespace, assetDescription, assetBody, assetType, assetLevel)

    # CREATE ASSET FLOW
    def createAssetFlow(self, idSolution: int, assetName: str, assetNamespace: str, assetDescription: str, assetBody, assetLevel: str,
                        publish: bool = False) -> AssetManagementData:
        """
        Create asset flow.

        Prerequisites
        ----------
        - User already authenticated.
        - Solution created.
        
        Parameters
        ----------
        idSolution : int
            Solution to create the asset.
        assetName : str
            New asset name.
        assetNamespace : str
            New asset namespace.
        assetDescription : str
            New asset description.
        assetBody : str | CircuitFlow obj
            New asset body as string or as a circtuit obj.
        assetLevel : str
            New asset level. It can be VL (Visual Language) or IL (Intermediate Language).
        publish : bool
            Publish flow or not.

        Output
        ----------
        AssetManagementData obj
        """
        checkUserSession(self.__context)

        # CHECK INPUTS
        checkInputTypes(
            ('idSolution', idSolution, (int,)),
            ('assetName', assetName, (str,)),
            ('assetNamespace', assetNamespace, (str,)),
            ('assetDescription', assetDescription, (str,)),
            ('assetBody', assetBody, (str, CircuitFlow)),
            ('assetLevel', assetLevel, (str,)),
            ('publish', publish, (bool,))
        )
        checkValues(
            ('assetLevel', assetLevel, ['VL', 'IL'])
        )

        return createAssetFlow(self.__context, idSolution, assetName, assetNamespace, assetDescription, assetBody, assetLevel, publish)

    # CREATE ASSET FLOW SYNC
    def createAssetFlowSync(self, idSolution: int, assetName: str, assetNamespace: str, assetDescription: str, assetBody, assetLevel: str,
                            publish: bool = False) -> AssetManagementResult:
        """
        Create asset flow and get result.

        Prerequisites
        ----------
        - User already authenticated.
        - Solution created.
        
        Parameters
        ----------
        idSolution : int
            Solution to create the asset.
        assetName : str
            New asset name.
        assetNamespace : str
            New asset namespace.
        assetDescription : str
            New asset description.
        assetBody : str | CircuitGates obj | CircuitAnnealing obj | CircuitFlow obj
            New asset body as string or as a circtuit obj.
        assetLevel : str
            New asset level. It can be VL (Visual Language) or IL (Intermediate Language).
        publish : bool
            Publish flow or not.

        Output
        ----------
        AssetManagementResult obj
        """
        checkUserSession(self.__context)

        # CHECK INPUTS
        checkInputTypes(
            ('idSolution', idSolution, (int,)),
            ('assetName', assetName, (str,)),
            ('assetNamespace', assetNamespace, (str,)),
            ('assetDescription', assetDescription, (str,)),
            ('assetBody', assetBody, (str, CircuitFlow)),
            ('assetLevel', assetLevel, (str,)),
            ('publish', publish, (bool,))
        )
        checkValues(
            ('assetLevel', assetLevel, ['VL', 'IL'])
        )

        return createAssetFlowSync(self.__context, idSolution, assetName, assetNamespace, assetDescription, assetBody, assetLevel, publish)

    # PUBLISH FLOW
    def publishFlow(self, idFlow: int, publish: bool) -> bool:
        """
        Change flow publish status.

        Prerequisites
        ----------
        - User already authenticated.
        - Access permission to the flow.

        Parameters
        ----------
        idFlow : int
            Flow ID to change publish status.
        publish : bool
            Publish flow or not.

        Output
        ----------
        bool
        """
        checkUserSession(self.__context)

        # CHECK INPUTS
        checkInputTypes(
            ('idFlow', idFlow, (int,)),
            ('publish', publish, (bool,))
        )

        return publishFlow(self.__context, idFlow, publish)

    # UPDATE ASSET
    def updateAsset(self, asset: Asset, assetName: str = None, assetNamespace: str = None, assetDescription: str = None, assetBody = None,
                    assetType: str = None, assetLevel: str = None) -> AssetManagementData:
        """
        Update asset values.

        Prerequisites
        ----------
        - User already authenticated.
        - Asset created.
        
        Parameters
        ----------
        asset : Asset obj
            Asset object to change information.
        assetName : str
            Optional argument. New asset name.
        assetNamespace : str
            Optional argument. New asset namespace.
        assetDescription : str
            Optional argument. New asset description.
        assetBody : str | CircuitGates obj | CircuitAnnealing obj | CircuitFlow obj
            Optional argument. New asset body as string or as a circtuit obj.
        assetType : str
            Optional argument. New asset type. It can be GATES, ANNEAL or FLOW.
        assetLevel : str
            Optional argument. New asset level. It can be VL (Visual Language) or IL (Intermediate Language).
        
        Output
        ----------
        AssetManagementData obj
        """
        checkUserSession(self.__context)

        # CHECK INPUTS
        checkInputTypes(
            ('asset', asset, (Asset,))
        )
        if assetName:
            checkInputTypes(
                ('assetName', assetName, (str,))
            )
        if assetNamespace:
            checkInputTypes(
                ('assetNamespace', assetNamespace, (str,))
            )
        if assetDescription:
            checkInputTypes(
                ('assetDescription', assetDescription, (str,))
            )
        if assetBody:
            checkInputTypes(
                ('assetBody', assetBody, (str, CircuitGates, CircuitAnnealing, CircuitFlow)),
                ('assetType', assetType, (str,)),
                ('assetLevel', assetLevel, (str,))
            )
            checkValues(
                ('assetType', assetType, ['GATES', 'ANNEAL', 'FLOW']),
                ('assetLevel', assetLevel, ['VL', 'IL'])
            )
        
        return updateAsset(self.__context, asset, assetName, assetNamespace, assetDescription, assetBody, assetType, assetLevel)

    # UPDATE ASSET SYNC
    def updateAssetSync(self, asset: Asset, assetName: str = None, assetNamespace: str = None, assetDescription: str = None, assetBody = None,
                        assetType: str = None, assetLevel: str = None) -> AssetManagementResult:
        """
        Update asset values and get result.

        Prerequisites
        ----------
        - User already authenticated.
        - Asset created.
        
        Parameters
        ----------
        asset : Asset obj
            Asset object to change information.
        assetName : str
            Optional argument. New asset name.
        assetNamespace : str
            Optional argument. New asset namespace.
        assetDescription : str
            Optional argument. New asset description.
        assetBody : str | CircuitGates obj | CircuitAnnealing obj | CircuitFlow obj
            Optional argument. New asset body as string or as a circtuit obj.
        assetType : str
            Optional argument. New asset type. It can be GATES, ANNEAL or FLOW.
        assetLevel : str
            Optional argument. New asset level. It can be VL (Visual Language) or IL (Intermediate Language).
        
        Output
        ----------
        AssetManagementResult obj
        """
        checkUserSession(self.__context)

        # CHECK INPUTS
        checkInputTypes(
            ('asset', asset, (Asset,))
        )
        if assetName:
            checkInputTypes(
                ('assetName', assetName, (str,))
            )
        if assetNamespace:
            checkInputTypes(
                ('assetNamespace', assetNamespace, (str,))
            )
        if assetDescription:
            checkInputTypes(
                ('assetDescription', assetDescription, (str,))
            )
        if assetBody:
            checkInputTypes(
                ('assetBody', assetBody, (str, CircuitGates, CircuitAnnealing, CircuitFlow)),
                ('assetType', assetType, (str,)),
                ('assetLevel', assetLevel, (str,))
            )
            checkValues(
                ('assetType', assetType, ['GATES', 'ANNEAL', 'FLOW']),
                ('assetLevel', assetLevel, ['VL', 'IL'])
            )
        
        return updateAssetSync(self.__context, asset, assetName, assetNamespace, assetDescription, assetBody, assetType, assetLevel)

    # GET ASSET MANAGEMENT RESULT
    def getAssetManagementResult(self, lifecycleToken: str) -> AssetManagementResult:
        """
        Get Asset Management Result from a lifecycle token.

        Prerequisites
        ----------
        - Existing asset lifecycle token.
        
        Parameters
        ----------
        lifecycleToken : str
            Asset lifecycle token.
        
        Output
        ----------
        AssetManagementResult obj
        """
        checkUserSession(self.__context)

        # CHECK INPUTS
        checkInputTypes(
            ('lifecycleToken', lifecycleToken, (str,))
        )

        return getAssetManagementResult(self.__context, lifecycleToken)

    # DELETE ASSET
    def deleteAsset(self, *args) -> bool:
        """
        Delete asset.

        Prerequisites
        ----------
        - User already authenticated.
        - Asset created.
        
        Parameters
        ----------
        asset : Asset obj
            Asset object to delete.
        
        Parameters
        ----------
        idAsset : int
            Asset id to delete.
        assetType : str
            Asset type to delete. It can be CIRCUIT or FLOW.
        
        Output
        ----------
        bool
        """
        checkUserSession(self.__context)

        # CHECK INPUTS
        if len(args) == 1:
            checkInputTypes(
                ('asset', args[0], (Asset,))
            )
        
        elif len(args) == 2:
            checkInputTypes(
                ('idAsset', args[0], (int,)),
                ('assetType', args[1], (str,))
            )
            checkValues(
                ('assetType', args[1], ['CIRCUIT', 'FLOW'])
            )

        return deleteAsset(self.__context, *args)
    
    # GET QUANTUM EXECUTION HISTORIC
    def getQuantumExecutionHistoric(self, idSolution: int = None, idFlow: int = None, idDevice: int = None, dateFrom: str = None, isSimulator: bool = None,
                                    top: int = None, resultType: bool = None) -> list:
        """
        Get a list of quantum execution history entries.

        Prerequisites
        ----------
        - User already authenticated.
        
        Parameters
        ----------
        idSolution : int
            Optional argument. Filter by solution ID.
        idFlow : int
            Optional argument. Filter by flow ID.
        idDevice : int
            Optional argument. Filter by device ID.
        dateFrom : str
            Optional argument. Filter from date. Format yyyy-mm-ddThh:mm:ss.
        isSimulator : bool
            Optional argument. Filter is simulator.
        top : int
            Optional argument. Number of top results. 10 by default.
        resultType : bool
            Optional argument. Result type.True if it is OK and false if ERR.
        
        Output
        ----------
        QuantumExecutionHistoryEntry obj list
        """
        checkUserSession(self.__context)

        # CHECK INPUTS
        if idSolution:
            checkInputTypes(
                ('idSolution', idSolution, (int,))
            )
        if idFlow:
            checkInputTypes(
                ('idFlow', idFlow, (int,))
            )
        if idDevice:
            checkInputTypes(
                ('idDevice', idDevice, (int,))
            )
        if dateFrom:
            checkInputTypes(
                ('dateFrom', dateFrom, (str,))
            )
        if isSimulator:
            checkInputTypes(
                ('isSimulator', isSimulator, (bool,))
            )
        if top:
            checkInputTypes(
                ('top', top, (int,))
            )
        if resultType:
            checkInputTypes(
                ('resultType', resultType, (bool,))
            )
        
        return getQuantumExecutionHistoric(self.__context, idSolution, idFlow, idDevice, dateFrom, isSimulator, top, resultType)

    # GET QUANTUM EXECUTION HISTORIC RESULT
    def getQuantumExecutionHistoricResult(self, idResult: int) -> QuantumExecutionHistoryEntry:
        """
        Get a quantum execution history entry.

        Prerequisites
        ----------
        - User already authenticated.
        - Existing result.
        
        Parameters
        ----------
        idResult : int
            Result ID to get information about.
        
        Output
        ----------
        QuantumExecutionHistoryEntry obj
        """
        checkUserSession(self.__context)

        # CHECK INPUTS
        checkInputTypes(
            ('idResult', idResult, (int,))
        )

        return getQuantumExecutionHistoricResult(self.__context, idResult)


    ##################_____CIRCUIT METHODS_____##################

    # CIRCUIT ANNEALING
    def CircuitAnnealing(self):
        """
        CircuitAnnealing object constructor.

        Prerequisites
        ----------
        - User already authenticated.

        Output
        ----------
        CircuitAnnealing obj
        """
        checkUserSession(self.__context)

        return CircuitAnnealing()
    
    # CIRCUIT FLOW
    def CircuitFlow(self):
        """
        CircuitFlow object constructor.

        Prerequisites
        ----------
        - User already authenticated.

        Output
        ----------
        CircuitFlow obj
        """
        checkUserSession(self.__context)

        return CircuitFlow()
    
    # CIRCUIT GATES
    def CircuitGates(self):
        """
        CircuitGates object constructor.

        Prerequisites
        ----------
        - User already authenticated.

        Output
        ----------
        CircuitGates obj
        """
        checkUserSession(self.__context)

        return CircuitGates()