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

import {
  to = aws_ecs_cluster.genshin_cluster
  id = "genshin-cluster"
}

resource "aws_ecs_cluster" "genshin_cluster" {
  name = "genshin-cluster"
}

import {
  to = aws_ecs_service.genshin_service
  id = "genshin-cluster/genshin-service"
}
resource "aws_ecs_service" "genshin_service" {
  name    = "genshin-service"
  cluster = aws_ecs_cluster.genshin_cluster.id
  lifecycle {
    ignore_changes = [task_definition]
  }
  desired_count    = 1
  launch_type      = "FARGATE"
  platform_version = "LATEST"

  deployment_configuration {
    strategy = "ROLLING"
  }
  network_configuration {
    assign_public_ip = true
    security_groups  = ["sg-028c4c4d1cc2cb8d6"]
    subnets = ["subnet-0677cf7ea85b8aa54",
    "subnet-0a9afdc166082a180", "subnet-0c87013b39a033a8c"]
  }
}