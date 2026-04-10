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