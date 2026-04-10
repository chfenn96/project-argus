resource "aws_cloudwatch_dashboard" "main" {
  dashboard_name = "Argus-Uptime-Monitor"

  # The 'dashboard_body' is a JSON string that describes the layout
  dashboard_body = jsonencode({
    widgets = [
      {
        type   = "metric"
        x      = 0
        y      = 0
        width  = 12
        height = 6
        properties = {
          metrics = [
            [ "AWS/Lambda", "Duration", "FunctionName", "argus-monitor-function" ]
          ]
          period = 300
          stat   = "Average"
          region = var.aws_region
          title  = "Lambda Execution Time (Latency)"
        }
      },
      {
        type   = "metric"
        x      = 12
        y      = 0
        width  = 12
        height = 6
        properties = {
          metrics = [
            [ "AWS/Lambda", "Invocations", "FunctionName", "argus-monitor-function" ]
          ]
          period = 300
          stat   = "Sum"
          region = var.aws_region
          title  = "Total Checks (Invocations)"
        }
      }
    ]
  })
}

# Explicitly create the Log Group
# This ensures it exists before the filter is applied
# tfsec:ignore:aws-cloudwatch-log-group-customer-key (FinOps: Using AWS managed keys to stay in free tier)
resource "aws_cloudwatch_log_group" "monitor_log_group" {
  name              = "/aws/lambda/${var.project_name}-monitor-function"
  retention_in_days = 7 # FinOps: Only keep logs for 7 days to save money!
  tags              = local.common_tags
}

# Update the Metric Filter to use the managed Log Group
resource "aws_cloudwatch_log_metric_filter" "uptime_success" {
  name           = "UptimeSuccessCount"
  # FIX: Look at the top level of the JSON line for status = "UP"
  pattern        = "{ $.status = \"UP\" }" 
  log_group_name = aws_cloudwatch_log_group.monitor_log_group.name

  metric_transformation {
    name      = "SuccessCount"
    namespace = "ArgusCustom"
    value     = "1"
  }
}