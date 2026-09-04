variable "location" {
  description = "lieu de deploiement de notre infra"
  type        = string
  default     = "swedencentral"
}

variable "cluster_name" {
  description = "cluster AKS"
  type        = string
  default     = "aks-task-api"
}

variable "node_count" {
  description = "nombre de noeuds"
  type        = number
  default     = 2
}

variable "vm_size" {
  description = "la taille de la VM"
  type        = string
  default     = "Standard_B2s"
}
