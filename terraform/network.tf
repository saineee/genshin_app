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