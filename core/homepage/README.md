# Homepage

[Homepage](https://gethomepage.dev/) dashboard, deployed as a Komodo stack. The LAN start page is `http://<docker-apps>:3001`.

## Layout

- `docker-compose.yaml` - homepage plus a read-only `socket-proxy` sidecar (`lscr.io/linuxserver/socket-proxy`).
  Homepage has no direct `docker.sock` mount; it talks to `socket-proxy:2375`, which exposes only
  `CONTAINERS`, `INFO`, `PING`, `VERSION` (no POST, no EVENTS).
- `config/` - homepage config tracked in git, mounted at `/app/config`. Secrets are never stored here;
  they are `{{HOMEPAGE_VAR_*}}` templates resolved from environment variables.
- `.env` - not in git, holds the `HOMEPAGE_VAR_*` values (see `.env.example`).
- Docker integration: only `apps` (through the local sidecar). docker-cloud is not connected on purpose:
  a Docker API reachable over the LAN, even read-only, leaks container env vars; services there use `siteMonitor`.

## Deploy

1. Create `.env` from `.env.example` (in Komodo: stack environment).
2. Deploy the stack; edit files in `config/` via git and redeploy/restart to apply.
