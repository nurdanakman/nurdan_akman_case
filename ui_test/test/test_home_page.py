import pytest

from ui_test.ui_config import UIConfig
from ui_test.pages.careers_page import CareersPage
from ui_test.pages.home_page import HomePage


@pytest.mark.usefixtures("driver")
class TestHomePage:

    def test_open_home_page(self, driver):
        home_page = HomePage(driver)

        home_page.go_to_home_page()

        assert UIConfig.UI_HOME_URL in driver.current_url, f"Unexpected URL: {driver.current_url}"
        assert home_page.verify_logo_visibility(), "Insider logo isn't visible"

    def test_navigate_to_careers_page(self, driver):
        home_page = HomePage(driver)
        careers_page = CareersPage(driver)

        home_page.go_to_home_page()

        home_page.click_company_menu()
        home_page.click_careers_link()

        assert careers_page.verify_career_page_url(), f"Unexpected URL: {driver.current_url}"
