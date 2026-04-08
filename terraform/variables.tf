variable "aws_region" {
  default = "us-east-1"
}

variable "project_name" {
  default = "project-argus"
}

variable "instance_type" {
  default = "t2.micro"
}

variable "my_ip" {
  description = "My home IP address for SSH access"
  type        = string
}