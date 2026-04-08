# 1. S3 Bucket for State
# tfsec:ignore:aws-s3-enable-bucket-logging (FinOps: Avoiding cost of extra logging bucket)
resource "aws_s3_bucket" "terraform_state" {
  bucket = "argus-tf-state-${data.aws_caller_identity.current.account_id}"

  lifecycle {
    prevent_destroy = true
  }
}

# 2. Enable versioning
resource "aws_s3_bucket_versioning" "enabled" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

# 3. Enable Server-Side Encryption (Free via S3-Managed Keys)
# tfsec:ignore:aws-s3-encryption-customer-key (FinOps: Using S3-managed key to stay in free tier)
resource "aws_s3_bucket_server_side_encryption_configuration" "default" {
  bucket = aws_s3_bucket.terraform_state.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# 4. BLOCK ALL PUBLIC ACCESS (Result #2, #3, #11 Fix)
resource "aws_s3_bucket_public_access_block" "public_access" {
  bucket                  = aws_s3_bucket.terraform_state.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# 5. DynamoDB Table for Locking
# tfsec:ignore:aws-dynamodb-table-customer-key (FinOps: Using AWS-managed key)
resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-state-locking"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  # Result #1 Fix: Enable encryption at rest
  server_side_encryption {
    enabled = true
  }

  point_in_time_recovery {
    enabled = true
  }

  attribute {
    name = "LockID"
    type = "S"
  }
}