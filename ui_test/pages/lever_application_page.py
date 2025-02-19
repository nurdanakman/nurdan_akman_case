from selenium.webdriver.common.by import By

from ui_test.pages.base_page import BasePage


class LeverApplicationPage(BasePage):
    # Apply for this jobs button locator
    APPLY_FOR_THIS_JOB_BUTTON = (By.XPATH, "//a[contains(text(), 'Apply for this job')]")

    def verify_apply_this_job_button_visibility(self):
        return self.is_element_present(self.APPLY_FOR_THIS_JOB_BUTTON)