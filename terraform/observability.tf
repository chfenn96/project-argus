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
          region = "us-east-1"
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
          region = "us-east-1"
          title  = "Total Checks (Invocations)"
        }
      }
    ]
  })
}