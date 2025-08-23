# Guacamole

Apache Guacamole is a free and open-source, clientless remote desktop gateway that allows you to access remote computers and servers through a web browser. It supports standard protocols like VNC, RDP, and SSH.

[Apache Guacamole Website](https://guacamole.apache.org/)

## How to start

1.  Create a `.env` file based on the `.env.example` file.
2.  Set the `PATH_TO_CONFIG` variable in the `.env` file.
3.  Run `docker-compose up -d` to start the application.
4.  The application will be available at [http://localhost:8080](http://localhost:8080).

## Setup

After starting the application, you can access the web interface and configure your connections.