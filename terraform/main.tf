terraform {
  backend "s3" {
    bucket       = "genshin-tfstate-330866750121"
    key          = "genshin/terraform.tfstate"
    region       = "us-east-1"
    encrypt      = true
    use_lockfile = true
  }
  required_version = ">= 1.10"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}
provider "aws" {
  region              = "us-east-1"
  allowed_account_ids = ["330866750121"]
}

import {
  to = aws_ecr_repository.genshin_app
  id = "genshin-app"
}

resource "aws_ecr_repository" "genshin_app" {
  name = "genshin-app"
}