variable "resource_group_name" {
    description = "Name of the resource group"
    type = string
    
}

variable "location" {
  description = "Azure region"
  type        = string

}

variable "sql_server_name" {
  description = "Name of the SQL server (must be globally unique)"
  type        = string
}

variable "sql_database_name" {
  description = "Name of the SQL database"
  type        = string
  default     = "mydatabase"
}

variable "environment" {
  description = "Environment name (dev/prod)"
  type        = string
  default     = "dev"
}

variable "admin_username" {
  description = "SQL Server admin username"
  type        = string
  default     = "sqladmin"
}

variable "admin_password" {
  description = "SQL Server admin password (must be complex)"
  type        = string
  sensitive   = true
}

variable "sku_name" {
  description = "SKU name (Basic, S0, S1, S2, etc.)"
  type        = string
  default     = "Basic"
}

variable "max_size_gb" {
  description = "Maximum size in GB"
  type        = number
  default     = 4
}
