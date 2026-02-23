def call(String projectKey, String projectName, String sonarUrl, String sonarToken, String scannerTool = 'sonar-scanner') {
    def scannerHome = tool scannerTool
    withSonarQubeEnv('sonarqube-server') {
        sh """
            ${scannerHome}/bin/sonar-scanner \\
              -Dsonar.projectKey=${projectKey} \\
              -Dsonar.projectName=${projectName} \\
              -Dsonar.sources=. \\
              -Dsonar.host.url=${sonarUrl} \\
              -Dsonar.token=${sonarToken}
        """
    }
}
