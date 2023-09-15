# Latch Challenge [Security automation]


## INTRO
This document describes the construction and deployment process for a secure API. The project has implemented  security best practices, including encryption in transit, input validation, error handling, web service hardening, internal network segmentation in Docker, and availability monitoring.

## Challenge link
https://docs.google.com/document/d/1LzKUEvYp4jXamb4GRsQLlVT79FLZNqzlqCg3fOaVX_Y/edit?pli=1

## Use case
### Endpoints

### `/name/{name}`

- **Method:** GET
- **Description:** Retrieve the data associated with a given name.

### `/names/prefix/{prefix}`

- **Method:** GET
- **Description:** Retrieve all the names that start with a given prefix.

### `/names/count/gender`

- **Method:** GET
- **Description:** Show the count of names per gender.

### `/names/top`

- **Method:** GET
- **Description:** Retrieve the top 10 used names, regardless of gender.

### `/name/validate`

- **Method:** GET
- **Description:** Check if a combined name is approved by splitting in parts.

### `/health`

- **Method:** GET
- **Description:** Check the health status of the API.


## Table of Contents

- [Building the API](#building-the-api)
- [Security Measures](#security-measures)
  * [Encryption in Transit (HTTPS)](#encryption-in-transit-https)
  * [Input Validation](#input-validation)
  * [Error Handling](#error-handling)
  * [Web Service Hardening](#web-service-hardening)
  * [Network Segmentation](#network-segmentation)
- [Monitoring](#monitoring)

## Building the API

1. Clone the repository:
   ```shell
   git clone [repo-url]

2. Goes to the directory
    ```shell
    cd [repo-dir]

3. Run the bash
     ```shell
    ./run.sh

## Request Example
` curl -v -k --ciphers TLS_AES_256_GCM_SHA384 https://127.0.0.1/health`
    



## Security Measures
### Encryption in Transit (HTTPS)
A self-signed certificate was configured to provide TLS in-transit encryption.
> **Nota:** In this case, for an internal service, an internal CA should be implemented. If the API is published, it should be signed with a public CA. 

### Input Validation
Parameterized arguments were used in the queries to prevent injection attempts.
> **Nota:** For input validation, the logic can still be improved further by validating the length and content of the inputs, for example.

### Error Handling
Some errors in the API are handled, such as the absence of results and database connection errors.

### Web Service Hardening
Best practice hardening was carried out at the nginx level.
> **Nota:**  An improvement in this area would be to include a WAF, such as modsecurity for open-source cases.

### Network Segmentation
Network segmentation was discriminated between external and internal, with services such as the database accessible only from the API service. Ports were limited to expose only the monitoring port and nginx. In more complete solutions, access to mgmt services could be included via VPN.

## Monitoring
A Prometheus service was set up to check the API's availability, hitting the health endpoint.
> **Nota:** The monitoring and observability part should include even more detail on the API logs, nginx logs, agents that report security behavior, etc.

## MISSING
There was a lack of including an authentication method for the API. One way to do this is through JWT
