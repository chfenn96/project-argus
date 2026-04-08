terraform {
  required_version = ">= 1.5.0"

  backend "s3" {
    bucket         = "argus-tf-state-638175140581"
    key            = "global/s3/terraform.tfstate" 
    region         = "us-east-1"
    dynamodb_table = "terraform-state-locking"
    encrypt        = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}