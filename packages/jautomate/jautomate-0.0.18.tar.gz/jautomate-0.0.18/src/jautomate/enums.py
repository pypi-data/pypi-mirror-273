"""Enums for jautomate"""

from enum import Enum


class AssetType(str, Enum):
    """
    Enum to assign asset type in standardized way.

    Used to define cli arguments for various commands and set as part of
    each Asset to determine their type if needed.
    """

    MOBILE = 'mobile'
    COMPUTER = 'computer'
    CHROMEBOOK = 'chromebook'
