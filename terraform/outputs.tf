output "resource_group_name" {
  description = "Nom du Resource Group créé"
  value       = azurerm_resource_group.this.name
}

output "aks_cluster_name" {
  description = "Nom du cluster AKS"
  value       = azurerm_kubernetes_cluster.this.name
}

output "kube_config_command" {
  description = "Commande pour récupérer les identifiants du cluster"
  value       = "az aks get-credentials --resource-group ${azurerm_resource_group.this.name} --name ${azurerm_kubernetes_cluster.this.name}"
}
