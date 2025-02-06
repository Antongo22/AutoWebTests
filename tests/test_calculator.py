import allure
import pytest
from selenium import webdriver
import os
import shutil
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class CalculatorPage:
    def __init__(self, driver):
        self.driver = driver
        self.num1_input = (By.XPATH, "//input[@name='num1']")
        self.num2_input = (By.XPATH, "//input[@name='num2']")
        self.operation_select = (By.XPATH, "//select[@name='operation']")
        self.submit_btn = (By.XPATH, "//button[@type='submit']")
        self.result_div = (By.XPATH, "//div[@id='result']")

    def open(self):
        self.driver.get("http://localhost:8000/")
        return self

    def enter_values(self, num1, num2):
        self.clear_inputs()
        if num1 is not None:
            self.driver.find_element(*self.num1_input).send_keys(str(num1))
        if num2 is not None:
            self.driver.find_element(*self.num2_input).send_keys(str(num2))
        return self

    def select_operation(self, operation):
        Select(self.driver.find_element(*self.operation_select)).select_by_value(operation)
        return self

    def calculate(self):
        self.driver.find_element(*self.submit_btn).click()
        return self

    def get_result(self):
        result_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.result_div)
        )
        if "error" in result_element.get_attribute("class"):
            return "Ошибка: " + result_element.text.split("Ошибка: ")[-1]
        return result_element.text

    def clear_inputs(self):
        self.driver.find_element(*self.num1_input).clear()
        self.driver.find_element(*self.num2_input).clear()
        return self



@pytest.fixture(scope="session", autouse=True)
def clear_allure_history():
    """Фикстура для очистки и создания директории Allure"""
    allure_dir = os.path.join(os.path.dirname(__file__), "allure-results")
    if os.path.exists(allure_dir):
        shutil.rmtree(allure_dir, ignore_errors=True)
    os.makedirs(allure_dir, exist_ok=True)

@pytest.fixture(scope="session")
def browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")  # Для стабильности в CI
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    driver.set_window_size(1920, 1080)  # Фиксированный размер окна
    yield driver
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        browser = item.funcargs.get("browser")
        if browser:
            # Сохраняем скриншот на диск для проверки
            browser.save_screenshot("debug_screenshot.png")
            # Прикрепляем в Allure
            allure.attach(
                browser.get_screenshot_as_png(),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG
            )

@allure.feature("Тесты калькулятора")
class TestAdvancedCalculator:
    @allure.story("Основные математические операции")
    @pytest.mark.parametrize("num1,num2,operation,expected", [
        (10, 5, "add", "15.1"),
        (20, 3, "subtract", "17.0"),
        (5, 6, "multiply", "30.0"),
        (100, 4, "divide", "25.0"),
        (0, 5, "add", "5.0"),
        (-5, 3, "subtract", "-8.0"),
        (2.5, 4, "multiply", "10.0"),
        (10, 0.5, "divide", "20.0"),
        (999, 1, "add", "1000.0"),
        (0, 0, "subtract", "0.0")
    ])
    def test_basic_operations(self, browser, num1, num2, operation, expected):
        calculator = CalculatorPage(browser)
        with allure.step("Открываем и заполняем форму"):
            (
                calculator.open()
                .enter_values(num1, num2)
                .select_operation(operation)
                .calculate()
            )

        time.sleep(1)
        with allure.step("Проверяем результат"):
            result = calculator.get_result()
            assert expected in result, f"Ожидалось {expected}, получено {result}"

    @allure.story("Проверка обработки ошибок")
    @pytest.mark.parametrize("num1,num2,operation,expected_error", [
        (10, 0, "divide", "Деление на ноль"),
        ("abc", 5, "add", "Некорректный формат числа"),
        (5, "xyz", "multiply", "Некорректный формат числа"),
        (None, 5, "add", "Пустые значения"),
        (5, None, "subtract", "Пустые значения")
    ])
    def test_error_cases(self, browser, num1, num2, operation, expected_error):
        calculator = CalculatorPage(browser)
        with allure.step("Открываем и заполняем форму с ошибками"):
            (
                calculator.open()
                .enter_values(num1, num2)
                .select_operation(operation)
                .calculate()
            )
        time.sleep(1)
        with allure.step("Проверяем сообщение об ошибке"):
            error = calculator.get_result()
            assert expected_error in error, f"Ожидалась ошибка: '{expected_error}', получено: '{error}'"

    @allure.story("Специальные кейсы")
    @pytest.mark.parametrize("num1,num2,operation,expected", [
        (0, 0, "multiply", "0.0"),
        (1000000, 1000000, "multiply", "1000000000000.0"),
        (1, -1, "add", "0.0"),
        (5, -5, "subtract", "10.0"),
        (0.1, 0.2, "add", "0.3")
    ])
    def test_special_cases(self, browser, num1, num2, operation, expected):
        calculator = CalculatorPage(browser)
        with allure.step("Проверка специальных кейсов"):
            (
                calculator.open()
                .enter_values(num1, num2)
                .select_operation(operation)
                .calculate()
            )
        time.sleep(1)
        with allure.step("Проверяем результат"):
            result = calculator.get_result()
            assert expected in result, f"Ожидалось {expected}, получено {result}"