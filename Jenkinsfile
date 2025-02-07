pipeline {
    agent {
        docker {
            image 'python:3.9-slim'
            args '-v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=:0 --privileged'
        }
    }

    environment {
        ALLURE_RESULTS = 'allure-results'
    }

    stages {
        // Установка необходимых зависимостей
        stage('Setup Environment') {
            steps {
                sh '''
                    apt-get update && apt-get install -y \
                    chromium \
                    chromium-driver \
                    wget \
                    unzip
                '''
                sh 'python -m pip install --upgrade pip'
            }
        }

        // Установка Python-зависимостей
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        // Запуск FastAPI сервера
        stage('Run Server') {
            steps {
                sh '''
                    uvicorn main:app --host 0.0.0.0 --port 8000 &
                    echo $! > server.pid
                    sleep 5  # Даем серверу время на запуск
                '''
            }
        }

        // Запуск тестов
        stage('Run Tests') {
            steps {
                sh '''
                    pytest --alluredir=${ALLURE_RESULTS} tests/
                '''
            }
            post {
                always {
                    sh 'kill $(cat server.pid) || true'  // Останавливаем сервер
                }
            }
        }
    }

    // Пост-обработка (генерация Allure-отчета)
    post {
        always {
            script {
                // Проверяем, что директория с результатами существует
                sh 'ls -la ${ALLURE_RESULTS}'
            }
            allure([
                includeProperties: false,
                jdk: '',
                properties: [],
                reportBuildPolicy: 'ALWAYS',
                results: [[path: 'allure-results']]
            ])
        }
    }
}