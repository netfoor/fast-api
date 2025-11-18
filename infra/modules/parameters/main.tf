resource "aws_ssm_parameter" "SUPABASE_URL" {
  name        = "/fastapi/dev/SUPABASE_URL"
  type       = "SecureString"
  value = var.SUPABASE_URL
}

resource "aws_ssm_parameter" "SUPABASE_KEY" {
  name        = "/fastapi/dev/SUPABASE_KEY"
  type       = "SecureString"
  value = var.SUPABASE_KEY
  
}

resource "aws_ssm_parameter" "POSTGRESQL_URL" {
  name        = "/fastapi/dev/POSTGRESQL_URL"
  type       = "SecureString"
  value = var.POSTGRESQL_URL
  
}

resource "aws_ssm_parameter" "SECRET_KEY" {
  name        = "/fastapi/dev/SECRET_KEY"
  type       = "SecureString"
  value = var.SECRET_KEY
  
}

resource "aws_ssm_parameter" "ALGORITHM" {
  name        = "/fastapi/dev/ALGORITHM"
  type       = "String"
  value = var.ALGORITHM
  
}

resource "aws_ssm_parameter" "ACCESS_TOKEN_EXPIRE_MINUTES" {
  name        = "/fastapi/dev/ACCESS_TOKEN_EXPIRE_MINUTES"
  type       = "String"
  value = var.ACCESS_TOKEN_EXPIRE_MINUTES
  
}
