pipeline {
    agent any

    environment {
        DOCKERHUB_CREDS = credentials('dockerhub-creds')
        SONAR_TOKEN     = credentials('sonar-token')
        SONAR_URL       = 'http://<SONARQUBE_IP>:9000'

        DOCKER_IMAGE    = "${DOCKERHUB_CREDS_USR}/knoxweather"
        IMAGE_TAG       = "${BUILD_NUMBER}"
        GITOPS_REPO     = 'https://github.com/<YOUR_USERNAME>/ClimaEngineX.git'
        GITOPS_REPO_RAW = 'github.com/<YOUR_USERNAME>/ClimaEngineX.git'
    }

    stages {
        stage('Clean Workspace') {
            steps { cleanWorkspace() }
        }

        stage('Checkout') {
            steps { gitCheckout(branch: 'main', repoUrl: "${GITOPS_REPO}") }
        }

        stage('Check for CI Skip') {
            steps { ciSkipCheck() }
        }

        stage('OWASP Dependency-Check') {
            when { expression { env.SKIP_CI != 'true' } }
            steps { owaspCheck() }
        }

        stage('SonarQube Analysis') {
            when { expression { env.SKIP_CI != 'true' } }
            steps {
                sonarAnalysis(
                    projectKey:  'knoxweather',
                    projectName: 'knoxweather',
                    sonarUrl:    "${SONAR_URL}",
                    sonarToken:  "${SONAR_TOKEN}"
                )
            }
        }

        stage('Trivy FS Scan') {
            when { expression { env.SKIP_CI != 'true' } }
            steps { trivyScan(type: 'fs', target: '.') }
        }

        stage('Docker Build & Push') {
            when { expression { env.SKIP_CI != 'true' } }
            steps {
                dockerBuildPush(
                    imageName: "${DOCKER_IMAGE}",
                    imageTag:  "${IMAGE_TAG}",
                    username:  "${DOCKERHUB_CREDS_USR}",
                    password:  "${DOCKERHUB_CREDS_PSW}"
                )
            }
        }

        stage('Trivy Image Scan') {
            when { expression { env.SKIP_CI != 'true' } }
            steps { trivyScan(type: 'image', target: "${DOCKER_IMAGE}:${IMAGE_TAG}") }
        }

        stage('Update K8s Manifests') {
            when { expression { env.SKIP_CI != 'true' } }
            steps {
                updateK8sManifests(
                    imageName: "${DOCKER_IMAGE}",
                    imageTag:  "${IMAGE_TAG}",
                    repoUrl:   "${GITOPS_REPO_RAW}"
                )
            }
        }
    }

    post {
        always {
            sh "docker rmi ${DOCKER_IMAGE}:${IMAGE_TAG} || true"
            cleanWs()
        }
        success {
            echo '✅ Pipeline completed successfully!'
            mail to: '<YOUR_EMAIL>',
                 subject: "✅ SUCCESS: ${currentBuild.fullDisplayName}",
                 body: "The KnoxWeather pipeline completed successfully.\n\nBuild: ${env.BUILD_URL}"
        }
        failure {
            echo '❌ Pipeline failed!'
            mail to: '<YOUR_EMAIL>',
                 subject: "❌ FAILED: ${currentBuild.fullDisplayName}",
                 body: "The KnoxWeather pipeline failed.\n\nBuild: ${env.BUILD_URL}"
        }
    }
}
