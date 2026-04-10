# 1. IAM Role for our Monitoring App
resource "aws_iam_role" "app_role" {
  name = "${var.project_name}-app-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# 2. This gives the Lambda permission to write logs to CloudWatch
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.app_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# 3. Security Group (The "Virtual Firewall")
resource "aws_security_group" "app_sg" {
  name        = "${var.project_name}-app-sg"
  description = "Allow outbound traffic for monitoring"
  vpc_id      = aws_vpc.main.id

  # Egress: Allow all outbound traffic so we can ping websites
  egress {
    # tfsec:ignore:aws-ec2-no-public-egress-sgr
    description = "Allow outbound pings to the internet for uptime monitoring"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    # tfsec:ignore:aws-ec2-no-public-egress-sgr
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Allow SSH from everywhere for troubleshooting"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip] 
  }

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-app-sg"
  })
}