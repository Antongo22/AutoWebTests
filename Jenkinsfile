pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Setup Environment') {
            steps {
                sh '''
                set -x
                python3 -m venv venv
                chmod -R 755 venv
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
                pip install jinja2
                '''
            }
        }
        stage('Check Access Rights') {
            steps {
                sh '''
                set -x
                ls -l venv/bin/pytest
                '''
            }
        }
        stage('Fix Permissions') {
            steps {
                sh '''
                set -x
                chmod +x venv/bin/pytest
                ls -l venv/bin/pytest
                '''
            }
        }
        stage('Start Test Server') {
            steps {
                sh '''
                set -x
                . venv/bin/activate
                uvicorn app.main:app --reload --host 127.0.0.1 --port 8000 &
                sleep 5
                '''
            }
        }
        stage('Run Tests') {
            steps {
                sh '''
                set -x
                . venv/bin/activate
                export PYTHONPATH=$PYTHONPATH:$WORKSPACE
                pytest tests/test_calculator.py --alluredir=allure-results
                '''
            }
        }
        stage('Generate Allure Report') {
            steps {
                script {
                    def allurePath = sh(script: 'which allure', returnStdout: true).trim()
                    if (allurePath) {
                        sh 'allure generate allure-results --clean -o allure-report'
                    } else {
                        echo "⚠️ Allure не найден! Чтобы открыть отчёт, выполните в терминале:"
                        echo "cd ${env.WORKSPACE} && allure serve allure-results"
                    }
                }
            }
        }
        stage('Deploy') {
            steps {
                sh '''
                echo "Deployment successful."
                '''
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'allure-results/*', fingerprint: true
        }
        failure {
            sh 'echo "Pipeline failed. Check the logs."'
        }
    }
}
