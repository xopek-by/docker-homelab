# OpenTelemetry Collector

Runs on every Docker host (docker-apps, docker-cloud). It:

- reads the logs of all containers (`/var/lib/docker/containers/*/*-json.log`), one receiver per container
  via `docker_observer` + `receiver_creator`, so each record carries `container.name` and `container.image.name`;
- accepts OTLP from local applications on `:4317` (gRPC) and `:4318` (HTTP);
- sends everything to two backends in parallel:
  - [OpenObserve](../openobserve/README.md) (`otlphttp/openobserve`) for search and dashboards;
  - Zabbix proxy `zabbix-proxy-lxc` with the APM collector (`otlp/zabbix`, OTLP/gRPC `10.0.0.110:4317`) for
    Monitoring > APM and Telemetry query items/triggers; it stores data in [ClickHouse](../clickhouse-otel/README.md).

File offsets are kept in `DATA_FOLDER`, so a restart does not resend old lines (`start_at: end` on first run).

## How to start

1. Create `.env` from `.env.example`; set `HOST_NAME` per host and `OPENOBSERVE_AUTH`
   (`echo -n 'email:password' | base64`).
2. `docker compose up -d`.
3. Health: `curl http://localhost:13133` inside the container network, or `docker logs otel-collector`.
