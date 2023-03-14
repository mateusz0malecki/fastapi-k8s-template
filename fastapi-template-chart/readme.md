# How to install charts to the cluster
Staging environment:
```commandline
helm install <STAGING-RELEASE-NAME> . --values=values.staging.yaml --namespace=staging --create-namespace
```
Production environment:
```commandline
helm install <PRODUCTION-RELEASE-NAME> . --values=values.prod.yaml --namespace=prod --create-namespace
```
Remember to have declared secrets created in specific namespace.