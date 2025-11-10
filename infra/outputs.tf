output "instance_id" {
  description = "The ID of the EC2 instance"
  value       = aws_instance.ubuntu.id
}

output "instance_public_ip" {
  description = "The public IP address of the EC2 instance"
  value       = aws_instance.ubuntu.public_ip
}

output "api_url" {
  description = "The URL to access the FastAPI application"
  value       = "http://${aws_instance.ubuntu.public_ip}:8000"
}

output "ssm_connect_command" {
  description = "AWS CLI command to connect to the instance via SSM"
  value       = "aws ssm start-session --target ${aws_instance.ubuntu.id}"
}

output "security_group_id" {
  description = "The ID of the security group attached to the EC2 instance"
  value       = aws_security_group.api.id
}