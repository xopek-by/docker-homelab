# Seafile

Seafile is an open-source, cross-platform file hosting and synchronization software system. It allows you to store files on a central server and access them from personal computers and mobile devices. Functionally similar to Dropbox or Google Drive, the primary difference is that Seafile is designed to be self-hosted, giving users more control over their data and infrastructure.

[Seafile Website](https://www.seafile.com/)

## Services

-   **seafile**: The main Seafile application.
-   **db**: A MariaDB database for Seafile.
-   **memcached**: A Memcached server for caching.

## How to start

1.  Create a `.env` file based on the `.env.example` file.
2.  Set the environment variables in the `.env` file.
3.  Run `docker-compose up -d` to start the application.
4.  The application will be available at [http://localhost](http://localhost).

## Setup

After starting the application, you can access the web interface and log in with the credentials you provided in the `.env` file.
