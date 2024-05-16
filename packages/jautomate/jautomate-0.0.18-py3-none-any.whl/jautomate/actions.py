"""Module to handle various actions performed with Jamf"""

import datetime
from typing import Dict, List
from jautomate.api import jamf_p, jamf_c
from jautomate.assets import Asset, Assets
from jautomate.exceptions import JautomateException
from jautomate.logger import j_logger
from jautomate import utils


def get_all_mobile_devices_pro() -> List[Dict]:
    """
    Returns dict of all mobile devices from Jamf using Pro API

    Returns:
        List[Dict]: List of all mobile devices from Jamf Pro API
    """
    # Pro API max page size is 2000
    page_size = 2000
    page = 0
    # remaining_results needs to be higher than the total amount of devices
    remaining_results = 10000
    device_list = []
    while remaining_results > 0:
        response = jamf_p.get_mobile_devices(
            page=page, page_size=page_size)

        if remaining_results == 10000:
            remaining_results = int(response['totalCount']) - page_size
        else:
            remaining_results -= page_size

        device_list.extend(response['results'])
        page += 1
    return device_list


def get_all_mobile_devices() -> List[Dict]:
    """
    Returns all mobile devices from Jamf Classic API

    This function looks for a saved search on Jamf that is
    set up return only Jamf ID, Serial Number, and Asset Tag.
    The name used was 'All iPads by Asset Tag'.

    This is done because Jamf does not include asset tag in their
    default information that gets returned. A custom search number be
    saved first from the Jamf Pro GUI.

    Also, note the structure of the response that is returned as there
    is a lot of other unneeded info returned with the saved search.

    Returns:
        List[Dict]: List of Dicts for all mobile devices on Jamf.
    """
    response = jamf_c.get_advanced_mobile_device_search(
        name='All iPads by Asset Tag',
        data_type='json')
    return response['advanced_mobile_device_search']['mobile_devices']


def get_mobile_device_jamf_ids_by_serial_number(asset_list: Assets) -> Assets:
    """
    Gets the Jamf IDs of the local assets by checking the serial number against those in Jamf.

    Compares the serial numbers of local assets to those retrieved from Jamf servers
    and sets the jamf_id proptery of each asset object. This is done because most of the
    Jamf API endpoints work off of the id jamf gives each asset.

    This is used when assigning assets as the serial numbers are typically more
    accurate of a comparison when assigning

    Args:
        asset_list (Assets): Obj of assets being worked with. See Assets class for structure.

    Returns:
        Assets: Asset object with lists of both local and remote assets
    """
    serial_format = utils.determine_serial_number_key_format(
        asset_list.remote[0])

    for asset in asset_list.local:
        matching_device = next(
            (device for device in asset_list.remote
                if device[serial_format] == asset.serial_number), None)
        if matching_device:
            asset.jamf_id = matching_device['id']
    return asset_list


def get_mobile_device_jamf_ids_by_asset_tag(asset_list: Assets) -> Assets:
    """
    Gets the Jamf IDs of the local assets by checking the asset tag against those in Jamf.

    Compares the asset tags of local assets to those retrieved from Jamf servers
    and sets the jamf_id proptery of each asset object.

    This is used mostly for unassigning assets where it is more likely the
    asset tag has been set and is accurate.

    Args:
        asset_list (Assets): Obj of assets being worked with. See Assets class for structure.

    Returns:
        Assets: Asset object with lists of both local and remote assets
    """
    for asset in asset_list.local:
        matching_device = next(
            (device for device in asset_list.remote
                if device['Asset_Tag'] == asset.asset_tag), None)
        if matching_device:
            asset.jamf_id = matching_device['id']
            # This isn't ideal, but we need to sync the serial
            # number so it stays in jamf
            if asset.serial_number is None:
                asset.serial_number = matching_device['Serial_Number']
    return asset_list


def get_building_id(building_name: str) -> str:
    """
    Gets building Id used by Jamf from string abbreviation

    Args:
        building_name (str): String abbreviation of building

    Returns:
        String: String representation of building ID number
    """

    response = jamf_p.get_buildings()
    jamf_buildings = []
    jamf_buildings.extend(response['results'])
    found_buildings = [building['id']
                       for building in jamf_buildings if building['name'] == building_name]

    return found_buildings[0] if len(found_buildings) > 0 else None


def sync_assets_to_jamf(asset_list: List[Asset]) -> None:
    """
    Syncs data from local assets to Jamf Pro server.

    Structure of payload can be found on Jamf's API doc:
    https://developer.jamf.com/jamf-pro/reference/patch_v2-mobile-devices-id
    https://developer.jamf.com/jamf-pro/reference/patch_v1-computers-inventory-detail-id

    Args:
        asset_list (Assets): Obj of assets being worked with.
            See Assets class for structure.
    """
    j_logger.debug('Syncing assets to Jamf')
    error_count = 0
    for asset in asset_list:
        if asset.jamf_id is None or asset.jamf_id == "":
            j_logger.error('Asset skipped. Not found in Jamf:')
            j_logger.error('%s \n', asset)
            error_count += 1
            continue
        if asset.building is None or asset.building == "":
            j_logger.error('Asset skipped. Building not set:')
            j_logger.error('%s \n', asset)
            error_count += 1
            continue

        # Process for mobile devices
        if asset.device_type == 'mobile':
            payload = {
                "location": {
                    "realName": asset.student_name,
                    "emailAddress": asset.email_address,
                    "room": asset.homeroom,
                    "buildingId": get_building_id(asset.building),
                    "position": "",
                    "phoneNumber": "",
                },
                "updatedExtensionAttributes": [
                    {
                        "name": "Grade",
                        "value": [asset.student_grade],
                    },
                    {
                        "name": "Owner",
                        "value": [asset.owner],
                    },
                    {
                        "name": "GradYear",
                        "value": [asset.grad_year],
                    },
                    {
                        "name": "Last Sync",
                        "value": [datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")],
                    }
                ],
                # This is set because it allows techs to see asset tag from settings on device
                "name": asset.asset_tag,
                "enforceName": True
            }

            jamf_p.update_mobile_device(payload, asset.jamf_id)
            j_logger.info("Asset: %s Ok", asset.asset_tag)

        # Process for computers
        if asset.device_type == 'computer':
            payload = {
                "userAndLocation": {
                    "realname": asset.student_name,
                    "email": asset.email_address,
                    "position": asset.position,
                    "phone": "",
                    "buildingId": get_building_id(asset.building),
                    "room": asset.homeroom,
                    "extensionAttributes": [
                        {
                            "definitionId": "4",
                            "name": "Grade",
                            "values": [
                                asset.student_grade
                            ]
                        },
                        {
                            "definitionId": "3",
                            "name": "GradYear",
                            "values": [
                                asset.grad_year
                            ]
                        },
                        {
                            "definitionId": "5",
                            "name": "Last Sync",
                            "values": [
                                datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")
                            ]
                        }
                    ]
                }
            }

            jamf_p.update_computer_inventory(payload, asset.jamf_id)
            j_logger.debug("Asset: %s Ok", asset.asset_tag)

    total_sync = len(asset_list) - error_count
    if total_sync == 0:
        j_logger.info('No Devices were synced')
        j_logger.info('Total number of skipped devices: %s', error_count)
        return

    j_logger.info('Total synced assets: %s', total_sync)
    j_logger.info('Total number of skipped devices: %s', error_count)


def get_single_computer_record_by_asset_tag(asset_tag: str) -> List[Dict]:
    """
    Gets Jamf record of single computer asset based on asset tag

    Args:
        asset_tag (str): Asset tag of computer

    Raises:
        JautomateException: Raised if no computer records found

    Returns:
        List[Dict]: List of dictionaries where each dict is a computer asset
    """
    j_logger.debug("Asset Tag: %s", asset_tag)
    # This endpoint allows us to filter by asset tag so we
    # only need to get the device we need
    endpoint_filter = f'general.assetTag==\"{asset_tag}\"'
    response = jamf_p.get_computer_inventories(
        section=["GENERAL"], filter=endpoint_filter)
    if response["totalCount"] >= 1:
        return response["results"]
    else:
        raise JautomateException("Computer record could not be found.")


def get_all_computers_from_jamf() -> List[Dict]:
    """
    Gets all computer assets from jamf using the Classic API protocol

    Raises:
        JautomateException: If not computer records found in Jamf

    Returns:
        List[Dict]: List of dictionaries where each dict is a computer asset
    """
    response = jamf_c.get_computers(None, True)
    if len(response["computers"]) >= 1:
        return response["computers"]
    # Raise exception if no records found
    raise JautomateException("Computer records could not be found.")


def update_computer_jamf_ids_from_asset_tag(asset_list: Assets):
    """
    Updates jamf ids of computers using asset tag

    Args:
        asset_list (Assets): Assets object containing list of local assets and
        list of remote assets

    Returns:
        Assets: Assets object containing list of local assets and
        list of remote assets
    """
    for asset in asset_list.local:
        matching_device = next(
            (device for device in asset_list.remote
                if device['general']['assetTag'] == asset.asset_tag), None)
        if matching_device:
            asset.jamf_id = matching_device['id']
    return asset_list


def get_all_device_jamf_ids_by_serial_number(asset_list: Assets):
    """
    Matches serial numbers from local asset list with remote asset list and
    updates the jamf ID so api calls can be made for that asset.

    Args:
        asset_list (Assets): Assets object containing list of local assets and
        list of remote assets

    Returns:
        Assets: Assets object containing list of local assets and
        list of remote assets
    """
    j_logger.debug("Syncing jamf ids")

    for asset in asset_list.local:
        matching_device = next(
            (device for device in asset_list.remote
             if device[utils.determine_serial_number_key_format(device)] == asset.serial_number),
            None)
        if matching_device:
            asset.jamf_id = matching_device['id']
    return asset_list
