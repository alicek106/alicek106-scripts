provider "aws" {
  region = "ap-northeast-2"
}

terraform {
  backend "s3" {
    bucket = "alicek106-terraform-state"
    key    = "kubernetes/terraform-test.tfstate"
    region = "ap-northeast-2"
  }
}
