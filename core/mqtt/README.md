# mqtt

Mosquitto broker for Home Assistant plus MQTT bridges.

| Service | What |
|---|---|
| mosquitto | broker on :1883, users in `/opt/docker_data/mqtt/passwd` (no anonymous) |
| ps5-mqtt | PS5 `PS5-540` (10.0.0.39, id B41F4D7028ED): power state, wake/standby. Web UI http://10.0.0.101:8645 (LAN only) |

Users: `homeassistant` (HA MQTT integration), `ps5` (ps5-mqtt). Passwords are in
`/opt/docker_data/mqtt/users.txt` (600, root). Add a user:

    docker exec mosquitto mosquitto_passwd -b /tmp/p user pass   # or regenerate passwd, then
    docker restart mosquitto

PS5 setup, once: open the web UI, sign in with the PSN account (Remote Play registration),
then the PS5 shows up in HA via MQTT discovery. "Now playing" needs PSN_ACCOUNTS with an NPSSO
token in `ps5-mqtt.env` (cloud, optional, not configured).
