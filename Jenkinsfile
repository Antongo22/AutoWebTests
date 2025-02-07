pipeline {
    agent any

    environment {
        PATH = "/home/anton/.local/bin:/usr/local/bin:$PATH"
    }

    stages {
        stage('Setup') {
            steps {
                script {
                    def allurePath = sh(script: 'which allure', returnStdout: true).trim()
                    if (!allurePath) {
                        echo "Allure не найден, создаю ссылку..."
                        sh 'sudo ln -s /home/anton/.local/bin/allure /usr/local/bin/allure || true'
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest tests/ --alluredir=allure-results'
            }
        }

        stage('Generate Allure Report') {
            steps {
                sh 'allure generate allure-results --clean -o allure-report'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying application...'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'allure-report/**', fingerprint: true
        }
        failure {
            echo 'Pipeline failed. Check the logs.'
        }
    }
}
