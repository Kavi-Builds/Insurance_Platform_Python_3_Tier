variable "location" {
  description = "Azure region"
  type        = string
  default     = "canadacentral"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
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
  default     = ""
}

variable "app_service_name" {
  description = "Name of the app service"
  type        = string
  default     = "insurance-app-dev-2026"
}

variable "sql_server_name" {
  description = "Name of SQL server"
  type        = string
  default     = "sql-insurance-dev-2026"
}
