locals {
  project_id     = "de-challengue-test"
  project_number = 935901401525
  default_region = "us-central1"
  defaul_zone    = "us-central1-a"
  owner_users    = ["zahidale.zg@gmail.com"]
  editor_users   = [
    "Gustavo.Aguilar0@walmart.com",
    "Mariano.Gonzalez0@walmart.com"
  ]
  viewer_users   = []
}

provider "google" {
  project = local.project_id
  zone    = local.defaul_zone
  region  = local.default_region
}