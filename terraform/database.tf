# tfsec:ignore:aws-dynamodb-table-customer-key
resource "aws_dynamodb_table" "monitoring_results" {
  name           = "ArgusMetrics"
  billing_mode   = "PAY_PER_REQUEST" 
  hash_key       = "url"             
  range_key      = "timestamp"       

  attribute {
    name = "url"
    type = "S" # S = String
  }

  attribute {
    name = "timestamp"
    type = "S"
  }

  # Enable recovery (Free for small tables)
  point_in_time_recovery {
    enabled = true
  }

  server_side_encryption {
    enabled = true
    # tfsec:ignore:aws-dynamodb-table-customer-key
  }

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-metrics-table"
  })
}

# Add a policy to App Role so it can actually WRITE to this table
resource "aws_iam_role_policy" "dynamodb_write_policy" {
  name = "${var.project_name}-dynamodb-policy"
  role = aws_iam_role.app_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "dynamodb:PutItem",
          "dynamodb:GetItem",
          "dynamodb:Query"
        ]
        Effect   = "Allow"
        Resource = aws_dynamodb_table.monitoring_results.arn
      }
    ]
  })
}