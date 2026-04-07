output "aws_account_id" {
  value = data.aws_caller_identity.current.account_id
}

output "ecr_repository_url" {
  description = "The URL of the private ECR repository used for Docker pushes"
  value       = aws_ecr_repository.app_repo.repository_url
}

output "dynamodb_table_name" {
  description = "The name of the DynamoDB table for metrics"
  value       = aws_dynamodb_table.monitoring_results.name
}

output "dynamodb_table_arn" {
  description = "The Amazon Resource Name (ARN) of the metrics table"
  value       = aws_dynamodb_table.monitoring_results.arn
}

output "app_iam_role_arn" {
  description = "The IAM Role ARN that the Lambda will assume"
  value       = aws_iam_role.app_role.arn
}