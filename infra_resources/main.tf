terraform {
  cloud {
    organization = "farisology"
    workspaces {
      name = "aws_zenml"
    }
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

# config provider
provider "aws" {
  region = "ap-southeast-1"
}

data "aws_vpc" "default" {
  default = true
}

module "dev_ssh_sg" {
  source = "terraform-aws-modules/security-group/aws"

  name        = "dev_ssh_sg"
  description = "Security group for dev_ssh_sg"
  vpc_id      = data.aws_vpc.default.id

  ingress_cidr_blocks = ["0.0.0.0/0"]
  ingress_rules       = ["ssh-tcp"]

  tags = {
    Name    = "dev_ssh_sg"
    Project = "MLOps"
    Owner   = "Farisology"

  }
}

module "zenml_ec2_sg" {
  source = "terraform-aws-modules/security-group/aws"

  name        = "zenml_ec2_sg"
  description = "Security group for zenml_ec2_sg"
  vpc_id      = data.aws_vpc.default.id

  ingress_cidr_blocks = ["0.0.0.0/0"]
  ingress_rules       = ["http-80-tcp", "https-443-tcp"]
  egress_rules        = ["all-all"]

  tags = {
    Name    = "zenml_ec2_sg"
    Project = "MLOps"
    Owner   = "Farisology"

  }
}


resource "aws_instance" "zenml_server" {
  ami           = "ami-0df7a207adb9748c7"
  instance_type = "t2.micro"
  key_name      = "zenml_server"
  root_block_device {
    volume_size = 30
  }
  vpc_security_group_ids = [
    module.zenml_ec2_sg.security_group_id,
    module.dev_ssh_sg.security_group_id,
  ]
  tags = {
    Name    = "ZenML Server"
    Project = "MLOps"
    Owner   = "Farisology"
  }
}

resource "aws_s3_bucket" "zenml_bucket" {
  bucket = "my-zenml-mlops-bucket"

  tags = {
    Name    = "ZenML Bucket"
    Project = "MLOps"
    Owner   = "Farisology"
  }
}

resource "aws_ecr_repository" "zenml_registry" {
  name                 = "zenml-registry"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
  tags = {
    Name    = "ZenML Registry"
    Project = "MLOps"
    Owner   = "Farisology"
  }
}
