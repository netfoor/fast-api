resource "aws_instance" "ubuntu" {
    ami = var.ami_id
    instance_type = var.instance_type
    subnet_id = data.aws_subnet_ids.default.ids[0]
    iam_instance_profile = aws_iam_instance_profile.ssm_instance_profile.name
    vpc_security_group_ids = [aws_security_group.ssm_sg.id]
    associate_public_ip_address = true
    
    user_data = <<-EOF
                #!/bin/bash
                apt-get update -y
                apt-get upgrade -y
                EOF


    lifecycle {
        create_before_destroy = true
    }


    tags = {
        Name = "${var.project_name}-${var.environment}-instance"
        Project = var.project_name
        Owner   = var.owner
        Environment = var.environment
    }
}
