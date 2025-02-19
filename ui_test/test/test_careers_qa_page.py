import pytest

from ui_test.ui_config import UIConfig
from ui_test.pages.careers_qa_page import CareersQaPage


@pytest.mark.usefixtures("driver")
class TestCareersQaPage:

    def test_open_careers_qa_page(self, driver):
        careers_qa_page = CareersQaPage(driver)

        careers_qa_page.go_to_careers_qa_page()

        assert UIConfig.CAREERS_QA_URL in driver.current_url, f"Unexpected URL: {driver.current_url}"
        assert careers_qa_page.verify_see_qa_jobs_button_visibility(), "See qa jobs button isn't visible"

    def test_navigates_to_open_qa_positions_jobs(self, driver):
        careers_qa_page = CareersQaPage(driver)

        careers_qa_page.go_to_careers_qa_page()
        careers_qa_page.click_see_all_qa_jobs_button()

        assert UIConfig.OPEN_POSITIONS_URL + "?department=qualityassurance" in driver.current_url, \
            f"Unexpected URL: {driver.current_url}"