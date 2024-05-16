"""Tests for jautomate.devices"""

from jautomate.models import Asset, User
import jautomate.devices

# Add serial number and asset tag for testing
SAMPLE_COMP = {
    'serial_number': 'FVFFV26HQ6L6',
    'asset_tag': '028516', }
SAMPLE_MOBILE = {
    'serial_number': 'F9GCL4H1MF3M',
    'asset_tag': '021546',
}


def check_for_computer_extension_attribute(attribute_name: str, value: str, payload: dict) -> bool:
    for item in payload["userAndLocation"]["extensionAttributes"]:
        if item.get("name") == attribute_name and item.get("values")[0] == value:
            return True
    return False


def check_for_mobile_extension_attribute(attribute_name: str, value: str, payload: dict) -> bool:
    for item in payload["updatedExtensionAttributes"]:
        if item.get("name") == attribute_name and item.get("value")[0] == value:
            return True
    return False


def test_build_computer_payload():
    asset = Asset(
        serial_number='123456',
        asset_tag='043521',
        device_type='computer',
        jamf_id='4532',
        user=User(
            first_name='Luke',
            last_name='Skywalker',
            email='skywalker.luke@ccpsstaff.org',
            position='Staff',
        )
    )
    payload = jautomate.devices.build_computer_payload(asset)

    assert payload["general"].get("assetTag") == '043521'
    assert payload["userAndLocation"].get("realname") == 'Luke Skywalker'
    assert payload["userAndLocation"].get("email") == 'skywalker.luke@ccpsstaff.org'
    assert payload["userAndLocation"].get("position") == 'Staff'

    asset = Asset(
        serial_number='123456',
        asset_tag='043521',
        device_type='computer',
        user=User(
            first_name='Ben',
            last_name='Solo',
            email='solo.ben@ccpsstaff.org',
            position='Student',
            grad_year='2034',
            grade='1',
            building='PES',
            homeroom='Organa'
        )
    )
    payload = jautomate.devices.build_computer_payload(asset)

    assert payload["general"].get("assetTag") == '043521'
    assert payload["userAndLocation"].get("realname") == 'Ben Solo'
    assert payload["userAndLocation"].get("email") == 'solo.ben@ccpsstaff.org'
    assert payload["userAndLocation"].get("position") == 'Student'
    assert payload["userAndLocation"].get("buildingId") == '5'
    assert payload["userAndLocation"].get("room") == 'Organa'
    assert check_for_computer_extension_attribute("Grade", "1", payload)
    assert check_for_computer_extension_attribute("GradYear", "2034", payload)


def test_build_mobile_payload():
    asset = Asset(
        serial_number='123456',
        asset_tag='043521',
        device_type='mobile',
        jamf_id='4532',
        user=User(
            first_name='Luke',
            last_name='Skywalker',
            email='skywalker.luke@ccpsstaff.org',
            position='Staff',
        )
    )
    payload = jautomate.devices.build_mobile_payload(asset)

    assert payload["name"] == '043521'
    assert payload["location"].get("realName") == 'Luke Skywalker'
    assert payload["location"].get("emailAddress") == 'skywalker.luke@ccpsstaff.org'
    assert payload["location"].get("room") is None

    asset = Asset(
        serial_number='123456',
        asset_tag='043521',
        device_type='mobile',
        user=User(
            first_name='Ben',
            last_name='Solo',
            email='solo.ben@ccpsstaff.org',
            position='Student',
            grad_year='2034',
            grade='1',
            building='PES',
            homeroom='Organa'
        )
    )
    payload = jautomate.devices.build_mobile_payload(asset)

    assert payload["name"] == '043521'
    assert payload["location"].get("realName") == 'Ben Solo'
    assert payload["location"].get("emailAddress") == 'solo.ben@ccpsstaff.org'
    assert payload["location"].get("room") == 'Organa'
    assert check_for_mobile_extension_attribute("Grade", "1", payload)
    assert check_for_mobile_extension_attribute("GradYear", "2034", payload)

    asset = Asset(
        serial_number='123456',
        asset_tag='043521',
        device_type='mobile',
        user=None
    )
    payload = jautomate.devices.build_mobile_payload(asset)
    print(f"Payload: {payload}")
    assert payload["name"] == '043521'
    assert payload["location"].get("realName") is " "
    assert payload["location"].get("emailAddress") is " "
    assert payload["location"].get("room") is " "


def test_get_computer_record_by_serial_number():
    computer = jautomate.devices.get_computer_record_by_serial_number(
        SAMPLE_COMP.get('serial_number')
    )
    assert isinstance(computer, dict)


def test_get_mobile_device_by_serial_number():
    mobile = jautomate.devices.get_mobile_device_by_serial_number(
        SAMPLE_MOBILE.get('serial_number'))
    assert isinstance(mobile, dict)


def test_get_jamf_id_of_mobile_device():
    jamf_id = jautomate.devices.get_jamf_id_of_mobile_device(SAMPLE_MOBILE.get('serial_number'))
    assert isinstance(jamf_id, str)


def test_update_mobile_device_for_staff():
    asset = Asset(
        serial_number=SAMPLE_MOBILE.get('serial_number'),
        asset_tag=SAMPLE_MOBILE.get('asset_tag'),
        device_type='mobile',
        user=User(
            first_name='Luke',
            last_name='Skywalker',
            email='skywalker.luke@ccpsstaff.org',
            position='Staff',
            building='PES',
        )
    )

    asset.jamf_id = jautomate.devices.get_jamf_id_of_mobile_device(asset.serial_number)

    jautomate.devices.update_device(asset)


def test_update_mobile_device_for_student():
    asset = Asset(
        serial_number=SAMPLE_MOBILE.get('serial_number'),
        asset_tag=SAMPLE_MOBILE.get('asset_tag'),
        device_type='mobile',
        user=User(
            first_name='Ben',
            last_name='Solo',
            email='solo.ben@ccpsstudent.org',
            position='Student',
            grad_year='2034',
            grade='1',
            building='PES',
            homeroom='Organa'
        )
    )

    asset.jamf_id = jautomate.devices.get_jamf_id_of_mobile_device(asset.serial_number)

    jautomate.devices.update_device(asset)


def test_unassign_mobile_device():
    asset = Asset(
        serial_number=SAMPLE_MOBILE.get('serial_number'),
        asset_tag=SAMPLE_MOBILE.get('asset_tag'),
        device_type='mobile',
    )

    asset.jamf_id = jautomate.devices.get_jamf_id_of_mobile_device(asset.serial_number)

    jautomate.devices.update_device(asset)


def test_update_computer_staff():
    asset = Asset(
        serial_number=SAMPLE_COMP.get('serial_number'),
        asset_tag=SAMPLE_COMP.get('asset_tag'),
        device_type='computer',
        user=User(
            first_name='Luke',
            last_name='Skywalker',
            username='skywalker-luke',
            email='skywalker.luke@ccpsstaff.org',
            position='Staff',
            building='FES',
            floor='1st',
            grad_year=' ',
            grade=' ',
            homeroom='  '
        )
    )

    asset.jamf_id = jautomate.devices.get_jamf_id_of_computer(asset.serial_number)

    jautomate.devices.update_device(asset)


def test_update_computer_student():
    asset = Asset(
        serial_number=SAMPLE_COMP.get('serial_number'),
        asset_tag=SAMPLE_COMP.get('asset_tag'),
        device_type='computer',
        user=User(
            first_name='Ben',
            last_name='Solo',
            username='solo-ben',
            email='solo.ben@ccpsstudent.org',
            position='Student',
            grad_year='2034',
            grade='1',
            building='PES',
            homeroom='Organa'
        )
    )

    asset.jamf_id = jautomate.devices.get_jamf_id_of_computer(asset.serial_number)

    jautomate.devices.update_device(asset)


def test_unassign_computer():
    asset = Asset(
        serial_number=SAMPLE_COMP.get('serial_number'),
        asset_tag=SAMPLE_COMP.get('asset_tag'),
        device_type='computer',
    )

    asset.jamf_id = jautomate.devices.get_jamf_id_of_computer(asset.serial_number)

    jautomate.devices.update_device(asset)
