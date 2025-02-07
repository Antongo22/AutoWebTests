# 📌 Калькулятор: Руководство по тестированию

## 🔧 Локальное тестирование

### 1️⃣ Установка зависимостей
```sh
python3 -m venv venv
source venv/bin/activate  # Для Linux/macOS
venv\Scripts\activate    # Для Windows
pip install -r requirements.txt
```

### 2️⃣ Запуск тестового сервера
```sh
uvicorn app.main:app --reload
```

### 3️⃣ Запуск тестов
```sh
pytest tests/ --alluredir=allure-results -v -s --disable-pytest-warnings
```

### 4️⃣ Генерация отчёта Allure
```sh
allure generate allure-results --clean
allure open
```

---

## 🤖 Тестирование через Jenkins

### 🔹 Настройка окружения
Перед запуском убедитесь, что в Jenkins установлены:
- Python 3.10+
- virtualenv
- Allure

### 🔹 Основной процесс
1. Запустить Jenkins и открыть `Manage Jenkins` → `Global Tool Configuration`
2. Добавить `Allure Commandline`, если его нет
3. Перейти в папку Jenkins с проектом
4. Выполнить команду для просмотра отчёта:

```sh
allure serve allure-results
```
5. Перейдите по url, который появиться в консоли

---

## 📸 Скриншоты (демонстрация работы Jenkins)

![image](https://github.com/user-attachments/assets/59a79587-70ba-40b0-a812-4220384fb5d3)
![image](https://github.com/user-attachments/assets/74ae7009-fb87-4b99-8127-1b75fe44d4be)
![image](https://github.com/user-attachments/assets/3c30cd6e-e4b7-49aa-91ea-1ee6a1886d75)
