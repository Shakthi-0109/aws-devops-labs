resource "aws_s3_bucket" "log_storage" {
  bucket = var.bucket_prefix

  tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
    Project     = "LogOffloader"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "log_storage_crypto" {
  bucket = aws_s3_bucket.log_storage.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "log_lifecycle" {
  bucket = aws_s3_bucket.log_storage.id

  rule {
    id     = "auto-archive-and-purge"
    status = "Enabled"

    filter {}

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    expiration {
      days = 90
    }
  }
}