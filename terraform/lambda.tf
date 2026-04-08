resource "aws_lambda_function" "monitor_lambda" {
  function_name = "argus-monitor-function"
  role          = aws_iam_role.app_role.arn
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.app_repo.repository_url}:latest"

  # Enable tracing
  tracing_config {
    mode = "Active"
  }

  # Prevents Terraform from trying to undo the work the GitHub Action does
  lifecycle {
    ignore_changes = [image_uri]
  }

  memory_size = 128 # The smallest (and cheapest) amount
  timeout     = 30

  environment {
    variables = {
      # Add as many URLs as you want here, separated by commas!
      URLS_TO_MONITOR = "https://www.google.com,https://www.github.com,https://www.wikipedia.org"
    }
  }

}