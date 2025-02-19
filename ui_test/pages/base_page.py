from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    # Cookies locator
    ACCEPT_ALL_COOKIES = (By.XPATH, "//a[contains(text(), 'Accept All')]")

    def __init__(self, driver):
        self.driver = driver
        self.timeout = 10

    def click_accept_cookies_button(self):
        return self.click(self.ACCEPT_ALL_COOKIES)


    def find(self, by_locator):
        return WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(by_locator))

    def click(self, by_locator):
        element = self.find(by_locator)
        element.click()

    def click_element(self, locator):
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(locator)
        )

        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

        try:
            element.click()
        except:
            self.driver.execute_script("arguments[0].click();", element)

    def get_text(self, by_locator):
        element = self.find(by_locator)
        return element.text.strip()

    def is_element_present(self, by_locator):
        try:
            self.find(by_locator)
            return True
        except:
            return False

    def find_elements(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(EC.presence_of_all_elements_located(locator))

    def get_texts_of_elements(self, locator):
        elements = self.driver.find_elements(*locator)
        return [element.get_attribute("textContent").strip() for element in elements]

    def switch_to_new_tab(self):
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[-1])
        return handles