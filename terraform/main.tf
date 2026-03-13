output "environments" {
  description = "Available environments"
  value = {
    dev  = "cd environments/dev && terraform init && terraform apply"
    prod = "cd environments/prod && terraform init && terraform apply"
    storage = "cd modules/storage_account && terraform init && terraform apply"
  }
}