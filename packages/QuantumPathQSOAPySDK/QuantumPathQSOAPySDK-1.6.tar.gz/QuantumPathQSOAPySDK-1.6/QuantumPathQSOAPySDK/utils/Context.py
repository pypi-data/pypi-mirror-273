from .apiConnection import apiConnection

from pathlib import Path
from configparser import ConfigParser


class Context:

    # CONSTRUCTOR
    def __init__(self, username: str = None, password: str = None, url: tuple = None):
        self.__environments = {
            'default-environments': {
                'pro': 'https://qsoa.quantumpath.app:8443/api/'
            },
            'custom-environments': {}
        }

        qpathFile = ConfigParser(allow_no_value=True)
        qpathFileExists = qpathFile.read(str(Path.home()) + '\.qpath')

        if qpathFileExists:
            self.__activeEnvironment = eval(qpathFile.options('active-environment')[0])

            for key in qpathFile['custom-environments']:
                value = eval(qpathFile['custom-environments'][key])

                if value[0][len(value)-1] != '/':
                    urlDirection = value[0] + '/'
                else:
                    urlDirection = value[0]

                self.__environments['custom-environments'][key] = (urlDirection, value[1])
        else:
            self.__activeEnvironment = ('default-environments', 'pro')

        self.__credentials = {
            "Username": username,
            "Password": password
        } if username else None

        self.__authToken = apiConnection(url[0], self.__credentials, 'string', 'data', validate=url[1]) if username else None

        self.__header = {
            "Authorization": 'Bearer ' + str(self.__authToken)
        } if username else None


    # GETTERS
    def getCredentials(self) -> dict:
        return self.__credentials

    def getAuthToken(self) -> str:
        return self.__authToken
    
    def getHeader(self) -> dict:
        return self.__header


    ##################_____METHODS_____##################

    # UPDATE CONTEXT
    def updateContext(self, username: str, password: str, url: tuple):
        self.__credentials = {
            "Username": username,
            "Password": password
        }

        self.__authToken = apiConnection(url[0], self.__credentials, 'string', 'data', validate=url[1])

        self.__header = {
            "Authorization": 'Bearer ' + str(self.__authToken)
        }

    # GET ENVIRONMENTS
    def getEnvironments(self) -> dict:
        return self.__environments

    # GET ACTIVE ENVIRONMENT
    def getActiveEnvironment(self) -> tuple:
        return self.__activeEnvironment

    # SET ACTIVE ENVIRONMENT
    def setActiveEnvironment(self, environmentName: str, qSOATargetURL: str, validateCert: bool) -> tuple:
        if qSOATargetURL:
            if environmentName in self.__environments['default-environments']:
                raise ValueError(f'Environment not valid, default-environments cannot be changed. Active environment is still {self.__activeEnvironment}')

            if qSOATargetURL[len(qSOATargetURL)-1] != '/':
                qSOATargetURL = qSOATargetURL + '/'

            self.__environments['custom-environments'][environmentName] = (qSOATargetURL, validateCert)

        if environmentName in self.__environments['default-environments']:
            newActiveEnvironment = ('default-environments', environmentName)
        
        elif environmentName in self.__environments['custom-environments']:
            newActiveEnvironment = ('custom-environments', environmentName)
        
        else:
            raise ValueError(f'Environment not valid. Active environment is still {self.__activeEnvironment}')

        self.__activeEnvironment = newActiveEnvironment

        return self.__activeEnvironment