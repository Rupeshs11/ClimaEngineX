def call(Map config = [:]) {
    String scanType = config.get('type', 'fs')       // 'fs' or 'image'
    String target   = config.get('target', '.')       // path or image name
    String severity = config.get('severity', 'HIGH,CRITICAL')

    sh "trivy ${scanType} --severity ${severity} --format table ${target}"
}
