output "repository_url" {
  description = "The URI of the created ECR repository"
  value       = aws_ecr_repository.log_collector_repo.repository_url
}

output "repository_arn" {
  description = "The ARN of the ECR repository"
  value       = aws_ecr_repository.log_collector_repo.arn
}