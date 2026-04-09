# 1. The Megaphone
resource "aws_sns_topic" "alerts" {
  name = "${var.project_name}-alerts"
  tags = merge(local.common_tags, {
    Name = "${var.project_name}-alerts"
  })
}

# 2. The Person listening to the megaphone
resource "aws_sns_topic_subscription" "email_alert" {
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "email"
  endpoint  = var.alert_email
}

# 3. Giving the Worker permission to use the megaphone
resource "aws_iam_role_policy" "sns_publish_policy" {
  name = "argus-sns-policy"
  role = aws_iam_role.app_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = "sns:Publish"
        Effect   = "Allow"
        Resource = aws_sns_topic.alerts.arn 
      }
    ]
  })
}

# Output the Topic ARN so our Python code can find it
output "sns_topic_arn" {
  value = aws_sns_topic.alerts.arn
}