def call(Map config = [:]) {
    String imageName = config.get('imageName')
    String imageTag  = config.get('imageTag')
    String username  = config.get('username')
    String password  = config.get('password')

    sh "docker build -t ${imageName}:${imageTag} ."
    sh "echo ${password} | docker login -u ${username} --password-stdin"
    sh "docker push ${imageName}:${imageTag}"
}
