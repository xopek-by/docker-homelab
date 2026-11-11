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
