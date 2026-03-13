

output "sql_server_name" {
  description = "Name of the SQL server"
  value       = azurerm_mssql_server.main.name
}

output "sql_server_fqdn" {
  description = "Fully qualified domain name of the SQL server"
  value       = azurerm_mssql_server.main.fully_qualified_domain_name
}

output "sql_database_name" {
  description = "Name of the SQL database"
  value       = azurerm_mssql_database.main.name
}

output "sql_database_id" {
  description = "ID of the SQL database"
  value       = azurerm_mssql_database.main.id
}

output "admin_username" {
  description = "SQL Server admin username"
  value       = azurerm_mssql_server.main.administrator_login
  sensitive   = true
}

output "admin_password" {
  description = "SQL Server admin password"
  value       = var.admin_password != "" ? var.admin_password : random_password.sql_password[0].result
  sensitive   = true
}