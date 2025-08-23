# BookStack

BookStack is a free and open-source platform for organizing and storing information, essentially functioning as a wiki or documentation system. It is designed to be simple, self-hosted, and easy to use.

[BookStack Website](https://www.bookstackapp.com/)

## Services

-   **bookstack**: The main BookStack application.
-   **bookstack_database**: A MariaDB database for BookStack.

## How to start

1.  Create a `.env` file based on the `.env.example` file.
2.  Set the environment variables in the `.env` file.
3.  Run `docker-compose up -d` to start the application.
4.  The application will be available at the URL you specified in the `APP_URL` environment variable.

## Setup

After starting the application, you can access the web interface and log in with the default credentials:

-   **Email**: `admin@admin.com`
-   **Password**: `password`

You will be prompted to change the password after your first login.