resource "aws_security_group" "ssm_sg" {
    name        = "${var.project_name}-${var.environment}-ssm-sg"
    description = "Security group for SSM only access"
    vpc_id      = data.aws_vpc.default.id

    egress = {
        description = "Allow HTTPS outbound for SSM"
        from_port   = 443
        to_port     = 443
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress = {
        description = "Allow HTTPS"
        from_port  = 8000   
        to_port    = 8000
        protocol   = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    tags = {
        Name        = "${var.project_name}-${var.environment}-ssm-sg"
        Environment = var.environment
        Project     = var.project_name
    }
}

data "aws_vpc" "default" {
    default = true
}

data "aws_subnet_ids" "default" {
    filter {
        name   = "vpc-id"
        values = [data.aws_vpc.default.id]
    }
}