terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_ecs_cluster" "poker" {
  name = "poker-cluster"
}

output "cluster_id" {
  value = aws_ecs_cluster.poker.id
}
