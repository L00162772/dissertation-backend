# Note SSL certs can only be created in this region
resource "aws_acm_certificate" "cloudfront_cert" {
  provider          = aws.east1
  domain_name       = local.cloudfront_domain
  validation_method = "DNS"
  lifecycle {
    create_before_destroy = true
  }
}



resource "aws_acm_certificate_validation" "cloudfront_cert_validation" {
  certificate_arn         = aws_acm_certificate.cloudfront_cert.arn
  provider                = aws.east1
  validation_record_fqdns = [for record in aws_route53_record.cloudfront_route53_validation_record : record.fqdn]
  depends_on = [
    aws_route53_record.cloudfront_route53_validation_record
  ]
}

resource "aws_acm_certificate" "alb_cert" {
  provider          = aws.east1
  domain_name       = local.alb_domain
  validation_method = "DNS"
  lifecycle {
    create_before_destroy = true
  }
}



resource "aws_acm_certificate_validation" "alb_cert_validation" {
  certificate_arn         = aws_acm_certificate.alb_cert.arn
  provider                = aws.east1
  validation_record_fqdns = [for record in aws_route53_record.alb_route53_validation_record : record.fqdn]
  depends_on = [
    aws_route53_record.alb_route53_validation_record
  ]
}