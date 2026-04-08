# 1. THE USER: This is the actual "identity" in AWS
resource "aws_iam_user" "grafana" {
  name = "grafana-cloud-reader"
}

# 2. THE KEYS: This generates the Access Key and Secret Key for Grafana
resource "aws_iam_access_key" "grafana" {
  user = aws_iam_user.grafana.name
}

# 3. THE POLICY: This gives the user permission to read Metrics and Logs
resource "aws_iam_user_policy" "grafana_read" {
  name = "GrafanaCloudWatchRead"
  user = aws_iam_user.grafana.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        # METRICS PERMISSIONS
        Action = [
          "cloudwatch:DescribeAlarms",
          "cloudwatch:GetMetricData",
          "cloudwatch:GetMetricStatistics",
          "cloudwatch:ListMetrics"
        ]
        Effect   = "Allow"
        Resource = "*"
      },
      {
        # LOGS PERMISSIONS
        Action = [
          "logs:DescribeLogGroups",
          "logs:GetLogEvents",
          "logs:GetLogRecord",
          "logs:FilterLogEvents",
          "logs:StartQuery",
          "logs:StopQuery",
          "logs:GetQueryResults"
        ]
        Effect   = "Allow"
        Resource = "*"
      },
      {
        # TAGGING PERMISSIONS
        Action = [
          "tag:GetResources"
        ]
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}

# --- OUTPUTS ---
# We need these to paste into the Grafana UI
output "grafana_access_key" {
  value = aws_iam_access_key.grafana.id
}

output "grafana_secret_key" {
  value     = aws_iam_access_key.grafana.secret
  sensitive = true # Hides the secret from the terminal for security
}