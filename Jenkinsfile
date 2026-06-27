pipeline {
    agent any

    environment {
        // Docker Hub image -> wojtek0/flask-cicd-app
        DOCKERHUB_USER  = 'wojtek0'
        IMAGE_NAME      = "wojtek0/flask-cicd-app"
        IMAGE_TAG       = "${env.BUILD_NUMBER}"
        // 'Username with password' credential ID stored in Jenkins
        DOCKERHUB_CREDS = 'dockerhub-creds'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build / Install deps') {
            steps {
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate.bat
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                bat '''
                    call venv\\Scripts\\activate.bat
                    pytest -v --junitxml=report.xml
                '''
            }
            post {
                always {
                    junit 'report.xml'
                }
            }
        }

        stage('Build Docker image') {
            steps {
                bat "docker build -t %IMAGE_NAME%:%IMAGE_TAG% -t %IMAGE_NAME%:latest ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                        credentialsId: "${DOCKERHUB_CREDS}",
                        usernameVariable: 'DH_USER',
                        passwordVariable: 'DH_PASS')]) {
                    bat '''
                        echo %DH_PASS% | docker login -u %DH_USER% --password-stdin
                        docker push %IMAGE_NAME%:%IMAGE_TAG%
                        docker push %IMAGE_NAME%:latest
                        docker logout
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline succeeded. Pushed ${IMAGE_NAME}:${IMAGE_TAG} and :latest"
        }
        failure {
            echo 'Pipeline failed - check the stage logs above.'
        }
        always {
            bat(script: 'docker image prune -f', returnStatus: true)
        }
    }
}
