#!/bin/sh
# Run the watchdog every CHECK_INTERVAL seconds; a failed run is logged and retried next time.
while true; do
    python /app/watchdog.py || echo "watchdog run failed"
    sleep "${CHECK_INTERVAL:-1800}"
done
