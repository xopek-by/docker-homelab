# Cloudflare DDNS

This directory contains a Docker Compose setup for a Cloudflare DDNS client.

This service will automatically update your Cloudflare DNS records with your public IP address.

## Docker Compose Setup

### Services

- **cloudflare-ddns**: The Cloudflare DDNS client.

### Environment Variables

- `CLOUDFLARE_API_TOKEN`: Your Cloudflare API token.
- `DOMAINS`: A comma-separated list of domains to update.
- `PROXIED`: Whether or not to proxy the domains through Cloudflare.

## Usage

1. Create a `.env` file with the following variables:

```
# Cloudflare API key. User -> My Profile -> API tokens
CLOUDFLARE_API_TOKEN=your_api_key

# Cloudflare zone, which will be used. Dashboard -> Web Sites
DOMAINS=your_domains
```

2. Run `docker-compose up -d` to start the container.
