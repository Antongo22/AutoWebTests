pipeline {
    agent any

    environment {
        // Укажите путь к вашему проекту
        PROJECT_DIR = 'app'
        // Путь для хранения отчетов Allure
        ALLURE_RESULT_DIR = 'allure-results'
        // Версия Python (если используете Python)
        PYTHON_VERSION = '3.8'
    }

    stages {
        stage('Checkout') {
            steps {
                // Получение кода из репозитория
                git 'https://github.com/yourusername/your-repo.git'
            }
        }

        stage('Setup Environment') {
            steps {
                // Установка зависимостей (например, для Python)
                sh 'python3 -m venv venv'
                sh 'venv/bin/pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                // Запуск тестов и генерация отчетов Allure
                sh '''
                    export PATH="$WORKSPACE/venv/bin:$PATH"
                    pytest --alluredir=allure-results
                '''
            }
        }

        stage('Generate Allure Report') {
            steps {
                // Генерация отчета Allure
                allure includeProperties: false, jdk: '', reportDir: 'allure-results'
            }
        }
    }

    post {
        always {
            // Архивирование отчетов Allure
            archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
            // Публикация отчета Allure
            allure includeProperties: false, jdk: '', reportDir: 'allure-results'
        }
        failure {
            // Отправка уведомлений (например, по email) в случае провала
            mail to: 'anton005go.too@gmail.com',
                 subject: "Jenkins Build Failed: ${currentBuild.fullDisplayName}",
                 body: "Something is wrong with ${env.BUILD_URL}"
        }
    }
}