from selenium.webdriver.common.by import By

from ui_test.ui_config import UIConfig
from ui_test.pages.base_page import BasePage


class CareersQaPage(BasePage):
    CAREERS_QA_PAGE_URL = UIConfig.CAREERS_QA_URL

    # See all qa jobs button locator
    SEE_QA_JOBS_BUTTON = (By.XPATH, "//a[contains(text(), 'See all QA jobs')]")

    def go_to_careers_qa_page(self):
        self.driver.get(self.CAREERS_QA_PAGE_URL)
        self.click_accept_cookies_button()

    def verify_see_qa_jobs_button_visibility(self):
        return self.is_element_present(self.SEE_QA_JOBS_BUTTON)

    def click_see_all_qa_jobs_button(self):
        return self.click(self.SEE_QA_JOBS_BUTTON)