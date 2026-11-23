"""Media watchdog: alerts in Telegram when a request is stuck.

Checks (run every CHECK_INTERVAL seconds by the container loop):
  1. Seerr request approved, older than STUCK_HOURS, but Radarr/Sonarr has neither
     the file nor an active download -> re-trigger a search once and alert.
     For TV only aired, monitored episodes without a file count as missing.
  2. Download in the Radarr/Sonarr queue without progress for STUCK_HOURS
     (e.g. no seeders), or finished but blocked/failed on import -> alert.
The same problem is reported again at most once per REALERT_HOURS.
Only the Python standard library is used; state lives in /state/state.json.
"""
import html
import json
import os
import re
import time
import urllib.request
from datetime import datetime, timezone

STUCK_HOURS = float(os.environ.get("STUCK_HOURS", "3"))
REALERT_HOURS = float(os.environ.get("REALERT_HOURS", "24"))
TG_CHAT = os.environ["TG_CHAT_ID"]
TG_TOPIC = os.environ.get("TG_TOPIC_ID")
STATE_FILE = "/state/state.json"
PUBLIC = {
    "radarr": os.environ.get("RADARR_PUBLIC_URL", "https://radarr.mbuz.uk"),
    "sonarr": os.environ.get("SONARR_PUBLIC_URL", "https://sonarr.mbuz.uk"),
    "seerr": os.environ.get("SEERR_PUBLIC_URL", "https://seerr.mbuz.uk"),
}
ARR = {"radarr": "http://radarr:7878/api/v3", "sonarr": "http://sonarr:8989/api/v3"}
SEERR = "http://seerr:5055/api/v1"

NOW = time.time()
STUCK = STUCK_HOURS * 3600


def arr_key(app):
    text = open(f"/keys/{app}/config.xml").read()
    return re.search(r"<ApiKey>(.*?)</ApiKey>", text).group(1)


def http(url, headers, method="GET", body=None):
    req = urllib.request.Request(url, method=method, headers={**headers, "Content-Type": "application/json"},
                                 data=None if body is None else json.dumps(body).encode())
    with urllib.request.urlopen(req, timeout=60) as r:
        raw = r.read()
        return json.loads(raw) if raw else None


KEYS = {app: arr_key(app) for app in ARR}
SEERR_KEY = json.load(open("/keys/seerr/settings.json"))["main"]["apiKey"]
TG_TOKEN = open("/keys/telegram/BOT_TOKEN").read().strip()


def arr(app, path, method="GET", body=None):
    return http(f"{ARR[app]}/{path}", {"X-Api-Key": KEYS[app]}, method, body)


def seerr(path):
    return http(f"{SEERR}/{path}", {"X-Api-Key": SEERR_KEY})


def ts(iso):
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).timestamp()


def hours(seconds):
    return f"{seconds / 3600:.0f} h" if seconds < 2 * 86400 else f"{seconds / 86400:.0f} d"


def telegram(text):
    body = {"chat_id": TG_CHAT, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True}
    if TG_TOPIC:
        body["message_thread_id"] = int(TG_TOPIC)
    http(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage", {}, "POST", body)


def load_state():
    try:
        return json.load(open(STATE_FILE))
    except (OSError, ValueError):
        return {}


state = load_state()
progress = state.get("progress", {})   # downloadId -> [sizeleft, since]
alerted = state.get("alerted", {})     # problem key -> last alert time
active = set()                         # problem keys seen in this run
messages = []


def report(key, text):
    active.add(key)
    if NOW - alerted.get(key, 0) >= REALERT_HOURS * 3600:
        messages.append(text)
        alerted[key] = NOW


# --- Queues: which items are downloading, and are they stuck -------------------
queued = {"radarr": set(), "sonarr": set()}   # movieId / seriesId with an active download
new_progress = {}
for app in ARR:
    for q in arr(app, "queue?pageSize=200&includeMovie=true&includeSeries=true")["records"]:
        owner = q.get("movieId") if app == "radarr" else q.get("seriesId")
        queued[app].add(owner)
        did = q.get("downloadId") or f"{app}-{q['id']}"
        if did in new_progress:      # season packs appear once per episode
            continue
        media = q.get("movie") or q.get("series") or {}
        name = html.escape(media.get("title") or q.get("title", "?"))
        state_ = q.get("trackedDownloadState", "")
        if state_ in ("importBlocked", "importFailed", "failedPending"):
            notes = "; ".join(m for s in q.get("statusMessages", []) for m in s.get("messages", []))[:300]
            report(f"import:{did}", f"⚠️ <b>{name}</b>: downloaded but import is {html.escape(state_)}.\n"
                                    f"{html.escape(notes or q.get('errorMessage') or '')}\n{PUBLIC[app]}/activity/queue")
            new_progress[did] = [q.get("sizeleft", 0), NOW]
            continue
        left = q.get("sizeleft", 0)
        prev_left, since = progress.get(did, [None, NOW])
        if prev_left is None or left < prev_left:
            since = NOW
        new_progress[did] = [left, since]
        if left > 0 and NOW - since >= STUCK:
            done = 100 - 100 * left / max(q.get("size", 1), 1)
            report(f"stalled:{did}", f"🐢 <b>{name}</b>: download stuck at {done:.0f}% for {hours(NOW - since)} "
                                     f"(probably no seeders).\nPick another release: {PUBLIC[app]}/activity/queue")
progress = new_progress

# --- Seerr requests that produced nothing ---------------------------------------
for r in seerr("request?take=100&filter=approved&sort=added")["results"]:
    media = r.get("media") or {}
    if media.get("status") == 5:          # available
        continue
    age = NOW - ts(r["createdAt"])
    if age < STUCK:
        continue
    app = "radarr" if r["type"] == "movie" else "sonarr"
    ext = media.get("externalServiceId")
    if not ext or ext in queued[app]:
        continue
    who = html.escape((r.get("requestedBy") or {}).get("displayName") or "?")
    if app == "radarr":
        movie = arr("radarr", f"movie/{ext}")
        if movie.get("hasFile") or not movie.get("isAvailable", True):
            continue
        name = html.escape(f"{movie['title']} ({movie.get('year')})")
        link = f"{PUBLIC['radarr']}/movie/{movie['titleSlug']}"
        key = f"missing:radarr:{ext}"
        if key not in alerted and not os.environ.get("DRY_RUN"):
            arr("radarr", "command", "POST", {"name": "MoviesSearch", "movieIds": [ext]})
        detail = "no release accepted by the quality profile"
    else:
        series = arr("sonarr", f"series/{ext}")
        seasons = {s["seasonNumber"] for s in r.get("seasons", [])}
        missing = [e for e in arr("sonarr", f"episode?seriesId={ext}")
                   if e.get("monitored") and not e.get("hasFile") and e.get("airDateUtc")
                   and ts(e["airDateUtc"]) < NOW and (not seasons or e["seasonNumber"] in seasons)]
        if not missing:
            continue
        name = html.escape(f"{series['title']} ({series.get('year')})")
        link = f"{PUBLIC['sonarr']}/series/{series['titleSlug']}"
        key = f"missing:sonarr:{ext}:{','.join(map(str, sorted(seasons)))}"
        if key not in alerted and not os.environ.get("DRY_RUN"):
            for season in sorted({e["seasonNumber"] for e in missing}):
                arr("sonarr", "command", "POST", {"name": "SeasonSearch", "seriesId": ext, "seasonNumber": season})
        detail = f"{len(missing)} aired episode(s) missing"
    report(key, f"🔍 <b>{name}</b> requested by {who} {hours(age)} ago, nothing is downloading "
                f"({detail}). Search re-triggered; if it keeps failing, check Interactive Search:\n{link}")

# Forget alerts for problems that are gone, so a new occurrence is reported at once.
alerted = {k: v for k, v in alerted.items() if k in active}

for text in messages:
    if os.environ.get("DRY_RUN"):     # test mode: print instead of sending
        print("ALERT:", text)
    else:
        telegram(text)
os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
json.dump({"progress": progress, "alerted": alerted}, open(STATE_FILE + ".tmp", "w"))
os.replace(STATE_FILE + ".tmp", STATE_FILE)
print(datetime.now(timezone.utc).isoformat(timespec="seconds"),
      f"checked: {len(progress)} downloads, {len(active)} problems, {len(messages)} alerts sent", flush=True)
