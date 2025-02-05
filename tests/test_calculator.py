import allure
import pytest
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
import time
import shutil
import os

@pytest.fixture(scope="session", autouse=True)
def clear_allure_history():
    """Фикстура для очистки истории Allure перед запуском тестов"""
    if os.path.exists("../allure_results"):
        shutil.rmtree("../allure_results")

@pytest.fixture(scope="session")
def browser():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver

@allure.feature("Расширенные тесты калькулятора")
class TestAdvancedCalculator:
    @allure.story("Основные математические операции")
    @pytest.mark.parametrize("num1,num2,operation,expected", [
        (10, 5, "add", "15.0"),
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
        with allure.step("Открываем и заполняем форму"):
            browser.get("http://localhost:8000/")
            browser.find_element(By.XPATH, "//input[@name='num1']").send_keys(str(num1))
            Select(browser.find_element(By.XPATH, "//select[@name='operation']")).select_by_value(operation)
            browser.find_element(By.XPATH, "//input[@name='num2']").send_keys(str(num2))
            browser.find_element(By.XPATH, "//button[@type='submit']").click()
        
        time.sleep(1)
        result = browser.find_element(By.XPATH, "//div[@id='result']").text
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
        with allure.step("Открываем и заполняем форму с ошибками"):
            browser.get("http://localhost:8000/")
            
            browser.find_element(By.XPATH, "//input[@name='num1']").clear()
            browser.find_element(By.XPATH, "//input[@name='num2']").clear()
            
            if num1 is not None:
                browser.find_element(By.XPATH, "//input[@name='num1']").send_keys(str(num1))
            if num2 is not None:
                browser.find_element(By.XPATH, "//input[@name='num2']").send_keys(str(num2))
                
            Select(browser.find_element(By.XPATH, "//select[@name='operation']")).select_by_value(operation)
            browser.find_element(By.XPATH, "//button[@type='submit']").click()
        
        time.sleep(1)
        
        with allure.step("Проверяем сообщение об ошибке"):
            error_div = browser.find_element(By.XPATH, "//div[@id='result' and contains(@class, 'error')]")
            error_text = error_div.text
            assert expected_error in error_text, f"Ожидалась ошибка: '{expected_error}', получено: '{error_text}'"


    @allure.story("Специальные кейсы")
    @pytest.mark.parametrize("num1,num2,operation,expected", [
        (0, 0, "multiply", "0.0"),
        (1000000, 1000000, "multiply", "1000000000000.0"),
        (1, -1, "add", "0.0"),
        (5, -5, "subtract", "10.0"),
        (0.1, 0.2, "add", "0.3")
    ])
    def test_special_cases(self, browser, num1, num2, operation, expected):
        with allure.step("Проверка специальных кейсов"):
            browser.get("http://localhost:8000/")
            browser.find_element(By.XPATH, "//input[@name='num1']").send_keys(str(num1))
            Select(browser.find_element(By.XPATH, "//select[@name='operation']")).select_by_value(operation)
            browser.find_element(By.XPATH, "//input[@name='num2']").send_keys(str(num2))
            browser.find_element(By.XPATH, "//button[@type='submit']").click()
        
        time.sleep(1)
        result = browser.find_element(By.XPATH, "//div[@id='result']").text
        assert expected in result