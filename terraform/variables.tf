variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "coordinator_image" {
  description = "Docker image for the coordinator service"
  type        = string
}

variable "lobby_image" {
  description = "Docker image for the lobby service"
  type        = string
}

variable "db_username" {
  description = "Database master username"
  type        = string
  default     = "postgres"
}

variable "db_password" {
  description = "Database master password"
  type        = string
  sensitive   = true
}

variable "api_secret" {
  description = "Shared API secret between services"
  type        = string
  sensitive   = true
}
