variable "resource_group_name" {
    description = "Name of the resource group"
    type = string
    default = "terraform_apps_rg"
}

variable "location" {
  description = "Location of the resource group"
  type = string
  default = "eastus"
}

variable "app_service_plan_name" {
  description = "Name of the service plan"
  type = string
  default = "asp_insurance_platform_2026"
}

variable "app_service_name" {
    description = "Name of the app service"
    type = string
    default = "insurance_platform_app_2026"
}

variable "environment" {
    description = "Name of the environment (Dev/Prod)"
    type = string
    default = "dev"
}

variable "python_version" {
    description = "Python version"
    type = string
    default = "3.9"
}

variable "sku_tier" {
  description = "SKU tier (free/basic/standard/premium)"
  type = string
  default = "Basic"
}

variable "sku_size" {
    description = "SKU size"
    type = string
    default = "B1"
}