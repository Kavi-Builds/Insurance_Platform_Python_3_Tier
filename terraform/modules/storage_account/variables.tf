variable "resource_group_name" {
    description = "Name of the resource group"
    type = string
    default = "terraform_state_rg"
}

variable "location" {
    description = "Name of the location"
    type = string
    default = "westus"
}

variable "environment" {
    description = "Environment Name (dev/prod)"
    type = string
    default = "dev"
}

variable "storage_account_name" {
    description = "Name of the storage account"
    type = string
    default = "tfstateinsurance2026"
}

variable "account_tier" {
  description = "Storage account tier"
  type = string
  default = "Standard"
}

variable "account_replication_type" {
    description = "Storage account replication type"
    type = string
    default = "LRS"
}

