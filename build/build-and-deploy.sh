#!/bin/bash

# Configuration
AWS_REGION="us-west-1"
ECR_REGISTRY="587344276961.dkr.ecr.us-west-1.amazonaws.com/covid-19-etl-registry"
EKS_CLUSTER="covid-19-etl"
IMAGE_NAME="covid-19-etl-registry"
KUBE_DEPLOYMENT_NAME="covid-19-etl-cron"

# Build Docker image
docker build -t $IMAGE_NAME .

# Authenticate Docker with the ECR
aws ecr get-login-password --region us-west-1 | docker login --username AWS --password-stdin 587344276961.dkr.ecr.us-west-1.amazonaws.com

# Tag the image
docker tag covid-19-etl-registry:latest 587344276961.dkr.ecr.us-west-1.amazonaws.com/covid-19-etl-registry:latest

# Push to ECR
docker push 587344276961.dkr.ecr.us-west-1.amazonaws.com/covid-19-etl-registry:latest

# Update the EKS cluster credentials
aws eks --region $AWS_REGION update-kubeconfig --name $EKS_CLUSTER

# Deploy to EKS
# kubectl set image deployment/$KUBE_DEPLOYMENT_NAME $KUBE_DEPLOYMENT_CONTAINER_NAME=$ECR_REGISTRY/$IMAGE_NAME:latest
kubectl apply -f k8s/cronjob.yaml

echo "Deployment complete."
