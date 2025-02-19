import random
import platform
import os
import time
import asyncio
import subprocess
import webbrowser
from locust import User, task, between, events
from playwright.async_api import async_playwright

#Functions for colored output to increase readability
def print_green(message):
    print(f"\033[92m{message}\033[0m")

def print_red(message):
    print(f"\033[91m{message}\033[0m")

# ✅ Define search terms for testing
SEARCH_TERMS = ["telefon", "laptop", "kulaklık", "monitör", "mouse", "ayakkabı", "çanta", "parfüm"]
LOCUST_OPTIONS = [
    "locust", "-f", "locust_test.py", "--headless", "--host=https://www.n11.com",
    "--run-time", "2m", "--html=locust_report.html"
]

# Detect OS
OS_TYPE = platform.system()

class N11SearchUser(User):
    wait_time = between(3, 6)  # Simulate real user behavior, since n11 block automated request activities!

    def on_start(self):
        """ Start an event loop and launch the browser """
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.playwright = self.loop.run_until_complete(async_playwright().start())
        self.browser = self.loop.run_until_complete(self.launch_browser())
        self.start_time = time.time()  # Track start time

    async def launch_browser(self):
        """ Launch Playwright browser instance """
        return await self.playwright.chromium.launch(headless=True)  # Use Chromium

    @task
    def perform_search(self):
        search_query = random.choice(SEARCH_TERMS)
        url = f"https://www.n11.com/arama?q={search_query}"

        print_green(f"Searching for: {search_query}")

        # Measure response time
        start_time = time.time()
        success = self.loop.run_until_complete(self.search(url, search_query))
        total_time = int((time.time() - start_time) * 1000)  # Convert to milliseconds

        # Report stats to Locust
        events.request.fire(
            request_type="SEARCH",
            name="Search Test",
            response_time=total_time,
            response_length=0,
            exception=None if success else "Failed Search"
        )

    async def search(self, url, search_query):
        """ Perform search in an async function """
        page = await self.browser.new_page()
        await page.goto(url, wait_until="networkidle")
        page_content = await page.content()

        if "No results found" in page_content:
            print_red(f" No results for '{search_query}'")
            await page.close()
            return False
        else:
            print_green(f" Search successful for '{search_query}'")
            await page.close()
            return True

    def on_stop(self):
        """ Ensure browser properly closes when test stops """
        if self.browser:
            print_green("Closing browser instance...")
            self.loop.run_until_complete(self.browser.close())
            self.loop.run_until_complete(self.playwright.stop())
            self.loop.close()
            print_green("Browser closed successfully!")

    if __name__ == "__main__":
        print_green("Starting locust test...")

        if OS_TYPE == "Darwin":
            LOCUST_CMD = ["python3", "-m", "locust", "-f", "locust_test.py", "--headless", "--host=https://www.n11.com",
                          "--run-time", "2m", "--html=locust_report.html"]
            # Run Locust
            try:
                print_green(f" Running Locust on {OS_TYPE}...")
                subprocess.run(LOCUST_CMD, check=True)
            except FileNotFoundError:
                print_red(f" Locust not found! Ensure it is installed correctly on {OS_TYPE}.")
        else:
            # Run Locust
            subprocess.run(LOCUST_OPTIONS, check=True)

        # Open Test Report
        report_file = "locust_report.html"
        print_green("Report is generated. Opening in browser...")
        if OS_TYPE == "Darwin":
            filepath = os.getcwd() + "/locust_report.html"
            fileuri = f"file:///{filepath}"
            webbrowser.open_new_tab(fileuri)
        else:
            webbrowser.open(report_file)