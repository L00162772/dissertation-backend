
resource "aws_acm_certificate" "alb_cert" {
  domain_name       = local.alb_domain
  validation_method = "DNS"
  lifecycle {
    create_before_destroy = true
  }
}



resource "aws_acm_certificate_validation" "alb_cert_validation" {
  certificate_arn         = aws_acm_certificate.alb_cert.arn
  validation_record_fqdns = [for record in aws_route53_record.alb_route53_validation_record : record.fqdn]
  depends_on = [
    aws_route53_record.alb_route53_validation_record
  ]
}