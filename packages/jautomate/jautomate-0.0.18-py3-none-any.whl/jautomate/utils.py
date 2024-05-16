"""Utility functions for Jautomate"""

import csv
import os
from typing import Dict, List, Union

from jautomate.assets import Asset
from jautomate.logger import j_logger


def get_assets_from_csv(file_path: Union[str, os.PathLike]) -> List[Asset]:
    """
    Imports assets from csv file and stores as Asset Objects.

    Will import from a CSV file of assets using specific keys for the
    information.
    The keys are as follows

    CCPS Tag#
    Serial Number
    School Calc
    Homeroom
    First
    Last
    Grade

    Args:
        file_path (Union[str, os.PathLike]): Path to csv file to import.

    Returns:
        List: List of Asset objects
    """
    assets = []
    with open(file_path, newline='', encoding='utf8') as file:
        reader = csv.DictReader(file)
        for row in reader:

            # Don't sync chromebooks to jamf
            if row['Hardware Type'] == 'Chromebook':
                continue

            # Skip empty rows
            if row['Hardware Type'] is None or row['Hardware Type'] == '':
                continue

            # Skip rows missing serial number and log them
            if row['Serial Number'] is None or row['Serial Number'] == '':
                j_logger.error('Import row skipped, missing Serial Number:')
                j_logger.error('%s \n', row)
                continue

            # Skip rows missing School and log them
            if row['School Calc'] is None or row['School Calc'] == '':
                j_logger.error('Import row skipped, missing School:')
                j_logger.error('%s \n', row)
                continue

            # position is set to empty for iPads
            if row['Hardware Type'] == 'Handheld Device':
                device_type = 'mobile'
                position = ''

            # position is still being used in some jamf policies as a
            # graduation year field so we set that for laptops
            if row['Hardware Type'] == 'Laptop':
                device_type = 'computer'
                position = row['Graduation Year Calc']

            # Assign rows to attributes of asset Object
            asset = Asset(
                device_type=device_type,
                asset_tag=row.get('CCPS Tag#'),
                serial_number=row.get('Serial Number'),
                building=row.get('School Calc'),
                homeroom=row.get('Homeroom'),
                student_name=f"{row.get('First')} {row.get('Last')}",
                student_grade=row.get('Grade'),
                email_address=row.get('Student Email from GAM'),
                grad_year=row.get('Graduation Year Calc'),
                position=position,
                owner='',
            )

            assets.append(asset)
    return assets


def determine_serial_number_key_format(remote_asset: Dict) -> str:
    """
    Determines the format of the serial number key being used by
    Jamf (Classic or Pro) and returns that as a string.

    Args:
        remote_asset (Dict): A Dict obj of a remote asset that was returned
        by Jamf API

    Raises:
        KeyError: Raises a KeyError if neither of the key options was found

    Returns:
        str: String value for the serial number key.
    """
    if remote_asset.get('serialNumber'):
        return 'serialNumber'
    if remote_asset.get('Serial_Number'):
        return 'Serial_Number'
    if remote_asset.get('serial_number'):
        return 'serial_number'
    raise KeyError('No valid key found for Serial Number')
