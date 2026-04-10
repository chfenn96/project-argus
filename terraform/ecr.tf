# tfsec:ignore:aws-ecr-repository-customer-key
resource "aws_ecr_repository" "app_repo" {
  name                 = "${var.project_name}-monitor"
  image_tag_mutability = "IMMUTABLE"

  force_delete         = true 

  # tfsec:ignore:aws-ecr-repository-customer-key
  image_scanning_configuration {
    scan_on_push = true
  }

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-repository"
  })
}

# Allows the Lambda service to pull images from this repository
resource "aws_ecr_repository_policy" "lambda_pull" {
  repository = aws_ecr_repository.app_repo.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowLambdaPull",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        },
        Action = [
          "ecr:BatchGetImage",
          "ecr:GetDownloadUrlForLayer"
        ]
      }
    ]
  })
}