# Home Assistant

Runs on `apps` (VM 101) as a plain Docker container (no Supervisor, so no
add-ons: anything an add-on would do runs as its own container/stack).

| What | Where |
| --- | --- |
| UI | https://ha.mbuz.uk (NPM proxy host, LAN + Tailscale only, no Authelia) |
| Direct | http://10.0.0.101:8123 (host network) |
| Config | `/opt/docker_data/homeassistant` on apps (backed up with the VM by PBS) |

## Why host network

Discovery of local devices (mDNS/zeroconf, SSDP, Yeelight multicast,
Bambu Lab printer SSDP) does not cross a Docker bridge. So the container
uses `network_mode: host` and NPM proxies to `10.0.0.101:8123`.

## Why no Authelia

The HA mobile apps and the companion API do not survive a forward-auth
redirect. HA uses its own users (enable TOTP in the profile). Access from
outside the LAN goes through Tailscale only; `ha.mbuz.uk` is not published
via Cloudflare.

`configuration.yaml` trusts the reverse proxy (`http.trusted_proxies`) so
that HA sees real client IPs and its `ip_ban` works.

## Devices

| Device | IP | Integration |
| --- | --- | --- |
| Bambu Lab A1 (LAN-only mode) | 10.0.0.25 (static lease) | HACS `greghesp/ha-bambulab`: serial + LAN access code from the printer screen |
| Yeelight color bulb (`yeelink.light.color5`) | 10.0.0.19 (static lease) | core `yeelight`; "LAN Control" must be on in the Yeelight app |

## Updates

Version is pinned; Renovate opens PRs. HA versions are `YYYY.M.patch`, so
monthly releases count as "minor" and are merged automatically after the
3-day soak. Read the release notes' "Backward-incompatible changes" if
something breaks after an update.
