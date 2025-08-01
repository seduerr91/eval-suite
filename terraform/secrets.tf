# --- AWS Secrets Manager ---
# Creates a secret to hold sensitive environment variables.
resource "aws_secretsmanager_secret" "app_secrets" {
  name = "${var.project_name}-env"
}

resource "aws_secretsmanager_secret_version" "app_secrets_version" {
  secret_id = aws_secretsmanager_secret.app_secrets.id

  secret_string = jsonencode({
    OPENAI_API_KEY       = var.openai_api_key
  })
}
