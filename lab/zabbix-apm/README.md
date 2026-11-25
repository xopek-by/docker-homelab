# Zabbix APM backend (Oracle VM)

Storage and collector for Zabbix 8.0 APM (Monitoring > APM, Telemetry query items). Runs on the Oracle VM
next to the Zabbix server and frontend, so they read ClickHouse locally.

```
home OTel collectors --OTLP/gRPC, mTLS--> Oracle :443 nginx (SNI otlp.apm)
    --> zabbix-apm-proxy 127.0.0.1:4317 (proxy "apm-proxy-oracle", APM collector)
    --> ClickHouse 127.0.0.1:8123 (database otel) <-- Zabbix server and frontend
```

Port 443 is already open in the OCI security list, so no new ports are exposed. nginx accepts only clients
with a certificate signed by the private CA.

## How to start

1. Create `.env` from `.env.example`.
2. `docker compose up -d`.
3. Schema (script from `zabbix-sql-scripts`), retention 14 days:

   ```bash
   /usr/share/zabbix/sql-scripts/clickhouse/otel_all.sh -s http://127.0.0.1:8123 -d otel -u default -p '<admin password>' -t 1209600
   ```

4. Zabbix user:

   ```sql
   CREATE USER zabbix IDENTIFIED WITH sha256_password BY '<password>';
   GRANT SELECT, INSERT ON otel.* TO zabbix;
   ```

5. Zabbix frontend:
   - Administration > Data source > APM: ClickHouse, `http://127.0.0.1:8123`, user `zabbix`, database `otel`;
   - Administration > Proxies: active proxy `apm-proxy-oracle`, APM tab: data collection enabled.
6. TLS for OTLP: private CA, server certificate `CN=otlp.apm`, one client certificate per Docker host,
   in `/etc/nginx/otlp-tls` (keys `chmod 600`). Install [nginx-otlp-grpc.conf](nginx-otlp-grpc.conf) as
   `/etc/nginx/conf.d/zz-otlp-grpc.conf` (it must load after the frontend vhost, otherwise it becomes the default
   server on :443 and the frontend answers 400), `nginx -t && systemctl reload nginx`.
   Collectors get `ca.crt`, `<host>.crt`, `<host>.key`, see [otel-collector](../otel-collector/README.md).
