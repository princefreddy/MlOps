pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub') // Assurez-vous que cet ID correspond à vos credentials Jenkins
        DOCKERHUB_REPO = 'princefreddy' // Votre dépôt DockerHub
    }

    stages {
        stage('Build Preprocessing Image') {
            steps {
                script {
                    bat """
                        echo Building preprocessing image...
                        docker build --target preprocessing -t ${DOCKERHUB_REPO}/preprocessing:latest .
                    """
                    bat """
                        echo Logging into DockerHub...
                        echo DockerHub Username: ${DOCKERHUB_CREDENTIALS_USR}
                        echo DockerHub Password: ${DOCKERHUB_CREDENTIALS_PSW}
                        echo %DOCKERHUB_CREDENTIALS_PSW% | docker login -u %DOCKERHUB_CREDENTIALS_USR% --password-stdin
                    """
                    bat """
                        echo Pushing preprocessing image to DockerHub...
                        docker push ${DOCKERHUB_REPO}/preprocessing:latest
                    """
                }
            }
        }

        stage('Run Preprocessing') {
            steps {
                script {
                    bat """
                        echo Running preprocessing container...
                        docker run --rm -v preprocessing-data:/app/data -v preprocessing-output:/app/output ${DOCKERHUB_REPO}/preprocessing:latest
                    """
                }
            }
        }

        stage('Build Training Image') {
            steps {
                script {
                    bat """
                        echo Building training image...
                        docker build --target training -t ${DOCKERHUB_REPO}/training:latest .
                    """
                    bat """
                        echo Logging into DockerHub...
                        echo %DOCKERHUB_CREDENTIALS_PSW% | docker login -u %DOCKERHUB_CREDENTIALS_USR% --password-stdin
                    """
                    bat """
                        echo Pushing training image to DockerHub...
                        docker push ${DOCKERHUB_REPO}/training:latest
                    """
                }
            }
        }

        stage('Run Training') {
            steps {
                script {
                    bat """
                        echo Running training container...
                        docker run --rm -v preprocessing-output:/app/data -v training-models:/app/models ${DOCKERHUB_REPO}/training:latest
                    """
                }
            }
        }

        stage('Build Evaluation Image') {
            steps {
                script {
                    bat """
                        echo Building evaluation image...
                        docker build --target evaluation -t ${DOCKERHUB_REPO}/evaluation:latest .
                    """
                    bat """
                        echo Logging into DockerHub...
                        echo %DOCKERHUB_CREDENTIALS_PSW% | docker login -u %DOCKERHUB_CREDENTIALS_USR% --password-stdin
                    """
                    bat """
                        echo Pushing evaluation image to DockerHub...
                        docker push ${DOCKERHUB_REPO}/evaluation:latest
                    """
                }
            }
        }

        stage('Run Evaluation') {
            steps {
                script {
                    bat """
                        echo Running evaluation container...
                        docker run --rm -v preprocessing-output:/app/data -v training-models:/app/models -v evaluation-metrics:/app/metrics ${DOCKERHUB_REPO}/evaluation:latest
                    """
                }
            }
        }

        stage('Store Model and Metrics on Jenkins') {
            steps {
                script {
                    bat """
                        echo Copying trained model from Docker volume...
                        docker run --rm -v training-models:/app/models -v ${WORKSPACE}:/output busybox cp -r /app/models /output/models
                    """
                    bat """
                        echo Copying evaluation metrics from Docker volume...
                        docker run --rm -v evaluation-metrics:/app/metrics -v ${WORKSPACE}:/output busybox cp -r /app/metrics /output/metrics
                    """
                    archiveArtifacts artifacts: 'models/**/*,metrics/**/*', onlyIfSuccessful: true
                }
            }
        }
    }

    post {
        always {
            script {
                bat 'echo Cleaning up Docker system...'
                bat 'docker system prune -f'
            }
        }
    }
}