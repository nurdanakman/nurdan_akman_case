from selenium.webdriver.common.by import By

from ui_test.ui_config import UIConfig
from ui_test.pages.base_page import BasePage


class CareersOpenPositionsPage(BasePage):
    OPEN_POSITIONS_URL = UIConfig.OPEN_POSITIONS_URL

    # Filters and options locators
    LOCATION_FILTER = (By.XPATH, "//*[@aria-labelledby='select2-filter-by-location-container']")
    DEPARTMENT_FILTER = (By.XPATH, "//*[@aria-labelledby='select2-filter-by-department-container']")
    ISTANBUL_OPTION = (By.XPATH, "//li[contains(text(), 'Istanbul, Turkiye')]")
    QUALITY_ASSURANCE_OPTION = (By.XPATH, "//li[contains(text(), 'Quality Assurance')]")

    # Job items locators
    JOB_ITEMS = (By.XPATH, "//div[contains(@class, 'position-list-item-wrapper')]")
    JOB_DEPARTMENT = (By.XPATH, ".//span[contains(@class, 'position-department')]")
    JOB_LOCATION = (By.XPATH, ".//span[contains(@class, 'position-location')]")
    VIEW_ROLE_BUTTON = (By.XPATH, ".//a[contains(text(), 'View Role')]")

    def go_to_open_positions_page(self):
        self.driver.get(self.OPEN_POSITIONS_URL)
        self.click_accept_cookies_button()

    def apply_location_filter(self):
        self.click(self.LOCATION_FILTER)
        self.click(self.ISTANBUL_OPTION)

    def apply_department_filter(self):
        self.click(self.DEPARTMENT_FILTER)
        self.click(self.QUALITY_ASSURANCE_OPTION)

    def is_job_list_present(self):
        return self.is_element_present(self.JOB_ITEMS)

    def locations_list_on_job_item(self):
        return self.get_texts_of_elements(self.JOB_LOCATION)

    def department_list_on_job_item(self):
        return self.get_texts_of_elements(self.JOB_DEPARTMENT)

    def click_view_role_on_first_job(self):
        self.is_job_list_present()
        self.click_element(self.VIEW_ROLE_BUTTON)
