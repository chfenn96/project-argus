# 1. THE CLOCK: Trigger every 5 minutes
resource "aws_cloudwatch_event_rule" "every_five_minutes" {
  name                = "${var.project_name}-check-timer"
  description         = "Triggers the Argus Uptime Monitor every 5 minutes"
  schedule_expression = "rate(5 minutes)" 
}

# 2. THE DIRECTION: Point the clock at the Lambda
resource "aws_cloudwatch_event_target" "check_every_five_minutes" {
  rule      = aws_cloudwatch_event_rule.every_five_minutes.name
  target_id = "TriggerLambda"
  arn       = aws_lambda_function.monitor_lambda.arn 
}

# 3. THE PERMISSION: Allow the clock to "turn the key" of the Lambda
resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.monitor_lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.every_five_minutes.arn
}