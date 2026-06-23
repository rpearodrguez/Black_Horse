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
_CHANNEL  = int(os.getenv("KAVITA_DISCORD_CHANNEL_ID") or 0)
_INTERVAL = int(os.getenv("KAVITA_POLL_INTERVAL") or 30)
_LIB_IDS  = {int(x) for x in os.getenv("KAVITA_LIBRARIES", "").split(",") if x.strip().isdigit()}

_SEEN_FILE = "kavita_seen.json"
_seen: dict = {"initialized": False, "series": [], "chapters": []}
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
    _seen = {"initialized": False, "series": [], "chapters": []}
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


def _get_cover(series_id: int) -> bytes | None:
    """Download cover bytes from Kavita (bot fetches it; Kavita may not be public)."""
    for ep in ("/api/Image/series-cover", "/api/Image/cover"):
        try:
            r = requests.get(
                f"{_URL}{ep}",
                headers=_headers(),
                params={"seriesId": series_id},
                timeout=15,
            )
            if r.ok and r.content:
                return r.content
            log.warning("[Kavita] Cover %s (series %s) → %s", ep, series_id, r.status_code)
        except Exception as e:
            log.warning("[Kavita] Cover %s (series %s) error: %s", ep, series_id, e)
        if _API_KEY:
            try:
                r = requests.get(
                    f"{_URL}{ep}",
                    params={"seriesId": series_id, "apiKey": _API_KEY},
                    timeout=15,
                )
                if r.ok and r.content:
                    return r.content
            except Exception:
                pass
    log.warning("[Kavita] Could not download cover for series %s.", series_id)
    return None


# ─── filtering / deduplication ────────────────────────────────────────────────

def _wanted(item: dict) -> bool:
    return not _LIB_IDS or item.get("libraryId") in _LIB_IDS


def _chapter_key(s: dict) -> str:
    # Composite key: seriesId + lastChapterAdded — changes whenever a new chapter arrives.
    return f"{s.get('id', '')}:{s.get('lastChapterAdded', '')}"


def _new_series() -> list[dict]:
    data = _post("/api/Series/recently-added-v2", params={"pageNumber": 1, "pageSize": 30})
    if not isinstance(data, list):
        data = (data or {}).get("content", [])
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


def _make_series_embed(s: dict) -> tuple[discord.Embed, str]:
    summary = (s.get("summary") or "").strip()
    embed = discord.Embed(
        title=s.get("name", "Nueva serie"),
        url=_series_url(s["id"], s.get("libraryId", 0)),
        description=summary[:300] if summary else None,
        color=_lib_color(s.get("libraryName", "")),
    )
    embed.add_field(name="Biblioteca", value=s.get("libraryName", "—"), inline=True)
    embed.add_field(name="Formato",    value=_fmt_format(s.get("format", 0)), inline=True)
    if s.get("created"):
        embed.add_field(name="Agregado", value=_fmt_date(s["created"]), inline=True)
    content = f"**{s.get('libraryName', 'Kavita')}:** {s.get('name', '')} se acaba de añadir a Kavita."
    return embed, content


def _make_chapter_embed(s: dict) -> tuple[discord.Embed, str]:
    # recently-updated-series returns series objects, not individual chapters.
    summary = (s.get("summary") or "").strip()
    embed = discord.Embed(
        title=s.get("name", "Actualización"),
        url=_series_url(s["id"], s.get("libraryId", 0)),
        description=summary[:300] if summary else None,
        color=_lib_color(s.get("libraryName", "")),
    )
    embed.add_field(name="Biblioteca", value=s.get("libraryName", "—"), inline=True)
    embed.add_field(name="Formato",    value=_fmt_format(s.get("format", 0)), inline=True)
    if s.get("lastChapterAdded"):
        embed.add_field(name="Actualizado", value=_fmt_date(s["lastChapterAdded"]), inline=True)
    content = f"**{s.get('libraryName', 'Kavita')}:** {s.get('name', '')} tiene nuevo contenido en Kavita."
    return embed, content


# ─── posting ─────────────────────────────────────────────────────────────────

async def _send(channel: discord.TextChannel, embed: discord.Embed, series_id: int, content: str = None) -> None:
    cover = await asyncio.to_thread(_get_cover, series_id)
    if cover:
        f = discord.File(io.BytesIO(cover), filename="cover.jpg")
        embed.set_thumbnail(url="attachment://cover.jpg")
        await channel.send(content=content, file=f, embed=embed)
    else:
        await channel.send(content=content, embed=embed)


_BATCH_THRESHOLD = 3


async def _send_batch(channel: discord.TextChannel, items: list[dict], kind: str) -> None:
    """Send a single summary embed when there are more than _BATCH_THRESHOLD items."""
    icon  = "📚" if kind == "series" else "📖"
    label = f"{len(items)} nuevas series en Kavita" if kind == "series" else f"{len(items)} series actualizadas en Kavita"

    by_lib: dict[str, list] = {}
    for item in items:
        by_lib.setdefault(item.get("libraryName", "—"), []).append(item)

    color = _lib_color(items[0].get("libraryName", "")) if len(by_lib) == 1 else 0x95A5A6
    embed = discord.Embed(title=f"{icon} {label}", color=color)

    for lib_name, lib_items in by_lib.items():
        lines = [f"• [{i.get('name', '?')}]({_series_url(i['id'], i.get('libraryId', 0))})" for i in lib_items]
        embed.add_field(name=lib_name, value="\n".join(lines), inline=False)

    await channel.send(embed=embed)


async def _post_all(
    channel: discord.TextChannel,
    series: list[dict],
    chapters: list[dict],
) -> None:
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
                await _send(channel, embed, s["id"], content=content)
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
                await _send(channel, embed, c.get("id", 0), content=content)
                _seen["chapters"].append(_chapter_key(c))
            except Exception as e:
                log.error("[Kavita] chapter %s: %s", c.get("id"), e)

    _save()


# ─── public API ──────────────────────────────────────────────────────────────

async def run_poll(client: discord.Client) -> tuple[int, int]:
    """Run one poll cycle. Returns (new_series_count, new_chapters_count)."""
    channel = client.get_channel(_CHANNEL)
    if not channel:
        log.warning("[Kavita] Channel %s not found.", _CHANNEL)
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

    if not (_URL and (_API_KEY or (_USER and _PASS)) and _CHANNEL):
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
    log.info("[Kavita] Poller started (interval: %d min, channel: %s).", _INTERVAL, _CHANNEL)
    return True
