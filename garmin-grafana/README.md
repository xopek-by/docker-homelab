# Garmin Grafana

This directory contains a Docker Compose setup for a Garmin Grafana dashboard.

This setup will fetch your Garmin Connect data and store it in an InfluxDB database. You can then use Grafana to visualize the data.

## Docker Compose Setup

### Services

- **garmin-fetch-data**: Fetches your Garmin Connect data and stores it in InfluxDB.
- **influxdb**: An InfluxDB database for storing your Garmin Connect data.
- **grafana**: A Grafana instance for visualizing your Garmin Connect data.

### Volumes

- `${GARMINCONNECT_TOKENS}`: Stores the Garmin Connect tokens.
- `influxdb_data`: Stores the InfluxDB database files.
- `grafana_data`: Stores the Grafana configuration files.

### Ports

- `8086:8086`: The InfluxDB API is accessible on port 8086.
- `3000:3000`: The Grafana web interface is accessible on port 3000.

## Usage

1. Create a `.env` file with the following variables:

```
# Your Garmin Connect email address
GARMINCONNECT_EMAIL=<your_email>

# Your Garmin Connect password, base64 encoded
GARMINCONNECT_PASSWORD=<your_base64_encoded_password>

# Path to a directory where the Garmin Connect tokens will be stored
GARMINCONNECT_TOKENS=/path/to/garminconnect/tokens
```

2. Run `docker-compose up -d` to start the containers.
