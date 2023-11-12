"""
# This loads the the TODO:lanuage file.
# Then selects codeblock or line and runs them in parell node
# To preserve the position cursor points to the code and gets updated via sibling nodes
"""

import DataType
from System import variables as sysVar # TODO Creation of System.py
import errorManager




class Variable:
    """
    It is class where programs Variables are hold
    """

    def __init__(self) -> None:
        """
        Initilizes the dict <scope> to hold all scopes and variables inside them
        Initilizes the dict <scopeArchive> to hold all the user names for scope and int id in the dict <scope>
        Initilizes the int <scopeCounter> to represent number of sucessful additional scopes in dict <scope>
        """

        # 0: Built in values of both Python & TODO:lanuage
        # 1: Variable outside any scope ie. Global
        # 2: Dict of code block names with unique int ID (2+)
        # for 2+ scope contains 2 dict:
            # enclosed: Enclosed variables
            # local: inside that code block
            # nest: empty by default; have id of nested codeblocks

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

        self.scopeArchive = {} # This holds the 

        self.scopeCounter = 0

    def ScopeAdder(self, name) -> bool:

        """
        Adds new element to self.scope representing new code block scope
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
                'nest': {}
            }

            self.scopeArchive[self.scopeCounter + 2] = name # Adding to Scope Archive with key Scope int val and value the user name of scope

            # Checks if len of Scopes is not equal to prev scopes + 2 default + 1 new scope. And if true raises MoreScopesIndex Error
            if not len(self.scopeArchive) == (self.scopeCounter + 3): raise errorManager.MoreScopesIndex()

        except errorManager.MoreScopesIndex:
            
            self.GarbageHandler(mode='unsucessful addition of Scope') # TODO: Creation of GarbageHandler with mode <unsucessful addition of Scope>

            return False

        except Exception as e:

            self.GarbageHandler(mode='Uknown error in addition of Scope') # TODO: Creation of GarbageHandler with mode <Uknown error in addition of Scope>

            errorManager.Report(f"<{e}> happened on addtion of {name} scope")

            return False
            
        
        self.scopeCounter += 1
        
        return True

