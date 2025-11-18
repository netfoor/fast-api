variable "SUPABASE_URL" {
  type = string
  sensitive = true
  
}

variable "SUPABASE_KEY" {
  type = string
  sensitive = true
  
}

variable "POSTGRESQL_URL" {
  type = string
  sensitive = true
  
}

variable "SECRET_KEY" {
  type = string
  sensitive = true
  
}

variable "ALGORITHM" {
  type = string
}

variable "ACCESS_TOKEN_EXPIRE_MINUTES" {
  type = number
}