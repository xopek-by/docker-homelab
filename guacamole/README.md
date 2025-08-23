# Guacamole

[Guacamole](https://guacamole.apache.org/) is a clientless remote desktop gateway. It supports standard protocols like VNC, RDP, and SSH.

This directory contains a Docker Compose setup for Guacamole.

## Docker Compose Setup

### Services

- **guacamole**: The Guacamole application.

### Volumes

- `${PATH_TO_CONFIG}`: Stores the Guacamole configuration files.

### Ports

- `8080:8080`: The Guacamole web interface is accessible on port 8080.

## Usage

1. Create a `.env` file with the following variables:

```
# Path to a directory where the Guacamole configuration files will be stored
PATH_TO_CONFIG=/path/to/guacamole/config
```

2. Run `docker-compose up -d` to start the container.
