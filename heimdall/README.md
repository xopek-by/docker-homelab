# Heimdall

[Heimdall](https://heimdall.site/) is a dashboard for all your web applications.

This directory contains a Docker Compose setup for Heimdall.

## Docker Compose Setup

### Services

- **heimdall**: The Heimdall application.

### Volumes

- `/home/mbuz/docker/heimdall/config:/config`: Stores the Heimdall configuration files. You should change this to a path on your own system.

### Ports

- `80:80`: The Heimdall web interface is accessible on port 80.
- `443:443`: The Heimdall web interface is accessible on port 443.

## Usage

1. Run `docker-compose up -d` to start the container.
