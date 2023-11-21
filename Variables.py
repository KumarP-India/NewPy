"""
- This handles the variables in the the TODO:lanuage file.

Raises: 
    - Not fully, but difrent errors are raised in difrent situations.
    - Which trigers difrent actions defined in except blocks.
    - And VariableErrorManager file logs every one of them.

Returns:
    _type_: TODO: RETURN OR INTERFACE FUNCTION/CLASS
        
"""

from typing import Any, List, Union

import DataType
from System import variables as sysVar, SystemShutdown # type:ignore :TODO: Creation of System.py
import VariableErrorManager




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

        # Each dict having 4 dict:
            # key: To hold unique int ID to user variable name
            # val: To hold unique int ID's value
            # age: To hold unique int ID's age ie. about of minor garbage collection it survived
            # acessed: To hold no. of unique int ID variable has been acessed for garbage collection

        self.scope = {
            0: {
                'key': sysVar.builtIn.key,
                'val': sysVar.builtIn.val
            },
            
            1: {
                'key': {},
                'val': {},
                'age': {},
                'acessed': {}
            }
        }

        self.scopeArchive = {}

        self.scopeCounter = 0


    def ScopeAdder(self, name:str, parent=None) -> Union[bool, int]:
        """
        This function is used to add new scope in the scope dict and scopeArchive
        
        Args:
        
            name (str): This is the name of scope given by user.   
            parent (int, optional): This is the id of parent scope. Defaults to None.
            
        Raises:
        
            VariableErrorManager.MoreScopesThanIndex: Refer to VariableErrorManager
            VariableErrorManager.MoreScopesIndex: Refer to VariableErrorManager
            VariableErrorManager.InvalidParentScope: Refer to VariableErrorManager
            VariableErrorManager.ParentScopeNotFound: Refer to VariableErrorManager
            
        Returns:
            bool: Its output describes wether the function was able to add it sucessfuly or not.
            or
            int: It returns the id of newly added scope.
        """
        # for all return True replace it with the value of Scope int id
        newScopeID = False
        
        try: 
            
            if isinstance(parent, int) and parent is not None: 
                raise VariableErrorManager.InvalidParentScope(name, parent)
            
            if parent is not None and parent not in self.scopeArchive.values(): 
                raise VariableErrorManager.ParentScopeNotFound(name, parent)

            self.scope[self.scopeCounter + 2] = {
                'enclosed': {
                    'key': {},
                    'val': {}, 
                    'age': {},
                    'acessed': {}
                },
                'local': {
                    'key': {},
                    'val': {},
                    'age': {},
                    'acessed': {}
                },
                'parent': parent
            }
            
            newScopeID = self.scopeCounter + 2

            self.scopeArchive[name] = (newScopeID) # Adding to Scope Archive with value Scope int val and key the user name of scope

            # Checks if len of Scope Archive is not equal to previous scope Counter + 1. And if true raises MoreScopesThanIndex Error
            if not len(self.scopeArchive) == (self.scopeCounter + 1): raise VariableErrorManager.MoreScopesThanIndex(name)
            
            # Checks if len of Scopes is not equal to just verified scope Archive + 2 default scopes. And if true raises MoreScopesIndex Error
            if not len(self.scope) == (len(self.scopeArchive) + 2): raise VariableErrorManager.MoreScopesIndex(name)


        except (VariableErrorManager.InvalidParentScope, VariableErrorManager.ParentScopeNotFound) as e:
            
            e.recorder(name, parent)


        except (VariableErrorManager.MoreScopesIndex, VariableErrorManager.MoreScopesThanIndex) as e:
            
            e.recorder(name)
            
            self.__GarbageHandler(mode='unsucessful addition of Scope')

            return False


        except Exception as e:

            self.__GarbageHandler(mode='Uknown error in addition of Scope', extraArgs=[VariableErrorManager._GetFullClassName(e), name])

            return False
                        
        
        self.scopeCounter += 1
        
        return newScopeID


    def VariableHandler(self, scopeName:str, location:str, variableName:str, value:Any) -> bool:
        """
        This function is used to add and change the value of variables in the scope.

        Args:
            scopeName (str): This is the name of scope given by user where variable is to be added or changed.
            
            location (str): 
                - This is the location of variable in the scope. It can be 'enclosed' or 'local'. 
                
                - However, if scopeName is 'Global' then it is ignored.
                
            variableName (str): This is the name of variable given by user.
            
            value (Any): This is the value of variable given by user.

        Raises:
            VariableErrorManager.InvalidVariableLocation: Refer to VariableErrorManager

        Returns:
            bool: Its output describes wether the function was able to add it sucessfuly or not.
        """
        
        if scopeName == "1":
            raise VariableErrorManager.SystemVariableAcessed()
        
        try:
        
            if scopeName == 'Global':
                
                # 1 is the scope ID of global
                
                # Check if the variable provied is in the Global scope or not and if not then add it to Global scope else upadte value of variable, please
                if variableName not in self.scope[1] ['key'].keys():
                        
                        self.scope[1] ['key'] [variableName] = len(self.scope[1] ['key'])
                        self.scope[1] ['val'] [len(self.scope[1] ['key']) - 1] = value
                        self.scope[1] ['age'] [len(self.scope[1] ['key']) - 1] = 0
                        self.scope[1] ['acessed'] [len(self.scope[1] ['key']) - 1] = 0
                        
                        return True
                
                intIDofVariable = self.scope[1] ['key'] [variableName] # Int ID of Variable
                
                self.scope[1] ['val'] [intIDofVariable] = value
                
                return True
                
                
            if location not in ['enclosed', 'local']: raise VariableErrorManager.InvalidVariableLocation(variableName, scopeName, location, value)
            
            if scopeName not in self.scopeArchive.keys(): raise VariableErrorManager.ScopeNotFound(variableName, scopeName, value)
                
            # use same scopeID to get the scope int id from scopeArchive if scope exsits, please
            scopeID = self.scopeArchive[scopeName]
                            
            if variableName not in self.scope[scopeID] [location] ['key'].keys():
            
                self.scope[scopeID] [location] ['key'] [variableName] = len(self.scope[scopeID] [location] ['key'])

                self.scope[scopeID] [location] ['value'] [len(self.scope[scopeID] [location] ['key']) - 1] = value
                
                self.scope[scopeID] [location] ['age'] [len(self.scope[scopeID] [location] ['key']) - 1] = 0
                
                self.scope[scopeID] [location] ['acessed'] [len(self.scope[scopeID] [location] ['key']) - 1] = 0

            else:
                        
                intIDofVariable = self.scope[scopeID] [location] ['key'] [variableName] # Int ID of Variable

                self.scope[scopeID] [location] ['value'] [intIDofVariable] = value
                    
                
        except VariableErrorManager.SystemVariableAcessed as e: 
            
            # call recoder funtion
            e.recorder()
        
        except VariableErrorManager.InvalidVariableLocation as e: 
            
            # call recoder funtion
            e.recorder(variableName, scopeName, location, value)
        
        except VariableErrorManager.ScopeNotFound as e: 
            
            # call recoder funtion
            e.recorder(variableName, scopeName, value)
            

        except Exception as e: 
            
            scopeID = self.scopeArchive[scopeName]
            
            intIDofVariable = self.scope[scopeID] [location] ['key'] [variableName] # Int ID of Variable
            
            val = self.scope[scopeID] [location] ['value'] [intIDofVariable]
            
            self.__GarbageHandler(mode='Uknown error in changing the value of variable', extraArgs=[VariableErrorManager._GetFullClassName(e), scopeName, location, variableName, value, val])
            
            return False
            
        return True  

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
                
            - Uknown error in changing the value of variable:
            
                - This is situation when unexpected error happened and it reports and call to shutdown
                - Requires [Name of error, Scope name, location, variable name, value, stored value] in extraArgs
        
        Returns: None or executes system.SystemShutdown()
        
        """

        match mode:

            case 'unsucessful addition of Scope': 
                
                sourceFound = True # This is used to track if scopeArchive or scope caused it.
                
                if len(self.scopeArchive) > self.scopeCounter: 
                    
                    for _ in range(self.scopeCounter - len(self.scopeArchive)):
                        _, scopeName = self.scopeArchive.popitem()
                        
                        VariableErrorManager.Report(f"Sucessfully deleted {scopeName} scope entry from scopeArchive", "Info")
                    
                    
                elif len(self.scopeArchive) == self.scopeCounter: sourceFound = False
                
                else: 
                
                    VariableErrorManager.Report(f"GarbageHandler found out the either scopeCounter is wrong or we lost {self.scopeCounter - len(self.scopeArchive)} scope index with count of {self.scopeCounter} and total index of {len(self.scopeArchive)}", 'Critical')
                    
                    SystemShutdown()
                
                
                if len(self.scope) > self.scopeCounter: 
                                        
                    for _ in range(self.scopeCounter - len(self.scopeArchive)):                    
                        _, scopeName = self.scope.popitem()
                        
                        VariableErrorManager.Report(f"Sucessfully deleted {scopeName} scope entry from scope", "Info")
                    
                    return
                
                
                if len(self.scope) == self.scopeCounter and sourceFound: return

                elif len(self.scope) == self.scopeCounter and not sourceFound: 
                
                    VariableErrorManager.Report("GarbageHandler did not found the problem in count of scopes oppsite to what caller claimed.", 'Critical')
                
                    
                else: 
                    
                    VariableErrorManager.Report(f"GarbageHandler found out the either scopeCounter is wrong or we lost {self.scopeCounter - len(self.scope)} scopes with count of {self.scopeCounter} and total scope of {len(self.scope)}", 'Critical')
                    
                    SystemShutdown()
                    
                    

            case 'Uknown error in addition of Scope':
                
                if extraArgs is None or not isinstance(extraArgs, list):
                    
                    VariableErrorManager.Report(f"Caller didn't provided which error happend and in addtion of which Scope", "Critical")
                                        
                elif not len(extraArgs) == 2: 
                    
                    VariableErrorManager.Report(f"Caller didn't provided which error happend and in addtion of which Scope", "Critical")
                                    
                else:
                    
                    VariableErrorManager.Report(f"During the addition of Scope {extraArgs[1]} - {extraArgs[0]} Exception happened", "Critical")
                
                SystemShutdown()
                
            
            case 'Uknown error in changing the value of variable':
                
                # Create this as copy of Unknow error in addition of Scope but as changing the value and variables. Also use all the extraArgs in the message
                
                if extraArgs is None or not isinstance(extraArgs, list):
                    
                    VariableErrorManager.Report(f"Caller didn't provided which error happend and in changing the value of which variable in which Scope", "Critical")
                                        
                elif not len(extraArgs) == 6: 
                    
                    VariableErrorManager.Report(f"Caller didn't provided which error happend and in changing the value of which variable in which Scope", "Critical")
                                    
                elif extraArgs[5] == extraArgs[4]:
                    
                    VariableErrorManager.Report(f"During the changing the value of variable {extraArgs[3]} in {extraArgs[2]} inside {extraArgs[1]} - {extraArgs[0]} Exception happened; The stored value is: {extraArgs[5]} and required value was: {extraArgs[4]}", "Error")
                
                    return
                
                else:
                    
                    VariableErrorManager.Report(f"During the changing the value of variable {extraArgs[3]} in {extraArgs[2]} inside {extraArgs[1]} - {extraArgs[0]} Exception happened; The stored value is: {extraArgs[5]} and required value was: {extraArgs[4]}", "Critical")
                
                    SystemShutdown()

                
                

            case other:
                
                # Use Report function and report it as Critical error and call to shutdown
                
                VariableErrorManager.Report(f"GarbageHandler was called with unknown mode: {other}", "Critical")
                
                SystemShutdown()

          
          
    # Interfaces for VariableHandler
    
    def AgePointerInterface(self, work:str, variable: List[Union[int, str]]):
        # variable = [varID, location, scope id or parent id, age, acessed]
        # check if variable has elements int, str, int, int, int
        if not isinstance(variable, list) or \
            not len(variable) == 4 or \
                not isinstance(variable[0], int) or \
                    not isinstance(variable[1], str) or \
                        not isinstance(variable[2], int) or \
                            not isinstance(variable[3], int) or \
                                not isinstance(variable[4], int): return
                                
                                # TODO: Raise error of wrong variable format
                                                       
        # TODO: create other errors
        match work:
            
            case 'increase age':
                
                while self.scope[variable[2]] ['parent']:
                    
                    variable[2] = self.scope[variable[2]] ['parent']
                    
                # I need to increase self.scope[variable[2]] [variable[1]] ['age'] [variable[0]] by 1
                self.scope[variable[2]] [variable[1]] ['age'] [variable[0]] += 1
                
            case 'increase acessed':
                
                while self.scope[variable[2]] ['parent']:
                    
                    variable[2] = self.scope[variable[2]] ['parent']
                    
                # I need to increase self.scope[variable[2]] [variable[1]] ['acessed'] [variable[0]] by 1
                self.scope[variable[2]] [variable[1]] ['acessed'] [variable[0]] += 1
                
                                   
                
      
                
class GarbageMan:
    
    #TODO: Create this class and its functions to act as garbage collector for variables
    # TODO: Create doc string for this class

    """refer to ./Garbagediscusion.txt"""

    def __init__(self, variableObject: Variable) -> None:
        """
        - Initilizes the list <minor> to hold all the variables which are young or new for garbage collection.
        - Initilizes the list <neutral> to hold all the variables which survived minor garbage collection.
        - Initilizes the list <major> to hold all the variables which survived major neutral collection.

        Args:
            variableHandlerInterface (Variable Class): TO handle Variables in the user file.
            
        Returns: None
        """

        self.minor = []

        self.neutral = []

        self.major = []

        self.variableWoman = variableObject
        
        # TODO: Each element will be [variable int, location, scope int or parent int, age, acessed]

    def CollectGarbage(self) -> None:
        """
        - This function implements the logic of garbage collection.
        TODO: Add logic
        
        Returns: None
        """

        self.minor = [item for item in self.minor if item is not None]

        for i in self.minor:

            self.variableWoman.AgePointerInterface(work='increase age', variable=i) # TODO: Create this interface <---
            
            # TODO: finish this with some logic about clearing.