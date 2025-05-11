Installitaion on MAc
download google cloud sdk.
add path to google cloud sdk folder
bash gcloud init
bash gcloud components install gke-gcloud-auth-plugin for use kubectl
gcloud container clusters create airline-app --zone=europe-north1-b --num-nodes=3 --machine-type=e2-medium --disk-size=25 quota
kubectl create secret generic db-credentials --from-file=database/postgres-credentials.json. db secretı oluştur
brew install helm
helm install postgres oci://registry-1.docker.io/bitnamicharts/postgresql -f db-values.yaml
gcloud services enable cloudbuild.googleapis.com
connect repository
gsutil mb gs://devops-build-log
