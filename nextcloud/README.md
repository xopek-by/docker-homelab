# Nextcloud

Nextcloud is a suite of open-source software that allows you to create your own self-hosted platform for file storage, sharing, and collaboration. It is a popular alternative to commercial cloud services like Google Drive, Dropbox, or Microsoft 365, with the main difference being that you have full control over your data.

[Nextcloud Website](https://nextcloud.com/)

## Services

-   **nextcloud**: The main Nextcloud application.
-   **nextcloud-mariadb**: A MariaDB database for Nextcloud.

## How to start

1.  Create a `stack.env` file based on the `stack.env.example` file.
2.  Set the environment variables in the `stack.env` file.
3.  Run `docker-compose up -d` to start the application.
4.  The application will be available at [https://localhost:5443](https://localhost:5443).

## Setup

After starting the application, you can access the web interface and create a new admin user. You can then install apps and configure the application to your needs.
