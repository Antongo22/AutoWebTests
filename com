uvicorn app.main:app --reload



pytest --alluredir=allure-results

allure generate allure-results --clean

allure open

allure serve allure_results




pytest tests/ --alluredir=allure-results -v --capture=no --disable-pytest-warnings

allure serve allure-results




pytest tests/ --alluredir=allure-results -v -s --disable-pytest-warnings