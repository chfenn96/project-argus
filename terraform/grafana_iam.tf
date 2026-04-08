# 1. THE USER
resource "aws_iam_user" "grafana" {
  name = "grafana-cloud-reader"
}

# 2. THE GROUP (Result #3 Fix: No direct user policies)
resource "aws_iam_group" "observability_readers" {
  name = "observability-readers"
}

# 3. THE MEMBERSHIP: Put the user in the group
resource "aws_iam_group_membership" "grafana_team" {
  name = "grafana-group-membership"
  users = [aws_iam_user.grafana.name]
  group = aws_iam_group.observability_readers.name
}

# 4. THE KEYS (Still linked to the user)
resource "aws_iam_access_key" "grafana" {
  user = aws_iam_user.grafana.name
}

# 5. THE GROUP POLICY (Results #1-2 Fix: Scoped Resources)
resource "aws_iam_group_policy" "grafana_read" {
  name  = "GrafanaCloudWatchRead"
  group = aws_iam_group.observability_readers.name

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
        Resource = "*" # tfsec:ignore:aws-iam-no-policy-wildcards (Required for discovery)
      },
      {
        # LOGS PERMISSIONS (Results #1-2 Fix)
        # We scope these to our specific Lambda Log Group
        Action = [
          "logs:GetLogEvents",
          "logs:FilterLogEvents",
          "logs:StartQuery",
          "logs:GetQueryResults"
        ]
        Effect   = "Allow"
        Resource = "arn:aws:logs:us-east-1:${local.account_id}:log-group:/aws/lambda/argus-monitor-function:*"
      },
      {
        # Result #1-2 Fix: DescribeLogGroups requires wildcard to list all groups
        Action = ["logs:DescribeLogGroups"]
        Effect = "Allow"
        # tfsec:ignore:aws-iam-no-policy-wildcards
        Resource = "*" 
      },
      {
        Action = ["tag:GetResources"]
        Effect = "Allow"
        # tfsec:ignore:aws-iam-no-policy-wildcards
        Resource = "*"
      }
    ]
  })
}