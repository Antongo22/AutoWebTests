# conftest.py
import pytest
import allure
import time
import os

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        browser = item.funcargs.get("browser")
        if browser:
            time.sleep(1)

            allure.attach(
                browser.get_screenshot_as_png(),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG
            )
            print("Скриншот прикреплён в Allure.")