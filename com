pytest --alluredir=allure-results

allure generate allure-results --clean

allure open

allure serve allure_results




pytest tests/ --alluredir=allure-results -v --capture=no --disable-pytest-warnings

allure serve allure-results