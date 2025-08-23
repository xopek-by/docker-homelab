# Nginx Proxy Manager

Nginx Proxy Manager (NPM) is an open-source tool that provides a simple, web-based graphical user interface (GUI) for managing Nginx reverse proxies. It's designed to simplify the complexities of configuring web servers, SSL certificates, and reverse proxies, making it accessible even for users without deep expertise in Nginx or command-line operations.

[Nginx Proxy Manager Website](https://nginxproxymanager.com/)

## How to start

1.  Create a `.env` file based on the `.env.example` file.
2.  Set the `NGINX_DATA` and `NGINX_LETSENCRYPT` variables in the `.env` file.
3.  Run `docker-compose up -d` to start the application.
4.  The application will be available at [http://localhost:81](http://localhost:81).

## Setup

After starting the application, you can access the web interface and log in with the default credentials:

-   **Email**: `admin@example.com`
-   **Password**: `changeme`

You will be prompted to change the password after your first login.
