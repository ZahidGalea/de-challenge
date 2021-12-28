variable "members" {
  type        = list(string)
  description = "provide iam members"
}
variable "role" {
  type        = string
  description = "role to be granted"
}
variable "project_id" {
  type        = string
  description = "Dataset id on which roles need to be granted"
}
variable "dataset_id" {
  type        = string
  description = "project_id"
}