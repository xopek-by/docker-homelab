# ClickHouse for Zabbix APM

Telemetry storage for Zabbix 8.0 APM (Monitoring > APM). Runs on docker-cloud: `http://10.0.0.102:8123`.

Data path: OTel collectors -> Zabbix proxy `zabbix-proxy-lxc` (APM collector, OTLP/gRPC :4317) -> this ClickHouse.
The Zabbix server and frontend on Oracle read it through the Tailscale subnet route `10.0.0.0/24`.

## How to start

1. Create `.env` from `.env.example`.
2. `docker compose up -d`.
3. Create the schema with the script shipped in `zabbix-sql-scripts` (`/usr/share/zabbix/sql-scripts/clickhouse/otel_all.sh`),
   retention 14 days:

   ```bash
   ./otel_all.sh -s http://10.0.0.102:8123 -d otel -u default -p '<admin password>' -t 1209600
   ```

4. Create the Zabbix user (read/write on `otel` only):

   ```sql
   CREATE USER zabbix IDENTIFIED WITH sha256_password BY '<password>';
   GRANT SELECT, INSERT ON otel.* TO zabbix;
   ```

5. In Zabbix: Administration > Data source > APM: ClickHouse, `http://10.0.0.102:8123`, user `zabbix`, database `otel`.
