from selenium.webdriver.common.by import By

from ui_test.pages.base_page import BasePage

from ui_test.ui_config import UIConfig


class CareersPage(BasePage):
    CAREERS_PAGE_URL = UIConfig.CAREERS_URL

    # Blocks titles locators
    TEAMS_BLOCK_TITLE = (By.XPATH, "//*[@data-id='4a40266']//h3[1]")
    LOCATIONS_BLOCK_TITLE = (By.XPATH, "//*[@data-id='b1a909d']//h3[1]")
    LIFE_AT_INSIDER_BLOCK_TITLE = (By.XPATH, "//*[@data-id='87842ec']//h2[1]")

    # Teams block details
    SEE_ALL_TEAMS_BUTTON = (By.XPATH, "//a[contains(text(), 'See all teams')]")
    TEAMS = (By.XPATH, "//h3[@class='text-center mb-4 mb-xl-5']")

    # Locations block details
    LOCATIONS = (By.XPATH, "//p[@class='mb-0']")

    # Life block details
    IMAGES = (By.XPATH, "//div[contains(@style, 'life-at-insider')]")

    def verify_career_page_url(self):
        return self.CAREERS_PAGE_URL in self.driver.current_url

    def go_to_careers_page(self):
        self.driver.get(self.CAREERS_PAGE_URL)
        self.click_accept_cookies_button()

    def actual_teams_title(self):
        return self.get_text(self.TEAMS_BLOCK_TITLE)

    def click_see_all_teams_button(self):
        self.click_element(self.SEE_ALL_TEAMS_BUTTON)

    def get_teams_list(self):
        return self.get_texts_of_elements(self.TEAMS)

    def actual_locations_title(self):
        return self.get_text(self.LOCATIONS_BLOCK_TITLE)

    def get_locations_list(self):
        return self.get_texts_of_elements(self.LOCATIONS)

    def actual_life_title(self):
        return self.get_text(self.LIFE_AT_INSIDER_BLOCK_TITLE)

    def get_images_list(self):
        return self.find_elements(self.IMAGES)
