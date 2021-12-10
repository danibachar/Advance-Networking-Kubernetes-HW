#!/bin/bash
echo curl to -> $1
for i in $(seq 1 20): do 
curl localhost:8080
done