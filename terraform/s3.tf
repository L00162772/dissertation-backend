data "aws_iam_policy_document" "s3-website-policy" {
  statement {
    actions = [
      "s3:GetObject"
    ]
    principals {
      identifiers = ["*"]
      type        = "AWS"
    }
    resources = [
      "arn:aws:s3:::${var.aws_region}-${var.bucket_name_postfix}/*"
    ]
  }
}

resource "aws_s3_bucket" "lambda_bucket" {
  bucket        = "${var.aws_region}-${var.bucket_name_postfix}"
  force_destroy = true
  acl           = "private"
}





