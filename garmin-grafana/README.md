# Garmin-Grafana

This directory contains the configuration for a set of services that fetches data from Garmin Connect, stores it in InfluxDB, and visualizes it with Grafana.

## Services

-   **garmin-fetch-data**: A service that fetches data from Garmin Connect.
-   **influxdb**: An InfluxDB database for storing Garmin Connect data.
-   **grafana**: A Grafana instance for visualizing the data.

## How to start

1.  Create a `.env` file based on the `.env.example` file.
2.  Set the `GARMINCONNECT_EMAIL` and `GARMINCONNECT_PASSWORD` variables in the `.env` file.
3.  Run `docker-compose up -d` to start the application.

## Setup

After starting the application, you can access the Grafana web interface at [http://localhost:3000](http://localhost:3000) and log in with the default credentials:

-   **User**: `admin`
-   **Password**: `admin`

You can then configure a new data source for InfluxDB and create dashboards to visualize your Garmin Connect data.