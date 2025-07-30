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

# --- ECR Repository ---
# Creates a repository in the Elastic Container Registry (ECR) to store the Docker images.
resource "aws_ecr_repository" "app_repo" {
  name = var.project_name

  tags = {
    Project = var.project_name
  }
}
