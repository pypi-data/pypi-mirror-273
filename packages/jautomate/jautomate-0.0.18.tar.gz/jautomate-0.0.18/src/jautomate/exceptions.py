"""Exceptions for jautomate"""

from jautomate.models import Asset


class JautomateException(Exception):
    """
    Base Exception for Jautomate
    """


class JautomateAssetException(JautomateException):
    """
    Base Exception for Jautomate
    """

    def __init__(self, message: str, asset: Asset | None = None):
        super().__init__(message)
        self.asset = asset
