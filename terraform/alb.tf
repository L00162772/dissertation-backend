data "aws_availability_zones" "available" {
  state = "available"
}

module "lb_security_group" {
  source  = "terraform-aws-modules/security-group/aws//modules/web"
  version = "4.9.0"

  name        = "lb-sg"
  description = "Security group for load balancer with HTTP ports open within VPC"
  vpc_id      = module.vpc.vpc_id

  ingress_cidr_blocks = ["0.0.0.0/0"]
}


resource "aws_lb" "alb" {
  name               = "${var.application_type}-alb"
  internal           = false
  load_balancer_type = "application"
  subnets            = module.vpc.public_subnets
  security_groups    = [module.lb_security_group.security_group_id]
}

resource "aws_lb_listener" "alb_http" {
  load_balancer_arn = aws_lb.alb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type = "redirect"

    redirect {
      host        = local.cloudfront_domain
      status_code = "HTTP_301"
    }
  }
}

# resource "aws_lb_listener" "alb_https" {
#   load_balancer_arn = aws_lb.alb.arn
#   port              = "443"
#   protocol          = "HTTPS"
#   ssl_policy        = "ELBSecurityPolicy-2016-08"
#   certificate_arn   = aws_acm_certificate.alb_cert.arn

#   default_action {
#     type = "redirect"

#     redirect {
#       host        = local.cloudfront_domain
#       status_code = "HTTP_301"
#     }
#   }

#   depends_on = [
#     aws_acm_certificate.alb_cert
#   ]
# }
