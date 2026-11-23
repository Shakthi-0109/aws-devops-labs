variable "aws_region" {
  description = "Target AWS region"
  type        = string
  default     = "us-east-1"
}

variable "repository_name" {
  description = "Name for the private ECR repository"
  type        = string
  default     = "devops-log-collector"
}