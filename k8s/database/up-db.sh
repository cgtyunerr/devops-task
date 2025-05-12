#!/bin/bash

base_dir=$(dirname "$(realpath "$0")")

helm install postgres oci://registry-1.docker.io/bitnamicharts/postgresql -f "$base_dir/db-values.yaml"
