variable "ami_id" {
  description = "The ID of the AMI to use for the EC2 instance"
  type        = string
  
}

variable "instance_type" {
  description = "The type of instance to use"
  type        = string
  default     = "t2.micro"
}

variable "subnet_id" {
  description = "The ID of the subnet to launch the instance in"
  type        = string
}

variable "security_groups" {
  description = "A list of security group IDs to associate with the instance"
  type        = list(string)
  default     = []
  
}

variable "public_ip" {
  description = "Whether to assign a public IP address to the instance"
  type        = bool
  default     = true
  
}

variable "iam_instance_profile" {
  description = "The name of the IAM instance profile to associate with the instance"
  type        = string
  default     = null
  
}

variable "disk_size" {
  description = "The size of the root EBS volume in GB"
  type        = number
  default     = 10
  
}

variable "disk_type" {
  description = "The type of the root EBS volume"
  type        = string
  default     = "gp2"
  
}

variable "project" {
  description = "The name of the project"
  type        = string
}

variable "environment" {
  description = "The deployment environment (e.g., dev, staging, prod)"
  type        = string
  
}

variable "tags" {
  description = "A map of tags to assign to the instance"
  type        = map(string)
  default     = {}
  
}