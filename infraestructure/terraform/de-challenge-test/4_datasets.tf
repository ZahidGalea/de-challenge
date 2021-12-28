module "analytics_dataset" {
  for_each   = local.analytics-datasets
  source     = "terraform-google-modules/bigquery/google"
  dataset_id = each.value
  project_id = local.project_id
  location   = "US"
  access     = []

}


module "analytics_dataset_data_editor" {
  for_each   = local.analytics-datasets
  source     = "../custom_modules/bigquery_iam"
  dataset_id = each.value
  role       = "roles/bigquery.dataEditor"
  project_id = local.project_id
  members    = local.metascore-bq-editor-access
  depends_on = [
    module.analytics_dataset
  ]
}

module "analytics_dataset_data_owner" {
  for_each   = local.analytics-datasets
  source     = "../custom_modules/bigquery_iam"
  dataset_id = each.value
  role       = "roles/bigquery.dataOwner"
  project_id = local.project_id
  members    = local.metascore-bq-owners-access
  depends_on = [
    module.analytics_dataset
  ]
}

module "analytics_dataset_data_viewer" {
  for_each   = local.analytics-datasets
  source     = "../custom_modules/bigquery_iam"
  dataset_id = each.value
  role       = "roles/bigquery.dataViewer"
  project_id = local.project_id
  members    = local.metascore-bq-viewers-access
  depends_on = [
    module.analytics_dataset
  ]
}


locals {
  analytics-datasets          = toset(["staging", "consumption"])
  metascore-bq-owners-access  = [for owner in local.owner_users : "user:${owner}"]
  metascore-bq-viewers-access = [for viewer in local.viewer_users : "user:${viewer}"]
  metascore-bq-editor-access  = [for editor in local.editor_users : "user:${editor}"]
}