"""
This is responsible to log error or warning events and holds custom Exception related to variables and scopes
"""

from typing import Any
from system import SystemShutdown #type: ignore
import logging

logging.basicConfig(filename="Log.log",
                    format='%(asctime)s: [%(levelname)s] %(message)s',
                    filemode='w')

logger = logging.getLogger()

class MoreScopesIndex(Exception): 
    """
    This Exceptions is raised when the code tried to add new scope but the addtions didn't increased the number of scopes

    Args:
        Exception (type: Not Valid): Not Valid
    """

    def __init__(self, ScopeName:str) -> None:
        """
        Refer parent class doc string
    
        Args:
            ScopeName (str): name of scope by user that was unsucessful in addition.
            
        Returns: None
        """
        
        message = f"{ScopeName} is in the Scope Archive but not in scope"

        Report(message, 'Error')
        
        super().__init__(message)
        
    def recorder(self, ScopeName:str) -> None:
        """
        This function is called when the exception steps are required and is cauhgt by the except block

        Args:
            ScopeName (str): name of scope by user that was unsucessful in addition.
            
        Returns: None
        """
        
        message = f"{ScopeName} is in the Scope Archive but not in scope"

        Report(message, 'Error')        

class MoreScopesThanIndex(Exception):
    """
    This Exception is raised when the code added new scope but Scope Index Archive didn't store

    Args:
        Exception (type: Not Valid): Not Valid
    """

    def __init__(self, ScopeName:str) -> None:
        """
        Refer parent class doc string
    
        Args:
            ScopeName (str): name of scope by user that was unsucessful in addition.
        
        Returns: None
        """
        
        message = f"{ScopeName} is in scope but not in the Scope Archives"

        Report(message, 'Error')
        
        super().__init__(message)   
        
    def recorder(self, ScopeName:str) -> None:
        """
        This function is called when the exception steps are required and is cauhgt by the except block

        Args:
            ScopeName (str): name of scope by user that was unsucessful in addition.
            
        Returns: None
        """
        
        message = f"{ScopeName} is in scope but not in the Scope Archives"

        Report(message, 'Error')

class SystemVariableAcessed(Exception):
    """
    This Exception is raised when the code tried to be add/update variable with the System Variable scope, which is illegal

    Args:
        Exception (type: Not Valid): Not Valid
    """

    def __init__(self) -> None:
        """
        Refer parent class doc string

        Returns: None
        """

        message = f"System Variable scope was given for creation of new variable or update of variable value."

        Report(message, 'Critical')

        super().__init__(message) 

    def recorder(self) -> None:
        """
        This function is called when the exception steps are required and is cauhgt by the except block

        Returns: None
        """

        message = f"System Variable scope was given for creation of new variable or update of variable value."

        Report(message, 'Critical')

        SystemShutdown()
        
class InvalidVariableLocation(Exception):
    """
    This Exception is raised when the code tried to be added/updated variable in invalid location within the scope

    Args:
        Exception (type: Not Valid): Not Valid
    """
    
    def __init__(self, variableName:str, scopeName:str, location:str, value:Any) -> None:
        """
        Refer parent class doc string

        Args:
            variableName (str): Name of variable that was tried to be added/updated
            scopeName (str): Name of scope that was tried to be added/updated
            location (str): Location within the scope that was tried to be added/updated
            value (Any): Value of variable given by user
            
        Returns: None
        """
        
        message = f"Variable '{variableName}' and/or its value, {value},  was tried to added/updated in {location} of {scopeName} but {location} is not valid"
        
        Report(message, 'Critical')
        
        super().__init__(message)
    
        
    def recorder(self, variableName:str, scopeName:str, location:str, value:Any) -> None:
        """
        This function is called when the exception steps are required and is cauhgt by the except block

        Args:
            variableName (str): Name of variable that was tried to be added/updated
            scopeName (str): Name of scope that was tried to be added/updated
            location (str): Location within the scope that was tried to be added/updated
            value (Any): Value of variable given by user
            
        Returns: Executes system.SystemShutdown()
        """
        
        message = f"Variable '{variableName}' and/or its value, {value},  was tried to added/updated in {location} of {scopeName} but {location} is not valid"
        
        Report(message, 'Critical')
        
        SystemShutdown()
        
class ScopeNotFound(Exception):
    """
    This Exception is raised when the code tried to be added/updated variable but provided scope is not found

    Args:
        Exception (type: Not Valid): Not Valid
    """
    
    def __init__(self, variableName:str, scopeName:str, value:Any) -> None:
        """
        Refer parent class doc string

        Args:
            variableName (str): Name of variable that was tried to be added/updated
            scopeName (str): Name of scope that was tried to be added/updated
            value (Any): Value of variable given by user
            
        Returns: None
        """
        
        message = f"Variable '{variableName}' and/or its value, {value},  was tried to added/updated in scope {scopeName} but scope {scopeName} is not found in scopeArchive."
        
        Report(message, 'Critical')
        
        super().__init__(message)
    
        
    def recorder(self, variableName:str, scopeName:str, value:Any) -> None:
        """
        This function is called when the exception steps are required and is cauhgt by the except block

        Args:
            variableName (str): Name of variable that was tried to be added/updated
            scopeName (str): Name of scope that was tried to be added/updated
            value (Any): Value of variable given by user
            
        Returns: Executes system.SystemShutdown()
        """
        
        message = f"Variable '{variableName}' and/or its value, {value},  was tried to added/updated in scope {scopeName} but scope {scopeName} is not found in scopeArchive."
        
        Report(message, 'Critical')
        
        SystemShutdown()
 



class InvalidParentScope(Exception):
    """
    This Exception is raised when the code tried to add new scope with invalid parent scope

    Args:
        Exception (type: Not Valid): Not Valid
    """
    
    def __init__(self, scopeName:str, parentScopeName:Any) -> None:
        """
        Refer parent class doc string

        Args:
            scopeName (str): Name of scope that was tried to be added
            parentScopeName (Any): Name of parent scope that was tried to be added
            
        Returns: None
        """
        
        message = f"Scope '{scopeName}' was tried to add with parent scope '{parentScopeName}' but '{parentScopeName}' is not valid value for parent scope"
        
        Report(message, 'Critical')
        
        super().__init__(message)
        
    def recorder(self, scopeName:str, parentScopeName:Any) -> None:
        """
        This function is called when the exception steps are required and is cauhgt by the except block
        
        Args:
            scopeName (str): Name of scope that was tried to be added
            parentScopeName (Any): Name of parent scope that was tried to be added
            
        Returns: Executes system.SystemShutdown()
        """
        
        message = f"Scope '{scopeName}' was tried to add with parent scope '{parentScopeName}' but '{parentScopeName}' is not valid value for parent scope"
        
        Report(message, 'Critical')
        
        SystemShutdown()
        

class ParentScopeNotFound(Exception):
    """
    This Exception is raised when the code tried to add new scope with parent scope that is not found in the scope archive

    Args:
        Exception (type: Not Valid): Not Valid
    """
    
    def __init__(self, scopeName:str, parentScopeName:Any) -> None:
        """
        Refer parent class doc string

        Args:
            scopeName (str): Name of scope that was tried to be added
            parentScopeName (Any): Name of parent scope that was not found in the scope archive
            
        Returns: None
        """
        
        message = f"Scope '{scopeName}' was tried to add with parent scope '{parentScopeName}' but '{parentScopeName}' is not found in the scope archive"
        
        Report(message, 'Critical')
        
        super().__init__(message)
        
    def recorder(self, scopeName:str, parentScopeName:Any) -> None:
        """
        This function is called when the exception steps are required and is cauhgt by the except block

        Args:
            scopeName (str): Name of scope that was tried to be added
            parentScopeName (Any): Name of parent scope that was not found in the scope archive
            
        Returns: Executes system.SystemShutdown()
        """
        
        message = f"Scope '{scopeName}' was tried to add with parent scope '{parentScopeName}' but '{parentScopeName}' is not found in the scope archive"
        
        Report(message, 'Critical')
        
        SystemShutdown()


def Report(message:str, level:str) -> None:
    """
    - This function logs the message with given level of importance

    - Code is sorted in aceding order of importance

    Args:
        message (str): The string that needs to be added to the log file
        level (str): level as decribed below
        
    - Levels:

        - Debug: This is for messages that are intended to be stored for research purposes of some part of code. It is not for error logging.

        - Info: It is general log message that is not negative - meaning not stored with unexpected result or event happens.

        - Warning: Use to warn bad event or result or use but is not error or exception or unexpected resulyt or event

        - Error: All errors inwhich rescue actions are available. For example upon unsucessful addtion of variable GarbageHandler() is available to rescue 

        - Critical: Severe Error ofwhich even rescue is not available or that crashes fundamental programs
    
    Returns: None
    """
    
    match level:

        case 'Debug':

            logger.debug(message)

        case 'Info':

            logger.info(message)

        case 'Warning':

            logger.warning(message)

        case 'Error':

            logger.error(message)

        case 'Critical':

            logger.critical(message)

        case other:

            logger.critical(f"Wrong level of log event giving -> {level} with message = {message}")


def _GetFullClassName(obj) -> str:
    """
    This is a helper to get the full name of object. For the context here, it gets the name of error with the external lib, if there is otherwise same.

    Args:
        obj (Any): Any object (usually error or Exception object)

    Returns:
        str: Full name of object with path, in terms of import sequence
    """
    
    module = obj.__class__.__module__
    
    if module is None or module == str.__class__.__module__: return str(obj.__class__.__name__)
    
    return str(module + '.' + obj.__class__.__name__)