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
data "aws_caller_identity" "current" {}

output "account_id" {
  value = data.aws_caller_identity.current.account_id
}

variable "db_password" {
  sensitive = true
}
variable "region" {
  type    = string
  default = "us-east-1"
}
provider "aws" {
  region              = var.region
  allowed_account_ids = ["330866750121"]
}

resource "aws_ecr_repository" "genshin_app" {
  name = "genshin-app"
}

resource "aws_ecs_cluster" "genshin_cluster" {
  name = "genshin-cluster"
}

resource "aws_ecs_service" "genshin_service" {
  name    = "genshin-service"
  cluster = aws_ecs_cluster.genshin_cluster.id
  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }
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
    security_groups  = [aws_security_group.genshin_app_sg.id]
    subnets = ["subnet-0677cf7ea85b8aa54",
    "subnet-0a9afdc166082a180", "subnet-0c87013b39a033a8c"]
  }
}

resource "aws_cloudwatch_log_group" "genshin_logs" {
  name              = "/ecs/genshin-task"
  retention_in_days = 14
}

resource "aws_db_instance" "genshin_db" {
  allocated_storage                     = 20
  auto_minor_version_upgrade            = true
  availability_zone                     = "us-east-1c"
  backup_retention_period               = 1
  backup_target                         = "region"
  backup_window                         = "09:01-09:31"
  ca_cert_identifier                    = "rds-ca-rsa2048-g1"
  copy_tags_to_snapshot                 = false
  customer_owned_ip_enabled             = false
  database_insights_mode                = "standard"
  db_name                               = "genshindb"
  db_subnet_group_name                  = "default"
  dedicated_log_volume                  = false
  delete_automated_backups              = true
  deletion_protection                   = true
  password_wo                           = var.db_password
  password_wo_version                   = 1
  enabled_cloudwatch_logs_exports       = []
  engine                                = "postgres"
  engine_lifecycle_support              = "open-source-rds-extended-support"
  engine_version                        = "15.17"
  iam_database_authentication_enabled   = false
  identifier                            = "genshin-db"
  instance_class                        = "db.t3.micro"
  iops                                  = 0
  license_model                         = "postgresql-license"
  maintenance_window                    = "tue:04:29-tue:04:59"
  max_allocated_storage                 = 0
  monitoring_interval                   = 0
  multi_az                              = false
  network_type                          = "IPV4"
  option_group_name                     = "default:postgres-15"
  parameter_group_name                  = "default.postgres15"
  performance_insights_enabled          = false
  performance_insights_retention_period = 0
  port                                  = 5432
  publicly_accessible                   = false
  region                                = var.region
  skip_final_snapshot                   = true
  storage_encrypted                     = true
  storage_throughput                    = 0
  storage_type                          = "gp2"
  tags                                  = {}
  username                              = "paul"
  vpc_security_group_ids                = [aws_security_group.genshin_rds_sg.id]
}