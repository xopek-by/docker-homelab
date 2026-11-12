#!/bin/sh
# Google Drive -> Seafile one-way sync loop.
# Remotes "gdrive" and "seafile" are defined in /config/rclone/rclone.conf.
# Telegram gets a message only when the state changes (first failure, recovery).
set -u

INTERVAL=${SYNC_INTERVAL:-900}
MAX_DELETE=${MAX_DELETE:-500}
CONF_DIR=/config/rclone
LOG=$CONF_DIR/sync.log
RUN_LOG=/tmp/run.log
STATE_FILE=$CONF_DIR/last_state

json_escape() {
    # Escape backslashes and quotes, turn newlines into \n
    sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' | awk 'BEGIN{ORS="\\n"} {print}'
}

notify() {
    [ -n "${TELEGRAM_BOT_TOKEN:-}" ] && [ -n "${TELEGRAM_CHAT_ID:-}" ] || return 0
    text=$(printf '%s' "$1" | json_escape)
    thread=""
    [ -n "${TELEGRAM_THREAD_ID:-}" ] && thread=",\"message_thread_id\":${TELEGRAM_THREAD_ID}"
    wget -q -O /dev/null --header "Content-Type: application/json" \
        --post-data "{\"chat_id\":\"${TELEGRAM_CHAT_ID}\"${thread},\"text\":\"${text}\"}" \
        "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
        || echo "telegram notification failed"
}

if [ ! -s "$CONF_DIR/rclone.conf" ]; then
    echo "No $CONF_DIR/rclone.conf yet - run setup.sh (see README). Waiting."
fi

while :; do
    if [ ! -s "$CONF_DIR/rclone.conf" ]; then
        sleep 60
        continue
    fi

    started=$(date +%s)
    echo "$(date '+%F %T') sync started"
    # rclone appends to --log-file, start every run with an empty one
    : > "$RUN_LOG"
    rclone sync gdrive: seafile: \
        --fast-list \
        --drive-export-formats docx,xlsx,pptx,svg \
        --drive-skip-dangling-shortcuts \
        --drive-acknowledge-abuse \
        --max-delete "$MAX_DELETE" \
        --transfers 4 --checkers 8 \
        --retries 3 --low-level-retries 10 \
        --stats 0 --log-level INFO --log-file "$RUN_LOG"
    rc=$?
    took=$(( $(date +%s) - started ))

    # Keep a persistent log, trimmed to the last 20000 lines
    cat "$RUN_LOG" >> "$LOG"
    tail -n 20000 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"

    copied=$(grep -c ': Copied' "$RUN_LOG")
    deleted=$(grep -c ': Deleted' "$RUN_LOG")
    prev=$(cat "$STATE_FILE" 2>/dev/null || echo ok)

    if [ "$rc" -eq 0 ]; then
        echo "$(date '+%F %T') sync ok in ${took}s: copied $copied, deleted $deleted"
        if [ "$prev" != "ok" ]; then
            notify "✅ Google Drive -> Seafile sync recovered (copied $copied, deleted $deleted, ${took}s)"
        fi
        echo ok > "$STATE_FILE"
    else
        echo "$(date '+%F %T') sync FAILED (rclone exit $rc) in ${took}s"
        errors=$(grep -E 'ERROR|NOTICE|Failed' "$RUN_LOG" | tail -n 5 | cut -c1-300)
        if [ "$prev" = "ok" ]; then
            notify "❌ Google Drive -> Seafile sync failed (rclone exit $rc)
$errors
Log: /opt/docker_data/gdrive-sync/sync.log on docker-cloud"
        fi
        echo failed > "$STATE_FILE"
    fi

    sleep "$INTERVAL"
done
