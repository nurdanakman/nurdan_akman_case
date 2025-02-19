import pytest

from ui_test.ui_config import UIConfig
import time

from ui_test.pages.careers_open_positions_page import CareersOpenPositionsPage
from ui_test.pages.lever_application_page import LeverApplicationPage


@pytest.mark.usefixtures("driver")
class TestCareersOpenPositionsPage:

    def test_open_positions_jobs_filters(self,driver):
        open_positions_page = CareersOpenPositionsPage(driver)
        open_positions_page.go_to_open_positions_page()

        time.sleep(10) #TODO There is an bug in the dropdown. If I don't wait, only All option visible on the list.

        open_positions_page.apply_location_filter()
        open_positions_page.apply_department_filter()

        time.sleep(15) # TODO There is an bug in the filter. Sometimes cards update again and I see some Sale related cards.

        # Assert open position carts
        assert open_positions_page.is_job_list_present(), "Open position cards is not present."

        # Assert location info on cards
        for location in open_positions_page.locations_list_on_job_item():
            assert location.text.strip() == "Istanbul, Turkiye", (
                f"Location mismatch: expected 'Istanbul, Turkiye', got '{location}'"
            )

        # Assert department info on cards
        for department in open_positions_page.department_list_on_job_item():
            assert department == "Quality Assurance", (
                f"Department mismatch: expected 'Quality Assurance', got '{department}'"
            )

    def test_navigate_to_lever_page(self, driver):
        open_positions_page = CareersOpenPositionsPage(driver)
        lever_application_page = LeverApplicationPage(driver)
        open_positions_page.go_to_open_positions_page()

        open_positions_page.click_view_role_on_first_job()

        # Assert new tab url
        handles = open_positions_page.switch_to_new_tab()
        time.sleep(5)
        assert len(handles) > 1, "New tab didn't opened"
        assert UIConfig.LEVER_URL in driver.current_url, "Lever page didn't opened"

        # Assert apply for this job button on lever page
        time.sleep(5)
        assert lever_application_page.verify_apply_this_job_button_visibility(), "Apply for this job button isn't visible"
