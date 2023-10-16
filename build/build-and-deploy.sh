#!/bin/bash

function fatal_if {
    if [ $1 -ne 0 ]; then
        echo "Error: $1"
        exit 1
    fi
}

# This script builds the Docker image, pushes it to ECR, and deploys it to EKS as a cronjob.

# Configuration
AWS_REGION="us-west-1"
ECR_REGISTRY="587344276961.dkr.ecr.us-west-1.amazonaws.com/covid-19-etl-registry"
EKS_CLUSTER="covid-19-etl"
IMAGE_NAME="covid-19-etl-registry"
KUBE_DEPLOYMENT_NAME="covid-19-etl-cron"

# Build Docker image
task="Building Docker image" && echo $task
docker build --platform linux/amd64 -t $IMAGE_NAME .
fatal_if $task

# Authenticate Docker with the ECR
task="Authenticating Docker with ECR" && echo $task
aws ecr get-login-password --region us-west-1 | docker login --username AWS --password-stdin 587344276961.dkr.ecr.us-west-1.amazonaws.com
fatal_if $task

# Tag the image
task="Tagging Docker image" && echo $task
docker tag covid-19-etl-registry:latest 587344276961.dkr.ecr.us-west-1.amazonaws.com/covid-19-etl-registry:latest
fatal_if $task

# Push to ECR
task="Pushing Docker image to ECR" && echo $task
docker push 587344276961.dkr.ecr.us-west-1.amazonaws.com/covid-19-etl-registry:latest
fatal_if $task

# Update the EKS cluster credentials
aws eks --region $AWS_REGION update-kubeconfig --name $EKS_CLUSTER

# Deploy to EKS
task="Deploying to EKS" && echo $task
kubectl apply -f k8s/cronjob.yaml
fatal_if $task

echo "Deployment complete."
