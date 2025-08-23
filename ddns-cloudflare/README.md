# Cloudflare DDNS

This directory contains the configuration for the `favonia/cloudflare-ddns` Docker image. This image provides a DDNS client for Cloudflare, which automatically updates your DNS records when your IP address changes.

[GitHub Repository](https://github.com/favonia/cloudflare-ddns)

## How to start

1.  Create a `.env` file based on the `.env.example` file.
2.  Set the `CLOUDFLARE_API_TOKEN` and `DOMAINS` variables in the `.env` file.
3.  Run `docker-compose up -d` to start the application.

## Setup

After starting the application, the DDNS client will automatically update your Cloudflare DNS records.