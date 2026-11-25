# Memos (diary)

Runs on `apps` (VM 101). URL: https://memos.mbuz.uk (LAN and Tailscale only).

- Image `ghcr.io/usememos/memos:stable`, Komodo auto-update like the rest of `lab/`.
- Data: `/opt/docker_data/memos` (SQLite `memos_prod.db` + attachments), backed up by PBS with the VM.
- No published port, container sits in the `proxy` network; NPM forwards to `memos:5230`.
- Auth: Memos' own login. The first account created becomes the admin;
  after that disable sign-ups in Settings -> System.
