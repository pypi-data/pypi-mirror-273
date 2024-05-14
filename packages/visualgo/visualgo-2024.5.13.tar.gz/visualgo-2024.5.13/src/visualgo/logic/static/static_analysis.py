import ast
from dataclasses import dataclass

from .types import StaticSymbolDescription, StaticSymbolDescription, StaticBasicDescription, CodeVariablesAndUserFunctions
from ..types import SymbolDescription

import importlib

@dataclass
class StaticAnalysisRes:
    variables_user_functions: CodeVariablesAndUserFunctions

class StaticAnalyser:
    
    def __init__(self):
        self._visualgo_types = self._get_structure_types()

    def _get_structure_types(self):
        try:
            structure_module = importlib.import_module('visualgo.structures')
            structure_types = set()
            for name in dir(structure_module):
                attr = getattr(structure_module, name)
                if "class 'visualgo.structures." in str(attr):
                    structure_types.add(name)
            return structure_types
        except ImportError:
            print("Error: Could not import visualgo.structures module")
            return set()
    
    def __analyse_code_types(self, code: str) -> StaticAnalysisRes:
        tree = ast.parse(code)

        variables = []
        functions = []


        def traverse(node, level=-1, current_function='<module>'):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        variables.append(StaticSymbolDescription(SymbolDescription(target.id, current_function, level), True))
            elif isinstance(node, ast.FunctionDef):
                functions.append(StaticSymbolDescription(SymbolDescription(node.name, node.name, level), True))
                current_function = node.name  # Update current function name

            for child_node in ast.iter_child_nodes(node):
                traverse(child_node, level + 1, current_function)  # Pass current function name

        traverse(tree)


        user_functions = [f for f in functions]

        return StaticAnalysisRes(CodeVariablesAndUserFunctions(variables, user_functions))

    def get_code_variables_and_user_functions(self, code: str) -> CodeVariablesAndUserFunctions:
        """
        :demand: F.2.7
        """
        return self.__analyse_code_types(code).variables_user_functions

