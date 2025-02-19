
# Insider Case

This repository contains automated tests for **API, Load and UI** components of our project. The API tests cover CRUD operations using the pet endpoints from Swagger Petstore, the load test focused on search module of n.11.com and the UI tests focus on the Insider website and its related pages.

---
## Table of Contents

- [Repository Structure](#repository-structure)
- [Prerequisites](#prerequisites)
- [Pet Store API Testing with Pytest](#pet-store-api-testing-with-pytest)
- [N11 Load Testing with Locust & Playwright](#n11-load-testing-with-locust--playwright)
- [Insider UI Testing with Pytest & POM](#insider-ui-testing-with-pytest--pom)

---

## Repository Structure

```
nurdan_akman_case/
├── api-tests/
│   ├── models/             # Contains API models for endpoints.
│   ├── service/            # API service classes that encapsulate request logic.
│   ├── tests/              # API test scripts for executing CRUD operations.
│   ├── utils/              # Utility have logger script.
│   ├── api_config.py       # Configuration file for API baseurl
│   └── test.png            # Example image file
├── load_test/              
│   └── locustfile.py       # Locust script defining user behavior for load tests.
│   └── locust_report.html.py # Generated load test report
├── ui-tests/
│   ├── pages/              # Page Object Model (POM) classes representing UI components and pages.
│   ├── tests/              # Selenium test scripts to execute UI scenarios.
│   ├── screenshots/        # Directory where screenshots are stored when tests fail.
│   ├── conftest.py         # Pytest configuration file for test setup.
│   ├── data.py             # Contains test data for expected list for UI tests.
│   └── ui_config.py        # Configuration file for UI urls
├── README.md               # Project overview and instructions for setup and execution.
└── requirements.txt        # Lists Python dependencies required for the project.

```
---

## Prerequisites

- Python 3.x
- Pip package installer
- Clone the repository

```bash
   git clone https://github.com/nurdanakman/nurdan_akman_case.git
  ```
---


# Pet Store API Testing with Pytest

The API tests interact with the **pet** endpoints on [Swagger Petstore](https://petstore.swagger.io/) and cover the **CRUD operations** via using **Pytest** and **Pydantic**.

## Features
- Uses **Pytest** to create test cases.
- Uses **Pydantic** for payload and response body assertion.
- Uses detailed log for debugging.

##  Installation

### Install Dependencies
Run the following command to install required packages:

```bash
pip install -r requirements.txt
or
pip3 install -r requirements.txt
```

### Running Apı Test with Pytest

- For Windows:
```bash
cd api_test/
python -m pytest
```
- For MacOS:
```bash
cd api_test/
python3 -m pytest
```

### Running Specific Test Groups

To run only specific groups of tests, use the -m flag with either the negative or positive marker.

- Run Negative Test Scenarios:
```bash
python -m pytest -v -m negative
or
python3 -m pytest -v -m negative
```

- Run Positive Test Scenarios:
```bash
python -m pytest -v -m negative
or
python3 -m pytest -v -m positive
```

---
# N11 Load Testing with Locust & Playwright

This project performs **load testing** on the **search module of N11.com** using **Locust** and **Playwright**.

## Features
- Uses **Playwright** to automate searches on [N11.com](https://www.n11.com/).
- Uses **Locust** for load testing.
- Runs in **headless mode** to avoid detection.
- **Automatically generates an HTML report** after the test.


##  Installation

### Install Dependencies
Run the following command to install required packages:

```bash
pip install -r requirements.txt
```
### Install Playwright Browsers

The project requires playwright to manage to browser activites for performance test with Locust.

- For Windows:
```bash
python -m playwright install
```
- For MacOS:

```bash
python3 -m playwright install
```

###  Configuration

Locust tests come with some predefined configuration.

```bash
LOCUST_OPTIONS = [
    "locust", "-f", "locust_test.py", "--headless", "--host=https://www.n11.com",
    "--run-time", "2m", "--html=locust_report.html"
]
```
- **--headless:** It performs actions headless to avoid detection
- **--host:** Allows configure URL
- **--run-time:** Load test duration
- **--html:** Generates a report

In default, this project runs on n11.com with a 2 minutes runtime and automatically generates report and opens. To change
duration **"2m"** value could be set to desired duration. As a requirement of the assignment, user number always set to 1.

### Running Load Test with Locust

- For Windows:
```bash
cd load_test/
python locust_test.py
```
- For MacOS:
```bash
cd load_test/
python3 locust_test.py
```

## Load Test Report

After test execution is completed, user can see the load test results on the screen.

---
# Insider UI Testing with Pytest & POM

This repository contains automated tests for the [Insider website](https://useinsider.com/)’s homepage and careers pages, developed using **Selenium** and **Python**. The tests are implemented using the **Page Object Model (POM)** architecture and can be executed parametrically on **both Chrome and Firefox** browsers. Additionally, screenshots are automatically captured when test cases fail.

## Features
- Uses **Pytest** for creating and executing test cases.
- Implements **POM** for more readable, scalable, and less redundant code.
- Utilizes **webdriver-manager** to run tests across different browsers.
- Includes a script that captures **screenshots on test failures**.

##  Installation

### Install Dependencies
Run the following command to install required packages:

```bash
pip install -r requirements.txt
```

### Running UI Test with Pytest

- For Windows:
```bash
cd ui_test/
python -m pytest
```
- For MacOS:
```bash
cd ui_test/
python3 -m pytest
```

### Running Specific Browser

To run tests with different browsers, commands below can be used. If browser option is not specified, tests will run on Chrome as default.

- Run Test on Firefox browser:
```bash
python -m pytest --browser firefox
or
python3 -m pytest --browser firefox
```

- Run Test on Chrome browser:
```bash
python -m pytest --browser chrome
or
python3 -m pytest --browser chrome
```

---
If you have any questions about the task, please don't hesitate the contact me via akman.nurdann@gmail.com
