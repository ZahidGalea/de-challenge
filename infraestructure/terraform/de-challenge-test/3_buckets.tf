################
# Buckets
################

module "landing-bucket-metascore" {
  source      = "terraform-google-modules/cloud-storage/google//modules/simple_bucket"
  version     = "~> 1.3"
  name        = "${local.project_id}-${local.metascore-ldn}"
  project_id  = local.project_id
  location    = local.default_region
  versioning  = false
  iam_members = concat(local.metascore-owners-access, local.metascore-editor-access, local.metascore-viewer-access)
}


module "raw-bucket-metascore" {
  source      = "terraform-google-modules/cloud-storage/google//modules/simple_bucket"
  version     = "~> 1.3"
  name        = "${local.project_id}-${local.metascore-raw}"
  project_id  = local.project_id
  location    = local.default_region
  versioning  = true
  iam_members = concat(local.metascore-owners-access, local.metascore-editor-access, local.metascore-viewer-access)
}

module "analytics-bucket-metascore" {
  source      = "terraform-google-modules/cloud-storage/google//modules/simple_bucket"
  version     = "~> 1.3"
  name        = "${local.project_id}-${local.metascore-analytics}"
  project_id  = local.project_id
  location    = local.default_region
  versioning  = true
  iam_members = concat(local.metascore-owners-access, local.metascore-editor-access, local.metascore-viewer-access)
}

module "artifacts-bucket" {
  source      = "terraform-google-modules/cloud-storage/google//modules/simple_bucket"
  version     = "~> 1.3"
  name        = "${local.project_id}-${local.artifacts-bucket}"
  project_id  = local.project_id
  location    = local.default_region
  versioning  = true
  iam_members = concat(local.metascore-owners-access, local.metascore-editor-access, local.metascore-viewer-access)
}

module "temporary-bucket" {
  source      = "terraform-google-modules/cloud-storage/google//modules/simple_bucket"
  version     = "~> 1.3"
  name        = "${local.project_id}-${local.temporary-bucket}"
  project_id  = local.project_id
  location    = local.default_region
  versioning  = true
  iam_members = concat(local.metascore-owners-access, local.metascore-editor-access, local.metascore-viewer-access)
}


################
# Landing Notification
################

# GCS Landing notification to pubsub
resource "google_storage_notification" "object_landing_notification" {
  provider       = google
  bucket         = "${local.project_id}-${local.metascore-ldn}"
  payload_format = "JSON_API_V1"
  topic          = google_pubsub_topic.ldn_arrive_topic.name
  event_types    = [
    "OBJECT_FINALIZE"
  ]
  depends_on     = [
    module.landing-bucket-metascore,
    google_pubsub_topic.ldn_arrive_topic,
    google_pubsub_topic_iam_binding.ldn_arrive_binding
  ]
}

resource "google_pubsub_topic" "ldn_arrive_topic" {
  provider = google
  name     = local.ldn-pubsub-topic
  project  = local.project_id
}

data "google_storage_project_service_account" "ldn_gcs_account" {}

# Pubsub iam binding
resource "google_pubsub_topic_iam_binding" "ldn_arrive_binding" {
  topic      = google_pubsub_topic.ldn_arrive_topic.name
  role       = "roles/pubsub.publisher"
  members    = [
    "serviceAccount:${data.google_storage_project_service_account.ldn_gcs_account.email_address}"
  ]
  depends_on = [
    google_pubsub_topic.ldn_arrive_topic
  ]
}


################
# Variables
################

locals {
  metascore-ldn           = "metascore-lnd"
  ldn-pubsub-topic        = "lnd-notification"
  metascore-raw           = "metascore-raw"
  metascore-analytics     = "metascore-analytics"
  artifacts-bucket        = "artifacts"
  temporary-bucket        = "temporary-pipeline"
  metascore-owners-access = [
  for owner in local.owner_users : {
    role   = "roles/storage.objectAdmin",
    member = "user:${owner}"
  }
  ]
  metascore-editor-access = [
  for editor in local.editor_users : {
    role   = "roles/storage.objectAdmin",
    member = "user:${editor}"
  }
  ]
  metascore-viewer-access = [
  for viewer in local.viewer_users : {
    role   = "roles/storage.objectAdmin",
    member = "user:${viewer}"
  }
  ]
}