#!/bin/bash

docker build -t adclab/simplefs:v0.1 -t adclab/simplefs:latest .
docker push adclab/simplefs:v0.1
docker push adclab/simplefs:latest
