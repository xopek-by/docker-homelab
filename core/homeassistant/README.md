# Home Assistant

Runs on `apps` (VM 101) as a plain Docker container (no Supervisor, so no
add-ons: anything an add-on would do runs as its own container/stack).

| What | Where |
| --- | --- |
| UI | https://home.mbuz.uk (NPM proxy host 34, LAN + Tailscale only, no Authelia) |
| Direct | http://10.0.0.101:8123 (host network) |
| Config | `/opt/docker_data/homeassistant` on apps (backed up with the VM by PBS) |

## Why host network

Discovery of local devices (mDNS/zeroconf, SSDP, Yeelight multicast,
Bambu Lab printer SSDP) does not cross a Docker bridge. So the container
uses `network_mode: host` and NPM proxies to `10.0.0.101:8123`.

## Why no Authelia

The HA mobile apps and the companion API do not survive a forward-auth
redirect. HA uses its own users (enable TOTP in the profile). Access from
outside the LAN goes through Tailscale only; `home.mbuz.uk` is not published
via Cloudflare.

Since 2026.x the `http:` settings are not in `configuration.yaml` any more:
they live in `.storage/http` and are edited in the UI (Settings -> System ->
Network). A change there is "pending" and is reverted after 5 minutes unless
confirmed in the UI. Current values: `use_x_forwarded_for: true`,
`trusted_proxies` 172.26.0.0/16 (nginx-proxy-manager_default) and
172.18.0.0/16 (proxy), `ip_ban_enabled`, `login_attempts_threshold: 10`.
If NPM's Docker network gets another subnet, HA answers 400 through the proxy.

## Devices

| Device | IP | Integration |
| --- | --- | --- |
| Bambu Lab A1 (LAN-only mode) | 10.0.0.25 (static lease) | built-in Marketplace -> `greghesp/ha-bambulab` (no HACS needed): serial + LAN access code from the printer screen |
| Yeelight color bulb (`yeelink.light.color5`) | 10.0.0.19 (static lease `yeelight-bulb` on the Pi) | core `yeelight`; "LAN Control" must be on in the Yeelight app |

## Updates

Version is pinned; Renovate opens PRs. HA versions are `YYYY.M.patch`, so
monthly releases count as "minor" and are merged automatically after the
3-day soak. Read the release notes' "Backward-incompatible changes" if
something breaks after an update.
