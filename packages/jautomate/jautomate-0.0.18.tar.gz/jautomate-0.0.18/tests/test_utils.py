"""Tests for jautomate utils"""
from typing import List
import pytest
from jautomate.assets import Assets
import jautomate.utils


@pytest.fixture
def mock_csv_import(mocker):
    mocked_data = mocker.mock_open(read_data="""\
        Student Number,First,Last,School Calc,CCPS Tag#,Serial Number,Hardware Type,Grade,Graduation Year Calc,Homeroom
        222123,Luke,Skywalker,GES,036300,H96BNW5PQ1GC,Handheld Device,1,2034,Organa""")
    builtin_open = "builtins.open"
    mocker.patch(builtin_open, mocked_data)


def test_get_assets_from_csv(mock_csv_import):
    test_assets = jautomate.utils.get_assets_from_csv(file_path='fakefile')
    assert isinstance(test_assets, List)


def test_serial_number_camelcase() -> None:
    remote_asset = {
        'serialNumber': '012345678HD',
        'asset_tag': '123456',
        'id': '1234'
    }
    serial_number_type = jautomate.utils.determine_serial_number_key_format(
        remote_asset)
    assert serial_number_type == 'serialNumber'


def test_serial_number_snakecase() -> None:
    remote_asset = {
        'Serial_Number': '012345678HD',
        'asset_tag': '123456',
        'id': '1234'
    }
    serial_number_type = jautomate.utils.determine_serial_number_key_format(
        remote_asset)
    assert serial_number_type == 'Serial_Number'


def test_serial_number_invalid() -> None:
    with pytest.raises(KeyError):
        remote_asset = {
            'xyx': '012345678HD',
            'asset_tag': '123456',
            'id': '1234'
        }
        jautomate.utils.determine_serial_number_key_format(remote_asset)
