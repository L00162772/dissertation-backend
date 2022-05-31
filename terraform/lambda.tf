data "archive_file" "crud_lambda_function" {
  type = "zip"

  source_dir  = "./backend/"
  output_path = "./backendOutput/crud-lambda.zip"
}

resource "aws_s3_object" "crud_lambda_function" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "crud-lambda.zip"
  source = data.archive_file.crud_lambda_function.output_path

  etag = filemd5(data.archive_file.crud_lambda_function.output_path)
  depends_on = [
    data.archive_file.crud_lambda_function
  ]
}

resource "aws_lambda_function" "crud_lambda_function" {
  function_name = "${var.application_type}_lambda"

  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.crud_lambda_function.key

  runtime = "nodejs14.x"
  handler = "crud-lambda.handler"

  source_code_hash = data.archive_file.crud_lambda_function.output_base64sha256

  role = aws_iam_role.crud_lambda_exec.arn

  timeout = 90
}

resource "aws_iam_role_policy" "crud_lambda_policy" {
  name = "crud_lambda_policy"
  role = aws_iam_role.crud_lambda_exec.id

  policy = file("policies/policy.json")
}


resource "aws_iam_role" "crud_lambda_exec" {
  name               = "${var.application_type}_crud_lambda_exec_role"
  assume_role_policy = file("policies/assume_role_policy.json")
}
resource "aws_iam_role_policy_attachment" "crud_lambda_exec_attacment" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.crud_lambda_exec.name
}


resource "aws_lambda_permission" "with_lb_crud_lambda" {
  statement_id  = "AllowExecutionFromlb"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.crud_lambda_function.arn
  principal     = "elasticloadbalancing.amazonaws.com"
  source_arn    = aws_lb_target_group.crud_lambda_tg.arn
}
