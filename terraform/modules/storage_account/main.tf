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

resource "azurerm_resource_group" "main"{
    name = var.resource_group_name
    location = var.location
    tags = {
        Environment = var.environment
        ManagedBy = "Kavitha_Terraform" 
    }
}

resource "azurerm_storage_account" "main"{
    name = var.storage_account_name
    location = var.location
    resource_group_name = var.resource_group_name
    account_tier = var.account_tier
    account_replication_type = var.account_replication_type

    depends_on = [ azurerm_resource_group.main ]

    tags = {
        Environment = var.environment
        ManagedBy = "Kavitha_Terraform"
    }
}

resource "azurerm_storage_container" "main" {
    name = "statefiles"
    storage_account_name = azurerm_storage_account.main.name
    container_access_type = "private"
    depends_on = [ azurerm_storage_account.main ]
}
