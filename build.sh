#!/bin/bash

docker build -t adclab/simplefs:v0.2 -t adclab/simplefs:latest .
docker push adclab/simplefs:v0.2
docker push adclab/simplefs:latest
