terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}
resource "azurerm_service_plan" "main" {
  name = var.app_service_plan_name
  location = var.location
  os_type = "Linux"
  resource_group_name = var.resource_group_name
  sku_name = var.sku_size

  tags = {
    Environment = var.environment
    ManagedBy = "Kavitha_Terraform"
  }
}

resource "azurerm_linux_web_app" "main" {
    name = var.app_service_name
    resource_group_name = var.resource_group_name
    location = var.location
    service_plan_id = azurerm_service_plan.main.id

    https_only = true
    site_config {
        application_stack {
          python_version = var.python_version
        }
      always_on = var.sku_tier !="Free" && var.sku_tier != "Standard"
    }

app_settings = {
    "WEBSITES_PORT" = "5000"
    "ENVIRONMENT" = var.environment
}

tags = {
  Environment = var.environment
  ManagedBy = "Kavitha_Terraform"
}
  
}