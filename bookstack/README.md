# Bookstack

[Bookstack](https://www.bookstackapp.com/) is a simple, self-hosted, easy-to-use platform for organizing and storing information.

## Docker Compose Setup

This directory contains a Docker Compose setup for Bookstack.

### Services

- **bookstack**: The Bookstack application itself.
- **bookstack_database**: A MariaDB database for Bookstack.

### Volumes

- `${PATH_TO_CONFIG}`: Stores the Bookstack configuration files.
- `${PATH_TO_DB}`: Stores the MariaDB database files.

### Ports

- `6875:80`: The Bookstack application is accessible on port 6875.

## Usage

1. Create a `.env` file with the following variables:

```
# Password for bookstack MySQL user
DB_USER_PASS=<your_strong_pass>

# Password for root MySQL user
DB_ROOT_PASS=<your_strongest_pass>

# Directory, where the bookstack itself will store the files
PATH_TO_CONFIG=/path/to/bookstack/config

# Directory, where MySQL data will be stored
PATH_TO_DB=/path/to/db/data

# Your timezone
TZ=Europe/Warsaw

# The IP:port or URL your application will be accessed on (ie. http://192.168.1.1:6875 or https://bookstack.mydomain.com
APP_URL=https://bookstack.example.com
```

2. Run `docker-compose up -d` to start the containers.
