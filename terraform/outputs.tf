
output "alb_dns_name" {
  description = "The dns name of the generated application load balancer."

  value = aws_lb.alb.dns_name
}

output "alb_route53_alias" {
  description = "The route53 alias for the application load balancer."

  value = local.alb_domain
}