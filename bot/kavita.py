"""Kavita integration — polls for new series/chapters and posts embeds to a private channel.

Owner-only: configured entirely via env vars. No guild BotConfig integration.
The bot downloads cover images directly (Kavita server may not be publicly reachable).
"""
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
_INTERVAL = int(os.getenv("KAVITA_POLL_INTERVAL") or 30)
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

_SEEN_FILE = "kavita_seen.json"
_seen: dict = {"initialized": False, "channel_id": 0, "series": [], "chapters": []}
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
        _seen.setdefault("series", [])
        _seen.setdefault("chapters", [])
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
    _seen = {"initialized": True, "channel_id": _seen.get("channel_id", 0), "series": [], "chapters": []}
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
    except Exception as e:
        log.warning("[Kavita] Jikan cover (mal %s): %s", mal_id, e)
    return None


# ─── library name cache ───────────────────────────────────────────────────────
# Seeded from KAVITA_LIBRARY_NAMES env var; enriched at runtime from recently-added-v2.

def _lib_name(lib_id: int) -> str:
    return _lib_cache.get(lib_id, f"Biblioteca {lib_id}")


# ─── filtering / deduplication ────────────────────────────────────────────────

def _wanted(item: dict) -> bool:
    return not _LIB_IDS or item.get("libraryId") in _LIB_IDS


def _chapter_key(s: dict) -> str:
    # Composite key: seriesId + created — changes whenever a new chapter arrives.
    return f"{s.get('seriesId', '')}:{s.get('created', '')}"


def _new_series() -> list[dict]:
    data = _post("/api/Series/recently-added-v2", params={"pageNumber": 1, "pageSize": 30})
    if not isinstance(data, list):
        data = (data or {}).get("content", [])
    # Enrich library cache from API data; env-configured names take precedence.
    for s in data:
        lib_id, lib_name = s.get("libraryId", 0), s.get("libraryName", "")
        if lib_id and lib_name and lib_id not in _lib_cache:
            _lib_cache[lib_id] = lib_name
    seen_set = set(_seen["series"])
    return [s for s in data if str(s.get("id", "")) not in seen_set and _wanted(s)]


def _new_chapters() -> list[dict]:
    data = _post("/api/Series/recently-updated-series", params={"pageNumber": 1, "pageSize": 30})
    if not isinstance(data, list):
        data = (data or {}).get("content", [])
    seen_set = set(_seen["chapters"])
    return [s for s in data if _chapter_key(s) not in seen_set and _wanted(s)]


# ─── embed builders ───────────────────────────────────────────────────────────

def _fmt_date(iso: str) -> str:
    try:
        dt = datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return dt.strftime("%d/%m/%Y")
    except Exception:
        return iso[:10]


def _fmt_format(fmt: int) -> str:
    return {0: "—", 1: "Archive", 2: "Imágenes", 3: "ePub", 4: "PDF"}.get(fmt, str(fmt))


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
    if s.get("created"):
        embed.add_field(name="Agregado", value=_fmt_date(s["created"]), inline=True)
    links = _external_links(s)
    if links:
        embed.add_field(name="Links", value=links, inline=False)
    content = f"**{s.get('libraryName', 'Kavita')}:** {s.get('name', '')} se acaba de añadir a Kavita."
    return embed, content


def _make_chapter_embed(s: dict) -> tuple[discord.Embed, str]:
    # recently-updated-series uses seriesName/seriesId, no libraryName.
    name    = s.get("seriesName", "Actualización")
    sid     = s.get("seriesId", 0)
    lib_id  = s.get("libraryId", 0)
    lib     = _lib_name(lib_id)
    embed = discord.Embed(
        title=name,
        url=_series_url(sid, lib_id),
        color=_lib_color(lib),
    )
    embed.add_field(name="Biblioteca", value=lib, inline=True)
    embed.add_field(name="Formato",    value=_fmt_format(s.get("format", 0)), inline=True)
    if s.get("created"):
        embed.add_field(name="Actualizado", value=_fmt_date(s["created"]), inline=True)
    content = f"**{lib}:** {name} tiene nuevo contenido en Kavita."
    return embed, content


# ─── posting ─────────────────────────────────────────────────────────────────

async def _send(channel: discord.TextChannel, embed: discord.Embed, mal_id: int = 0, content: str = None) -> None:
    if mal_id:
        cover_url = await asyncio.to_thread(_mal_cover_url, mal_id)
        if cover_url:
            embed.set_image(url=cover_url)
    await channel.send(content=content, embed=embed)


_BATCH_THRESHOLD = 3


async def _send_batch(channel: discord.TextChannel, items: list[dict], kind: str) -> None:
    """Send one summary embed per library when there are more than _BATCH_THRESHOLD items."""
    is_chapters = kind == "chapters"
    icon = "📚" if kind == "series" else "📖"

    by_lib: dict[str, list] = {}
    for item in items:
        lib = _lib_name(item.get("libraryId", 0)) if is_chapters else item.get("libraryName", "—")
        by_lib.setdefault(lib, []).append(item)

    for lib_name, lib_items in by_lib.items():
        n = len(lib_items)
        label = f"{n} nuevas series" if kind == "series" else f"{n} series actualizadas"
        if is_chapters:
            lines = [f"• [{i.get('seriesName', '?')}]({_series_url(i.get('seriesId', 0), i.get('libraryId', 0))})" for i in lib_items]
        else:
            lines = [f"• [{i.get('name', '?')}]({_series_url(i['id'], i.get('libraryId', 0))})" for i in lib_items]
        desc = "\n".join(lines)
        if len(desc) > 4096:
            desc = desc[:4093] + "…"
        embed = discord.Embed(
            title=f"{icon} {label} — {lib_name}",
            description=desc,
            color=_lib_color(lib_name),
        )
        await channel.send(embed=embed)


async def _post_all(
    channel: discord.TextChannel,
    series: list[dict],
    chapters: list[dict],
) -> None:
    # A newly-added series also appears in recently-updated; keep it only in series.
    # Mark the skipped chapters as seen so they don't reappear on the next poll cycle.
    new_series_ids = {s["id"] for s in series}
    skipped, chapters = [], []
    for c in chapters:
        (skipped if c.get("seriesId") in new_series_ids else chapters).append(c)
    for c in skipped:
        _seen["chapters"].append(_chapter_key(c))

    if len(series) > _BATCH_THRESHOLD:
        try:
            await _send_batch(channel, series, "series")
        except Exception as e:
            log.error("[Kavita] batch series: %s", e)
        for s in series:
            _seen["series"].append(str(s["id"]))
    else:
        for s in series:
            try:
                embed, content = _make_series_embed(s)
                await _send(channel, embed, s.get("malId", 0), content=content)
                _seen["series"].append(str(s["id"]))
            except Exception as e:
                log.error("[Kavita] series %s: %s", s.get("id"), e)

    if len(chapters) > _BATCH_THRESHOLD:
        try:
            await _send_batch(channel, chapters, "chapters")
        except Exception as e:
            log.error("[Kavita] batch chapters: %s", e)
        for c in chapters:
            _seen["chapters"].append(_chapter_key(c))
    else:
        for c in chapters:
            try:
                embed, content = _make_chapter_embed(c)
                await _send(channel, embed, content=content)
                _seen["chapters"].append(_chapter_key(c))
            except Exception as e:
                log.error("[Kavita] chapter %s: %s", c.get("id"), e)

    _save()


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

    series   = await asyncio.to_thread(_new_series)
    chapters = await asyncio.to_thread(_new_chapters)

    if not _seen["initialized"]:
        for s in series:
            _seen["series"].append(str(s["id"]))
        for c in chapters:
            _seen["chapters"].append(_chapter_key(c))
        _seen["initialized"] = True
        _save()
        log.info("[Kavita] First-run snapshot: %d series, %d chapters.", len(series), len(chapters))
        return 0, 0

    if series or chapters:
        log.info("[Kavita] %d new series, %d new chapters.", len(series), len(chapters))
        await _post_all(channel, series, chapters)

    return len(series), len(chapters)


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
