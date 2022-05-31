data "aws_route53_zone" "route53" {
  name         = var.route53_domain
  private_zone = false
}

resource "aws_route53_record" "cloudfront_route53_validation_record" {
  for_each = {
    for dvo in aws_acm_certificate.cloudfront_cert.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = data.aws_route53_zone.route53.zone_id
  depends_on = [
    aws_acm_certificate.cloudfront_cert
  ]
}

resource "aws_route53_record" "alb_route53_validation_record" {
  for_each = {
    for dvo in aws_acm_certificate.alb_cert.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = data.aws_route53_zone.route53.zone_id
  depends_on = [
    aws_acm_certificate.alb_cert
  ]
}

resource "aws_route53_record" "cloudfront" {
  zone_id = data.aws_route53_zone.route53.zone_id
  name    = "${var.aws_region}-cloudfront-${var.application_type}"
  type    = "CNAME"
  ttl     = "5"

  records = [aws_cloudfront_distribution.cloudfront_distribution.domain_name]
}

resource "aws_route53_record" "alb" {
  zone_id = data.aws_route53_zone.route53.zone_id
  name    = "${var.aws_region}-alb-${var.application_type}"
  type    = "A"

  alias {
    name                   = aws_lb.alb.dns_name
    zone_id                = aws_lb.alb.zone_id
    evaluate_target_health = true
  }

  depends_on = [
    aws_lb.alb
  ]
}

