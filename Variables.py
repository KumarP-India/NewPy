"""
- This handles the variables in the the TODO:lanuage file.

Raises:
    errorManager.MoreScopesThanIndex: Refer to errorManager
    errorManager.MoreScopesIndex: Refer to errorManager

Returns:
    _type_: TODO: RETURN OR INTERFACE FUNCTION/CLASS
        
"""

from typing import Any

import DataType
from System import variables as sysVar, SystemShutdown # type:ignore :TODO: Creation of System.py
import errorManager




class Variable:
    """    
    It is class where programs Variables are hold
    """

    def __init__(self) -> None:
        """
        - Initilizes the dict <scope> to hold all scopes and variables inside them
        - Initilizes the dict <scopeArchive> to hold all the user names for scope and int id in the dict <scope>
        - Initilizes the int <scopeCounter> to represent number of sucessful additional scopes in dict <scope>

        Returns: None 
        """

        # 0: Built in values of both Python & TODO:lanuage
        # 1: Variable outside any scope ie. Global
        # for 1+ scope contains 3 dict:
            # enclosed: Enclosed variables
            # local: inside that code block
            # parent: empty by default; have id of parent codeblocks

        # Each dict having 2 dict:
            # key: To hold unique int ID to user variable name
            # val: To hold unique int ID's value

        self.scope = {
            0: {
                'key': sysVar.builtIn.key,
                'val': sysVar.builtIn.val
            },
            
            1: {
                'key': {},
                'val': {}
            }
        }

        self.scopeArchive = {} # This holds the int id and user scope name

        self.scopeCounter = 0

    def ScopeAdder(self, name:str, parent=None) -> bool:

        """
        Adds new element to self.scope representing new code block scope
        
        Args:
            name (str): It is the name of Scope by User that is requested to be added.

        Raises:
            errorManager.MoreScopesThanIndex: Refer to errorManager
            errorManager.MoreScopesIndex: Refer to errorManager

        Returns:
            bool: Its output describes wether the function was able to add it sucessfuly or not.
        """

        try: 

            self.scope[self.scopeCounter + 2] = {
                'enclosed': {
                    'key': {},
                    'val': {}
                },
                'local': {
                    'key': {},
                    'val': {}
                },
                'parent': parent
            }

            self.scopeArchive[name] = (self.scopeCounter + 2) # Adding to Scope Archive with value Scope int val and key the user name of scope

            # Checks if len of Scopes is not equal to prev scopes + 2 default + 1 new scope. And if true raises MoreScopesIndex Error
            if not len(self.scopeArchive) == (self.scopeCounter + 1): raise errorManager.MoreScopesThanIndex(name)
            if not len(self.scope) == (len(self.scopeArchive) + 2): raise errorManager.MoreScopesIndex(name)

        except (errorManager.MoreScopesIndex, errorManager.MoreScopesThanIndex):
            
            self.__GarbageHandler(mode='unsucessful addition of Scope')

            return False

        except Exception as e:

            self.__GarbageHandler(mode='Uknown error in addition of Scope', extraArgs=[errorManager._GetFullClassName(e), name])

            return False
                        
        
        self.scopeCounter += 1
        
        return True

    def VariableHandler(self, scopeName:str, location:str, variableName:str, value:Any) -> bool:

        newVariable = False

        if scopeName not in self.scopeArchive.values(): 
            
            if not self.ScopeAdder(scopeName): return False

            newVariable = True

        try:

            if not newVariable and variableName not in self.scope[self.scopeArchive[scopeName]] [location] [keys].keys():
            
                match location:

                    case 'enclosed':

                        self.scope[self.scopeArchive[scopeName]] ['enclosed'] ['key'] [variableName] = len(self.scope[self.scopeArchive[scopeName]] ['enclosed'] ['key'])

                        self.scope[self.scopeArchive[scopeName]] ['enclosed'] ['value'] [len(self.scope[self.scopeArchive[scopeName]] ['enclosed'] ['key']) - 1] = value

                    case 'local': # TODO: Write other case

                        self.scope[self.scopeArchive[scopeName]] ['local'] ['key'] [variableName] = len(self.scope[self.scopeArchive[scopeName]] ['local'] ['key'])

                        self.scope[self.scopeArchive[scopeName]] ['local'] ['value'] [len(self.scope[self.scopeArchive[scopeName]] ['local'] ['key']) - 1] = value

            else:

                match location:

                    case 'enclosed':
                        
                        iid = self.scope[self.scopeArchive[scopeName]] ['enclosed'] ['key'] [variableName]

                        self.scope[self.scopeArchive[scopeName]] ['enclosed'] ['value'] [iid] = value

                    case 'local': # TODO: Write other case

                        iid = self.scope[self.scopeArchive[scopeName]] ['local'] ['key'] [variableName]

                        self.scope[self.scopeArchive[scopeName]] ['local'] ['value'] [iid] = value

        except Exception as e: 
            
            iid = self.scope[self.scopeArchive[scopeName]] [location] ['key'] [variableName]
            
            val = self.scope[self.scopeArchive[scopeName]] [location] ['value'] [iid]
            
            self.__GarbageHandler(mode='Uknown error in changing the value of variable', extraArgs=[errorManager._GetFullClassName(e), scopeName, location, variableName, value, val])
            
            

    def __GarbageHandler(self, mode:str, extraArgs=None) -> None:
        """
        - This is Executing function for all actions related to deletion and maintainance of variables.


        Args:
            mode (str): described below
            extraArgs (List, optional): It is used as extra arguments when needed; every mode will list them below if they need it. Defaults to None.    
            
        - It consits of multiple modes, each performing required task.
            
            - unsucessful addition of Scope: This reduces the ScopeCounter or drops the latest scope
            
            - Uknown error in addition of Scope: 
                - This is situation when unexpected error happened and it reports and call to shutdown
                - Requires [Name of error, Scope name] in extraArgs
        
        Returns: None
        
        """

        match mode:

            case 'unsucessful addition of Scope': 
                
                sourceFound = True # This is used to track if scopeArchive or scope caused it.
                
                if len(self.scopeArchive) > self.scopeCounter: 
                    
                    for _ in range(self.scopeCounter - len(self.scopeArchive)):
                        _, scopeName = self.scopeArchive.popitem()
                        
                        errorManager.Report(f"Sucessfully deleted {scopeName} scope entry from scopeArchive", "Info")
                    
                    
                elif len(self.scopeArchive) == self.scopeCounter: sourceFound = False
                
                else: 
                
                    errorManager.Report(f"GarbageHandler found out the either scopeCounter is wrong or we lost {self.scopeCounter - len(self.scopeArchive)} scope index with count of {self.scopeCounter} and total index of {len(self.scopeArchive)}", 'Critical')
                    
                    SystemShutdown()
                
                
                if len(self.scope) > self.scopeCounter: 
                                        
                    for _ in range(self.scopeCounter - len(self.scopeArchive)):                    
                        _, scopeName = self.scope.popitem()
                        
                        errorManager.Report(f"Sucessfully deleted {scopeName} scope entry from scope", "Info")
                    
                    return
                
                
                if len(self.scope) == self.scopeCounter and sourceFound: return

                elif len(self.scope) == self.scopeCounter and not sourceFound: 
                
                    errorManager.Report("GarbageHandler did not found the problem in count of scopes oppsite to what caller claimed.", 'Critical')
                
                    
                else: 
                    
                    errorManager.Report(f"GarbageHandler found out the either scopeCounter is wrong or we lost {self.scopeCounter - len(self.scope)} scopes with count of {self.scopeCounter} and total scope of {len(self.scope)}", 'Critical')
                    
                    SystemShutdown()
                    
                    

            case 'Uknown error in addition of Scope':
                
                if extraArgs is None or not isinstance(extraArgs, list):
                    
                    errorManager.Report(f"Caller didn't provided which error happend and in addtion of which Scope", "Critical")
                                        
                elif not len(extraArgs) == 2: 
                    
                    errorManager.Report(f"Caller didn't provided which error happend and in addtion of which Scope", "Critical")
                                    
                else:
                    
                    errorManager.Report(f"During the addition of Scope {extraArgs[1]} - {extraArgs[0]} Exception happened", "Critical")
                
                SystemShutdown()
                
            
            case 'Uknown error in changing the value of variable':
                
                # Create this as copy of Unknow error in addition of Scope but as changing the value and variables. Also use all the extraArgs in the message
                
                if extraArgs is None or not isinstance(extraArgs, list):
                    
                    errorManager.Report(f"Caller didn't provided which error happend and in changing the value of which variable in which Scope", "Critical")
                                        
                elif not len(extraArgs) == 6: 
                    
                    errorManager.Report(f"Caller didn't provided which error happend and in changing the value of which variable in which Scope", "Critical")
                                    
                elif extraArgs[5] == extraArgs[4]:
                    
                    errorManager.Report(f"During the changing the value of variable {extraArgs[3]} in {extraArgs[2]} inside {extraArgs[1]} - {extraArgs[0]} Exception happened; The stored value is: {extraArgs[5]} and required value was: {extraArgs[4]}", "Error")
                
                    return
                
                else:
                    
                    errorManager.Report(f"During the changing the value of variable {extraArgs[3]} in {extraArgs[2]} inside {extraArgs[1]} - {extraArgs[0]} Exception happened; The stored value is: {extraArgs[5]} and required value was: {extraArgs[4]}", "Critical")
                
                    SystemShutdown()
                
#   # errorManager._GetFullClassName(e), 
    # scopeName, l
    # ocation, 
    # variableName,
    # value, 
    # val])

                
                

            case other:

                ... # TODO: Add this mode after creation of all grabage