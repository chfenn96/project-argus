resource "aws_lambda_function" "monitor_lambda" {
  function_name = "argus-monitor-function"
  role          = aws_iam_role.app_role.arn
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.app_repo.repository_url}:latest"


  memory_size = 128 # The smallest (and cheapest) amount
  timeout     = 30

}