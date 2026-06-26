"""Kavita integration — polls for new series/chapters and posts embeds to a private channel.

Owner-only: configured entirely via env vars. No guild BotConfig integration.
The bot downloads cover images directly (Kavita server may not be publicly reachable).
"""
import io
import json
import logging
import asyncio
import datetime
import os

import requests
import discord
from discord.ext import tasks

log = logging.getLogger(__name__)

# ─── env config ──────────────────────────────────────────────────────────────
_URL      = (os.getenv("KAVITA_URL") or "").rstrip("/")
_API_KEY  = os.getenv("KAVITA_API_KEY", "")
_USER     = os.getenv("KAVITA_USER", "")
_PASS     = os.getenv("KAVITA_PASSWORD", "")
_INTERVAL  = int(os.getenv("KAVITA_POLL_INTERVAL") or 30)
_LIB_IDS  = {int(x) for x in os.getenv("KAVITA_LIBRARIES", "").split(",") if x.strip().isdigit()}

# Pre-populate library name cache from KAVITA_LIBRARY_NAMES=1:Manga,2:Novelas Ligeras,5:Comics
def _parse_lib_names(raw: str) -> dict[int, str]:
    result: dict[int, str] = {}
    for entry in raw.split(","):
        entry = entry.strip()
        if ":" in entry:
            lid, _, lname = entry.partition(":")
            if lid.strip().isdigit():
                result[int(lid.strip())] = lname.strip()
    return result

_lib_cache: dict[int, str] = _parse_lib_names(os.getenv("KAVITA_LIBRARY_NAMES", ""))

_SEEN_FILE    = "kavita_seen.json"
_PENDING_FILE = "pending_notifications.json"
_seen: dict = {"initialized": False, "channel_id": 0, "last_poll_time": "", "notified": {}}
_NOTIFY_TTL = datetime.timedelta(hours=24)
_jwt: str = ""

# Exposed so on_ready() can call poll manually via force_poll()
_poll_task = None


# ─── library colors ──────────────────────────────────────────────────────────

def _lib_color(name: str) -> int:
    n = name.lower()
    if "manga" in n:
        return 0xE74C3C   # red
    if "comic" in n:
        return 0x3498DB   # blue
    if "book" in n or "libro" in n:
        return 0x2ECC71   # green
    return 0x95A5A6       # grey


# ─── persistence ─────────────────────────────────────────────────────────────

def _load() -> None:
    global _seen
    if not os.path.exists(_SEEN_FILE):
        return
    try:
        with open(_SEEN_FILE, encoding="utf-8") as f:
            _seen = json.load(f)
        _seen.setdefault("initialized", False)
        _seen.setdefault("channel_id", 0)
        _seen.setdefault("last_poll_time", "")
        _seen.setdefault("notified", {})
        _purge_notified()
    except Exception as e:
        log.warning("[Kavita] Could not load seen file: %s", e)


def _save() -> None:
    try:
        with open(_SEEN_FILE, "w", encoding="utf-8") as f:
            json.dump(_seen, f)
    except Exception as e:
        log.warning("[Kavita] Could not save seen file: %s", e)


def reset_seen() -> None:
    """Clear seen cache so the next poll re-announces everything."""
    global _seen
    _seen = {"initialized": True, "channel_id": _seen.get("channel_id", 0), "last_poll_time": "", "notified": {}}
    _save()


def set_channel(channel_id: int) -> None:
    """Persist the notification channel ID chosen by the owner."""
    _seen["channel_id"] = channel_id
    _save()


# ─── authentication ───────────────────────────────────────────────────────────

def _authenticate() -> bool:
    global _jwt
    if not _URL:
        return False

    # Primary: exchange API key for JWT (Kavita 0.8+)
    if _API_KEY:
        url = f"{_URL}/api/Account/authenticate"
        try:
            r = requests.post(url, json={"apiKey": _API_KEY}, timeout=10)
            if r.ok:
                _jwt = r.json().get("token", "")
                if _jwt:
                    log.info("[Kavita] Authenticated via API key.")
                    return True
            log.warning("[Kavita] API key auth failed: %s %s — %s", r.status_code, url, r.text[:200])
        except Exception as e:
            log.warning("[Kavita] API key auth error: %s — %s", url, e)

    # Fallback: username / password
    if _USER and _PASS:
        url = f"{_URL}/api/Account/login"
        try:
            r = requests.post(url, json={"username": _USER, "password": _PASS}, timeout=10)
            if r.ok:
                _jwt = r.json().get("token", "")
                if _jwt:
                    log.info("[Kavita] Authenticated via username/password.")
                    return True
            log.warning("[Kavita] Login failed: %s %s — %s", r.status_code, url, r.text[:200])
        except Exception as e:
            log.warning("[Kavita] Login error: %s — %s", url, e)

    log.warning("[Kavita] Authentication failed. Check KAVITA_USER/KAVITA_PASSWORD in .env.")
    return False


def _headers() -> dict:
    return {"Authorization": f"Bearer {_jwt}"} if _jwt else {}


# ─── API helpers ──────────────────────────────────────────────────────────────

def _get(path: str, **kwargs):
    """GET from Kavita API, refreshing JWT once on 401."""
    url = f"{_URL}{path}"
    for attempt in range(2):
        try:
            r = requests.get(url, headers=_headers(), timeout=15, **kwargs)
            if r.status_code == 401 and attempt == 0:
                log.warning("[Kavita] 401 on %s — refreshing JWT.", path)
                _authenticate()
                continue
            if r.ok:
                return r.json()
            log.warning("[Kavita] GET %s → %s: %s", path, r.status_code, r.text[:200])
        except Exception as e:
            log.warning("[Kavita] GET %s error: %s", path, e)
    return None


def _post(path: str, body: dict = None, **kwargs):
    """POST to Kavita API, refreshing JWT once on 401."""
    url = f"{_URL}{path}"
    for attempt in range(2):
        try:
            r = requests.post(url, headers=_headers(), json=body or {}, timeout=15, **kwargs)
            if r.status_code == 401 and attempt == 0:
                log.warning("[Kavita] 401 on %s — refreshing JWT.", path)
                _authenticate()
                continue
            if r.ok:
                return r.json()
            log.warning("[Kavita] POST %s → %s: %s", path, r.status_code, r.text[:200])
        except Exception as e:
            log.warning("[Kavita] POST %s error: %s", path, e)
    return None


def _mal_cover_url(mal_id: int) -> str | None:
    """Return the MAL cover URL via Jikan API (no key required)."""
    if not mal_id:
        return None
    try:
        r = requests.get(f"https://api.jikan.moe/v4/manga/{mal_id}", timeout=10)
        if r.ok:
            imgs = r.json().get("data", {}).get("images", {})
            return (imgs.get("webp") or imgs.get("jpg") or {}).get("large_image_url")
        log.warning("[Kavita] Jikan cover (mal %s): HTTP %s", mal_id, r.status_code)
    except Exception as e:
        log.warning("[Kavita] Jikan cover (mal %s): %s", mal_id, e)
    return None


def _kavita_cover_bytes(series_id: int) -> bytes | None:
    """Download cover image bytes from Kavita (fallback when Jikan fails or MAL ID missing)."""
    if not series_id:
        return None
    try:
        r = requests.get(
            f"{_URL}/api/Image/series-cover",
            headers=_headers(),
            params={"seriesId": series_id},
            timeout=15,
        )
        if r.ok and r.content:
            return r.content
        log.warning("[Kavita] Kavita cover series %s: HTTP %s", series_id, r.status_code)
    except Exception as e:
        log.warning("[Kavita] Kavita cover series %s: %s", series_id, e)
    return None


# ─── library name cache ───────────────────────────────────────────────────────
# Seeded from KAVITA_LIBRARY_NAMES env var; enriched at runtime from recently-added-v2.

def _lib_name(lib_id: int) -> str:
    return _lib_cache.get(lib_id, f"Biblioteca {lib_id}")


# ─── filtering / deduplication ────────────────────────────────────────────────

def _purge_notified() -> None:
    cutoff = datetime.datetime.utcnow() - _NOTIFY_TTL
    _seen["notified"] = {
        sid: ts for sid, ts in _seen.get("notified", {}).items()
        if datetime.datetime.fromisoformat(ts) > cutoff
    }

def _already_notified(series_id: int) -> bool:
    ts = _seen.get("notified", {}).get(str(series_id))
    if not ts:
        return False
    return datetime.datetime.fromisoformat(ts) > datetime.datetime.utcnow() - _NOTIFY_TTL

def _mark_notified(series_id: int) -> None:
    _seen.setdefault("notified", {})[str(series_id)] = datetime.datetime.utcnow().isoformat()

def _wanted(item: dict) -> bool:
    return not _LIB_IDS or item.get("libraryId") in _LIB_IDS



def _new_series() -> tuple[list[dict], str]:
    """Returns (new_series, max_created_timestamp_in_kavita_tz)."""
    data = _post("/api/Series/recently-added-v2", params={"pageNumber": 1, "pageSize": 30})
    if not isinstance(data, list):
        data = (data or {}).get("content", [])
    # Enrich library cache from API data; env-configured names take precedence.
    for s in data:
        lib_id, lib_name = s.get("libraryId", 0), s.get("libraryName", "")
        if lib_id and lib_name and lib_id not in _lib_cache:
            _lib_cache[lib_id] = lib_name
    max_ts    = max((s.get("created", "") for s in data), default="")
    last_poll = _seen.get("last_poll_time", "")
    filtered  = [
        s for s in data
        if _wanted(s)
        and (not last_poll or s.get("created", "") > last_poll)
        and not _already_notified(s.get("id", 0))
    ]
    return filtered, max_ts



# ─── embed builders ───────────────────────────────────────────────────────────




def _series_url(series_id: int, lib_id: int) -> str:
    return f"{_URL}/library/{lib_id}/series/{series_id}"


def _cover_color(s: dict) -> int:
    raw = (s.get("primaryColor") or "").lstrip("#")
    try:
        return int(raw, 16) if len(raw) == 6 else _lib_color(s.get("libraryName", ""))
    except ValueError:
        return _lib_color(s.get("libraryName", ""))


def _external_links(s: dict) -> str | None:
    parts = []
    if s.get("malId"):
        parts.append(f"[MyAnimeList](https://myanimelist.net/manga/{s['malId']})")
    if s.get("aniListId"):
        parts.append(f"[AniList](https://anilist.co/manga/{s['aniListId']})")
    return " · ".join(parts) if parts else None


def _make_series_embed(s: dict) -> tuple[discord.Embed, str]:
    summary = (s.get("summary") or "").strip()
    embed = discord.Embed(
        title=s.get("name", "Nueva serie"),
        url=_series_url(s["id"], s.get("libraryId", 0)),
        description=summary[:300] if summary else None,
        color=_cover_color(s),
    )
    embed.add_field(name="Biblioteca", value=s.get("libraryName", "—"), inline=True)
    now_ts = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    embed.add_field(name="Agregado", value=f"<t:{now_ts}:f>", inline=True)
    links = _external_links(s)
    if links:
        embed.add_field(name="Links", value=links, inline=False)
    content = f"**{s.get('libraryName', 'Kavita')}:** {s.get('name', '')} se acaba de añadir a Kavita."
    return embed, content



# ─── episode-catcher pending notifications ───────────────────────────────────

def _read_pending() -> list[dict]:
    """Read and atomically clear pending_notifications.json written by Kavita Episode Catcher."""
    if not os.path.exists(_PENDING_FILE):
        return []
    try:
        with open(_PENDING_FILE, encoding="utf-8") as f:
            data = json.load(f)
        os.remove(_PENDING_FILE)
        return data if isinstance(data, list) else []
    except Exception as e:
        log.warning("[Kavita] Could not read pending notifications: %s", e)
        return []


def _fetch_series_info(series_id: int) -> dict | None:
    """Fetch full series metadata from Kavita by series ID."""
    try:
        r = requests.get(
            f"{_URL}/api/Series/{series_id}",
            headers={"Authorization": f"Bearer {_jwt}"},
            timeout=10,
        )
        if r.ok:
            return r.json()
        log.warning("[Kavita] Series %s fetch: HTTP %s", series_id, r.status_code)
    except Exception as e:
        log.warning("[Kavita] Series %s fetch: %s", series_id, e)
    return None


def _make_pending_embed(info: dict, chapters_added: int) -> tuple[discord.Embed, str]:
    """Build embed for a series notified via Episode Catcher (chapter upload event)."""
    name   = info.get("name", "Actualización")
    sid    = info.get("id", 0)
    lib_id = info.get("libraryId", 0)
    lib    = info.get("libraryName") or _lib_name(lib_id)
    embed = discord.Embed(
        title=name,
        url=_series_url(sid, lib_id),
        color=_cover_color(info),
    )
    embed.add_field(name="Biblioteca",        value=lib,                   inline=True)
    embed.add_field(name="Capítulos subidos", value=str(chapters_added),   inline=True)
    links = _external_links(info)
    if links:
        embed.add_field(name="Links", value=links, inline=False)
    content = f"**{lib}:** {name} — {chapters_added} capítulo(s) nuevo(s) disponible(s)."
    return embed, content


async def _process_pending(channel: discord.TextChannel) -> int:
    """Process pending notifications from Episode Catcher. Returns count of notifications sent."""
    items = await asyncio.to_thread(_read_pending)
    if not items:
        return 0
    sent = 0
    for item in items:
        kavita_id     = item.get("kavita_id", 0)
        chapters_added = item.get("chapters_added", 0)
        name          = item.get("name", "?")
        if not kavita_id:
            log.warning("[Kavita] Pending item '%s' has no kavita_id — skipping.", name)
            continue
        try:
            info = await asyncio.to_thread(_fetch_series_info, kavita_id)
            if not info:
                log.warning("[Kavita] Could not fetch series info for kavita_id=%s (%s).", kavita_id, name)
                continue
            embed, content = _make_pending_embed(info, chapters_added)
            await _send(channel, embed, info.get("malId", 0), content=content, series_id=kavita_id)
            sent += 1
        except Exception as e:
            log.error("[Kavita] pending '%s': %s", name, e)
    return sent


# ─── posting ─────────────────────────────────────────────────────────────────

async def _send(channel: discord.TextChannel, embed: discord.Embed, mal_id: int = 0, content: str = None, series_id: int = 0) -> None:
    cover_url = None
    if mal_id:
        cover_url = await asyncio.to_thread(_mal_cover_url, mal_id)

    if cover_url:
        embed.set_image(url=cover_url)
        await channel.send(content=content, embed=embed)
    elif series_id:
        cover_bytes = await asyncio.to_thread(_kavita_cover_bytes, series_id)
        if cover_bytes:
            f = discord.File(io.BytesIO(cover_bytes), filename="cover.jpg")
            embed.set_image(url="attachment://cover.jpg")
            await channel.send(content=content, embed=embed, file=f)
        else:
            await channel.send(content=content, embed=embed)
    else:
        await channel.send(content=content, embed=embed)


_BATCH_THRESHOLD = 3


async def _send_batch(channel: discord.TextChannel, series: list[dict]) -> None:
    """Send one summary embed per library when there are more than _BATCH_THRESHOLD new series."""
    by_lib: dict[str, list] = {}
    for s in series:
        lib = s.get("libraryName", "—")
        by_lib.setdefault(lib, []).append(s)

    for lib_name, lib_items in by_lib.items():
        n = len(lib_items)
        lines = [f"• [{i.get('name', '?')}]({_series_url(i['id'], i.get('libraryId', 0))})" for i in lib_items]
        desc = "\n".join(lines)
        if len(desc) > 4096:
            desc = desc[:4093] + "…"
        embed = discord.Embed(
            title=f"📚 {n} nuevas series — {lib_name}",
            description=desc,
            color=_lib_color(lib_name),
        )
        await channel.send(embed=embed)


async def _post_series(channel: discord.TextChannel, series: list[dict]) -> None:
    if len(series) > _BATCH_THRESHOLD:
        try:
            await _send_batch(channel, series)
            for s in series:
                _mark_notified(s.get("id", 0))
        except Exception as e:
            log.error("[Kavita] batch series: %s", e)
    else:
        for s in series:
            try:
                embed, content = _make_series_embed(s)
                await _send(channel, embed, s.get("malId", 0), content=content, series_id=s.get("id", 0))
                _mark_notified(s.get("id", 0))
            except Exception as e:
                log.error("[Kavita] series %s: %s", s.get("id"), e)


# ─── public API ──────────────────────────────────────────────────────────────

async def run_poll(client: discord.Client) -> tuple[int, int]:
    """Run one poll cycle. Returns (new_series_count, new_chapters_count)."""
    ch_id = _seen.get("channel_id", 0)
    if not ch_id:
        log.warning("[Kavita] No notification channel set. Use /kavita canal to configure.")
        return 0, 0
    channel = client.get_channel(ch_id)
    if not channel:
        log.warning("[Kavita] Channel %s not found.", ch_id)
        return 0, 0

    if not _jwt:
        if not await asyncio.to_thread(_authenticate):
            return 0, 0

    series, max_ts = await asyncio.to_thread(_new_series)
    # Use Kavita's own timestamp so last_poll_time and created are always in the same timezone.
    _seen["last_poll_time"] = max_ts or datetime.datetime.utcnow().isoformat()

    if not _seen["initialized"]:
        _seen["initialized"] = True
        _save()
        log.info("[Kavita] First-run snapshot complete. Next poll will report new content.")
        return 0, 0

    if series:
        def _label(s: dict) -> str:
            name = s.get("name", "?")
            iso  = s.get("created", "")
            try:
                dt = datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))
                return f"{name} ({dt.strftime('%H:%M')})"
            except Exception:
                return name
        log.info("[Kavita] %d new series:\n  %s", len(series), "\n  ".join(_label(s) for s in series))
        await _post_series(channel, series)

    pending = await _process_pending(channel)
    if pending:
        log.info("[Kavita] %d pending notification(s) from Episode Catcher sent.", pending)

    _save()
    return len(series), pending


def setup_kavita_poller(client: discord.Client) -> bool:
    """
    Start the background polling loop.
    Returns True if started, False if env vars are missing.
    Call from on_ready().
    """
    global _poll_task

    if not (_URL and (_API_KEY or (_USER and _PASS))):
        log.info("[Kavita] Not configured — poller disabled.")
        return False

    _load()

    @tasks.loop(minutes=_INTERVAL)
    async def _loop() -> None:
        await run_poll(client)

    @_loop.before_loop
    async def _before() -> None:
        await client.wait_until_ready()

    _loop.start()
    _poll_task = _loop
    log.info("[Kavita] Poller started (interval: %d min, channel: %s).", _INTERVAL, _seen.get("channel_id", "not set"))
    return True


def fetch_recent_series(limit: int = 15) -> list[dict]:
    """Return the most recently added series from Kavita (for the /kavita series command)."""
    data = _post("/api/Series/recently-added-v2", params={"pageNumber": 1, "pageSize": limit})
    if not isinstance(data, list):
        data = (data or {}).get("content", [])
    return [s for s in data if _wanted(s)]
