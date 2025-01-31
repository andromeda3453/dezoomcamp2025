variable "project" {
  description = "Project ID"
  default     = "triple-grove-449111-b5"
}

variable "location" {
  description = "Project Location"
  default     = "me-central1"

}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "demo_dataset"
}

variable "gcs_storage_class" {
  description = "bucket storage class"
  default     = "STANDARD"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "triple-grove-449111-b5-demo-bucket"
}