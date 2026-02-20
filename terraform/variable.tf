variable "ec2_instance_type" {
    default = "t3.micro"
    type = string
}

variable "aws_root_storage_size"{
    default = 15
    type = number
}

variable "ec2_ami_id" {
    default = "ami-0317b0f0a0144b137"
    type = string
  
}