resource "aws_instance" "this" {
    ami          = var.ami_id
    instance_type = var.instance_type

    subnet_id = var.subnet_id
    vpc_security_group_ids = var.security_groups

    associate_public_ip_address = var.public_ip

    iam_instance_profile = var.iam_instance_profile

    lifecycle {
    create_before_destroy = true
  }
  
    root_block_device {
      volume_type = var.disk_type
      volume_size = var.disk_size
      delete_on_termination = true
      encrypted = true
    }

    metadata_options {
      http_tokens = "required"
      http_endpoint = "enabled"
    }

    tags = merge(
      var.tags,
      {
        Name = "${var.project}-${var.environment}-instance"
      }
    )
  
}