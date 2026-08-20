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
      Resource = ["arn:aws:ecr:us-east-1:330866750121:repository/genshin-app"]
      Sid      = "ecrUpload"
      }, {
      Action   = ["ecs:RegisterTaskDefinition", "ecs:DescribeTaskDefinition"]
      Effect   = "Allow"
      Resource = ["*"]
      Sid      = "ecsTaskRegistration"
      }, {
      Action   = ["ecs:UpdateService", "ecs:DescribeServices"]
      Effect   = "Allow"
      Resource = ["arn:aws:ecs:us-east-1:330866750121:service/genshin-cluster/genshin-service"]
      Sid      = "ecsServiceTasks"
      }, {
      Action = ["iam:PassRole"]
      Condition = {
        StringEquals = {
          "iam:PassedToService" = "ecs-tasks.amazonaws.com"
        }
      }
      Effect   = "Allow"
      Resource = "arn:aws:iam::330866750121:role/ecsTaskExecutionRole"
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
        Federated = "arn:aws:iam::330866750121:oidc-provider/token.actions.githubusercontent.com"
      }
      Sid = "GHAuth"
    }]
    Version = "2012-10-17"
  })
  force_detach_policies = false
  name                  = "GHAuth"
}
