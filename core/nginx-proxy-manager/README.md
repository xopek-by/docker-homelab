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

## Origin firewall (host `apps`, not part of the stack)

The router forwards WAN 80/443 straight to apps, so NPM is reachable without
Cloudflare. `host/origin-firewall.sh` (installed to `/usr/local/sbin/`, run by
`origin-firewall.service`, re-applied on every Docker restart) adds rules to
`DOCKER-USER`:

- 80/443: only LAN `10.0.0.0/24`, Tailscale `100.64.0.0/10`, Docker bridges
  on the VM and Cloudflare edge ranges (refreshed from cloudflare.com/ips-v4,
  cached in `/etc/origin-firewall/cf-ips-v4`). Drops are logged with prefix
  `origin-drop-web:`.
- 81 (NPM admin UI): LAN and Tailscale only.

Install / update:

    sudo install -m 755 host/origin-firewall.sh /usr/local/sbin/
    sudo install -m 644 host/origin-firewall.service /etc/systemd/system/
    sudo systemctl daemon-reload && sudo systemctl enable --now origin-firewall

Because only Cloudflare (and LAN) can reach NPM, the public proxy hosts take
the client IP from `CF-Connecting-IP` (`real_ip_header CF-Connecting-IP;` at
the top of their Advanced config). Without it the apps behind them saw
Cloudflare edge IPs, and any client could inject `X-Real-IP` through
Cloudflare.
