# Google Drive -> Seafile sync

One-way sync of "My Drive" into the folder **Google Drive** (`DEST_DIR`) of
an existing Seafile library (normally your own "My Library"), every
15 minutes (`SYNC_INTERVAL`). Runs on `cloud` (VM 102) next to Seafile as
[rclone](https://rclone.org/) in a loop (`sync.sh`).

- Only `DEST_DIR` is mirrored: the rest of the library is never touched.
  Don't put your own files into that folder, the next run deletes anything
  that is not in Drive.
- Drive is the source of truth: files deleted in Drive are deleted in Seafile
  as well. They stay recoverable from the library history / trash in Seafile.
- A run that would delete more than `MAX_DELETE` files stops and alerts
  instead (protects against an empty or broken Drive listing).
- Google Docs/Sheets/Slides/Drawings are exported as docx/xlsx/pptx/svg.
  Forms, Sites and Maps cannot be exported and are skipped.
- "Shared with me" and the Drive trash are not synced.
- Google access is read-only (`drive.readonly` scope).
- Telegram (Homelab group, Alerts topic) gets a message on the first failed
  run and on recovery, not on every run.
- Uploads go through NPM (`seafile.mbuz.uk`), whose default body limit is
  2000 MB, so single files bigger than ~2 GB will fail.

## Files

| Path | What |
| --- | --- |
| `sync.sh` | The loop, mounted into the container |
| `setup.sh` | One-time creation of `rclone.conf` |
| `/opt/docker_data/gdrive-sync/rclone.conf` | Google token + Seafile credentials (not in git) |
| `/opt/docker_data/gdrive-sync/sync.log` | rclone log of all runs (last 20000 lines) |

## One-time setup

1. **Seafile sync user.** In Seafile: System Admin -> Users -> Add user, e.g.
   `gdrive-sync@mbuz.uk` with a long random password, no 2FA. A separate
   account keeps 2FA on your own login and limits the sync to one library.
   Then share **your** library (e.g. "My Library") with this user with
   **Read-Write** permission.
2. **Google token.** On a PC with a browser and
   [rclone](https://rclone.org/downloads/) installed:

   ```
   rclone authorize "drive" "eyJzY29wZSI6ImRyaXZlLnJlYWRvbmx5In0="
   ```

   (the base64 is `{"scope":"drive.readonly"}`). Log in to Google and copy the
   JSON line printed between the arrows.
3. **rclone.conf.** On `cloud`, from the Komodo checkout of this directory
   (or a copy of `setup.sh`):

   ```
   sudo sh setup.sh
   ```

   Paste the token, the Seafile user, password and the library name. The
   script checks that both remotes are reachable.
4. The container picks up the config within a minute: `docker logs -f gdrive-sync`.

## Operations

- Run now: `docker restart gdrive-sync`.
- Token expired / revoked: repeat steps 2-3.
- Full log: `sudo tail -f /opt/docker_data/gdrive-sync/sync.log`.
