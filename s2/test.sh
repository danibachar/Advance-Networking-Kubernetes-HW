#!/bin/sh

# Testing script

# Creating a cluster on local kind environment
# Building and pushing a new Docker image
# Deploying the microservice based applicaiton (all 3 services)
# Exposing the frontend service to our local computer
# Calling with curl to the frontend service

# TODO check if cluster named cluster1 is up, if it does
kind create cluster --name test1

make build 

echo "Wating for Docker image to update..."
sleep 5

make deploy

echo "Wating for the application to run..."
sleep 45
kubectl get pods
echo "Any pods in NOT in Running state? - The script might fail"

# Note that this will keep running even after the script is done running, so make sure to kill the process eventually
kubectl port-forward service/frontend 8080:8080 & 

echo "Wating for app connection..."
sleep 10


echo
echo "Prepare for output"
echo
echo "#############################################"
echo
curl localhost:8080
echo
echo "#############################################"
sleep 5


# Cleanup
echo "Cleaning up..."
kind delete clusters test1 # Delete testing cluster
ps -A | grep kubectl | awk '{print $1}' | xargs kill -9 $1 # Kill port-forward process