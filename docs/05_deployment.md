# CI/CD

## Table of contents
* [General Information](#general-information)
* [Installation](#installation)
* [Secrets](#secrets)
* [Database](#database)
* [Backend App](#backend-app)

## General Information
This deployment is made by using Kubernetes. To up the system, after the GCP installation, run:
```bash
./k8s/deploy.sh
```

## Installation
After account creation in GCP, download google cloud sdk. Add this sdk as a path in shell to use gcloud command.
Download kubectl to manage kubernetes environment. After that, run:

```bash
gcloud init
```
to connect gcloud and your account. After that, run:
```bash
gcloud components install gke-gcloud-auth-plugin
```
for use kubernetes in gcloud. Run:
```bash
gcloud container clusters create {cluster_name} --zone={zone} --num-nodes={vm_count} --machine-type={machine_type} --disk-size={disk_size}
```
according to your needs. With this step, we have a kubernetes cluster on GCP. Run:
```bash
brew install helm
```
on mac because in this project, we use helm for database.

## Secrets
In this project, we have 3 secrets:
- app-env-secret: The secret that is used in backend app. ".env.test" is an example of this secret.
- db-secret: Hold the password for db. k8s/secrets/db-secret/env.db.test is an example of this secret.
- image-registry-secret: Hold the image registry parameters. This secret is essential for GCP pull the our docker images.
k8s/image-registry-secret/.env.registry.test is an example for this secret.
In every secret directory, there have a creator scripts. In every script directory, there have a secret holder .env file
for creation of secret. There has a create-all-secrets scripts in secret folder to create all secrets.
## Database
Run:
```bash
helm install {db_name} oci://registry-1.docker.io/bitnamicharts/postgresql -f db-values.yaml
```

or

```bash
./k8s/database/up-db.sh
```

This command creates database architecture by using values in db-values.yaml. If you want to change configuration, you
can check https://artifacthub.io/packages/helm/bitnami/postgresql.
## Backend App
Backend app consists of 3 components:
- job: Main purpose of job is check database connection and send migration to database. deployment scripts is used by
the job. There is need to change {_TAG} with real tag but cd and up-app.sh scripts handle it.
- deployment: The deployment provides initialization of 2 backend app pods. This pods has liveness and readiness probes.
If unlive condition is happened, pod restart container. If unready condition is happened, service stop to direct traffic
to this pod, until it will be ready again. There is need to change {_TAG} with real tag but cd and up-app.sh scripts
handle it.
- loadBalancer: Load balancer is service of the pods that is created by the deployment. It provides load balancing to
the pods and provides external ip for reach app.
