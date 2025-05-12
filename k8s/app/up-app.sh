#!/bin/bash


VERSION=$1

base_dir=$(dirname "$(realpath "$0")")

if [ -z "$VERSION" ]; then
  echo "Error: VERSION parameter is required."
  exit 1
fi

if sed "s/\${TAG}/$VERSION/g" $base_dir/deployment.yaml | kubectl apply -f -; then
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
