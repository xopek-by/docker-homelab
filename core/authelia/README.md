# Authelia

Single sign-on and 2FA (TOTP, passkeys) for services published through Nginx Proxy Manager.

- Portal: `https://auth.mbuz.uk`
- Runs on docker-apps on the external Docker network `proxy`, shared with NPM. No published ports.
- Config: [`configuration.yml`](configuration.yml) (in git, no secrets).
- Host data in `${AUTHELIA_DATA}` (default `/opt/docker_data/authelia`):
  - `secrets/JWT_SECRET`, `secrets/SESSION_SECRET`, `secrets/STORAGE_ENCRYPTION_KEY` — random, `chmod 600`, never in git;
  - `data/users_database.yml` — users and argon2 password hashes;
  - `data/db.sqlite3` — 2FA devices, sessions;
  - `data/notification.txt` — one-time codes until SMTP is configured.

## First-time setup

```bash
# On docker-apps
sudo mkdir -p /opt/docker_data/authelia/{data,secrets}
for s in JWT_SECRET SESSION_SECRET STORAGE_ENCRYPTION_KEY; do
  sudo sh -c "tr -dc 'A-Za-z0-9' </dev/urandom | head -c 64 > /opt/docker_data/authelia/secrets/$s"
done
sudo chmod 700 /opt/docker_data/authelia/secrets && sudo chmod 600 /opt/docker_data/authelia/secrets/*
docker network create proxy   # once; NPM joins it too

# Password hash (asks for the password interactively, prints only the hash)
docker run --rm -it authelia/authelia:4.39.28 authelia crypto hash generate argon2
```

`data/users_database.yml`:

```yaml
users:
  mbuz:
    displayname: 'Maksim'
    password: '$argon2id$...'   # paste the generated hash
    email: 'you@example.com'
    groups: ['admins']
```

Register TOTP or a passkey at `https://auth.mbuz.uk` → the confirmation code appears in `data/notification.txt`.

## Portal host in NPM (`auth.mbuz.uk`)

A regular NPM proxy host, visible in the UI:

- Domain `auth.mbuz.uk` → `http` `authelia` `9091`; SSL: `*.mbuz.uk` certificate, Force SSL, HTTP/2, Websockets on, Block exploits off.
- **Advanced** tab owns `location /` (so NPM does not add its default one):

```nginx
location / {
  set $upstream_authelia http://authelia:9091;
  proxy_pass $upstream_authelia;
  proxy_set_header Host $host;
  proxy_set_header X-Original-URL $scheme://$http_host$request_uri;
  proxy_set_header X-Forwarded-Proto $scheme;
  proxy_set_header X-Forwarded-Host $http_host;
  proxy_set_header X-Forwarded-URI $request_uri;
  proxy_set_header X-Forwarded-For $authelia_client_ip;
  proxy_set_header X-Real-IP $authelia_client_ip;
  proxy_http_version 1.1;
  proxy_set_header Upgrade $http_upgrade;
  proxy_set_header Connection "upgrade";
}
```

`$authelia_client_ip` is an http-level `map` (it cannot live inside a proxy host), kept in
`/opt/docker_data/nginx-proxy/data/nginx/custom/http.conf` on docker-apps:

```nginx
# Client IP for Authelia: Cloudflare sends it in CF-Connecting-IP
map $http_cf_connecting_ip $authelia_client_ip {
  "" $remote_addr;
  default $http_cf_connecting_ip;
}
```

## Protecting an NPM proxy host

NPM mounts the snippets from [`../nginx-proxy-manager/snippets`](../nginx-proxy-manager/snippets) at `/snippets`.
In the proxy host → **Advanced** tab (leave Custom Locations empty):

```nginx
include /snippets/authelia-location.conf;

location / {
    include /snippets/authelia-authrequest.conf;
    include conf.d/include/proxy.conf;
}
```

Do **not** put behind forward auth anything used by apps/clients rather than a browser:
Vaultwarden, Immich (mobile app), git over HTTPS, webhooks. Use the app's own 2FA or OIDC for those.
