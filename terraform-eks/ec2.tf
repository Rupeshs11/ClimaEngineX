resource "aws_default_vpc" "default" {}

resource "aws_security_group" "devops-sg" {
  name        = "devops-sg"
  vpc_id      = aws_default_vpc.default.id

  # SSH Access
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Jenkins Port
  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # SonarQube Port
  ingress {
    from_port   = 9000
    to_port     = 9000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Outbound Rules
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Jenkins & SonarQube CI/CD Server

resource "aws_instance" "ci_server" {
  key_name               = "sage"
  vpc_security_group_ids = [aws_security_group.devops-sg.id]
  instance_type          = "m7i-flex.large"
  ami                    = var.ec2_ami_id

  root_block_device {
    volume_size = 40
    volume_type = "gp3"
  }

  user_data = file("scripts/setup.sh")

  tags = {
    Name = "Jenkins-SonarQube-Server"
  }
}
