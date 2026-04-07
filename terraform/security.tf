# 1. IAM Role for our Monitoring App
resource "aws_iam_role" "app_role" {
  name = "argus-app-role"

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

# 2. Security Group (The "Virtual Firewall")
resource "aws_security_group" "app_sg" {
  name        = "argus-app-sg"
  description = "Allow outbound traffic for monitoring"
  vpc_id      = aws_vpc.main.id

  # Egress: Allow all outbound traffic so we can ping websites
  egress {
    # tfsec:ignore:aws-ec2-no-public-egress-sgr
    description = "Allow outbound pings to the internet for uptime monitoring"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "argus-app-sg"
  }
}