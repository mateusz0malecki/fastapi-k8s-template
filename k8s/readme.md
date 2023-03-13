# Step by step how to initialize this app in GKE with connection with Cloud SQL
Connection is provided by Cloud SQL Proxy using Private IP of the SQL instance. 
It is attached to the main app container in a sidecar pattern.
1. Create VPC Network.
2. Create Cloud SQL Postgres instance. After choosing name, version and zone for your instance proceed to connection 
section and select **Private IP** option. Dropdown **Network** list will appear for you to select your newly created
VPC network. After this whole operation move to your instance create a database with name of your choice.
3. Create VPC-native GKE cluster connected with your VPC network.
4. Create service account in your GCP project. It must be given at least a Cloud SQL Client IAM role.
5. Create the credential key file using the gcloud command:
```commandline
gcloud iam service-accounts keys create ~/key.json --iam-account=<YOUR-SA-NAME>@<YOUR-GCP-PROJECT-ID>.iam.gserviceaccount.com
```
6. Create kubernetes secret from the credentials file:
```commandline
kubectl create secret generic <YOUR-SA-SECRET> --from-file=service_account.json=~/key.json
```
7. Change SQL instance connection address and name of your service account secret in k8s deployment file.
8. Apply k8s manifest files to your cluster.