resource "google_project_service" "cloudresourcemanager" {
  project = local.project_id
  service = "cloudresourcemanager.googleapis.com"

  timeouts {
    create = "30m"
    update = "40m"
  }

  disable_dependent_services = true
}

resource "google_project_service" "project" {
  for_each = toset(local.apis)
  project  = local.project_id
  service  = each.value

  timeouts {
    create = "30m"
    update = "40m"
  }

  disable_dependent_services = true
  depends_on                 = [google_project_service.cloudresourcemanager]
}

locals {
  apis = [
    "iam.googleapis.com", "iamcredentials.googleapis.com", "cloudbuild.googleapis.com", "appengine.googleapis.com",
    "cloudfunctions.googleapis.com", "compute.googleapis.com", "container.googleapis.com", "datastudio.googleapis.com",
    "storage-component.googleapis.com", "bigquery.googleapis.com", "dataflow.googleapis.com", "workflows.googleapis.com"
  ]
}
