output "public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.docker_host.public_ip
}

output "ssh_command" {
  description = "Exact command to connect into the Linux Docker host"
  value       = "ssh -i ~/.ssh/devops_ec2_key ubuntu@${aws_instance.docker_host.public_ip}"
}