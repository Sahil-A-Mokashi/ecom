# 🌐 Live Demo

The application has been successfully deployed to Amazon EC2 using the CI/CD pipeline.

**Live URL:**

http://13.62.58.236

> The application is automatically updated whenever code is pushed to the `prod` branch through the GitHub Actions → Amazon ECR → Ansible deployment pipeline.



# E-Commerce CI/CD Pipeline on AWS

## Project Overview

This project demonstrates a complete CI/CD pipeline for deploying a
Django e-commerce application on AWS using Docker, Amazon ECR, GitHub
Actions, Terraform, and Ansible.

## Architecture

``` text
Developer
    |
git push (dev / qa / prod)
    |
GitHub Actions
    |
+-------------------------------+
| Build Docker Image            |
| Django Health Check           |
| Push Image to Amazon ECR      |
+-------------------------------+
               |
               v
         Amazon ECR
               |
        (prod only)
               |
          Ansible via SSH
               |
               v
         Amazon EC2
      Ubuntu + Docker
               |
      Pull latest image
      Stop old container
      Run new container
               |
               v
       Live Django Website
```

------------------------------------------------------------------------

# Technology Stack

-   Python 3.11
-   Django 4.2
-   Docker
-   GitHub Actions
-   Amazon ECR
-   Amazon EC2
-   Terraform
-   Ansible
-   Ubuntu Server 22.04+
-   AWS IAM

------------------------------------------------------------------------

# Repository Structure

``` text
ecom/
│
├── .github/
│   └── workflows/
│       ├── dev.yml
│       ├── qa.yml
│       └── prod.yml
│
├── ansible/
│   ├── ansible.cfg
│   ├── inventory.ini
│   └── playbook.yml
│
├── terraform/
│   ├── main.tf
│   ├── provider.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── terraform.tfvars
│
├── Dockerfile
├── requirements.txt
├── manage.py
└── ...
```

------------------------------------------------------------------------

# Branch Strategy

## dev

-   Builds Docker image
-   Runs Django health check
-   Pushes:
    -   dev-latest
    -   dev-`<commit_sha>`{=html}

## qa

-   Builds Docker image
-   Runs health check
-   Pushes:
    -   qa-latest
    -   qa-`<commit_sha>`{=html}

## prod

-   Builds Docker image
-   Runs health check
-   Pushes:
    -   prod-latest
    -   prod-`<commit_sha>`{=html}
-   Connects to EC2 using Ansible
-   Pulls latest image
-   Recreates Docker container

------------------------------------------------------------------------

# Docker

Dockerfile: - Python 3.11 slim base image - Installs requirements -
Copies source code - Exposes port 8787 - Runs Django on 0.0.0.0:8787

Container mapping:

Host Port 80 -\> Container Port 8787

------------------------------------------------------------------------

# Amazon ECR

Repository:

network_assignment

Tags used:

-   dev-latest
-   qa-latest
-   prod-latest

Version tags:

-   dev-`<commit>`{=html}
-   qa-`<commit>`{=html}
-   prod-`<commit>`{=html}

------------------------------------------------------------------------

# Terraform

Terraform provisions:

-   Security Group
-   EC2 Instance
-   IAM Instance Profile / Role attachment (if configured)
-   Docker installation using user_data

Ports:

22 - SSH

80 - HTTP

Terraform is intended for infrastructure provisioning. Application
deployments are handled by GitHub Actions and Ansible.

------------------------------------------------------------------------

# Ansible

The playbook performs:

1.  Connect to EC2 using SSH.
2.  Install AWS CLI if needed.
3.  Authenticate to Amazon ECR.
4.  Pull the latest Docker image.
5.  Stop any existing container.
6.  Remove the old container.
7.  Run the new container.

Container:

network_assignment

------------------------------------------------------------------------

# GitHub Actions Workflows

## Development Pipeline

Trigger:

Push to dev

Steps:

1.  Checkout repository
2.  Configure AWS credentials
3.  Login to ECR
4.  Build Docker image
5.  Django health check
6.  Tag image
7.  Push image

------------------------------------------------------------------------

## QA Pipeline

Trigger:

Push to qa

Same process as Development, but pushes QA tags only.

------------------------------------------------------------------------

## Production Pipeline

Trigger:

Push to prod

Steps:

1.  Checkout code
2.  Configure AWS credentials
3.  Login to ECR
4.  Build Docker image
5.  Django health check
6.  Push production image
7.  Install Ansible
8.  Generate SSH private key from GitHub Secret
9.  Generate inventory file
10. Connect to EC2
11. Login to Amazon ECR
12. Pull latest Docker image
13. Replace running container
14. Deploy updated application

------------------------------------------------------------------------

# GitHub Secrets

-   AWS_ACCESS_KEY_ID
-   AWS_SECRET_ACCESS_KEY
-   AWS_REGION
-   EC2_HOST
-   EC2_SSH_PRIVATE_KEY
-   ECR_REPOSITORY

------------------------------------------------------------------------

# Deployment Flow

``` text
Developer
    |
git push prod
    |
GitHub Actions
    |
Docker Build
    |
Health Check
    |
Push to Amazon ECR
    |
SSH to EC2
    |
Login to ECR
    |
Pull latest image
    |
Replace container
    |
Website updated
```

------------------------------------------------------------------------

# Security

-   IAM User for GitHub Actions
-   IAM Role attached to EC2 for ECR pull
-   SSH private key stored as GitHub Secret
-   Security Group allowing:
    -   Port 22
    -   Port 80

------------------------------------------------------------------------

# Troubleshooting

## Invalid HTTP_HOST

Resolved by configuring Django `ALLOWED_HOSTS`.

## Host key verification failed

Resolved by adding the EC2 host to known_hosts and disabling Ansible
host key checking.

## InvalidKeyPair

Resolved by using the correct EC2 key pair.

## Duplicate Security Group

Infrastructure was already provisioned. Terraform should not recreate
existing resources without state management.

------------------------------------------------------------------------

# Future Improvements

-   Store Terraform state remotely in Amazon S3.
-   Add DynamoDB state locking.
-   Create a dedicated staging EC2 instance.
-   Add HTTPS using Nginx and Let's Encrypt.
-   Deploy with Docker Compose or Kubernetes.
-   Add automated rollback on deployment failure.
-   Add monitoring with CloudWatch.

------------------------------------------------------------------------

# Result

The completed solution provides an automated CI/CD pipeline:

-   Source control with GitHub
-   Automated builds using GitHub Actions
-   Docker containerization
-   Image storage in Amazon ECR
-   Infrastructure provisioning with Terraform
-   Automated deployment using Ansible
-   Hosting on Amazon EC2
-   Live Django application accessible through the EC2 public IP

This project demonstrates an end-to-end DevOps workflow following modern
CI/CD practices.
