from selenium.webdriver.common.by import By

from ui_test.ui_config import UIConfig
from ui_test.pages.base_page import BasePage


class HomePage(BasePage):
    HOME_PAGE_URL = UIConfig.UI_HOME_URL

    # Insider logo locator
    LOGO = (By.XPATH, "//img[contains(@alt, 'insider_logo')]")

    # Navigation locators
    COMPANY_MENU = (By.XPATH, "//a[contains(text(), 'Company')]")
    CAREERS_LINK = (By.XPATH, "//a[contains(text(), 'Careers')]")

    def go_to_home_page(self):
        self.driver.get(self.HOME_PAGE_URL)
        self.click_accept_cookies_button()

    def verify_logo_visibility(self):
        return self.is_element_present(self.LOGO)

    def click_company_menu(self):
        return self.click(self.COMPANY_MENU)

    def click_careers_link(self):
        return self.click(self.CAREERS_LINK)