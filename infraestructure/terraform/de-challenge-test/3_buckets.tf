module "landing-bucket-metascore" {
  source      = "terraform-google-modules/cloud-storage/google//modules/simple_bucket"
  version     = "~> 1.3"
  name        = "${local.project_id}-${local.metascore-ldn}"
  project_id  = local.project_id
  location    = local.default_region
  versioning  = false
  iam_members = concat(local.metascore-owners-access, local.metascore-editor-access, local.metascore-viewer-access)
}

locals {
  metascore-ldn : metascore-lnd
  metascore-raw : metascore-raw
  metascore-owners-access : [
  for owner in local.owner_users : {
    role   = "roles/storage.objectAdmin",
    member = "user:${owner}"
  }
  ]
  metascore-editor-access : [
  for editor in local.editor_users : {
    role   = "roles/storage.objectAdmin",
    member = "user:${editor}"
  }
  ]
  metascore-viewer-access : [
  for viewer in local.viewer_users : {
    role   = "roles/storage.objectViewer",
    member = "user:${viewer}"
  }
  ]
}