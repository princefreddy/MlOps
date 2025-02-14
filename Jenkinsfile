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
                    docker.build("${env.DOCKERHUB_REPO}/preprocessing:latest", "--target preprocessing .").push()
                }
            }
        }

        stage('Run Preprocessing') {
            steps {
                script {
                    docker.image("${env.DOCKERHUB_REPO}/preprocessing:latest").run(
                        "-v preprocessing-data:/app/data -v preprocessing-output:/app/output"
                    )
                }
            }
        }

        stage('Build Training Image') {
            steps {
                script {
                    docker.build("${env.DOCKERHUB_REPO}/training:latest", "--target training .").push()
                }
            }
        }

        stage('Run Training') {
            steps {
                script {
                    docker.image("${env.DOCKERHUB_REPO}/training:latest").run(
                        "-v preprocessing-output:/app/data -v training-models:/app/models"
                    )
                }
            }
        }

        stage('Build Evaluation Image') {
            steps {
                script {
                    docker.build("${env.DOCKERHUB_REPO}/evaluation:latest", "--target evaluation .").push()
                }
            }
        }

        stage('Run Evaluation') {
            steps {
                script {
                    docker.image("${env.DOCKERHUB_REPO}/evaluation:latest").run(
                        "-v preprocessing-output:/app/data -v training-models:/app/models -v evaluation-metrics:/app/metrics"
                    )
                }
            }
        }

        stage('Store Model and Metrics on Jenkins') {
            steps {
                script {
                    // Copier le modèle entraîné depuis le volume Docker
                    sh 'docker run --rm -v training-models:/app/models -v ${WORKSPACE}:/output busybox cp -r /app/models /output/models'

                    // Copier les métriques d'évaluation depuis le volume Docker
                    sh 'docker run --rm -v evaluation-metrics:/app/metrics -v ${WORKSPACE}:/output busybox cp -r /app/metrics /output/metrics'

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
                sh 'docker system prune -f'
            }
        }
    }
}