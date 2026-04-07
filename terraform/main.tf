# This just asks AWS "Who am I?" to verify our credentials work
data "aws_caller_identity" "current" {}

output "aws_account_id" {
  value = data.aws_caller_identity.current.account_id
}