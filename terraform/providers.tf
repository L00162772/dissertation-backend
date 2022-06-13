

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.17.0"
    }
  }
  required_version = ">= 1.1.9"

  backend "remote" {
    organization = "dissertation-backend"

    workspaces {
      name = "###TERRAFORM_CLOUD_WORKSPACE###"
    }
  }
}


data "aws_caller_identity" "current" {}
provider "aws" {
  region = var.aws_region

  skip_requesting_account_id  = true # this can be tricky
  skip_get_ec2_platforms      = true
  skip_metadata_api_check     = true
  skip_region_validation      = true
  skip_credentials_validation = true

  #profile = "lyit"
  default_tags {
    tags = {
      Region = var.aws_region
      Name   = var.application_type
    }
  }
}
provider "aws" {
  region = "us-east-1"
  alias  = "east1"
  #profile = "lyit"
}
locals {
  alb_domain       = "${var.aws_region}-alb-${var.application_type}.${var.route53_domain}"
  top_level_domain = "${var.application_type}.${var.route53_domain}"
  s3_origin_id     = "${var.aws_region}-${var.application_type}-s3-origin"
}
