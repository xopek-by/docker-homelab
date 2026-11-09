# n8n

Automation platform. Runs on docker-apps as a Komodo stack.

- UI: `https://automate.mbuz.uk` — NPM host protected by Authelia; `/webhook/*` and `/webhook-test/*` bypass
  Authelia so external services (Telegram, Komodo, ...) can call workflows.
- LAN: `http://10.0.0.101:5678` (webhooks from other hosts).
- Data: `/opt/docker_data/n8n/app` (SQLite DB + `config` with the credentials encryption key, must stay `chmod 600`).
  Losing `config` makes all saved credentials unreadable — keep it in backups together with the DB.
- No secrets in this stack's environment.
