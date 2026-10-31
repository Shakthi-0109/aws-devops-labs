variable "aws_region" {
  description = "Target AWS region for infrastructure"
  type        = string
  default     = "us-east-1"
}

variable "bucket_prefix" {
  description = "Unique naming prefix for the logging bucket"
  type        = string
  default     = "devops-iac-logs-shakthi-1147"
}

variable "environment" {
  description = "Deployment environment name"
  type        = string
  default     = "production"
}