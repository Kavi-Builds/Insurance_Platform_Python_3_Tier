variable "location" {
  description = "Azure region"
  type        = string
  default     = "canadacentral"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "prod"
}

variable "sql_admin_username" {
  description = "SQL Server admin username"
  type        = string
  default     = "sqladmin"
}

variable "sql_admin_password" {
  description = "SQL Server admin password"
  type        = string
  sensitive   = true
}

variable "app_service_name" {
  description = "Name of the app service"
  type        = string
  default     = "insurance-app-prod-2026"
}

variable "sql_server_name" {
  description = "Name of SQL server"
  type        = string
  default     = "sql-insurance-prod-2026"
}