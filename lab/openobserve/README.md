# OpenObserve

Logs, traces and metrics store with a web UI. Receives OpenTelemetry (OTLP) data from the
[OTel collectors](../otel-collector/README.md) on the Docker hosts.

[OpenObserve docs](https://openobserve.ai/docs/)

- Runs on docker-apps: UI at `http://10.0.0.101:5080`.
- OTLP/HTTP: `http://10.0.0.101:5080/api/default` (organization `default`), Basic auth with the root user.
- OTLP/gRPC: `10.0.0.101:5081`.
- Docker container logs land in the `default` logs stream; filter by `container_name` or `host_name`.

## How to start

1. Create `.env` from `.env.example`, set a strong `ZO_ROOT_USER_PASSWORD`.
2. `docker compose up -d`.

The same data is also sent to the Zabbix APM proxy, see [otel-collector](../otel-collector/README.md).
