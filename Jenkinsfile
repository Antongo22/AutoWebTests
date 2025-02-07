pipeline {
    agent {
        docker {
            image 'python:3.9-slim'
            args '-v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=:0'
        }
    }

    environment {
        ALLURE_RESULTS = 'allure-results'
    }

    stages {
        stage('Setup Environment') {
            steps {
                sh 'apt-get update && apt-get install -y chromium-driver'
                sh 'python -m pip install --upgrade pip'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Server') {
            steps {
                sh '''
                uvicorn main:app --host 0.0.0.0 --port 8000 &
                echo $! > server.pid
                sleep 5  
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                pytest --alluredir=${ALLURE_RESULTS} tests/
                '''
            }
            post {
                always {
                    sh 'kill $(cat server.pid) || true'  
                }
            }
        }
    }

    post {
        always {
            allure(
                includeProperties: false,
                jdk: '',
                properties: [],
                reportBuildPolicy: 'ALWAYS',
                allureInstallation: 'Allure 2.32.2',
                results: [[path: 'allure-results']]
            )
        }
    }
}