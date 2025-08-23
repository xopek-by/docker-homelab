# Portainer

Portainer is a lightweight, open-source tool that provides a graphical user interface (GUI) to simplify the management of containerized environments. It is designed to make working with containers more accessible, especially for those who may not be comfortable with the command-line interface (CLI).

[Portainer Website](https://www.portainer.io/)

## How to start

1.  Create a `.env` file based on the `.env.example` file.
2.  Set the `PORTAINER_DATA` variable in the `.env` file.
3.  Run `docker-compose up -d` to start the application.
4.  The application will be available at [https://localhost:9443](https://localhost:9443).

## Setup

After starting the application, you can access the web interface and create a new admin user. You can then connect to your Docker environment and start managing your containers.
