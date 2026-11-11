# Docker Projects

Docker Compose stacks for my homelab. Each project lives in its own directory with a `docker-compose.yaml`, a `.env.example` (where variables are needed) and usually a README.

## Layout

### `core/` - services in daily use

- Image versions are pinned to exact tags.
- Updates arrive as [Renovate](https://docs.renovatebot.com/) pull requests: patch and minor updates are auto-merged after 3 days, major updates are merged manually.
- Stacks are deployed by [Komodo](https://komo.do/) from this repository.

| Project | Description |
| --- | --- |
| [AdGuard Home sync](core/adguardhome-sync/README.md) | Keeps the Pi and CT104 AdGuard instances in sync |
| [Authelia](core/authelia/README.md) | SSO and 2FA in front of NPM proxy hosts |
| [DDNS Cloudflare](core/ddns-cloudflare/README.md) | Dynamic DNS updates for Cloudflare |
| [Homepage](core/homepage/README.md) | Dashboard |
| [Immich](core/immich/README.md) | Photo and video library |
| [IT-Tools](core/it-tools/README.md) | Handy tools for developers |
| [Komodo](core/komodo) | Deployment and management of the stacks |
| [n8n](core/n8n/README.md) | Automations, notification hub, homelab assistant |
| [Nginx Proxy Manager](core/nginx-proxy-manager/README.md) | Reverse proxy |
| [Transmission (haugene-openvpn)](core/transmission/README.md) | BitTorrent client behind OpenVPN |
| [Vaultwarden](core/vaultwarden/README.md) | Password manager |

### `lab/` - experiments

- May use `:latest` and unpinned images.
- Updated automatically every night by the Komodo Global Auto Update.

| Project | Description |
| --- | --- |
| [Bookstack](lab/bookstack/README.md) | Wiki |
| [Guacamole](lab/guacamole/README.md) | Remote desktop gateway |
| [Mealie](lab/mealie/README.md) | Recipe manager |
| [Media](lab/media/README.md) | Plex, Seerr, Prowlarr, Radarr, Sonarr |
| [Seafile](lab/seafile/README.md) | File sync and share |
| [Semaphore UI](lab/semaphore-ui) | Ansible UI |

## Configuration

Environment variables are stored in the Environment section of each Komodo stack, not in the repository. The `.env.example` file in each project documents the variables it needs.

## Manual usage

Without Komodo, a project can be started with Docker Compose. Create a `.env` file from `.env.example` and run:

```
cd core/<project>
docker compose up -d
```