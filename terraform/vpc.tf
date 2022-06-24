module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  # version = "2.64.0"
  version = "3.14.2"

  name = var.vpc_name
  cidr = var.vpc_cidr_block

  azs             = data.aws_availability_zones.available.names
  private_subnets = slice(var.private_subnet_cidr_blocks, 0, var.private_subnet_count)
  public_subnets  = slice(var.public_subnet_cidr_blocks, 0, var.public_subnet_count)

  enable_nat_gateway = false
  enable_vpn_gateway = var.enable_vpn_gateway

  tags = {
    Terraform   = "true"
    Environment = "dev"
  }
}