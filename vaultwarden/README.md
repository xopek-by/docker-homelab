# Vaultwarden

Vaultwarden is a free and open-source password manager that is an alternative implementation of the Bitwarden server. It is written in the Rust programming language and is designed to be lightweight and efficient, making it suitable for running on low-powered devices like a Raspberry Pi. Formerly known as Bitwarden_RS, Vaultwarden is not associated with Bitwarden, Inc.

[Vaultwarden GitHub](https://github.com/dani-garcia/vaultwarden)

## How to start

1.  Create a `.env` file based on the `.env.example` file.
2.  Set the `DOMAIN` and `PATH_TO_DATA` variables in the `.env` file.
3.  Run `docker-compose up -d` to start the application.
4.  The application will be available at the domain you specified in the `.env` file.

## Setup

After starting the application, you can access the web interface and create a new user. You can then use the official Bitwarden clients to connect to your self-hosted server.
