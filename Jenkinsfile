pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        DOCKERHUB_REPO = 'princefreddy'
    }

    stages {
        stage('Build Preprocessing Image') {
            steps {
                script {
                    bat """
                        docker build --target preprocessing -t ${DOCKERHUB_REPO}/preprocessing:latest .
                        echo %DOCKER_PASSWORD% | docker login -u %DOCKER_USERNAME% --password-stdin
                        docker push ${DOCKERHUB_REPO}/preprocessing:latest
                    """
                }
            }
        }

        stage('Run Preprocessing') {
            steps {
                script {
                    bat """
                        docker run --rm -v preprocessing-data:/app/data -v preprocessing-output:/app/output ${DOCKERHUB_REPO}/preprocessing:latest
                    """
                }
            }
        }

        stage('Build Training Image') {
            steps {
                script {
                    bat """
                        docker build --target training -t ${DOCKERHUB_REPO}/training:latest .
                        echo %DOCKER_PASSWORD% | docker login -u %DOCKER_USERNAME% --password-stdin
                        docker push ${DOCKERHUB_REPO}/training:latest
                    """
                }
            }
        }

        stage('Run Training') {
            steps {
                script {
                    bat """
                        docker run --rm -v preprocessing-output:/app/data -v training-models:/app/models ${DOCKERHUB_REPO}/training:latest
                    """
                }
            }
        }

        stage('Build Evaluation Image') {
            steps {
                script {
                    bat """
                        docker build --target evaluation -t ${DOCKERHUB_REPO}/evaluation:latest .
                        echo %DOCKER_PASSWORD% | docker login -u %DOCKER_USERNAME% --password-stdin
                        docker push ${DOCKERHUB_REPO}/evaluation:latest
                    """
                }
            }
        }

        stage('Run Evaluation') {
            steps {
                script {
                    bat """
                        docker run --rm -v preprocessing-output:/app/data -v training-models:/app/models -v evaluation-metrics:/app/metrics ${DOCKERHUB_REPO}/evaluation:latest
                    """
                }
            }
        }

        stage('Store Model and Metrics on Jenkins') {
            steps {
                script {
                    // Copier le modèle entraîné depuis le volume Docker
                    bat """
                        docker run --rm -v training-models:/app/models -v ${WORKSPACE}:/output busybox cp -r /app/models /output/models
                    """

                    // Copier les métriques d'évaluation depuis le volume Docker
                    bat """
                        docker run --rm -v evaluation-metrics:/app/metrics -v ${WORKSPACE}:/output busybox cp -r /app/metrics /output/metrics
                    """

                    // Archiver les artefacts pour les stocker sur Jenkins
                    archiveArtifacts artifacts: 'models/**/*,metrics/**/*', onlyIfSuccessful: true
                }
            }
        }
    }

    post {
        always {
            script {
                // Clean up Docker images and containers
                bat 'docker system prune -f'
            }
        }
    }
}