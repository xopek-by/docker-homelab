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
4. CWA imports it (subfolders included), converts it to EPUB and runs the
   Kindle EPUB fixer.
5. CWA auto-sends every new book to the Kindle (`auto_send_enabled` for user
   `mbuz`, 5 min delay). Needs SMTP in Admin -> Email server and the Kindle
   address in the user profile; the sender must be on Amazon's approved list.

Prowlarr pushes its indexers to LazyLibrarian (application "LazyLibrarian",
full sync, book categories only), so a new indexer in Prowlarr shows up there
without manual steps.

## Accounts

- CWA user `mbuz` (admin) matches the Authelia user; login comes from the
  `Remote-User` header. Local password for API/OPDS/Homepage:
  `/opt/docker_data/calibre-web/ADMIN_PASSWORD` (also `HOMEPAGE_VAR_CALIBREWEB_PASS`
  in the homepage stack).
- LazyLibrarian has no own login (Authelia only); API key in its `config.ini`.
