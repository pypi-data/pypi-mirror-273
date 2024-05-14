import typing
from dataclasses import dataclass

from ..types import SymbolDescription

@dataclass
class TransferVariable:
    description: SymbolDescription
    value: typing.Any


@dataclass
class TransferVariables:
    variables: typing.List[TransferVariable]
