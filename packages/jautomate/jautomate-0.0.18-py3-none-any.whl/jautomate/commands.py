"""
These are non cli versions of the commands originally created for use as
a command line tool. Since we moved to calling them from an API there
were issues getting default values passed as the proper type through
the Typer versions in cli.py. These may eventually become the primary
way in which this tool will be used.
"""

from jautomate import actions
from jautomate.assets import Asset, Assets, AssetType
from jautomate.logger import j_logger


def assign_device(
    asset_tag: str,
    building: str,
    device_type: AssetType,
    homeroom: str,
    serial_number: str,
    student_name: str,
    student_grade: str,
    email_address: str = '',
    grad_year: str = '',
    owner: str = '',
    position: str = ''
) -> None:
    """
    Assigns data to a single asset record in Jamf Pro.

    Args:
        device_type (AssetType, required): Type of device being updated. mobile or computer
        asset_tag (str, required): Asset tag should be a 6 digit number
        serial_number (str, required): Serial Number of device
        student_name (str, required):  Student full name
        homeroom (str, required): Homeroom teachers last name
        student_grade (str, required): Student grade as a number
        building (str, required): Three letter building abbreviation. ex: COA
        email_address (Annotated[Optional[str], typer.Option, optional): 
            _description_. Defaults to 'Student email address')]=None.
        grad_year (Annotated[Optional[str], typer.Option, optional): 
            _description_. Defaults to 'Year student graduates')]=None.
        owner (Annotated[Optional[str], typer.Option, optional): 
            _description_. Defaults to 'Owner of device, this was used in the 
            past as a way to target devices but should be deprecated')]=None.
        position (Annotated[Optional[str], typer.Option, optional): 
            _description_. Defaults to 'For now, this will also be the 
            Graduation year, will be transitioned to Student or Staff')]=None.
    """
    j_logger.debug('%s asset assign is running...', device_type.value)

    # Create asset with all passed data
    asset = Asset(
        asset_tag=asset_tag,
        building=building,
        device_type=device_type.value,
        email_address=email_address,
        grad_year=grad_year,
        homeroom=homeroom,
        owner=owner,
        position=position,
        serial_number=serial_number,
        student_grade=student_grade,
        student_name=student_name,
    )

    if asset.device_type == 'computer':
        asset_list = Assets(
            [asset],
            actions.get_single_computer_record_by_asset_tag(asset.asset_tag))
        asset_list = actions.update_computer_jamf_ids_from_asset_tag(
            asset_list)

    if asset.device_type == 'mobile':
        asset_list = Assets([asset], actions.get_all_mobile_devices())
        asset_list = actions.get_mobile_device_jamf_ids_by_serial_number(
            asset_list)

    actions.sync_assets_to_jamf(asset_list.local)


def unassign_device(
    device_type: AssetType,
    asset_tag: str,
) -> None:
    """
    Unassigns data from a single asset record in Jamf Pro

    Args:
        device_type (str, required): Type of device being updated. mobile or computer
        asset_tag (str, required): Asset tag, should be a 6 digit number
    """
    j_logger.debug('%s device unassign is running...', device_type.value)

    # Set all properties to empty str except asset_tag, building, device_type
    asset = Asset(
        asset_tag=asset_tag,
        building='0',
        device_type=device_type.value,
        email_address='',
        grad_year='',
        homeroom='',
        owner='',
        position='',
        phone_number='',
        student_grade='',
        student_name='',
    )

    if device_type.value == 'computer':
        asset_list = Assets(
            [asset],
            actions.get_single_computer_record_by_asset_tag(asset.asset_tag))
        asset_list = actions.update_computer_jamf_ids_from_asset_tag(
            asset_list)

    if asset.device_type == 'mobile':
        asset_list = Assets([asset], actions.get_all_mobile_devices())
        asset_list = actions.get_mobile_device_jamf_ids_by_asset_tag(
            asset_list)

    actions.sync_assets_to_jamf(asset_list.local)
