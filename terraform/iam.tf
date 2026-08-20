resource "aws_iam_role_policy" "ghauthpolicy" {
  name = "CDforGenshin"
  policy = jsonencode({
    Statement = [{
      Action   = ["ecr:GetAuthorizationToken"]
      Effect   = "Allow"
      Resource = ["*"]
      Sid      = "authtoken"
      }, {
      Action   = ["ecr:BatchCheckLayerAvailability", "ecr:InitiateLayerUpload", "ecr:UploadLayerPart", "ecr:CompleteLayerUpload", "ecr:PutImage"]
      Effect   = "Allow"
      Resource = ["arn:aws:ecr:${var.region}:${data.aws_caller_identity.current.account_id}:repository/genshin-app"]
      Sid      = "ecrUpload"
      }, {
      Action   = ["ecs:RegisterTaskDefinition", "ecs:DescribeTaskDefinition"]
      Effect   = "Allow"
      Resource = ["*"]
      Sid      = "ecsTaskRegistration"
      }, {
      Action   = ["ecs:UpdateService", "ecs:DescribeServices"]
      Effect   = "Allow"
      Resource = ["arn:aws:ecs:${var.region}:${data.aws_caller_identity.current.account_id}:service/genshin-cluster/genshin-service"]
      Sid      = "ecsServiceTasks"
      }, {
      Action = ["iam:PassRole"]
      Condition = {
        StringEquals = {
          "iam:PassedToService" = "ecs-tasks.amazonaws.com"
        }
      }
      Effect   = "Allow"
      Resource = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/ecsTaskExecutionRole"
      Sid      = "ecsExecRole"
    }]
    Version = "2012-10-17"
  })
  role = aws_iam_role.ghauth.name
}

resource "aws_iam_role" "ghauth" {
  assume_role_policy = jsonencode({
    Statement = [{
      Action = "sts:AssumeRoleWithWebIdentity"
      Condition = {
        StringEquals = {
          "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
          "token.actions.githubusercontent.com:sub" = "repo:saineee/genshin_app:ref:refs/heads/master"
        }
      }
      Effect = "Allow"
      Principal = {
        Federated = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:oidc-provider/token.actions.githubusercontent.com"
      }
      Sid = "GHAuth"
    }]
    Version = "2012-10-17"
  })
  force_detach_policies = false
  name                  = "GHAuth"
}

resource "aws_security_group" "genshin_app_sg" {
  vpc_id = "vpc-014e3c9cf478486ff"
  name   = "genshin-app-sg"
  ingress {
    from_port   = 5000
    protocol    = "tcp"
    to_port     = 5000
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "genshin_rds_sg" {
  vpc_id = "vpc-014e3c9cf478486ff"
  name   = "genshin-rds-sg"

  ingress {
    from_port       = 5432
    protocol        = "tcp"
    to_port         = 5432
    security_groups = [aws_security_group.genshin_app_sg.id]
  }
}