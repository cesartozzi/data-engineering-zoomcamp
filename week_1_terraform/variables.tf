variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "terraform-demo-413910-bucket"
}

variable "location" {
  description = "Project Location"
  default     = "EU"
}

variable "bq_dataset_name" {
  description = "My BIgQuery Dataset Name"
  default     = "example_dataset"
}

variable "project_name" {
  description = "Prject Name"
  default     = "terraform-demo-413910"
}


variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}

variable "project_region" {
  description = "Prject Region"
  default     = "europe-west1"
}

variable "credentials" {
  description = "My Credentials"
  default     = "./keys/my-creds.json"
}