variable "SUPABASE_URL" {
  description = "Supabase project URL"
  type        = string
}

variable "SUPABASE_KEY" {
  description = "Supabase anon key"
  type        = string
  sensitive   = true
}

variable "POSTGRESQL_URL" {
  description = "PostgreSQL connection URL"
  type        = string
  sensitive   = true
}

variable "SECRET_KEY" {
  description = "JWT secret key"
  type        = string
  sensitive   = true
}

variable "ALGORITHM" {
  description = "JWT algorithm"
  type        = string
}

variable "ACCESS_TOKEN_EXPIRE_MINUTES" {
  description = "Access token expiration time in minutes"
  type        = number
}