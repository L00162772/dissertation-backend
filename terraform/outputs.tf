output "cloudfront_route53_alias" {
  description = "The route53 CloudFront alias."

  value = local.cloudfront_domain
}

output "cloudfront_distribution_id" {
  description = "The CloudFront distribution id."

  value = aws_cloudfront_distribution.cloudfront_distribution.id
}

output "alb_dns_name" {
  description = "The dns name of the generated application load balancer."

  value = aws_lb.alb.dns_name
}

output "alb_route53_alias" {
  description = "The route53 alias for the application load balancer."

  value = local.alb_domain
}