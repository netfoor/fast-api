variable "project" {
    description = "The project ID where the security group will be created."
    type        = string
}

variable "environment" {
    description = "The environment where the security group will be created."
    type        = string
}

variable "description" {
    description = "The description of the security group."
    type        = string
}

variable "vpc_id" {
    description = "The VPC ID where the security group will be created."
    type        = string
}

variable "ingress_rules" {
    description = "The list of ingress rules for the security group."
    type        = list(object({
        description = string
        from_port   = number
        to_port     = number
        protocol    = string
        cidr_blocks = list(string)
    }))
}

variable "tags" {
    description = "The tags to assign to the security group."
    type        = map(string)
    default     = {}
}