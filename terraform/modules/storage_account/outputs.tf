output "resource_group_name" {
    description = "Name of the resource group"
    value = azurerm_resource_group.main.name  
}

output "storage_account_name" {
    description = "Name of the storage account"
    value = azurerm_storage_account.main.name
}

output "storage_container_name" {
    description = "Name of the container"
    value = azurerm_storage_container.main.name
}

output "storage_account_id" {
    description = "Storage account ID"
    value = azurerm_storage_account.main.id
}

output "primary_blob_endpoint" {
    description = "Primary blob URL"
    value = azurerm_storage_account.main.primary_blob_endpoint
}

output "primary_access_key" {
    description = "Primary access key for the storage account"
    value = azurerm_storage_account.main.primary_access_key
    sensitive = true 
}