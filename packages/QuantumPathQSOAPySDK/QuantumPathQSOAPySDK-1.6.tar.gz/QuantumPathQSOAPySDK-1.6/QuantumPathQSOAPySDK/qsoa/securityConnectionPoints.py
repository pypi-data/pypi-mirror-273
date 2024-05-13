from ..utils.apiConnection import apiConnection
from ..utils.checker import getURL
from ..utils.Exception import (ConfigFileError, Base64Error)

import base64
import hashlib
from pathlib import Path
from configparser import ConfigParser

# API ENDPOINTS
securityEndpoints = {
    'echoping': 'login/echoping/',
    'echouser': 'login/echouser/',
    'echostatus': 'login/echostatus',
    'authenticate': 'login/authenticate/',
    'authenticateEx': 'login/authenticateEx/'
}

# PRIVATE METHODS
def __getCredentialsFromConfigFile(context) -> list:
    try:
        qpathcredentials = ConfigParser(allow_no_value=True)
        qpathcredentials.read(str(Path.home()) + '\.qpath')

        username = qpathcredentials[context.getActiveEnvironment()[1] + '-credentials']['username']
        password = qpathcredentials[context.getActiveEnvironment()[1] + '-credentials']['password']

    except:
        raise ConfigFileError('Error reading username or password in config file')
    
    return [username, password]

def __decodePassword(password: str) -> str:
    try:
        return base64.b64decode(password).decode('utf-8')
    
    except:
        raise Base64Error('Invalid Base64 encoding in password')


##################_____SECURITY METHODS_____##################

# ENCODE PASSWORD
def encodePassword(password: str):
    encoded_bytes = base64.b64encode(password.encode('utf-8'))
    encoded_password = encoded_bytes.decode('utf-8')

    return encoded_password

# ENCRYPT PASSWORD
def encryptPassword(password: str):
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    return hashed_password

# AUTHENTICATE BASIC
def authenticateBasic(context, username: str = None, password: str = None) -> bool:
    urlData = getURL(context)
    url = (urlData[0] + securityEndpoints['authenticate'], urlData[1])

    if not username and not password:
        credentials = __getCredentialsFromConfigFile(context)
        username = credentials[0]
        password = credentials[1]

    elif not username or not password:
        raise ValueError('QSOAPlatform.authenticateBasic() takes from 1 to 3 positional arguments')

    context.updateContext(username, password, url)

    return True

# AUTHENTICATE
def authenticate(context, username: str = None, password: str = None) -> bool:
    urlData = getURL(context)
    url = (urlData[0] + securityEndpoints['authenticate'], urlData[1])

    if not username and not password:
        credentials = __getCredentialsFromConfigFile(context)
        username = credentials[0]
        password = credentials[1]
        
    elif not username or not password:
        raise ValueError('QSOAPlatform.authenticate() takes from 1 to 3 positional arguments')

    else:
        password = __decodePassword(password)

    context.updateContext(username, password, url)

    return True

# AUTHENTICATE EX
def authenticateEx(context, username: str = None, password: str = None) -> bool:
    urlData = getURL(context)
    url = (urlData[0] + securityEndpoints['authenticateEx'], urlData[1])

    if not username and not password:
        credentials = __getCredentialsFromConfigFile(context)
        username = credentials[0]
        password = credentials[1]

    elif not username or not password:
        raise ValueError('QSOAPlatform.authenticateEx() takes from 1 to 3 positional arguments')

    context.updateContext(username, password, url)

    return True

# ECHOPING
def echoping(context) -> bool:
    urlData = getURL(context)
    url = urlData[0] + securityEndpoints['echoping']
    validate = urlData[1]
    
    return apiConnection(url, 'boolean', validate=validate)

# ECHOSTATUS
def echostatus(context) -> bool:
    urlData = getURL(context)
    url = urlData[0] + securityEndpoints['echostatus']
    validate = urlData[1]

    return apiConnection(url, context.getHeader(), 'boolean', validate=validate)

# ECHOUSER
def echouser(context) -> str:
    urlData = getURL(context)
    url = urlData[0] + securityEndpoints['echouser']
    validate = urlData[1]

    return apiConnection(url, context.getHeader(), 'string', validate=validate)