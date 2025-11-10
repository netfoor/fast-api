locals {
  public_subnets = [
    for subnet in data.aws_subnet.default :
    subnet.id if subnet.map_public_ip_on_launch == true
  ]

  selected_subnet = length(local.public_subnets) > 0 ? local.public_subnets[0] : data.aws_subnets.default.ids[0]
}

resource "aws_instance" "ubuntu" {
  ami           = var.ami_id
  instance_type = var.instance_type

  subnet_id                   = local.selected_subnet
  vpc_security_group_ids      = [aws_security_group.api.id]
  associate_public_ip_address = true

  iam_instance_profile = aws_iam_instance_profile.ssm_instance_profile.name

  user_data = <<-EOF
                #!/bin/bash
                apt-get update -y
                apt-get upgrade -y
                EOF


  lifecycle {
    create_before_destroy = true
  }

  root_block_device {
    volume_type           = "gp2"
    delete_on_termination = true
    volume_size           = 20
    encrypted             = true
    tags = {
      Name    = "${var.project_name}-${var.environment}-root-volume"
      Project = var.project_name
    }
  }

  metadata_options {
    http_tokens                 = "required"
    http_endpoint               = "enabled"
    http_put_response_hop_limit = 1
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-instance"
    Project     = var.project_name
    Owner       = var.owner
    Environment = var.environment
  }
}
