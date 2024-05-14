from dataclasses import dataclass

from ..types import SymbolDescription

@dataclass
class StaticSymbolDescription:
    description: SymbolDescription
    is_shown: bool

@dataclass
class StaticBasicDescription:
    name: str
    is_shown: bool

@dataclass
class CodeVariablesAndUserFunctions:
    variables: list[StaticSymbolDescription] 
    user_functions: list[StaticSymbolDescription] # will ignore all variables defined in this user code function