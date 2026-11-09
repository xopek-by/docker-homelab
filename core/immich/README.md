# Immich

Immich is a free and open-source, self-hosted photo and video management application. It is designed to be a private alternative to cloud-based services like Google Photos, allowing you to store and manage your media on your own hardware. This gives you complete control over your data and privacy.

[Immich Website](https://immich.app/)

## Services

-   **immich-server**: The main application server.
-   **immich-machine-learning**: Handles machine learning tasks like image tagging and object recognition.
-   **redis**: A Redis server for caching.
-   **database**: A PostgreSQL database for storing application data.

## How to start

1.  Create a `.env` file based on the `.env.example` file.
2.  Set the `UPLOAD_LOCATION` and `DB_DATA_LOCATION` variables in the `.env` file.
3.  Run `docker-compose up -d` to start the application.
4.  The application will be available at [http://localhost:2283](http://localhost:2283).

## Setup

After starting the application, you can access the web interface and create a new user. You can also download the mobile apps for Android and iOS to automatically back up your photos and videos.
