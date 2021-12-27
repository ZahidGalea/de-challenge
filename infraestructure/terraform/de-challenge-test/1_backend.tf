terraform {
  backend "gcs" {
    bucket = "terraform-backend-de-challengue-test"
    prefix = "backend"
  }
}