# Books (Calibre-Web Automated + LazyLibrarian)

Runs on `apps` (VM 101). Reading device: Kindle (Send-to-Kindle by e-mail).

| Service | URL | Purpose |
| --- | --- | --- |
| Calibre-Web Automated | https://books.mbuz.uk | Library, web reader, Send-to-Kindle |
| LazyLibrarian | https://lazylibrarian.mbuz.uk | Wanted books, searches Prowlarr indexers, downloads via Transmission |

Both publish no ports and sit behind NPM + Authelia forward-auth (LAN and
Tailscale only). CWA trusts the `Remote-User` header from Authelia
("Reverse Proxy Login" in its admin settings).

## Storage

```
/srv/books/library   <- Calibre library (metadata.db + books), dedicated 20G disk scsi1 of VM 101
/srv/books/ingest    <- drop zone: CWA imports, converts to EPUB and DELETES files here
/opt/docker_data/{calibre-web,lazylibrarian}   <- app configs
/mnt/media/transmission/completed/books        <- LazyLibrarian torrents (seeding)
```

The library is not on the TrueNAS share on purpose: CWA writes `metadata.db`
all the time and SQLite over CIFS can get corrupted. The desktop Calibre app
is no longer used for this library. The old copy stays read-only in
`/mnt/media/calibre` (state of 2026-01-08). Backups: PBS backs up the whole VM,
including the books disk.

## Flow

1. Add an author or book in LazyLibrarian (or drop a file into `/srv/books/ingest`).
2. LazyLibrarian searches Prowlarr indexers and sends the torrent to
   `transmission-openvpn:9091` with download dir `/data/completed/books`
   (`/mnt/media/transmission/completed/books` on the host).
3. When the download is done, LazyLibrarian copies the book into `/ingest`
   (the torrent keeps seeding).
4. CWA imports it, converts it to EPUB, fetches metadata and a cover.
5. Send it to the Kindle from the book page.
