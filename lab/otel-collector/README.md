# OpenTelemetry Collector

Runs on every Docker host (docker-apps, docker-cloud). It:

- reads the logs of all containers (`/var/lib/docker/containers/*/*-json.log`), one receiver per container
  via `docker_observer` + `receiver_creator`, so each record carries `container.name` and `container.image.name`
  (the telemetry containers themselves are skipped to avoid feedback loops);
- accepts OTLP from local applications on `:4317` (gRPC) and `:4318` (HTTP);
- sends everything to two backends in parallel:
  - [OpenObserve](../openobserve/README.md) on docker-apps (`otlphttp/openobserve`) for search and dashboards;
  - [Zabbix APM](../zabbix-apm/README.md) on the Oracle VM (`otlp/zabbix`): OTLP/gRPC to nginx on `:443`,
    mutual TLS with a client certificate from the private CA. The export queue is kept on disk, so short
    internet outages do not lose data.

File offsets are kept in `DATA_FOLDER`, so a restart does not resend old lines (`start_at: end` on first run).

## How to start

1. Create `.env` from `.env.example`; set `HOST_NAME` per host, `OPENOBSERVE_AUTH`
   (`echo -n 'email:password' | base64`) and `ZABBIX_APM_ENDPOINT`.
2. Put `ca.crt`, `client.crt`, `client.key` for this host into `TLS_FOLDER` (`client.key` mode 600).
3. `docker compose up -d`.
4. Check: `docker logs otel-collector` has no `error` lines; nginx on the Oracle VM logs
   `POST /opentelemetry.proto.collector.logs.v1.LogsService/Export 200`.
