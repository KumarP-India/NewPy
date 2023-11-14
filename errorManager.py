"""
This is responsible to log error or warning events and holds custom Exception
"""

import logging

logging.basicConfig(filename="Log.log",
                    format='%(asctime)s: [%(levelname)s] %(message)s',
                    filemode='w')

logger = logging.getLogger()

class MoreScopesIndex(Exception): 
    """
    This Exceptions is raised when the code tried to add new scope but the addtions didn't increased the number of scopes
    """

    def __init__(self, ScopeName) -> None:
        
        self.name = ScopeName
        
        message=f"{self.ScopeName} is in the Scope Archive but not in scope"

        Report(message, 'Error')
        
        super().__init__(message)

class MoreScopesThanIndex(Exception):
    """
    This Exception is raised when the code added new scope but Scope Index Archive didn't store
    """

    def __init__(self, ScopeName) -> None:
        
        self.name = ScopeName
        
        message=f"{self.ScopeName} is in scope but not in the Scope Archives"

        Report(message, 'Error')
        
        super().__init__(message)   


def Report(message, level) -> None:
    """
    # This function logs the message with given level of importance

    # Code is sorted in aceding order of importance

    # Levels:

        Debug: This is for messages that are intended to be stored for research purposes of some part of code. It is not for error logging.

        Info: It is general log message that is not negative - meaning not stored with unexpected result or event happens.

        Warning: Use to warn bad event or result or use but is not error or exception or unexpected resulyt or event

        Error: All errors inwhich rescue actions are available. For example upon unsucessful addtion of variable GarbageHandler() is available to rescue 

        Critical: Severe Error ofwhich even rescue is not available or that crashes fundamental programs
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





