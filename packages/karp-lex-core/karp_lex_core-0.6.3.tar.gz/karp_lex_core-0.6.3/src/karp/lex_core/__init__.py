__version__ = "0.6.3"  # noqa: D104

import warnings

from karp_lex_types import alias_generators, commands, dtos, value_objects
from karp_lex_types.dtos import EntryDto, GenericEntryDto

__all__ = [
    "EntryDto",
    "GenericEntryDto",
    "value_objects",
    "commands",
    "dtos",
    "alias_generators",
]

warnings.warn(
    "karp-lex-core is renamed to karp-lex-types, please update dependencies",
    DeprecationWarning,
    stacklevel=2,
)
