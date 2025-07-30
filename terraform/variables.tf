variable "aws_region" {
  description = "The AWS region to deploy resources in."
  type        = string
  default     = "us-west-2"
}

variable "project_name" {
  description = "The name of the project, used for naming resources."
  type        = string
  default     = "clinical-eval-suite"
}

variable "aws_account_id" {
  description = "The AWS Account ID."
  type        = string
  # You must provide your AWS Account ID. You can set this via a .tfvars file or environment variable.
}

variable "openai_api_key" {
  description = "The OpenAI API key."
  type        = string
  sensitive   = true
}
