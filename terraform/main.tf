# This just asks AWS "Who am I?" to verify our credentials work
data "aws_caller_identity" "current" {}

# Look up the region we are currently working in (should be us-east-1)
data "aws_region" "current" {}

locals {
  account_id = data.aws_caller_identity.current.account_id
  region     = data.aws_region.current.name
  
  # Logic: Create a standard set of tags to apply to EVERYTHING
  common_tags = {
    Project   = var.project_name
    ManagedBy = "Terraform"
    Owner     = "Christian Fenn"
    Environment = "Dev"
  }
}