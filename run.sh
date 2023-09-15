#!/bin/sh

docker build -t latchchallenge:v1 . && docker-compose up -d
