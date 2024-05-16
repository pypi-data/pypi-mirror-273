"""Module to handle asset structure and storage"""

from abc import ABC
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from jautomate.enums import AssetType


@dataclass
class Asset(ABC):
    """
    Base class for our assets

    Args:
        asset_tag (str): Six digit asset tag number
        building (str): Three letter abbrevieated building label
        homeroom (str): Homeroom teachers name
        student_grade (str): Grade number -1 thru 12
        student_name (str): Student's full name
        owner (str): Asset owner (previously used for smart groups)
        serial_number (str): Serial Number of asset
        jamf_id (str): ID assigned by Jamf to the asset
    """

    asset_tag: str
    building: str
    homeroom: str
    student_grade: str
    student_name: str
    device_type: AssetType
    email_address: Optional[str] = None
    grad_year: Optional[str] = None
    jamf_id: Optional[str] = None
    owner: Optional[str] = None
    position: Optional[str] = None
    phone_number: Optional[str] = None
    serial_number: Optional[str] = None


@dataclass
class Assets():
    """
    Container to house the lists of assets.

    local will be the list of assets imported or created locally
    while remote is the response from the Jamf API of devices.
    """
    local: List[Asset] = field(default_factory=list)
    remote: List[Dict] = field(default_factory=list)


def check_jamf_ids_set(assets: List[Dict]) -> bool | list:
    missing = [asset for asset in assets if getattr(
        asset, 'jamf_id', None) is None]
    if not missing:
        return True
    return missing
