output "dev_instance_id" {
  description = "The ID of the development instance"
  value       = module.ec2_api.instance_id

}

output "dev_instance_public_ip" {
  description = "The public IP address of the development instance"
  value       = module.ec2_api.instance_public_ip

}
