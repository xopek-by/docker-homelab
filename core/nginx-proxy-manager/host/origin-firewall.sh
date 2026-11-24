#!/bin/sh
# Origin firewall for Nginx Proxy Manager on apps (10.0.0.101).
# The router forwards WAN 80/443 straight to this VM, so without this anyone
# could bypass Cloudflare and talk to NPM directly (and spoof CF-Connecting-IP).
#   80/443 -> allowed from LAN, Tailscale and Cloudflare edge ranges only
#   81     -> NPM admin UI, LAN and Tailscale only
# Rules live in DOCKER-USER (published Docker ports bypass INPUT).
# Re-applied by origin-firewall.service on every Docker (re)start.
set -eu

VM_IP=10.0.0.101
CACHE=/etc/origin-firewall/cf-ips-v4
# LAN, Tailscale, and Docker bridge networks on this VM (containers calling *.mbuz.uk)
TRUSTED="10.0.0.0/24 100.64.0.0/10 172.16.0.0/12 192.168.0.0/16"

# Refresh Cloudflare ranges; keep the cached list if the download fails or looks wrong
mkdir -p "$(dirname "$CACHE")"
if tmp=$(curl -fsS --max-time 10 https://www.cloudflare.com/ips-v4) \
   && [ "$(printf '%s\n' "$tmp" | grep -cE '^[0-9.]+/[0-9]+$')" -ge 10 ]; then
  printf '%s\n' "$tmp" | grep -E '^[0-9.]+/[0-9]+$' > "$CACHE"
fi
[ -s "$CACHE" ] || { echo "no Cloudflare ranges available" >&2; exit 1; }

iptables -N DOCKER-USER 2>/dev/null || true

# Remove our old jump from DOCKER-USER (idempotent re-run)
while iptables -D DOCKER-USER -j ORIGIN-JUMP 2>/dev/null; do :; done
for c in ORIGIN-JUMP ORIGIN-WEB ORIGIN-ADMIN; do
  iptables -F "$c" 2>/dev/null || iptables -N "$c"
done

# 80/443: LAN, Tailscale, Cloudflare
for n in $TRUSTED $(cat "$CACHE"); do iptables -A ORIGIN-WEB -s "$n" -j RETURN; done
iptables -A ORIGIN-WEB -m limit --limit 6/min -j LOG --log-prefix "origin-drop-web: "
iptables -A ORIGIN-WEB -j DROP

# 81: LAN and Tailscale only
for n in $TRUSTED; do iptables -A ORIGIN-ADMIN -s "$n" -j RETURN; done
iptables -A ORIGIN-ADMIN -j DROP

# Match on the original (pre-DNAT) destination so other containers' port 80 is unaffected
for p in 80 443; do
  iptables -A ORIGIN-JUMP -p tcp -m conntrack --ctstate NEW --ctorigdst "$VM_IP" --ctorigdstport "$p" -j ORIGIN-WEB
done
iptables -A ORIGIN-JUMP -p tcp -m conntrack --ctstate NEW --ctorigdst "$VM_IP" --ctorigdstport 81 -j ORIGIN-ADMIN
iptables -I DOCKER-USER 1 -j ORIGIN-JUMP
echo "origin firewall applied ($(wc -l < "$CACHE") Cloudflare ranges)"
