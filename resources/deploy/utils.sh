###### Helper Functions!
realpath() {
  [[ $1 == /* ]] && echo "$1" || echo "$PWD/${1#./}"
}

gcloud_http_function_deploy() {
  export function_name="$1"
  export source="$2"
  export project="$3"
  echo "Deploying function ${function_name} on path: ${source}"

  gcloud functions deploy ${function_name} \
    --entry-point main \
    --runtime python37 \
    --trigger-http \
    --source=${source} \
    --clear-max-instances \
    --project ${project} \
    --region us-central1 \
    --memory 128MB
}

gcloud_pubsub_function_deploy() {
  export function_name="$1"
  export source="$2"
  export project="$3"
  export pubsub_topic="$4"
  echo "Deploying function ${function_name} on path: ${source}"

  gcloud functions deploy ${function_name} \
    --entry-point main \
    --runtime python37 \
    --trigger-topic=${pubsub_topic} \
    --source=${source} \
    --clear-max-instances \
    --region us-central1 \
    --project ${project} \
    --memory 128MB \
    $5
}

gcloud_workflows_deploy() {
  export workflow_name="$1"
  export source="$2"

  gcloud workflows deploy $workflow_name \
    --source=$source

}
