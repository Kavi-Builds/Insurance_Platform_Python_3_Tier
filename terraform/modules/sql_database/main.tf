terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "random_password" "sql_password" {
  count  = var.admin_password == "" ? 1 : 0
  length = 16
  special = true
  override_special = "!#$%&"
}


resource "azurerm_mssql_server" "main" {
  name                         = var.sql_server_name
  resource_group_name          = var.resource_group_name
  location                     = var.location
  version                      = "12.0"
  administrator_login          = var.admin_username
  administrator_login_password = var.admin_password != "" ? var.admin_password : random_password.sql_password[0].result

  tags = {
    Environment = var.environment
    ManagedBy   = "Kavitha_Terraform"
  }
}

resource "azurerm_mssql_database" "main" {
  name         = var.sql_database_name
  server_id    = azurerm_mssql_server.main.id
  collation      = "SQL_Latin1_General_CP1_CI_AS"
  license_type   = "LicenseIncluded"
  max_size_gb  = var.max_size_gb
  sku_name     = var.sku_name

  tags = {
    Environment = var.environment
    ManagedBy   = "Kavitha_Terraform"
  }
}

resource "azurerm_mssql_firewall_rule" "azure_services" {
  name             = "AllowAzureServices"
  server_id        = azurerm_mssql_server.main.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}