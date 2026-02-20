terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }

  backend "s3" {
    bucket = "knoxweather-tf-state"
    key    = "terraform.tfstate"
    region = "ap-south-1"
  }
}
