#!/bin/sh
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ./data/latch.key -out ./data/latch.crt -subj "/C=AR/ST=BA/L=BA/O=YourOrg/OU=BA/CN=latchchallenge.local"
docker build -t latchchallenge:v1 . && docker-compose up -d
