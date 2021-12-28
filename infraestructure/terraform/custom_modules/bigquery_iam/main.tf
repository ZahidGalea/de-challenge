resource "google_bigquery_dataset_iam_member" "dataset_iam" {
  for_each   = toset(var.members)
  dataset_id = var.dataset_id
  role       = var.role
  member     = each.key
  project    = var.project_id
}