import time

import pytest

from ui_test.pages.careers_page import CareersPage
from ui_test.data import expected_teams_list, expected_locations_list


@pytest.mark.usefixtures("driver")
class TestHomePage:

    def test_careers_page_blocks(self, driver):
        careers_page = CareersPage(driver)

        careers_page.go_to_careers_page()

        # Assertion for team block
        assert careers_page.actual_teams_title() == "Find your calling", \
            f"Unexpected team title: {careers_page.actual_teams_title()}"

        careers_page.click_see_all_teams_button()
        time.sleep(2)
        actual_teams_list = careers_page.get_teams_list()
        assert (len(actual_teams_list) == len(expected_teams_list)), \
            f"Unexpected teams found: {set(actual_teams_list) - set(expected_teams_list)}"

        for expected_team in expected_teams_list:
            assert expected_team in actual_teams_list, f"Missing team: {expected_team}"

        # Assertion for location block
        assert careers_page.actual_locations_title() == "Our Locations", \
            f"Unexpected location title: {careers_page.actual_locations_title()}"

        actual_locations_list = careers_page.get_locations_list()
        assert (len(actual_locations_list) == len(expected_locations_list)), \
            f"Unexpected location found: {set(actual_locations_list) - set(expected_locations_list)}"

        for expected_location in expected_locations_list:
            assert expected_location in actual_locations_list, f"Missing location: {expected_location}"

        # Assertion for life block
        assert careers_page.actual_life_title() == "Life at Insider", \
            f"Unexpected life insider title: {careers_page.actual_life_title()}"

        actual_images_list = careers_page.get_images_list()
        assert len(actual_images_list) > 0, f"Image list is empty"
