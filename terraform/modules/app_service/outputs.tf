

output "app_service_plan_name"{
    description = "Name of the app service plan"
    value = azurerm_service_plan.main.name
}

output "app_service_plan_id"{
    description = "Id of the app service plan"
    value = azurerm_service_plan.main.id
}

output "app_service_name" {
    description = "Name of the app service"
    value = azurerm_linux_web_app.main.name
}

output "app_service_id" {
    description = "Id of the app service"
    value = azurerm_linux_web_app.main.id
}

output "app_service_url" {
    description = "URL for the app service"
    value = "https://${azurerm_linux_web_app.main.default_hostname}"
}