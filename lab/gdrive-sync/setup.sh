#!/bin/sh
# One-time setup of rclone.conf for the gdrive-sync stack. Run on docker-cloud:
#   sudo sh setup.sh
# Asks for the Google Drive token (from "rclone authorize" on a PC with a browser)
# and for the Seafile sync user, then writes /opt/docker_data/gdrive-sync/rclone.conf.
set -eu

CONF_DIR=${CONFIG_DIR:-/opt/docker_data/gdrive-sync}
LIBRARY=${SEAFILE_LIBRARY:-Google Drive}
SEAFILE_URL=${SEAFILE_URL:-https://seafile.mbuz.uk}

install -d -m 700 "$CONF_DIR"

rc() {
    docker run --rm -i -v "$CONF_DIR:/config/rclone" rclone/rclone:latest "$@"
}

echo "Paste what 'rclone authorize' printed between ---> and <--- (JSON or the base64 blob of newer rclone):"
read -r TOKEN
case "$TOKEN" in
    "{"*) ;;
    *)
        # rclone >= 1.7x prints base64(JSON{client_id, client_secret, token}); keep only the token
        TOKEN=$(printf '%s' "$TOKEN" | python3 -c 'import base64,json,sys
t=sys.stdin.read().strip(); d=json.loads(base64.urlsafe_b64decode(t+"="*(-len(t)%4)))
tok=d.get("token",d); print(tok if isinstance(tok,str) else json.dumps(tok,separators=(",",":")))')
        ;;
esac
echo "Seafile user (e-mail of the sync account):"
read -r SF_USER
printf 'Seafile password: '
stty -echo; read -r SF_PASS; stty echo; echo

rc config create gdrive drive scope=drive.readonly token="$TOKEN" --non-interactive >/dev/null
rc config create seafile seafile url="$SEAFILE_URL" user="$SF_USER" pass="$SF_PASS" \
    library="$LIBRARY" create_library=true --obscure --non-interactive >/dev/null
chmod 600 "$CONF_DIR/rclone.conf"

echo "Checking Google Drive..."
rc lsd gdrive: --max-depth 1 | head -n 10
echo "Checking Seafile..."
rc mkdir seafile:
rc about seafile: || true
echo "Done. Restart the stack (or wait a minute) and watch: docker logs -f gdrive-sync"
