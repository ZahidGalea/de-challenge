terraform {
  backend "gcs" {
    bucket = "terraform-backend-de-challengue"
    prefix = "backend"
  }
}