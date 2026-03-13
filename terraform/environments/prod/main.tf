terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
  
  backend "azurerm" {
    resource_group_name  = "terraform_state_rg"
    storage_account_name = "tfstateinsurance2026"
    container_name       = "statefiles"
    key                  = "prod/terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "main" {
  name     = "rg-insurance-prod-001"
  location = var.location  

  tags = {
    Environment = var.environment
    ManagedBy   = "Kavitha_Terraform"
  }
}

module "sql_database" {
  source = "../../modules/sql_database"
  
  resource_group_name = azurerm_resource_group.main.name  
  location           = azurerm_resource_group.main.location
  environment        = var.environment
  sql_server_name    = "sql-insurance-prod-2026"
  sql_database_name  = "sqldb-insurance-prod"
  admin_username     = "sqladmin"
  admin_password     = var.sql_admin_password
  sku_name           = "Basic"
  max_size_gb        = 2
}

module "app_service" {
  source = "../../modules/app_service"
  
  resource_group_name   = azurerm_resource_group.main.name  
  location              = azurerm_resource_group.main.location
  environment           = var.environment
  app_service_plan_name = "asp-insurance-prod-001"
  app_service_name      = "app-insurance-prod-2026"
  python_version        = "3.9"
  sku_tier              = "Standard"
  sku_size              = "S1"
  
  
}