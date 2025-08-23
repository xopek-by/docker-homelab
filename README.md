# Docker Projects

This directory contains Docker Compose setups for various self-hosted applications. Each project is in its own directory and includes a `docker-compose.yaml` file and any other necessary configuration files.

Most of these configurations use `.env` files for environment variables. These were designed to be used with Portainer, but can be used with `docker-compose` as well.

## Projects

- [Bookstack](bookstack/README.md)
- [DDNS Cloudflare](ddns-cloudflare/README.md)
- [Garmin Grafana](garmin-grafana/README.md)
- [Guacamole](guacamole/README.md)
- [Heimdall](heimdall/README.md)
- [Homepage](homepage/README.md)
- [Immich](immich/README.md)
- [IT-Tools](it-tools/README.md)
- [Mealie](mealie/README.md)
- [n8n](n8n/README.md)
- [Nextcloud](nextcloud/README.md)
- [Nginx Proxy Manager](nginx-proxy-manager/README.md)
- [pgAdmin](pgadmin/README.md)
- [Portainer](portainer/README.md)
- [Seafile](seafile/README.md)
- [Transmission (haugene-openvpn)](transmission/haugene-openvpn/README.md)
- [Transmission (lscr.io)](transmission/lscr.io/README.md)
- [Vaultwarden](vaultwarden/README.md)
- [Webtop](webtop/README.md)

## Usage

To use these projects, you will need to have Docker and Docker Compose installed. You will also need to create a `.env` file in each project directory with the required environment variables.

Once you have Docker and Docker Compose set up and the `.env` file created, you can start a project using the following command:

```
cd <project_directory>
docker-compose up -d
```
