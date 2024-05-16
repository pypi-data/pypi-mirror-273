"""This module provides the Jautomate CLI."""

from pathlib import Path
from typing import Optional
import typer
from jautomate import actions, utils, __app_name__, __version__
from jautomate.assets import Asset, Assets, AssetType
from jautomate.logger import j_logger


app = typer.Typer(add_completion=False)


def _version(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def callback(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        help="Show the app version and exit",
        callback=_version,
        is_eager=True
    )
) -> None:
    """Tools to automate MDM tasks using the Jamf API."""
    # Used for cli description only


@app.command()
def sync(
    file_path: Path = typer.Argument(
        ...,
        exists=True,
        help='The path to the csv file to be imported and synced with Jamf')
) -> None:
    """
    Syncs a csv file of asset information with Jamf Pro

    Args:
        file_path (Path, required): The path to the csv file to be imported 
            and synced with Jamf
    """

    j_logger.debug('Sync is running from: %s', file_path)

    imported_assets = utils.get_assets_from_csv(file_path)

    computers = actions.get_all_computers_from_jamf()
    mobiles = actions.get_all_mobile_devices()
    jamf_assets = computers + mobiles

    asset_list = Assets(imported_assets, jamf_assets)
    asset_list = actions.get_all_device_jamf_ids_by_serial_number(asset_list)

    actions.sync_assets_to_jamf(asset_list.local)


@app.command()
def assign(
    device_type: AssetType = typer.Argument(
        ...,
        case_sensitive=False,
        help='Type of device being updated'),
    asset_tag: str = typer.Argument(
        ..., help='Asset tag should be a 6 digit number'),
    serial_number: str = typer.Argument(..., help='Serial Number of device'),
    student_name: str = typer.Argument(..., help=' Student full name'),
    homeroom: str = typer.Argument(..., help='Homeroom teachers last name'),
    student_grade: int = typer.Argument(..., help='Student grade as a number'),
    building: str = typer.Argument(
        ...,
        help='Three letter building abbreviation. ex: COA'),
    email_address: Optional[str] = typer.Argument(
        default=None, help='Student email address'),
    grad_year: Optional[str] = typer.Argument(
        default=None, help='Year student graduates'),
    owner: Optional[str] = typer.Argument(
        default='', help='Owner of device, this was used in the past as a way to target devices but should be deprecated'),
    position: Optional[str] = typer.Argument(
        default=None, help='For now, this will also be the Graduation year, will be transitioned to Student or Staff'),
) -> None:
    """
    Assigns data to a single asset record in Jamf Pro.

    Args:
        device_type (str, required): Type of device being updated. mobile or computer
        asset_tag (str, required): Asset tag should be a 6 digit number
        serial_number (str, required): Serial Number of device
        student_name (str, required):  Student full name
        homeroom (str, required): Homeroom teachers last name
        student_grade (str, required): Student grade as a number
        building (str, required): Three letter building abbreviation. ex: COA
        email_address (Annotated[Optional[str], typer.Option, optional): _description_. Defaults to 'Student email address')]=None.
        grad_year (Annotated[Optional[str], typer.Option, optional): _description_. Defaults to 'Year student graduates')]=None.
        owner (Annotated[Optional[str], typer.Option, optional): _description_. Defaults to 'Owner of device, this was used in the past as a way to target devices but should be deprecated')]=None.
        position (Annotated[Optional[str], typer.Option, optional): _description_. Defaults to 'For now, this will also be the Graduation year, will be transitioned to Student or Staff')]=None.
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


@app.command()
def unassign(
    device_type: AssetType = typer.Argument(
        ...,
        case_sensitive=False,
        help='Type of device being updated'),
    asset_tag: str = typer.Argument(
        ..., help='Asset tag should be a 6 digit number'),
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
