import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser. Options: chrome or firefox")

@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser").lower()
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    else:
        raise ValueError(f"Browser not supported: {browser}")
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture(autouse=True)
def screenshot_on_failure(request, driver):
    yield
    if request.node.rep_call.failed:
        screenshot_dir = "screenshots"
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        file_name = os.path.join(screenshot_dir, request.node.name + ".png")
        driver.save_screenshot(file_name)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

def pytest_report_teststatus(report, config):
    if report.when == "call":
        if report.passed:
            return "PASS", "PASS", "green"
        elif report.failed:
            return "FAIL", "FAIL", "red"
    elif report.when == "setup":
        if report.skipped:
            return "SKIP", "SKIP", "yellow"

