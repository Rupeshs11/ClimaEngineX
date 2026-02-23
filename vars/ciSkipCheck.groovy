def call() {
    script {
        def commitMessage = sh(script: 'git log -1 --pretty=%B', returnStdout: true).trim()
        if (commitMessage.contains('[ci skip]')) {
            env.SKIP_CI = 'true'
            currentBuild.description = 'Skipped - automated commit'
        } else {
            env.SKIP_CI = 'false'
        }
    }
}
