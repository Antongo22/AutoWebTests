pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Antongo22/AutoWebTests'
            }
        }

        stage('Setup Environment') {
            steps {
                sh '''
                    python3 -m venv ${VENV_DIR}
                    chmod -R 755 ${VENV_DIR}
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                set -x
                . venv/bin/activate
                python --version
                which pip
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Start Test Server') {
            steps {
                sh '''
                    source ${VENV_DIR}/bin/activate
                    python app.py &  # Запуск тестируемого сервиса
                    sleep 5  # Ожидание запуска сервера
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    source ${VENV_DIR}/bin/activate
                    export PYTHONPATH=$PYTHONPATH:$(pwd)
                    pytest tests/ --alluredir=allure-results
                '''
            }
        }

        stage('Generate Allure Report') {
            steps {
                script {
                    allure([
                        results: [[path: 'allure-results']]
                    ])
                }
            }
        }

        stage('Archive Test Results') {
            steps {
                archiveArtifacts artifacts: 'allure-results/**/*', fingerprint: true
            }
        }
    }

    post {
        always {
            sh 'echo Pipeline execution completed.'
        }
        failure {
            sh 'echo Pipeline failed. Check the logs.'
        }
    }
}
