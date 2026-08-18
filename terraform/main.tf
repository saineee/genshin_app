terraform {
  backend "s3" {
    bucket       = "genshin-tfstate-330866750121"
    key          = "genshin/terraform.tfstate"
    region       = "us-east-1"
    encrypt      = true
    use_lockfile = true
  }
  required_version = ">= 1.10"
}