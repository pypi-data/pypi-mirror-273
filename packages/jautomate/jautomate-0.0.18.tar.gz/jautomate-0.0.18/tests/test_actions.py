"""Test for jautomate.actions"""
import jautomate.actions


def test_get_building_id():
    building_id = jautomate.actions.get_building_id('test')
    assert building_id is None

    building_id = jautomate.actions.get_building_id('FES')
    assert building_id is not None
