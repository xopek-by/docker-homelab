# Transmission with OpenVPN (haugene/transmission-openvpn)

This directory contains the configuration for the `haugene/transmission-openvpn` Docker image. This image bundles the Transmission BitTorrent client with an OpenVPN client, which ensures that all of Transmission's traffic is routed through a VPN tunnel, enhancing privacy and security.

[GitHub Repository](https://github.com/haugene/docker-transmission-openvpn)

## How to start

1.  Create a `.env` file based on the `.env.example` file.
2.  Set the environment variables in the `.env` file, including your VPN provider and credentials.
3.  Run `docker-compose up -d` to start the application.
4.  The Transmission web interface will be available at [http://localhost:9091](http://localhost:9091).

## Setup

After starting the application, you can access the Transmission web interface to manage your torrents. The OpenVPN client will automatically connect to your VPN provider.
