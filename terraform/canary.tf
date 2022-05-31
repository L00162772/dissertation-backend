
resource "aws_iam_role" "canary_role" {
  name = "${var.aws_region}-canary_role"

  # Terraform's "jsonencode" function converts a
  # Terraform expression result to valid JSON syntax.
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_s3_bucket" "canary_s3_bucket" {
  bucket        = "${var.aws_region}-canary-${var.bucket_name_postfix}"
  force_destroy = true
  acl           = "private"
}


resource "aws_s3_bucket_public_access_block" "canary_s3_access_control" {
  bucket             = aws_s3_bucket.canary_s3_bucket.id
  block_public_acls  = true
  ignore_public_acls = true
}

# Zip the Lamda function on the fly
data "archive_file" "zip_synthetic_monitor" {
  type        = "zip"
  source_dir  = "./syntheticMonitorScripts"
  output_path = "./syntheticMonitorScriptsOutput/syntheticMonitor.zip"
}

# Upload synthetic monitoring test file to S3
resource "aws_s3_object" "synthetic_monitor" {
  bucket = aws_s3_bucket.canary_s3_bucket.id
  key    = "syntheticMonitor.zip"
  source = data.archive_file.zip_synthetic_monitor.output_path
  etag   = filemd5(data.archive_file.zip_synthetic_monitor.output_path)

  depends_on = [
    data.archive_file.zip_synthetic_monitor
  ]
}

resource "aws_synthetics_canary" "canary" {
  name                 = "${var.application_type}_canary"
  artifact_s3_location = "s3://${aws_s3_bucket.canary_s3_bucket.id}"
  execution_role_arn   = aws_iam_role.canary-role.arn
  runtime_version      = "syn-python-selenium-1.3"
  handler              = "syntheticMonitor.handler"
  s3_bucket            = aws_s3_bucket.canary_s3_bucket.id
  s3_key               = "syntheticMonitor.zip"
  start_canary         = false

  success_retention_period = 2
  failure_retention_period = 14

  schedule {
    expression          = "rate(1 minute)"
    duration_in_seconds = 0
  }

  run_config {
    timeout_in_seconds    = 60
    memory_in_mb          = 960
    active_tracing        = false
    environment_variables = { APPLICATION_URL = "https://${local.cloudfront_domain}" }
  }
  depends_on = [
    aws_s3_object.synthetic_monitor
  ]
}

data "aws_iam_policy_document" "canary-assume-role-policy" {
  statement {
    actions = ["sts:AssumeRole"]
    effect  = "Allow"

    principals {
      identifiers = ["lambda.amazonaws.com"]
      type        = "Service"
    }
  }
}

resource "aws_iam_role" "canary-role" {
  name               = "${var.aws_region}-${var.application_type}-canary-role"
  assume_role_policy = data.aws_iam_policy_document.canary-assume-role-policy.json
  description        = "IAM role for AWS Synthetic Monitoring Canaries"
}

data "aws_iam_policy_document" "canary-policy" {
  statement {
    sid    = "CanaryGeneric"
    effect = "Allow"
    actions = [
      "s3:PutObject",
      "s3:GetBucketLocation",
      "s3:ListAllMyBuckets",
      "cloudwatch:PutMetricData",
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "canary-policy" {
  name        = "${var.aws_region}-${var.application_type}-canary-policy"
  policy      = data.aws_iam_policy_document.canary-policy.json
  description = "IAM role for AWS Synthetic Monitoring Canaries"
}

resource "aws_iam_role_policy_attachment" "canary-policy-attachment" {
  role       = aws_iam_role.canary-role.name
  policy_arn = aws_iam_policy.canary-policy.arn
}

resource "aws_cloudwatch_event_rule" "canary-failed-event-rule" {
  name = "${var.aws_region}-canary-event-rule"
  event_pattern = jsonencode({
    source = ["aws.synthetics"]
    detail = {
      "canary-name" : [aws_synthetics_canary.canary.name],
      "test-run-status" : ["FAILED", "PASSED"]
    }
  })
}


resource "aws_cloudwatch_event_target" "canary-failed-event-target" {
  target_id = "${var.aws_region}-${var.application_type}CanaryFailed"
  arn       = aws_lambda_function.terraform_lambda_func.arn
  rule      = aws_cloudwatch_event_rule.canary-failed-event-rule.name
}


resource "aws_iam_role" "canary_lambda_role" {
  name               = "${var.aws_region}-canary-lambda-role"
  assume_role_policy = <<EOF
{
 "Version": "2012-10-17",
 "Statement": [
   {
     "Action": "sts:AssumeRole",
     "Principal": {
       "Service": "lambda.amazonaws.com"
     },
     "Effect": "Allow",
     "Sid": ""
   }
 ]
}
EOF
}

resource "aws_iam_policy" "canary_iam_policy_for_lambda" {

  name        = "${var.aws_region}_terraform_aws_lambda_role"
  path        = "/"
  description = "AWS IAM Policy for managing aws lambda role"
  policy      = <<EOF
{
 "Version": "2012-10-17",
 "Statement": [
   {
     "Action": [
       "logs:CreateLogGroup",
       "logs:CreateLogStream",
       "logs:PutLogEvents"
     ],
     "Resource": "arn:aws:logs:*:*:*",
     "Effect": "Allow"
   },
   {
     "Action": [
        "globalaccelerator:ListAccelerators",
        "globalaccelerator:ListTagsForResource",
        "globalaccelerator:ListListeners",
        "globalaccelerator:CreateEndpointGroup",
        "globalaccelerator:ListEndpointGroups",
        "globalaccelerator:DeleteEndpointGroup",
        "elasticloadbalancing:DescribeLoadBalancers"
     ],
     "Resource": "*",
     "Effect": "Allow"
   }
 ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "canary_attach_iam_policy_to_iam_role" {
  role       = aws_iam_role.canary_lambda_role.name
  policy_arn = aws_iam_policy.canary_iam_policy_for_lambda.arn
}

# Zip the Lamda function on the fly
data "archive_file" "zip_canary_lambda" {
  type        = "zip"
  source_dir  = "./canaryLambda"
  output_path = "./canaryLambdaOutput/canary_lambda.zip"
}

# Upload canary lambda file to S3
resource "aws_s3_object" "canary_lambda" {
  bucket = aws_s3_bucket.canary_s3_bucket.id
  key    = "canary_lambda.zip"
  source = data.archive_file.zip_canary_lambda.output_path
  etag   = filemd5(data.archive_file.zip_canary_lambda.output_path)

  depends_on = [
    data.archive_file.zip_canary_lambda
  ]
}

resource "aws_lambda_function" "terraform_lambda_func" {
  s3_bucket        = aws_s3_bucket.canary_s3_bucket.id
  s3_key           = "canary_lambda.zip"
  function_name    = "${var.application_type}_canary_lambda"
  role             = aws_iam_role.canary_lambda_role.arn
  handler          = "canary_lambda.lambda_handler"
  runtime          = "python3.9"
  source_code_hash = data.archive_file.zip_canary_lambda.output_base64sha256
  timeout          = 300

  environment {
    variables = {
      REGION           = var.aws_region
      APPLICATION_TYPE = var.application_type
    }
  }

  depends_on = [
    aws_iam_role_policy_attachment.canary_attach_iam_policy_to_iam_role,
    data.archive_file.zip_canary_lambda,
    aws_s3_object.canary_lambda
  ]
}

resource "aws_lambda_permission" "allow_eventbridge_to_call_canary_lambda" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = "${var.application_type}_canary_lambda"
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.canary-failed-event-rule.arn
}