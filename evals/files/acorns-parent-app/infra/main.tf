provider "aws" {
  region = "eu-west-1"
}

resource "aws_db_instance" "main" {
  identifier        = "acorns-db"
  engine            = "postgres"
  instance_class    = "db.t3.micro"
  allocated_storage = 20
  backup_retention_period = 35
}

resource "aws_s3_bucket" "class_photos" {
  bucket = "acorns-class-photos"
}
