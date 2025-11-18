output "sg_id" {
  description = "The ID of the security group"
  value       = aws_security_group.this.id
  
}

output "iam_instance_profile" {
  description = "The IAM instance profile for SSM"
  value       = aws_iam_instance_profile.ssm_instance_profile.name
  
}