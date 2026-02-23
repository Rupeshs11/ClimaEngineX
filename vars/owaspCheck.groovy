def call(String installationName = 'DP-Check') {
    dependencyCheck additionalArguments: '--scan . --format HTML --format XML', odcInstallation: installationName
    dependencyCheckPublisher pattern: 'dependency-check-report.xml'
}
