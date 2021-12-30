locals {
  project_id     = "de-challenge-336404"
  project_number = 710981158804
  default_region = "us-central1"
  defaul_zone    = "us-central1-a"
  owner_users    = ["zahidale.zg@gmail.com"]
  editor_users   = []
  viewer_users   = [
    "Gustavo.Aguilar0@walmart.com",
    "Mariano.Gonzalez0@walmart.com"
  ]
}

provider "google" {
  project = local.project_id
  zone    = local.defaul_zone
  region  = local.default_region
}