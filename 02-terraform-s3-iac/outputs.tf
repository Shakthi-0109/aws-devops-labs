output "bucket_name" {
  description = "The globally unique S3 bucket name"
  value       = aws_s3_bucket.log_storage.id
}

output "bucket_arn" {
  description = "The Amazon Resource Name (ARN) of the bucket"
  value       = aws_s3_bucket.log_storage.arn
}