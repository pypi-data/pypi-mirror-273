"""Functions for devices."""

import datetime
from typing import Dict, List
from jps_api_wrapper.request_builder import (
    ClientError, NotFound, RequestConflict, RequestTimedOut, InvalidDataType
)
from jautomate.api import jamf_p, jamf_c
from jautomate.exceptions import JautomateAssetException, JautomateException
from jautomate.logger import j_logger
from jautomate.models import Asset
from jautomate.actions import get_building_id

# #################################
# Mobile Device functions
# #################################


def get_mobile_device_by_serial_number(serial_number: str) -> Dict:
    try:
        response = jamf_c.get_mobile_device(serialnumber=serial_number)

    except (ClientError, NotFound, RequestConflict, RequestTimedOut, InvalidDataType) as e:
        raise JautomateException("Error communicating with Jamf") from e

    return response


def get_jamf_id_of_mobile_device(serial_number: str) -> Dict:
    mobile_device = get_mobile_device_by_serial_number(serial_number)

    return str(mobile_device.get('mobile_device').get('general').get('id'))


def build_mobile_payload(asset: Asset) -> Dict:
    payload = {
        "enforceName": True,
        "location": {},
        "updatedExtensionAttributes": [],
    }

    if getattr(asset, 'asset_tag', None):
        payload["name"] = asset.asset_tag
        payload["assetTag"] = asset.asset_tag

    # Unset values if no user is passed, typically during an unassign action
    if asset.user is None:
        payload["location"]["realName"] = " "
        payload["location"]["emailAddress"] = " "
        payload["location"]["username"] = " "
        payload["location"]["room"] = " "
        payload["location"]["buildingId"] = None
        payload["location"]["position"] = " "
        payload["location"]["phoneNumber"] = " "

        payload["updatedExtensionAttributes"].append(
            {
                "name": "Grade",
                "value": None,
            }
        )
        payload["updatedExtensionAttributes"].append(
            {
                "name": "Owner",
                "value": None,
            }
        )
        payload["updatedExtensionAttributes"].append(
            {
                "name": "GradYear",
                "value": None,
            }
        )
        payload["updatedExtensionAttributes"].append(
            {
                "name": "Last Sync",
                "value": [datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")],
            }
        )
        return payload

    # Begin checking for user attributes
    if getattr(asset.user, 'full_name', None):
        payload["location"]["realName"] = asset.user.full_name

    if getattr(asset.user, 'email', None):
        payload["location"]["emailAddress"] = asset.user.email

    if getattr(asset.user, 'username', None):
        payload["location"]["username"] = asset.user.username

    if getattr(asset.user, 'position', None):
        payload["location"]["position"] = asset.user.position

    if getattr(asset.user, 'phone_number', None):
        payload["location"]["phoneNumber"] = asset.user.phone_number

    if getattr(asset.user, 'building', None):
        payload["location"]["buildingId"] = get_building_id(asset.user.building)

    if getattr(asset.user, 'homeroom', None):
        payload["location"]["room"] = asset.user.homeroom

    if getattr(asset.user, 'grade', None):
        payload["updatedExtensionAttributes"].append(
            {
                "name": "Grade",
                "value": [asset.user.grade],
            }
        )
    if getattr(asset.user, 'grad_year', None):
        payload["updatedExtensionAttributes"].append(
            {
                "name": "GradYear",
                "value": [asset.user.grad_year],
            }
        )
    if getattr(asset.user, 'owner', None):
        payload["updatedExtensionAttributes"].append(
            {
                "name": "Owner",
                "value": [asset.user.owner],
            }
        )
    # Set Last Sync time
    payload["updatedExtensionAttributes"].append(
        {
            "name": "Last Sync",
            "value": [datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")],
        }
    )

    return payload


# #################################
# Computer Device functions
# #################################
def build_computer_extension_attribute(extension_id: str, name: str, values: List) -> Dict:
    if isinstance(values, str):
        values = [values]

    extension_attribute = {
        "definitionId": extension_id,
        "name": name,
        "values": values
    }
    return extension_attribute


def build_computer_payload(asset: Asset) -> Dict:
    """Use entire asset object ^ because there may be additional fields we want to sync later"""

    payload = {
        "general": {
            "assetTag": ""
        },
        "userAndLocation": {
            "extensionAttributes": []
        }
    }

    # Set Asset Tag
    if getattr(asset, 'asset_tag', None):
        payload["general"]["assetTag"] = asset.asset_tag

    # Unset values if no user is passed, typically during an unassign action
    if asset.user is None:

        payload["userAndLocation"]["realname"] = ""
        payload["userAndLocation"]["email"] = ""
        payload["userAndLocation"]["position"] = ""
        payload["userAndLocation"]["phone"] = ""
        payload["userAndLocation"]["buildingId"] = None
        payload["userAndLocation"]["room"] = ""
        payload["userAndLocation"]["username"] = ""
        payload["userAndLocation"]["extensionAttributes"].append(
            build_computer_extension_attribute("3", "GradYear", [])
        )
        payload["userAndLocation"]["extensionAttributes"].append(
            build_computer_extension_attribute("4", "Grade", [])
        )
        payload["userAndLocation"]["extensionAttributes"].append(
            build_computer_extension_attribute(
                "5", "Last Sync", datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")))
        payload["userAndLocation"]["extensionAttributes"].append(
            build_computer_extension_attribute("6", "Floor", [])
        )
        return payload

    # Begin checking for user attributes
    if getattr(asset.user, 'full_name', None):
        payload["userAndLocation"]["realname"] = asset.user.full_name

    if getattr(asset.user, 'email', None):
        payload["userAndLocation"]["email"] = asset.user.email

    if getattr(asset.user, 'username', None):
        payload["userAndLocation"]["username"] = asset.user.username

    if getattr(asset.user, 'position', None):
        payload["userAndLocation"]["position"] = asset.user.position

    if getattr(asset.user, 'phone_number', None):
        payload["userAndLocation"]["phone"] = asset.user.phone_number

    if getattr(asset.user, 'building', None):
        payload["userAndLocation"]["buildingId"] = get_building_id(asset.user.building)

    if getattr(asset.user, 'homeroom', None):
        payload["userAndLocation"]["room"] = asset.user.homeroom

    if getattr(asset.user, 'grad_year', None):
        payload["userAndLocation"]["extensionAttributes"].append(
            build_computer_extension_attribute("3", "GradYear", [asset.user.grad_year])
        )
    if getattr(asset.user, 'grade', None):
        payload["userAndLocation"]["extensionAttributes"].append(
            build_computer_extension_attribute("4", "Grade", [asset.user.grade])
        )
    if getattr(asset.user, 'floor', None):
        payload["userAndLocation"]["extensionAttributes"].append(
            build_computer_extension_attribute("6", "Floor", [asset.user.floor])
        )
    # Set last sync because we are modifying the record
    payload["userAndLocation"]["extensionAttributes"].append(
        build_computer_extension_attribute(
            "5", "Last Sync", datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")))

    return payload


def get_computer_record_by_serial_number(serial_number: str) -> Dict:
    """
    Gets Jamf record of single computer asset based on asset tag

    Args:   asset_tag (str): Asset tag of computer

    Raises: JautomateException: Raised if no computer records found

    Returns:    List[Dict]: List of dictionaries where each dict is a computer asset
    """

    endpoint_filter = f'hardware.serialNumber==\"{serial_number}\"'

    try:
        response = jamf_p.get_computer_inventories(filter=endpoint_filter)

    except (ClientError, NotFound, RequestConflict, RequestTimedOut, InvalidDataType) as e:
        raise JautomateException("Error communicating with Jamf") from e

    if response["totalCount"] >= 1:
        if response["totalCount"] > 1:
            j_logger.warning(
                "Multiple computer records found with serial number %s. "
                "Only the first record will be returned", serial_number)

        return response["results"][0]

    raise JautomateException(f"Computer with serial number {serial_number} not found in Jamf")


def get_jamf_id_of_computer(serial_number: str) -> str:
    computer = get_computer_record_by_serial_number(serial_number)
    return computer.get('id')


# #########################
# Update Functions
# #########################


def build_update_payload(asset: Asset) -> Dict | None:
    if asset.device_type.value == 'mobile':
        return build_mobile_payload(asset)
    if asset.device_type.value == 'computer':
        return build_computer_payload(asset)
    return None


def update_device(asset: Asset) -> None:
    if asset.jamf_id is None or asset.jamf_id == "":
        raise JautomateAssetException("Jamf ID not set", asset)

    payload = build_update_payload(asset)

    if payload is None:
        raise JautomateAssetException("Update payload not set", asset)

    try:
        if asset.device_type.value == 'computer':
            jamf_p.update_computer_inventory(payload, asset.jamf_id)
            j_logger.info("Computer Asset: %s Ok", asset.asset_tag)

        if asset.device_type.value == 'mobile':
            jamf_p.update_mobile_device(payload, asset.jamf_id)
            j_logger.info("Mobile Asset: %s Ok", asset.asset_tag)

    except (ClientError, NotFound, RequestConflict, RequestTimedOut) as e:
        raise JautomateException("Error communicating with Jamf") from e

    except InvalidDataType as e:
        raise JautomateException(
            "Invalid Data sent to Jamf. Check the payload was properly formed") from e
