#!/bin/bash


VERSION=$1

base_dir=$(dirname "$(realpath "$0")")

if [ -z "$VERSION" ]; then
  echo "Error: VERSION parameter is required."
  exit 1
fi

kubectl delete job migration-job --ignore-not-found

echo "Applying migration job..."

if sed "s/\${_TAG}/$VERSION/g" "$base_dir/job.yaml" | kubectl apply -f -; then
  echo "Migration job applied. Waiting for it to complete..."
else
  echo "Error: Migration job could not be created"
  exit 1
fi

JOB_NAME="migration-job"
TIMEOUT=300

if kubectl wait --for=condition=complete --timeout=${TIMEOUT}s job/$JOB_NAME; then
  echo "Migration job completed successfully."
else
  echo "Error: Migration job failed or timed out"
  kubectl logs job/$JOB_NAME
  exit 1
fi


if sed "s/\${_TAG}/$VERSION/g" $base_dir/deployment.yaml | kubectl apply -f -; then
  echo "Deployment applied with VERSION: $VERSION"
else
  echo "Error: Deployment failed"
  exit 1
fi

if kubectl apply -f $base_dir/loadBalancer.yaml ; then
  echo "Load Balancer service is created."
else
  echo "Error: Service creation failed"
  exit 1
fi
