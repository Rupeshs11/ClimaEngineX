def call(Map config = [:]) {
    String imageName   = config.get('imageName')
    String imageTag    = config.get('imageTag')
    String repoUrl     = config.get('repoUrl')
    String credentialsId = config.get('credentialsId', 'github-creds')

    withCredentials([gitUsernamePassword(credentialsId: credentialsId, gitToolName: 'Default')]) {
        sh """
            cd k8s

            sed -i "s|image:.*|image: '${imageName}:${imageTag}'|" deployment.yaml

            git config user.email "jenkins@knoxcloud.tech"
            git config user.name "Jenkins CI"

            git add deployment.yaml
            git commit -m "Pipeline deployment: ${imageTag} [ci skip]"

            git push "https://\${GIT_USERNAME}:\${GIT_PASSWORD}@${repoUrl}" HEAD:main
        """
    }
}
