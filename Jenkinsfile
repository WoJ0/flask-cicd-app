pipeline {
    agent any

    environment {
        // Docker Hub image name -> wojtek0/flask-cicd-app
        DOCKERHUB_USER  = 'wojtek0'
        IMAGE_NAME      = "wojtek0/flask-cicd-app"
        IMAGE_TAG       = "${env.BUILD_NUMBER}"
        // ID of the 'Username with password' credential you add in Jenkins
        DOCKERHUB_CREDS = 'dockerhub-creds'
    }

    stages {
        stage('Checkout') {
            steps {
                // Pulls the code from GitHub (configured in the job / via webhook)
                checkout scm
            }
        }

        stage('Build / Install deps') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . venv/bin/activate
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
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                        credentialsId: "${DOCKERHUB_CREDS}",
                        usernameVariable: 'DH_USER',
                        passwordVariable: 'DH_PASS')]) {
                    sh '''
                        echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin
                        docker push ''' + "${IMAGE_NAME}:${IMAGE_TAG}" + '''
                        docker push ''' + "${IMAGE_NAME}:latest" + '''
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
            sh 'docker image prune -f || true'
        }
    }
}
