# Media (Plex + *arr)

Runs on `apps` (VM 101). Torrents are downloaded by the existing
[Transmission over OpenVPN](../../core/transmission/README.md) stack, so all
BitTorrent traffic stays inside NordVPN.

| Service | Port | Purpose |
| --- | --- | --- |
| Plex | 32400 (host network) | Media server for the Hisense TV |
| Seerr | 5055 | Request page ("I want this movie"), login with Plex |
| Prowlarr | 9696 | Indexers (RuTracker, RuTor, ...), synced to Radarr/Sonarr |
| Radarr | 7878 | Movies |
| Sonarr | 8989 | TV shows |

## Storage

Everything lives on the TrueNAS SMB share mounted at `/mnt/media` on the VM:

```
/mnt/media/transmission/completed/{radarr,sonarr}   <- Transmission downloads (seeding)
/mnt/media/library/movies                           <- Radarr library (Plex)
/mnt/media/library/tv                               <- Sonarr library (Plex)
```

Radarr and Sonarr mount the whole share as `/mnt/media`, so an import is a
hardlink: one copy on disk serves both seeding and Plex. Hardlinks were tested
on this CIFS mount. Transmission sees the share as `/data`, hence the remote
path mapping `transmission-openvpn: /data/ -> /mnt/media/transmission/` in
Radarr and Sonarr.

App configs (SQLite) are on the VM disk in `/opt/docker_data/<app>`, never on
the SMB share.

## Quality policy: Direct Play, no transcoding

The host has no GPU, so files must play on the TV as they are:

- 1080p only (WEB-DL, WEBRip, Bluray encodes). 2160p, Remux and BR-DISK are
  not allowed; a 4K picture is not worth the size on a 42" TV.
- Size limits per minute of runtime keep a 2 h movie around 3-6 GB and a
  45 min episode around 1-2 GB.
- H.264 and HEVC are both fine for the TV.
- Russian audio track is required, the original track is preferred
  (custom formats in Radarr/Sonarr).
- Text subtitles (SRT) only; image subtitles (PGS) make Plex burn them in on
  the CPU.

If Plex still transcodes (usually DTS/TrueHD audio), only the audio is
converted, which is cheap.

## Connections

- Radarr/Sonarr join the `transmission_default` network and use
  `transmission-openvpn:9091`. Going through the host port does not work:
  the VPN container would send replies into the tunnel.
- Notifications go to the Telegram group Homelab.

## What is configured (2026-11-11)

- Radarr/Sonarr: profile `1080p Direct Play` (the only one), size limits
  5/25/60 MB per minute for 1080p and 3/15/35 for 720p. Custom formats:
  Russian audio +100, Original audio +50, HEVC +10, Dolby Vision -1000,
  Hardcoded subs -1000, 3D -10000. Minimum score 50 (Russian or original),
  upgrades continue until 150 (Russian + original).
- Prowlarr: RuTor, NoNaMe Club, NewStudio (public, "RUS" appended to titles),
  synced to Radarr/Sonarr with category 8000 added. RuTracker needs an
  account: add it in Prowlarr with "Add RUS to title" enabled.
- Notifications: Telegram group Homelab, topic Media.
- Plex preferences: transcoder temp in `/transcode` (tmpfs), scheduled library
  scan every 15 min (no inotify on SMB), video preview thumbnails off.

## First run (manual steps)

1. Plex: open `http://10.0.0.101:32400/web` from the LAN, sign in, add
   libraries Movies -> `/library/movies` and TV Shows -> `/library/tv`.
   On the TV, set the Plex client quality to Original / Maximum.
2. Seerr: open `http://10.0.0.101:5055`, sign in with Plex, add Radarr
   (`http://radarr:7878`) and Sonarr (`http://sonarr:8989`), profile
   `1080p Direct Play`.
