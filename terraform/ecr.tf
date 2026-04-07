# tfsec:ignore:aws-ecr-repository-customer-key
resource "aws_ecr_repository" "app_repo" {
  name                 = "argus-monitor"
  image_tag_mutability = "IMMUTABLE"

  # tfsec:ignore:aws-ecr-repository-customer-key
  image_scanning_configuration {
    scan_on_push = true
  }
}