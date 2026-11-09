# AdGuard Home sync

[adguardhome-sync](https://github.com/bakito/adguardhome-sync) copies the configuration of the origin
AdGuard Home to the replica every 10 minutes.

| Role | Host | Notes |
| --- | --- | --- |
| Origin | Raspberry Pi `10.0.0.5` | Make all changes (filters, user rules, rewrites, upstreams, clients) here |
| Replica | CT104 `10.0.0.104` | Overwritten on every sync; also runs DHCP, which is **not** synced |

Both instances have a dedicated AdGuard user `sync` (bcrypt hash in `AdGuardHome.yaml`).
Its password is in the Komodo stack environment as `SYNC_PASSWORD`
(source on docker-apps: `/opt/docker_data/adguardhome-sync/SYNC_PASSWORD`).

Logs: `docker logs adguardhome-sync`.
