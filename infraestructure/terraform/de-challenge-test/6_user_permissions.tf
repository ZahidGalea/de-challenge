resource "google_project_iam_member" "owners" {
  for_each = toset(local.owner_users)
  project  = local.project_id
  role     = "roles/owner"
  member   = "user:${each.value}"
}

resource "google_project_iam_member" "editors" {
  for_each = toset(local.editor_users)
  project  = local.project_id
  role     = "roles/editor"
  member   = "user:${each.value}"
}

resource "google_project_iam_member" "viewers" {
  for_each = toset(local.viewer_users)
  project  = local.project_id
  role     = "roles/viewer"
  member   = "user:${each.value}"
}