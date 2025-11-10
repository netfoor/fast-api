variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "FastAPI on EC2"
}

variable "owner" {
  description = "Owner of the resources"
  type        = string
  default     = "fortino.rom@gmail.com"
}

variable "environment" {
  description = "Environment for the resources"
  type        = string
  default     = "development"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "ami_id" {
  description = "AMI ID for the EC2 instance"
  type        = string
  default     = "ami-0ecb62995f68bb549"
}

variable "allowed_ssh_cidr" {
  description = "CIDR blocks allowed to access via SSH"
  type        = list(string)
  default     = []
}