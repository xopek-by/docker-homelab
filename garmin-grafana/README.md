# Garmin-Grafana

This directory contains the configuration for a set of services that fetches data from Garmin Connect, stores it in InfluxDB, and visualizes it with Grafana.

## Services

-   **garmin-fetch-data**: A service that fetches data from Garmin Connect.
-   **influxdb**: An InfluxDB database for storing Garmin Connect data.
-   **grafana**: A Grafana instance for visualizing the data.

## How to start

1.  Create a `.env` file based on the `.env.example` file.
2.  Set the `GARMINCONNECT_EMAIL` and `GARMINCONNECT_PASSWORD` (Base64 encoded) variables in the `.env` file.
3.  **If you have 2FA enabled:** You must authenticate manually once to generate the session tokens.
    ```bash
    docker-compose run --rm garmin-fetch-data
    ```
    Enter your 2FA code when prompted. The tokens will be saved to the `./garminconnect_tokens` folder.

    > **Server Console (Komodo/Portainer) - Robust Method:**
    > The fetcher requires a database connection to start. Use the provided [`server-token-setup.yaml`](./server-token-setup.yaml) file.
    >
    > 1. Copy `server-token-setup.yaml` to your server.
    > 2. **Important:** Ensure the target folder exists and is writable by the container user (UID 1000):
    >    ```bash
    >    sudo mkdir -p /opt/docker/garmin-grafana/tokens
    >    sudo chown -R 1000:1000 /opt/docker/garmin-grafana/tokens
    >    ```
    > 3. Run:
    >    ```bash
    >    docker-compose -f server-token-setup.yaml run --rm setup-fetcher
    >    ```
    > The script will interactively prompt you for your **Garmin Email**, **Password (Plain Text)**, and **2FA Code**.
    > The tokens will be generated in `/opt/docker/garmin-grafana/tokens` (as defined in the yaml).
    >
    > Finally, in Komodo/Portainer, set the environment variable `GARMINCONNECT_TOKENS=/opt/docker/garmin-grafana/tokens`.

4.  Run `docker-compose up -d` to start the application.

## Setup & Access

After starting the application, you can access the Grafana web interface at [http://localhost:3000](http://localhost:3000).

-   **User**: `admin`
-   **Password**: `admin`

Configure a new data source for InfluxDB (URL: `http://influxdb:8086`, Database: `GarminStats`) and import the dashboards.

## Setup Dashboard

You need to manually import the dashboard into Grafana to visualize your data.

**Method 1: Import via ID (Recommended)**
1.  Go to Grafana (`http://localhost:3000`).
2.  Navigate to **Dashboards -> New -> Import**.
3.  Enter the Dashboard ID: `23245` and click **Load**.
4.  Select your InfluxDB data source and click **Import**.

**Method 2: Import via JSON File**
1.  Download the dashboard JSON file:
    [Garmin-Grafana-Dashboard.json](https://raw.githubusercontent.com/arpanghosh8453/garmin-grafana/main/Grafana_Dashboard/Garmin-Grafana-Dashboard.json)
2.  Go to Grafana -> **Dashboards -> New -> Import**.
3.  Upload the downloaded JSON file.
4.  Select your InfluxDB data source and click **Import**.

## Historical Data Download (Bulk Import)

To download old history, use the `MANUAL_START_DATE` variable. This will fetch data in reverse chronological order from the current date (or `MANUAL_END_DATE`) back to the start date.

```bash
docker-compose run --rm -e MANUAL_START_DATE=YYYY-MM-DD garmin-fetch-data
```

**Options:**
-   `MANUAL_END_DATE=YYYY-MM-DD`: Optional end date (defaults to today).
-   `FETCH_SELECTION=...`: Limit what data is fetched (e.g., `activity,sleep`).

*Note: Garmin archives intraday data older than 6 months, so very old detailed data (HR, sleep stages) might be missing unless manually refreshed in the Garmin Connect app.*