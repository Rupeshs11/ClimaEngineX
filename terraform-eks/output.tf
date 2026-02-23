output "ci_server_public_ip" {
  description = "Public IP of the Jenkins/SonarQube CI server"
  value       = aws_instance.ci_server.public_ip
}

output "ci_server_instance_id" {
  description = "Instance ID of the CI server"
  value       = aws_instance.ci_server.id
}

output "security_group_id" {
  description = "Security Group ID for the CI server"
  value       = aws_security_group.devops-sg.id
}
