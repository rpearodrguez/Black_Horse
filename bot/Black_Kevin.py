import ast as _ast
import random
import asyncio
import datetime
import discord
from discord import app_commands
import operator as _op
from zoneinfo import ZoneInfo
import data as D
import Scrapper
import Roleplay
import Feels
import BotConfig
import kavita
import os
import json
import logging
from collections import deque

'''
Bot para Stick Horse
Version 3.1.0 - Slash Commands (app_commands) + BotConfig
Autor: Richard Pena (Vaalus)
Sin Message Content Intent.
'''

ADMIN_ID = int(os.environ.get('ADMIN_ID', 0))

_RESURRECCION = datetime.date(2026, 6, 18)


def _lore_footer() -> str:
    dias = (datetime.date.today() - _RESURRECCION).days
    return f'\u2620\ufe0f 7/9/2025  \u2728 18/6/2026  \u00b7  D\u00eda {dias}'


_OrigEmbed = discord.Embed


class _BotEmbed(_OrigEmbed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_footer(text=_lore_footer())


discord.Embed = _BotEmbed


# Buffer de logs en memoria
_log_buffer: deque[str] = deque(maxlen=50)

class _BufferHandler(logging.Handler):
    def emit(self, record):
        _log_buffer.append(self.format(record))

class _AnsiFormatter(logging.Formatter):
    _C = {'DEBUG': '[36m', 'INFO': '[32m', 'WARNING': '[33m', 'ERROR': '[31m', 'CRITICAL': '[35m'}
    _RST = '[0m'; _DIM = '[2;37m'
    def format(self, record):
        t = self.formatTime(record, self.datefmt)
        c = self._C.get(record.levelname, '')
        return f"{self._DIM}{t}{self._RST} {c}[{record.levelname}]{self._RST} {record.name}: {record.getMessage()}"

_fmt = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s', datefmt='%H:%M:%S')
_buf_handler = _BufferHandler()
_buf_handler.setFormatter(_AnsiFormatter(datefmt='%H:%M:%S'))

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s', datefmt='%H:%M:%S')
logging.getLogger('discord').addHandler(_buf_handler)
logging.getLogger('discord').setLevel(logging.WARNING)
logging.getLogger('kavita').addHandler(_buf_handler)

logger = logging.getLogger('bot')
logger.addHandler(_buf_handler)
logging.getLogger('kavita').addHandler(_buf_handler)

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    await tree.sync()
    logger.info(f'Bot conectado como {client.user} (id: {client.user.id})')
    logger.info(f'Activo en {len(client.guilds)} servidor(es):')
    for guild in client.guilds:
        logger.info(f'  [{guild.id}] {guild.name} — {guild.member_count} miembros')
    logger.info('Slash commands sincronizados.')
    kavita.setup_kavita_poller(client)


# ──────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────

def _embed(titulo: str, imagen: str, footer: str = "Via Giphy") -> discord.Embed:
    embed = discord.Embed(title=titulo)
    embed.set_image(url=imagen)
    embed.set_footer(text=footer)
    return embed


async def _check_module(interaction: discord.Interaction, modulo: str) -> bool:
    if not BotConfig.module_enabled(interaction.guild_id, modulo):
        await interaction.response.send_message(BotConfig.t(interaction.guild_id, "modulo_desactivado"), ephemeral=True)
        return False
    return True


def _is_bot_admin(interaction: discord.Interaction) -> bool:
    """Solo el propietario del bot (ADMIN_ID)."""
    return interaction.user.id == ADMIN_ID


def _is_server_admin(interaction: discord.Interaction) -> bool:
    """ADMIN_ID, dueño del servidor, o cualquier miembro con Gestionar servidor."""
    if interaction.user.id == ADMIN_ID:
        return True
    if not interaction.guild:
        return False
    if interaction.guild.owner_id == interaction.user.id:
        return True
    return interaction.user.guild_permissions.manage_guild


# ──────────────────────────────────────────────
# ADMIN
# ──────────────────────────────────────────────

@tree.command(name="servers", description="Lista los servidores donde esta activo el bot")
async def servers_cmd(interaction: discord.Interaction):
    if not _is_bot_admin(interaction):
        await interaction.response.send_message(BotConfig.t(interaction.guild_id, "solo_bot_admin"), ephemeral=True)
        return
    lines = [f"Bot activo en **{len(client.guilds)}** servidor(es):\n"]
    for guild in client.guilds:
        lines.append(f"• **{guild.name}** — {guild.member_count} miembros (id: `{guild.id}`)")
    await interaction.response.send_message("\n".join(lines), ephemeral=True)


@tree.command(name="logs", description="Muestra los ultimos logs del bot (solo admin)")
async def logs_cmd(interaction: discord.Interaction):
    if not _is_bot_admin(interaction):
        await interaction.response.send_message(BotConfig.t(interaction.guild_id, "solo_bot_admin"), ephemeral=True)
        return
    if not _log_buffer:
        await interaction.response.send_message(BotConfig.t(interaction.guild_id, "no_logs"), ephemeral=True)
        return
    texto = "\n".join(list(_log_buffer)[-20:])
    await interaction.response.send_message(f"```ansi\n{texto[-1900:]}\n```", ephemeral=True)


@tree.command(name="sync", description="Sincroniza los slash commands con Discord (solo admin)")
async def sync_cmd(interaction: discord.Interaction):
    if not _is_bot_admin(interaction):
        await interaction.response.send_message(BotConfig.t(interaction.guild_id, "solo_bot_admin"), ephemeral=True)
        return
    await interaction.response.defer(ephemeral=True)
    await tree.sync()
    await interaction.followup.send(BotConfig.t(interaction.guild_id, "sync_ok"), ephemeral=True)


# ── /kavita ────────────────────────────────────

kavita_group = app_commands.Group(name="kavita", description="Control del poller de Kavita (solo admin)")
tree.add_command(kavita_group)


@kavita_group.command(name="check", description="Fuerza un ciclo de polling ahora")
async def kavita_check_cmd(interaction: discord.Interaction):
    if not _is_bot_admin(interaction):
        await interaction.response.send_message("Solo el admin del bot puede usar este comando.", ephemeral=True)
        return
    await interaction.response.defer(ephemeral=True)
    n_series, n_chapters = await kavita.run_poll(client)
    if n_series == 0 and n_chapters == 0:
        await interaction.followup.send("Sin novedades (o poller no configurado).", ephemeral=True)
    else:
        await interaction.followup.send(
            f"✅ Posteado: **{n_series}** serie(s) nueva(s), **{n_chapters}** capítulo(s) nuevo(s).",
            ephemeral=True,
        )


@kavita_group.command(name="reset", description="Limpia el cache de vistos (el siguiente check re-anuncia todo)")
async def kavita_reset_cmd(interaction: discord.Interaction):
    if not _is_bot_admin(interaction):
        await interaction.response.send_message("Solo el admin del bot puede usar este comando.", ephemeral=True)
        return
    kavita.reset_seen()
    await interaction.response.send_message("🗑️ Cache de Kavita borrado. El próximo ciclo comenzará desde cero.", ephemeral=True)


@kavita_group.command(name="status", description="Muestra el estado del poller de Kavita")
async def kavita_status_cmd(interaction: discord.Interaction):
    if not _is_bot_admin(interaction):
        await interaction.response.send_message("Solo el admin del bot puede usar este comando.", ephemeral=True)
        return
    enabled   = bool(kavita._poll_task and kavita._poll_task.is_running())
    init      = kavita._seen.get("initialized", False)
    last_poll = kavita._seen.get("last_poll_time") or "—"
    url       = kavita._URL or "—"
    ch        = kavita._seen.get("channel_id") or "—"
    interval  = kavita._INTERVAL

    embed = discord.Embed(title="Kavita Poller", color=0x2ECC71 if enabled else 0xE74C3C)
    embed.add_field(name="Estado",       value="✅ Activo" if enabled else "❌ Inactivo", inline=True)
    embed.add_field(name="Intervalo",    value=f"{interval} min", inline=True)
    embed.add_field(name="Canal",        value=f"<#{ch}>" if ch != "—" else "—", inline=True)
    embed.add_field(name="Servidor",     value=url, inline=False)
    embed.add_field(name="Inicializado", value="Sí" if init else "No (próximo ciclo hace snapshot)", inline=True)
    embed.add_field(name="Último poll",  value=last_poll[:19].replace("T", " ") + " UTC" if last_poll != "—" else "—", inline=True)
    await interaction.response.send_message(embed=embed, ephemeral=True)


@kavita_group.command(name="series", description="Lista las series agregadas recientemente en Kavita")
@app_commands.describe(cantidad="Cuántas series mostrar (default: 15, máx: 30)")
async def kavita_series_cmd(interaction: discord.Interaction, cantidad: int = 15):
    if not _is_bot_admin(interaction):
        await interaction.response.send_message("Solo el admin del bot puede usar este comando.", ephemeral=True)
        return
    await interaction.response.defer(ephemeral=True)
    cantidad = max(1, min(cantidad, 30))
    series = await asyncio.to_thread(kavita.fetch_recent_series, cantidad)
    if not series:
        await interaction.followup.send("No se encontraron series.", ephemeral=True)
        return
    lines = []
    for s in series:
        name    = s.get("name", "?")
        lib     = s.get("libraryName", "—")
        created = s.get("created", "")
        ts      = ""
        if created:
            try:
                import datetime as _dt
                dt = _dt.datetime.fromisoformat(created.replace("Z", "+00:00"))
                ts = f" · <t:{int(dt.timestamp())}:f>"
            except Exception:
                pass
        lines.append(f"• **{name}** ({lib}){ts}")
    desc = "\n".join(lines)
    if len(desc) > 4096:
        desc = desc[:4093] + "…"
    embed = discord.Embed(title=f"📚 {len(series)} series recientes en Kavita", description=desc, color=0x3498DB)
    await interaction.followup.send(embed=embed, ephemeral=True)


@kavita_group.command(name="canal", description="Establece el canal de notificaciones de Kavita")
@app_commands.describe(canal="Canal donde se publicarán las novedades")
async def kavita_canal_cmd(interaction: discord.Interaction, canal: discord.TextChannel):
    if not _is_bot_admin(interaction):
        await interaction.response.send_message("Solo el admin del bot puede usar este comando.", ephemeral=True)
        return
    kavita.set_channel(canal.id)
    await interaction.response.send_message(f"✅ Canal de Kavita configurado: <#{canal.id}>", ephemeral=True)


# ── /lista ─────────────────────────────────────

_LISTAS_FILE = "listas.json"
_listas: dict = {}

def _listas_load() -> None:
    global _listas
    try:
        if os.path.exists(_LISTAS_FILE):
            with open(_LISTAS_FILE, encoding="utf-8") as f:
                _listas = json.load(f)
    except Exception:
        _listas = {}

def _listas_save() -> None:
    try:
        with open(_LISTAS_FILE, "w", encoding="utf-8") as f:
            json.dump(_listas, f, ensure_ascii=False)
    except Exception:
        pass

def _guild_listas(guild_id: int) -> dict:
    return _listas.setdefault(str(guild_id), {})

def _lista_access(interaction: discord.Interaction, nombre: str) -> bool:
    lista = _guild_listas(interaction.guild_id).get(nombre)
    if not lista:
        return False
    rol_id = lista.get("rol_id")
    if not rol_id:
        return True
    if interaction.user.guild_permissions.manage_guild:
        return True
    return any(r.id == rol_id for r in interaction.user.roles)

_listas_load()

lista_group = app_commands.Group(name="lista", description="Listas colaborativas por rol")
tree.add_command(lista_group)

async def _lista_autocomplete(interaction: discord.Interaction, current: str):
    nombres = list(_guild_listas(interaction.guild_id).keys())
    return [app_commands.Choice(name=n, value=n) for n in nombres if current.lower() in n.lower()][:25]

@lista_group.command(name="crear", description="Crea una nueva lista (solo admins del servidor)")
@app_commands.describe(nombre="Nombre de la lista", rol="Rol que puede ver y editar la lista")
async def lista_crear_cmd(interaction: discord.Interaction, nombre: str, rol: discord.Role = None):
    if not interaction.user.guild_permissions.manage_guild:
        await interaction.response.send_message("Solo los admins del servidor pueden crear listas.", ephemeral=True)
        return
    gl = _guild_listas(interaction.guild_id)
    if nombre in gl:
        await interaction.response.send_message(f"Ya existe una lista llamada **{nombre}**.", ephemeral=True)
        return
    gl[nombre] = {"rol_id": rol.id if rol else None, "items": []}
    _listas_save()
    rol_txt = f"Rol: {rol.mention}" if rol else "Sin restricción de rol (acceso público)"
    await interaction.response.send_message(f"✅ Lista **{nombre}** creada. {rol_txt}", ephemeral=True)

@lista_group.command(name="rol", description="Cambia el rol de acceso de una lista (solo admins)")
@app_commands.describe(nombre="Nombre de la lista", rol="Nuevo rol (vacío = sin restricción)")
@app_commands.autocomplete(nombre=_lista_autocomplete)
async def lista_rol_cmd(interaction: discord.Interaction, nombre: str, rol: discord.Role = None):
    if not interaction.user.guild_permissions.manage_guild:
        await interaction.response.send_message("Solo los admins del servidor pueden configurar roles.", ephemeral=True)
        return
    gl = _guild_listas(interaction.guild_id)
    if nombre not in gl:
        await interaction.response.send_message(f"No existe una lista llamada **{nombre}**.", ephemeral=True)
        return
    gl[nombre]["rol_id"] = rol.id if rol else None
    _listas_save()
    rol_txt = rol.mention if rol else "sin restricción"
    await interaction.response.send_message(f"✅ Rol de **{nombre}** cambiado a {rol_txt}.", ephemeral=True)

@lista_group.command(name="agregar", description="Agrega un item a la lista")
@app_commands.describe(nombre="Nombre de la lista", item="Qué quieres agregar", enlace="URL opcional (ej: link de Steam)")
@app_commands.autocomplete(nombre=_lista_autocomplete)
async def lista_agregar_cmd(interaction: discord.Interaction, nombre: str, item: str, enlace: str = None):
    if not _lista_access(interaction, nombre):
        await interaction.response.send_message("No tienes acceso a esta lista o no existe.", ephemeral=True)
        return
    gl = _guild_listas(interaction.guild_id)
    gl[nombre]["items"].append({
        "texto": item,
        "url": enlace or "",
        "autor": interaction.user.display_name,
        "fecha": str(datetime.date.today()),
    })
    _listas_save()
    total = len(gl[nombre]["items"])
    await interaction.response.send_message(f"✅ **{item}** agregado a **{nombre}** (#{total}).", ephemeral=True)

@lista_group.command(name="ver", description="Muestra el contenido de una lista")
@app_commands.describe(nombre="Nombre de la lista")
@app_commands.autocomplete(nombre=_lista_autocomplete)
async def lista_ver_cmd(interaction: discord.Interaction, nombre: str):
    if not _lista_access(interaction, nombre):
        await interaction.response.send_message("No tienes acceso a esta lista o no existe.", ephemeral=True)
        return
    items = _guild_listas(interaction.guild_id)[nombre]["items"]
    if not items:
        await interaction.response.send_message(f"La lista **{nombre}** está vacía.", ephemeral=True)
        return
    def _fmt(i, it):
        texto = f"[{it['texto']}]({it['url']})" if it.get("url") else it["texto"]
        return f"`{i}.` {texto}  — *{it['autor']}*"
    lineas = [_fmt(i, it) for i, it in enumerate(items, 1)]
    embed = discord.Embed(title=f"📋 {nombre}", description="\n".join(lineas), color=0x5865F2)
    embed.set_footer(text=f"{len(items)} item(s)")
    await interaction.response.send_message(embed=embed)

@lista_group.command(name="quitar", description="Quita un item de la lista por número")
@app_commands.describe(nombre="Nombre de la lista", numero="Número del item a quitar")
@app_commands.autocomplete(nombre=_lista_autocomplete)
async def lista_quitar_cmd(interaction: discord.Interaction, nombre: str, numero: int):
    if not _lista_access(interaction, nombre):
        await interaction.response.send_message("No tienes acceso a esta lista o no existe.", ephemeral=True)
        return
    items = _guild_listas(interaction.guild_id)[nombre]["items"]
    if numero < 1 or numero > len(items):
        await interaction.response.send_message(f"Número inválido. La lista tiene {len(items)} item(s).", ephemeral=True)
        return
    removed = items.pop(numero - 1)
    _listas_save()
    await interaction.response.send_message(f"🗑️ **{removed['texto']}** quitado de **{nombre}**.", ephemeral=True)

@lista_group.command(name="borrar", description="Elimina una lista completa (solo admins)")
@app_commands.describe(nombre="Nombre de la lista a eliminar")
@app_commands.autocomplete(nombre=_lista_autocomplete)
async def lista_borrar_cmd(interaction: discord.Interaction, nombre: str):
    if not interaction.user.guild_permissions.manage_guild:
        await interaction.response.send_message("Solo los admins del servidor pueden borrar listas.", ephemeral=True)
        return
    gl = _guild_listas(interaction.guild_id)
    if nombre not in gl:
        await interaction.response.send_message(f"No existe una lista llamada **{nombre}**.", ephemeral=True)
        return
    del gl[nombre]
    _listas_save()
    await interaction.response.send_message(f"🗑️ Lista **{nombre}** eliminada.", ephemeral=True)


# ── /config ─────────────────────────────────────

config_group = app_commands.Group(name="config", description="Configuracion del bot (solo admin)")
tree.add_command(config_group)


@config_group.command(name="idioma", description="Cambia el idioma en que responde el bot")
@app_commands.describe(idioma="Idioma del bot")
@app_commands.choices(idioma=[
    app_commands.Choice(name="Espanol", value="es"),
    app_commands.Choice(name="English", value="en"),
])
async def config_idioma_cmd(interaction: discord.Interaction, idioma: app_commands.Choice[str]):
    if not _is_server_admin(interaction):
        await interaction.response.send_message(BotConfig.t(interaction.guild_id, "solo_server_admin"), ephemeral=True)
        return
    BotConfig.set_language(interaction.guild_id, idioma.value)
    await interaction.response.send_message(BotConfig.t(interaction.guild_id, "config_idioma_ok", lang=idioma.name), ephemeral=True)


@config_group.command(name="modulo", description="Activa o desactiva un modulo de comandos")
@app_commands.describe(modulo="Modulo a configurar", estado="Activar o desactivar")
@app_commands.choices(
    modulo=[app_commands.Choice(name=m, value=m) for m in BotConfig.MODULES],
    estado=[
        app_commands.Choice(name="activar", value="on"),
        app_commands.Choice(name="desactivar", value="off"),
    ],
)
async def config_modulo_cmd(interaction: discord.Interaction,
                             modulo: app_commands.Choice[str],
                             estado: app_commands.Choice[str]):
    if not _is_server_admin(interaction):
        await interaction.response.send_message(BotConfig.t(interaction.guild_id, "solo_server_admin"), ephemeral=True)
        return
    enabled = estado.value == "on"
    BotConfig.set_module(interaction.guild_id, modulo.value, enabled)
    estado_str = BotConfig.t(interaction.guild_id, "config_modulo_on" if enabled else "config_modulo_off")
    await interaction.response.send_message(
        BotConfig.t(interaction.guild_id, "config_modulo_ok", modulo=modulo.value, estado=estado_str), ephemeral=True
    )


@config_group.command(name="estado", description="Muestra la configuracion actual del bot")
async def config_estado_cmd(interaction: discord.Interaction):
    if not _is_server_admin(interaction):
        await interaction.response.send_message(BotConfig.t(interaction.guild_id, "solo_server_admin"), ephemeral=True)
        return
    modulos = BotConfig.get_modules(interaction.guild_id)
    modulos_str = "\n".join(f"{'✅' if v else '❌'} `{k}`" for k, v in modulos.items())
    embed = discord.Embed(title=BotConfig.t(interaction.guild_id, "config_estado_titulo"), color=0x5865F2)
    embed.add_field(name=BotConfig.t(interaction.guild_id, "config_idioma_label"), value=f"`{BotConfig.get_language(interaction.guild_id)}`", inline=True)
    embed.add_field(name=BotConfig.t(interaction.guild_id, "config_modulos_label"), value=modulos_str, inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)


# ──────────────────────────────────────────────
# GENERAL
# ──────────────────────────────────────────────

@tree.command(name="help", description="Muestra la lista de comandos disponibles")
async def help_cmd(interaction: discord.Interaction):
    if not await _check_module(interaction, "general"): return
    embed = discord.Embed(title="Kevin, la deidad primordial", description="Comandos disponibles")
    embed.add_field(name="General", inline=False, value=(
        "`/hola` Saluda al bot\n"
        "`/jueves` ¿Hoy es jueves?\n"
        "`/say` El bot repite tu mensaje\n"
        "`/epitafio` El epitafio de la Bruja Dorada\n"
        "`/invite` Invita al bot a tu servidor"
    ))
    embed.add_field(name="Utilidades", inline=False, value=(
        "`/diccionario` Busca una palabra en el diccionario de la RAE\n"
        "`/hora` Hora actual en distintas zonas horarias\n"
        "`/calcular` Evalua una expresion matematica directamente\n"
        "`/calc` Calculadora interactiva con botones"
    ))
    embed.add_field(name="Entretenimiento", inline=False, value=(
        "`/anime` Informacion de un anime\n"
        "`/manga` Informacion de un manga\n"
        "`/steam` Informacion de un juego en Steam\n"
        "`/img` Busca una imagen (solo canales SFW)\n"
        "`/cc` Meme aleatorio de CuantoCabron\n"
        "`/scp` Entrada de la SCP Foundation Wiki\n"
        "`/convert` Conversion de divisas\n"
                "`/pokemon` Info de un Pokemon (nombre, numero o 'random')\n"
        "`/poketype` Pokemon aleatorio de un tipo (con autocompletado)\n"
        "`/vn` Informacion de una novela visual (VNDB)\n"
        "`/horoscopo` Horoscopo del dia\n"
        "`/personaje` Informacion de un personaje de anime\n"
        "`/pelicula` Informacion de una pelicula (IMDb)\n"
        "`/receta` Receta de cocina\n"
        "`/caracola` Consulta a la Caracola Magica"
    ))
    embed.add_field(name="Juegos", inline=False, value=(
                "`/gato` Tic-tac-toe — vs otro usuario o vs el bot\n"
        "`/ppt` Piedra Papel Tijeras — vs otro usuario o vs el bot\n"
        "`/trivia` Pregunta de trivia con 4 opciones (13 categorias)\n"
        "`/dungeon` Dungeon crawler de 3 niveles\n"
        "`/ahorcado` Adivina la palabra letra por letra\n"
        "`/dosmil` 2048 — combina fichas hasta llegar a 2048\n"
        "`/buscaminas` Buscaminas 5x5 — no pises las minas"
    ))
    embed.add_field(name="Roleplay", inline=False, value=(
        "`/roll` Tira dados estandar (ej: `/roll 2 20 3` = 2d20+3)\n"
        "`/fate` Tira dados Fate dF"
    ))
    embed.add_field(name="Reacciones — sobre otros", inline=False, value=(
        "`/escobazo` `/pat` `/slap` `/lick` `/feed` `/kick` `/baka` `/bite`"
    ))
    embed.add_field(name="Reacciones — propias", inline=False, value=(
        "`/smug` `/pout` `/plaf` `/spin` `/blush` `/shy` `/tsundere` `/lewd` `/jojo` `/cry` `/smile` `/suicide`"
    ))
    embed.add_field(name="Reacciones — duales (usuario opcional)", inline=False, value=(
        "`/resucitar` `/hug` `/kiss` `/dance` `/angry` `/run` `/sleep` `/happy` `/cookie` `/escupefuego`"
    ))
    if interaction.channel.is_nsfw():
        embed.add_field(name="NSFW", inline=False, value=(
            "`/patas` `/piernas` Imagenes de safebooru\n"
            "`/safebooru` Busqueda personalizada en safebooru\n"
            "`/danbooru` Busqueda en danbooru\n"
            "`/hanime` Busca en hentai-id"
        ))
    if _is_server_admin(interaction):
        embed.add_field(name=BotConfig.t(interaction.guild_id, "help_config_titulo"), inline=False, value=(
            f"`/config idioma` {BotConfig.t(interaction.guild_id, 'help_config_idioma')}\n"
            f"`/config modulo` {BotConfig.t(interaction.guild_id, 'help_config_modulo')}\n"
            f"`/config estado` {BotConfig.t(interaction.guild_id, 'help_config_estado')}"
        ))
    if _is_bot_admin(interaction):
        embed.add_field(name=BotConfig.t(interaction.guild_id, "help_bot_admin_titulo"), inline=False, value=(
            f"`/servers` {BotConfig.t(interaction.guild_id, 'help_bot_servers')}\n"
            f"`/logs` {BotConfig.t(interaction.guild_id, 'help_bot_logs')}\n"
            f"`/sync` {BotConfig.t(interaction.guild_id, 'help_bot_sync')}"
        ))
    await interaction.response.send_message(embed=embed)


@tree.command(name="invite", description="Obtén el link para invitar al bot a tu servidor")
async def invite_cmd(interaction: discord.Interaction):
    if not await _check_module(interaction, "general"): return
    await interaction.response.send_message(
        "https://discord.com/api/oauth2/authorize?client_id=558102665695985674&permissions=92160&scope=bot+applications.commands"
    )


@tree.command(name="hola", description="Saluda al bot")
async def hola_cmd(interaction: discord.Interaction):
    if not await _check_module(interaction, "general"): return
    await interaction.response.send_message(BotConfig.t(interaction.guild_id, "hola"))


@tree.command(name="twitter", description="Muestra el contenido de un tweet en Discord (videos, imagenes, etc)")
@app_commands.describe(url="Link del tweet")
async def twitter_cmd(interaction: discord.Interaction, url: str):
    if not await _check_module(interaction, "general"): return
    fixed = (url
        .replace("https://twitter.com", "https://fxtwitter.com")
        .replace("https://x.com", "https://fxtwitter.com")
        .replace("http://twitter.com", "https://fxtwitter.com")
        .replace("http://x.com", "https://fxtwitter.com")
    )
    if fixed == url:
        await interaction.response.send_message(BotConfig.t(interaction.guild_id, "link_invalido"), ephemeral=True)
        return
    await interaction.response.send_message(BotConfig.t(interaction.guild_id, "twitter_compartio", user=interaction.user.display_name, url=fixed))


@tree.command(name="celacanto", description="Un celacanto aparece")
async def celacanto_cmd(interaction: discord.Interaction):
    if not await _check_module(interaction, "general"): return
    await interaction.response.send_message(BotConfig.t(interaction.guild_id, "celacanto", user=interaction.user.display_name))


@tree.command(name="epitafio", description="El epitafio de la Bruja Dorada")
async def epitafio_cmd(interaction: discord.Interaction):
    if not await _check_module(interaction, "general"): return
    embed = discord.Embed(title="Epitafio de la Bruja Dorada", color=0xFFD700)
    embed.add_field(name="​", inline=False, value=(
        "*Elogia mi nombre, reverencia a la Tierra Dorada.\n"
        "Mi amada tierra natal, resucitada por la llave del oro.*"
    ))
    embed.add_field(name="​", inline=False, value=(
        "En el primer crepusculo, ofrece a los seis elegidos por la llave.\n"
        "En el segundo crepusculo, los dos que estan cerca seran separados.\n"
        "En el tercer crepusculo, los dos que estan cerca seran alabados.\n"
        "En el cuarto crepusculo, perfora la cabeza y mata.\n"
        "En el quinto crepusculo, perfora el pecho y mata.\n"
        "En el sexto crepusculo, perfora el estomago y mata.\n"
        "En el septimo crepusculo, perfora las rodillas y mata.\n"
        "En el octavo crepusculo, perfora los pies y mata.\n"
        "En el noveno crepusculo, la bruja revivira y no quedara nadie.\n"
        "En el decimo crepusculo, el viaje terminara y llegaras a la Tierra Dorada."
    ))
    embed.add_field(name="​", inline=False, value=(
        "La bruja elogiara al sabio y le otorgara cuatro tesoros.\n"
        "Uno sera todo el oro de la Tierra Dorada.\n"
        "Uno sera la resurreccion de las almas de todos los muertos.\n"
        "Uno sera la realizacion de un milagro que es imposible.\n"
        "Uno sera poner a la bruja a dormir por toda la eternidad."
    ))
    embed.set_footer(text="Duerme en paz, mi mas amada bruja, Beatrice.")
    await interaction.response.send_message(embed=embed)


@tree.command(name="jueves", description="¿Hoy es jueves?")
async def jueves_cmd(interaction: discord.Interaction):
    if not await _check_module(interaction, "general"): return
    if datetime.datetime.today().weekday() == 3:
        embed = discord.Embed(title=BotConfig.t(interaction.guild_id, "jueves_si"), description=BotConfig.t(interaction.guild_id, "jueves_si_desc"))
        embed.set_image(url="https://c.tenor.com/-W6QXc36TfQAAAAd/asuka-eva.gif")
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(BotConfig.t(interaction.guild_id, "jueves_no"))



@tree.command(name="say", description="Hace que el bot repita un mensaje")
@app_commands.describe(mensaje="El mensaje a repetir")
async def say_cmd(interaction: discord.Interaction, mensaje: str):
    if not await _check_module(interaction, "general"): return
    await interaction.response.send_message(mensaje)


async def _hora_autocomplete(interaction: discord.Interaction, current: str) -> list:
    lang = BotConfig.get_language(interaction.guild_id)
    idx = 0 if lang == "es" else 1
    return [
        app_commands.Choice(name=f"{tz[3]} {tz[idx]}", value=tz[2])
        for tz in D.TIMEZONES
        if current.lower() in tz[0].lower() or current.lower() in tz[1].lower()
    ][:25]


@tree.command(name="hora", description="Hora actual en el mundo")
@app_commands.describe(zona="Ciudad (opcional — autocompletado disponible)")
@app_commands.autocomplete(zona=_hora_autocomplete)
async def hora_cmd(interaction: discord.Interaction, zona: str = None):
    if not await _check_module(interaction, "utilidades"): return
    lang = BotConfig.get_language(interaction.guild_id)
    days = D.DAYS[lang]
    now_utc = datetime.datetime.now(datetime.timezone.utc)

    if zona:
        try:
            tz = ZoneInfo(zona)
        except Exception:
            await interaction.response.send_message(BotConfig.t(interaction.guild_id, "sin_resultados"), ephemeral=True)
            return
        now = now_utc.astimezone(tz)
        offset_secs = now.utcoffset().total_seconds()
        offset_h = int(offset_secs // 3600)
        offset_m = int((abs(offset_secs) % 3600) // 60)
        offset_str = f"UTC{'+' if offset_h >= 0 else ''}{offset_h}" + (f":{offset_m:02d}" if offset_m else "")
        entry = next((t for t in D.TIMEZONES if t[2] == zona), None)
        flag = entry[3] if entry else "🌐"
        city = entry[0 if lang == "es" else 1] if entry else zona
        embed = discord.Embed(title=f"{flag} {city} — {now.strftime('%H:%M')}", color=0x2F81C7)
        embed.add_field(name=BotConfig.t(interaction.guild_id, "hora_fecha"),
                        value=f"{now.strftime('%d/%m/%Y')} ({days[now.weekday()]})", inline=True)
        embed.add_field(name="UTC", value=offset_str, inline=True)
        await interaction.response.send_message(embed=embed)
    else:
        main = D.TIMEZONES[:D.HORA_MAIN]
        lines = []
        for es_name, en_name, tz_id, flag in main:
            now = now_utc.astimezone(ZoneInfo(tz_id))
            city = es_name if lang == "es" else en_name
            lines.append(f"{flag} **{city}** — {now.strftime('%H:%M')} ({days[now.weekday()]})")
        embed = discord.Embed(
            title=BotConfig.t(interaction.guild_id, "hora_titulo"),
            description="\n".join(lines),
            color=0x2F81C7,
        )
        embed.set_footer(text=f"UTC {now_utc.strftime('%H:%M')}")
        await interaction.response.send_message(embed=embed)


@tree.command(name="calc", description="Calculadora interactiva")
async def calc_cmd(interaction: discord.Interaction):
    if not await _check_module(interaction, "utilidades"): return
    view = _Calculator()
    await interaction.response.send_message(embed=view._build_embed(), view=view)


@tree.command(name="gato", description="Juega al gato (tic-tac-toe)")
@app_commands.describe(oponente="Usuario con quien jugar (opcional — sin @usuario juegas contra el bot)")
async def gato_cmd(interaction: discord.Interaction, oponente: discord.Member = None):
    if not await _check_module(interaction, "entretenimiento"): return
    if oponente is not None:
        if oponente.id == interaction.user.id:
            await interaction.response.send_message(
                BotConfig.t(interaction.guild_id, "gato_vs_si"), ephemeral=True)
            return
        if oponente.bot:
            await interaction.response.send_message(
                BotConfig.t(interaction.guild_id, "gato_vs_bot"), ephemeral=True)
            return
    view = _TicTacToe(interaction.user, oponente, interaction.guild_id)
    await interaction.response.send_message(embed=view._build_embed(), view=view)


async def _trivia_autocomplete(interaction: discord.Interaction, current: str):
    lang = BotConfig.get_language(interaction.guild_id)
    name_idx = 1 if lang == "es" else 2
    return [
        app_commands.Choice(name=cat[name_idx], value=str(cat[0]))
        for cat in D.TRIVIA_CATEGORIES
        if current.lower() in cat[1].lower() or current.lower() in cat[2].lower()
    ][:25]


@tree.command(name="trivia", description="Pregunta de trivia aleatoria")
@app_commands.describe(categoria="Categoría de la pregunta (opcional)")
@app_commands.autocomplete(categoria=_trivia_autocomplete)
async def trivia_cmd(interaction: discord.Interaction, categoria: str = None):
    if not await _check_module(interaction, "entretenimiento"): return
    await interaction.response.defer()
    cat_id = int(categoria) if categoria and categoria.isdigit() else None
    q = Scrapper.triviaQuestion(cat_id)
    if not q:
        await interaction.followup.send(BotConfig.t(interaction.guild_id, "sin_resultados"))
        return
    lang = BotConfig.get_language(interaction.guild_id)
    if lang == 'es':
        try:
            parts = [q['question'], q['correct']] + q['incorrect']
            joined = '\n||||\n'.join(parts)
            translated = Scrapper.translate(joined, dest='es')
            t_parts = translated.split('\n||||\n')
            if len(t_parts) == 5:
                q['question']  = t_parts[0]
                q['correct']   = t_parts[1]
                q['incorrect'] = t_parts[2:]
        except Exception as e:
            logger.warning(f'trivia_cmd translate error: {e}')
    view = _Trivia(q, interaction.guild_id)
    msg = await interaction.followup.send(embed=view._question_embed(lang), view=view)
    view.message = msg


@tree.command(name="dungeon", description="Dungeon crawler — explora, mata enemigos y sobrevive")
async def dungeon_cmd(interaction: discord.Interaction):
    if not await _check_module(interaction, "entretenimiento"): return
    view = _Dungeon(interaction.guild_id, interaction.user.id)
    await interaction.response.send_message(embed=view._build_embed(), view=view)
    view.message = await interaction.original_response()


@tree.command(name='ahorcado', description='Adivina la palabra letra por letra')
async def ahorcado_cmd(interaction: discord.Interaction):
    if not await _check_module(interaction, 'entretenimiento'): return
    view = _Hangman(interaction.guild_id, interaction.user.id)
    await interaction.response.send_message(embed=view._build_embed(), view=view)



@tree.command(name='dosmil', description='2048 — combina fichas hasta llegar a 2048')
async def dosmil_cmd(interaction: discord.Interaction):
    if not await _check_module(interaction, 'entretenimiento'): return
    view = _Game2048(interaction.guild_id, interaction.user.id)
    await interaction.response.send_message(embed=view._build_embed(), view=view)
    view.message = await interaction.original_response()


@tree.command(name='calcular', description='Evalua una expresion matematica')
@app_commands.describe(expresion='Expresion a calcular (ej: 2+2, 10/3, (5+3)*2, 2**8)')
async def calcular_cmd(interaction: discord.Interaction, expresion: str):
    if not await _check_module(interaction, 'utilidades'): return
    if len(expresion) > 200:
        await interaction.response.send_message('Expresion demasiado larga.', ephemeral=True)
        return
    expr = expresion.replace('×', '*').replace('÷', '/').replace('−', '-')
    result = _calc_eval(expr)
    color = 0xE74C3C if result.startswith('Error') else 0x57F287
    embed = discord.Embed(title='Calculadora', color=color)
    embed.add_field(name='Expresion', value='`' + expresion + '`', inline=False)
    embed.add_field(name='Resultado', value='`' + result + '`', inline=False)
    await interaction.response.send_message(embed=embed)


@tree.command(name='diccionario', description='Busca una palabra en el Diccionario de la RAE')
@app_commands.describe(palabra='Palabra a buscar')
async def diccionario_cmd(interaction: discord.Interaction, palabra: str):
    if not await _check_module(interaction, 'utilidades'): return
    await interaction.response.defer()
    result = Scrapper.raeSearch(palabra)
    if not result:
        await interaction.followup.send(BotConfig.t(interaction.guild_id, 'sin_resultados'))
        return
    lang = BotConfig.get_language(interaction.guild_id)
    embed = discord.Embed(
        title=f'📖 {result["palabra"]}',
        color=0x2C3E50,
        url=result['url'],
    )
    desc = '\n\n'.join(result['definiciones'])
    if lang == 'en':
        label = 'Definitions (RAE — Spanish only)'
        embed.add_field(name=label, value=desc[:1024], inline=False)
    else:
        embed.description = desc[:4096]
    embed.set_footer(text='Fuente: Diccionario de la lengua espanola (RAE)')
    await interaction.followup.send(embed=embed)


@tree.command(name='ppt', description='Piedra, Papel o Tijeras')
@app_commands.describe(oponente='Usuario contra quien jugar (opcional — sin @usuario juegas contra el bot)')
async def ppt_cmd(interaction: discord.Interaction, oponente: discord.Member = None):
    if not await _check_module(interaction, 'entretenimiento'): return
    if oponente is not None:
        if oponente.id == interaction.user.id:
            await interaction.response.send_message(BotConfig.t(interaction.guild_id, 'gato_vs_si'), ephemeral=True)
            return
        if oponente.bot:
            await interaction.response.send_message(BotConfig.t(interaction.guild_id, 'gato_vs_bot'), ephemeral=True)
            return
    view = _RPS(interaction.user, oponente, interaction.guild_id)
    vs = oponente.mention if oponente else '🤖 Bot'
    embed = discord.Embed(title='🪨📄✂️ Piedra Papel Tijeras',
                          description=f'{interaction.user.mention} vs {vs}\nElige en secreto:',
                          color=0x3498DB)
    await interaction.response.send_message(embed=embed, view=view)
    view.message = await interaction.original_response()


@tree.command(name='buscaminas', description='Buscaminas 5×5 — no pises las minas')
async def buscaminas_cmd(interaction: discord.Interaction):
    if not await _check_module(interaction, 'entretenimiento'): return
    view = _Minesweeper(interaction.guild_id, interaction.user.id)
    await interaction.response.send_message(embed=view._build_embed(), view=view)
    view.message = await interaction.original_response()


# Horoscopo
async def _horoscopo_ac(interaction: discord.Interaction, current: str):
    lang = BotConfig.get_language(interaction.guild_id)
    choices = []
    for api, es, en, emoji in D.HOROSCOPE_SIGNS:
        label = f'{emoji} {es if lang == "es" else en}'
        if not current or current.lower() in label.lower() or current.lower() in api:
            choices.append(app_commands.Choice(name=label, value=api))
    return choices[:25]


@tree.command(name='horoscopo', description='Horoscopo del dia segun tu signo zodiacal')
@app_commands.describe(signo='Tu signo zodiacal')
@app_commands.autocomplete(signo=_horoscopo_ac)
async def horoscopo_cmd(interaction: discord.Interaction, signo: str):
    if not await _check_module(interaction, 'entretenimiento'): return
    await interaction.response.defer()
    result = Scrapper.horoscopoSearch(signo)
    if not result:
        await interaction.followup.send(BotConfig.t(interaction.guild_id, 'sin_resultados')); return
    lang = BotConfig.get_language(interaction.guild_id)
    info = next((s for s in D.HOROSCOPE_SIGNS if s[0] == signo), None)
    emoji = info[3] if info else '⭐'
    name  = info[1] if lang == 'es' else info[2] if info else signo.capitalize()
    text  = result['text']
    if lang == 'es':
        try: text = Scrapper.translate(text, dest='es')
        except Exception as e: logger.warning(f'horoscopo translate: {e}')
    embed = discord.Embed(title=f'{emoji} {name}', description=text, color=0x9B59B6)
    embed.set_footer(text=result['date'])
    await interaction.followup.send(embed=embed)


@tree.command(name='personaje', description='Informacion de un personaje de anime o manga')
@app_commands.describe(nombre='Nombre del personaje')
async def personaje_cmd(interaction: discord.Interaction, nombre: str):
    if not await _check_module(interaction, 'entretenimiento'): return
    await interaction.response.defer()
    result = Scrapper.personajeSearch(nombre)
    if not result:
        await interaction.followup.send(BotConfig.t(interaction.guild_id, 'sin_resultados')); return
    lang  = BotConfig.get_language(interaction.guild_id)
    title = result['name'] + (f' ({result["kanji"]})' if result['kanji'] else '')
    embed = discord.Embed(title=title, color=0xE74C3C, url=result['url'])
    if result['about']:
        desc = result['about']
        if lang == 'es':
            try: desc = Scrapper.translate(desc, dest='es')
            except Exception as e: logger.warning(f'personaje translate: {e}')
        embed.description = desc
    if result['anime']:
        label = 'Aparece en' if lang == 'es' else 'Appears in'
        embed.add_field(name=label, value='\n'.join(result['anime']), inline=False)
    embed.add_field(name='Favoritos' if lang == 'es' else 'Favorites',
                    value=f'❤️ {result["favs"]:,}', inline=True)
    if result['image']:
        embed.set_thumbnail(url=result['image'])
    await interaction.followup.send(embed=embed)


@tree.command(name='pelicula', description='Busca informacion de una pelicula (IMDb/OMDB)')
@app_commands.describe(titulo='Titulo de la pelicula')
async def pelicula_cmd(interaction: discord.Interaction, titulo: str):
    if not await _check_module(interaction, 'entretenimiento'): return
    await interaction.response.defer()
    result = Scrapper.peliculaSearch(titulo)
    if not result:
        await interaction.followup.send(BotConfig.t(interaction.guild_id, 'sin_resultados')); return
    lang  = BotConfig.get_language(interaction.guild_id)
    year  = f' ({result["year"]})' if result['year'] else ''
    embed = discord.Embed(title=f'🎬 {result["title"]}{year}', color=0xE67E22)
    if result['plot']:
        plot = result['plot']
        if lang == 'es':
            try: plot = Scrapper.translate(plot, dest='es')
            except Exception as e: logger.warning(f'pelicula translate: {e}')
        embed.description = plot
    if result['poster']:
        embed.set_thumbnail(url=result['poster'])
    if result['imdb']:
        embed.add_field(name='IMDb', value=f'⭐ {result["imdb"]}/10', inline=True)
    if result['runtime']:
        embed.add_field(name='Duracion' if lang == 'es' else 'Runtime', value=result['runtime'], inline=True)
    if result['genre']:
        embed.add_field(name='Genero' if lang == 'es' else 'Genre', value=result['genre'], inline=False)
    if result['director']:
        embed.add_field(name='Director', value=result['director'], inline=True)
    if result['actors']:
        embed.add_field(name='Reparto' if lang == 'es' else 'Cast', value=result['actors'], inline=False)
    await interaction.followup.send(embed=embed)


class _RecetaSelect(discord.ui.View):
    def __init__(self, resultados: list, guild_id: int):
        super().__init__(timeout=60)
        self.guild_id = guild_id
        lang = BotConfig.get_language(guild_id)
        ph = 'Elige una receta...' if lang == 'es' else 'Choose a recipe...'
        opts = [discord.SelectOption(label=r['title'][:100], value=str(r['id']))
                for r in resultados]
        sel = discord.ui.Select(placeholder=ph, options=opts)
        sel.callback = self._on_select
        self.add_item(sel)

    async def _on_select(self, interaction: discord.Interaction):
        await interaction.response.defer()
        recipe_id = int(interaction.data['values'][0])
        detail = Scrapper.spoonacularDetail(recipe_id)
        lang = BotConfig.get_language(interaction.guild_id)
        if not detail:
            await interaction.followup.send(
                BotConfig.t(interaction.guild_id, 'sin_resultados'), ephemeral=True)
            return
        embed = discord.Embed(title=f'\U0001f37d\ufe0f {detail["title"]}', color=0x2ECC71,
                              url=detail['url'] or None)
        if detail['image']:
            embed.set_thumbnail(url=detail['image'])
        if detail['readyIn']:
            embed.add_field(name='\u23f1\ufe0f',
                            value=f'{detail["readyIn"]} min', inline=True)
        if detail['servings']:
            label = 'Porciones' if lang == 'es' else 'Servings'
            embed.add_field(name=label, value=str(detail['servings']), inline=True)
        if detail['ingredients']:
            label = 'Ingredientes' if lang == 'es' else 'Ingredients'
            ings_display = Scrapper.translate_ingredients(detail['ingredients'], lang)
            embed.add_field(name=label,
                            value='\n'.join(f'\u2022 {i}' for i in ings_display)[:1024],
                            inline=False)
        if detail['instructions']:
            instr = detail['instructions']
            if lang == 'es':
                try: instr = Scrapper.translate(instr, dest='es')
                except Exception as e: logger.warning(f'receta translate: {e}')
            label = 'Instrucciones' if lang == 'es' else 'Instructions'
            embed.add_field(name=label, value=instr[:1000], inline=False)
        if detail['url']:
            label = '¿Dudas? Receta completa aquí' if lang == 'es' else 'Full recipe here'
            embed.add_field(name=label, value=detail['url'], inline=False)
        await interaction.message.edit(embed=embed, view=None)


@tree.command(name='receta', description='Busca recetas por ingrediente o nombre de plato')
@app_commands.describe(busqueda='Ingrediente o plato a buscar (funciona en espanol e ingles)')
async def receta_cmd(interaction: discord.Interaction, busqueda: str):
    if not await _check_module(interaction, 'entretenimiento'): return
    await interaction.response.defer()
    resultados = Scrapper.spoonacularSearch(busqueda)
    if not resultados:
        await interaction.followup.send(BotConfig.t(interaction.guild_id, 'sin_resultados'))
        return
    lang = BotConfig.get_language(interaction.guild_id)
    n = len(resultados)
    desc = (f'Se encontraron **{n}** recetas con ese ingrediente. Elige una:'
            if lang == 'es' else
            f'Found **{n}** recipes with that ingredient. Choose one:')
    embed = discord.Embed(title=f'\U0001f37d\ufe0f {busqueda.title()}',
                          description=desc, color=0x2ECC71)
    await interaction.followup.send(embed=embed, view=_RecetaSelect(resultados, interaction.guild_id))

@tree.command(name='caracola', description='Consulta a la Caracola Magica')
@app_commands.describe(pregunta='Tu pregunta para la Caracola Magica (opcional)')
async def caracola_cmd(interaction: discord.Interaction, pregunta: str = None):
    if not await _check_module(interaction, 'entretenimiento'): return
    lang = BotConfig.get_language(interaction.guild_id)
    pool = D.CARACOLA_ES if lang == 'es' else D.CARACOLA_EN
    respuesta = random.choice(pool)
    titulo = '🐚 La Caracola Magica' if lang == 'es' else '🐚 The Magic Conch'
    embed = discord.Embed(title=titulo, color=0x00B4D8)
    embed.set_thumbnail(url='https://static.wikia.nocookie.net/spongebob/images/e/e4/Magic_Conch_Shell.png/revision/latest?cb=20200602194627')
    if pregunta:
        label = 'Tu pregunta' if lang == 'es' else 'Your question'
        embed.add_field(name=label, value=f'*{pregunta}*', inline=False)
    label_r = 'La Caracola dice...' if lang == 'es' else 'The Conch says...'
    embed.add_field(name=label_r, value=f'**{respuesta}**', inline=False)
    await interaction.response.send_message(embed=embed)


# ──────────────────────────────────────────────
# NSFW
# ──────────────────────────────────────────────


@tree.command(name="patas", description="Imagen aleatoria de patas en safebooru (solo canales NSFW)")
async def patas_cmd(interaction: discord.Interaction):
    if not await _check_module(interaction, "nsfw"): return
    if not interaction.channel.is_nsfw():
        await interaction.response.send_message(BotConfig.t(interaction.guild_id, "solo_nsfw"), ephemeral=True)
        return
    await interaction.response.defer()
    busqueda = Scrapper.safebooruSearch("feet")
    if busqueda != "No se pudo encontrar resultado":
        embed = discord.Embed(title=BotConfig.t(interaction.guild_id, "resultado_imagen"), description="Cochinon")
        embed.set_image(url=busqueda)
        embed.set_footer(text="Creditos a safebooru.org")
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send(BotConfig.t(interaction.guild_id, "sin_resultado"))


@tree.command(name="piernas", description="Imagen aleatoria de piernas en safebooru (solo canales NSFW)")
async def piernas_cmd(interaction: discord.Interaction):
    if not await _check_module(interaction, "nsfw"): return
    if not interaction.channel.is_nsfw():
        await interaction.response.send_message(BotConfig.t(interaction.guild_id, "solo_nsfw"), ephemeral=True)
        return
    await interaction.response.defer()
    busqueda = Scrapper.safebooruSearch("thighs")
    if busqueda != "No se pudo encontrar resultado":
        embed = discord.Embed(title=BotConfig.t(interaction.guild_id, "resultado_imagen"), description="Piernas")
        embed.set_image(url=busqueda)
        embed.set_footer(text="Creditos a safebooru.org")
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send(BotConfig.t(interaction.guild_id, "sin_resultado"))


@tree.command(name="safebooru", description="Busca imagenes en safebooru (solo canales NSFW)")
@app_commands.describe(tags="Tags de busqueda separados por espacios")
async def safebooru_cmd(interaction: discord.Interaction, tags: str):
    if not await _check_module(interaction, "nsfw"): return
    if not interaction.channel.is_nsfw():
        await interaction.response.send_message(BotConfig.t(interaction.guild_id, "solo_nsfw"), ephemeral=True)
        return
    await interaction.response.defer()
    busqueda = Scrapper.safebooruSearch("+".join(tags.split()))
    if busqueda != "No se pudo encontrar resultado":
        embed = discord.Embed(title=BotConfig.t(interaction.guild_id, "busqueda"), description=tags)
        embed.set_image(url=busqueda)
        embed.set_footer(text="Creditos a safebooru.org")
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send(BotConfig.t(interaction.guild_id, "sin_resultado"))


@tree.command(name="danbooru", description="Busca imagenes en danbooru (solo canales NSFW)")
@app_commands.describe(tags="Tags de busqueda")
async def danbooru_cmd(interaction: discord.Interaction, tags: str):
    if not await _check_module(interaction, "nsfw"): return
    if not interaction.channel.is_nsfw():
        await interaction.response.send_message(BotConfig.t(interaction.guild_id, "solo_nsfw"), ephemeral=True)
        return
    await interaction.response.defer()
    busqueda = "_".join(tags.split()).replace("/", "%2F")
    resultado = Scrapper.danbooruSearch(busqueda)
    try:
        embed = discord.Embed(title=BotConfig.t(interaction.guild_id, "busqueda"), description=tags)
        embed.set_image(url=resultado[1])
        embed.add_field(name="Id en danbooru", value=resultado[0], inline=True)
        embed.add_field(name="Artista", value=resultado[2], inline=True)
        embed.add_field(name="Tags", value=resultado[3], inline=False)
        embed.set_footer(text="Creditos a https://danbooru.donmai.us")
        await interaction.followup.send(embed=embed)
    except Exception as e:
        logger.error(f'danbooru_cmd error: {e}')
        await interaction.followup.send(resultado[0])


@tree.command(name="hanime", description="Busca en hentai-id (solo canales NSFW)")
@app_commands.describe(titulo="Titulo o tags de busqueda")
async def hanime_cmd(interaction: discord.Interaction, titulo: str):
    if not await _check_module(interaction, "nsfw"): return
    if not interaction.channel.is_nsfw():
        await interaction.response.send_message(BotConfig.t(interaction.guild_id, "solo_nsfw"), ephemeral=True)
        return
    await interaction.response.defer()
    resultado = Scrapper.hIdShow("+".join(titulo.split()))
    if not resultado:
        await interaction.followup.send(BotConfig.t(interaction.guild_id, "sin_resultados"))
        return
    embed = discord.Embed(title=titulo, url=resultado[0][0], color=0xFF69B4)
    if resultado[0][1]:
        embed.set_image(url=resultado[0][1])
    for i in range(min(9, len(resultado[1]))):
        try:
            embed.add_field(name=resultado[1][i], value=resultado[2][i] or "—", inline=False)
        except Exception as e:
            logger.warning(f'hanime field: {e}')
    embed.set_footer(text=resultado[0][0])
    await interaction.followup.send(embed=embed)


# ──────────────────────────────────────────────
# ROLEPLAY
# ──────────────────────────────────────────────

@tree.command(name="roll", description="Tira dados — /roll 2 20 para 2d20")
@app_commands.describe(dados="Cantidad de dados", caras="Caras por dado", bonificador="Bonificador opcional")
async def roll_cmd(interaction: discord.Interaction, dados: int, caras: int, bonificador: int = 0):
    if not await _check_module(interaction, "roleplay"): return
    resultado = Roleplay.roll(dados, caras, bonificador, interaction.user.display_name)
    await interaction.response.send_message(resultado)


@tree.command(name="fate", description="Tira dados de Fate (dF)")
@app_commands.describe(dados="Cantidad de dados Fate", modificador="Modificador numerico")
async def fate_cmd(interaction: discord.Interaction, dados: int, modificador: int = 0):
    if not await _check_module(interaction, "roleplay"): return
    resultado = Roleplay.fateroll(dados, modificador, interaction.user.display_name)
    await interaction.response.send_message(resultado)


# ──────────────────────────────────────────────
# ENTRETENIMIENTO
# ──────────────────────────────────────────────

@tree.command(name="anime", description="Busca informacion de un anime")
@app_commands.describe(nombre="Nombre del anime")
async def anime_cmd(interaction: discord.Interaction, nombre: str):
    if not await _check_module(interaction, "entretenimiento"): return
    await interaction.response.defer()
    resultado = Scrapper.animeScrap(nombre.replace(" ", "+"))
    try:
        embed = discord.Embed(title=BotConfig.t(interaction.guild_id, "titulo"), description=resultado[0])
        try: embed.set_image(url=resultado[1])
        except Exception: pass
        try: embed.add_field(name=BotConfig.t(interaction.guild_id, "sinopsis"), value=resultado[2], inline=False)
        except Exception: pass
        try: embed.add_field(name=BotConfig.t(interaction.guild_id, "lanzamiento"), value=resultado[3], inline=True)
        except Exception: pass
        try: embed.add_field(name=BotConfig.t(interaction.guild_id, "finalizacion"), value=resultado[4], inline=True)
        except Exception: pass
        try: embed.add_field(name=BotConfig.t(interaction.guild_id, "estado"), value=resultado[5], inline=True)
        except Exception: pass
        try: embed.add_field(name=BotConfig.t(interaction.guild_id, "tipo"), value=resultado[6], inline=True)
        except Exception: pass
        try: embed.add_field(name="Rating", value=resultado[7], inline=True)
        except Exception: pass
        try: embed.add_field(name=BotConfig.t(interaction.guild_id, "episodios"), value=resultado[8], inline=True)
        except Exception: pass
        try:
            if resultado[9] != "":
                embed.add_field(name=BotConfig.t(interaction.guild_id, "generos"), value=resultado[9], inline=True)
        except Exception: pass
        embed.set_footer(text="Obtenido de kitsu.io")
        await interaction.followup.send(embed=embed)
    except Exception as e:
        logger.error(f'anime_cmd error: {e}')
        await interaction.followup.send(str(resultado[0]))


@tree.command(name="manga", description="Busca informacion de un manga")
@app_commands.describe(nombre="Nombre del manga")
async def manga_cmd(interaction: discord.Interaction, nombre: str):
    if not await _check_module(interaction, "entretenimiento"): return
    await interaction.response.defer()
    resultado = Scrapper.mangaScrap(nombre.replace(" ", "+"))
    try:
        embed = discord.Embed(title=BotConfig.t(interaction.guild_id, "titulo"), description=resultado[0])
        try: embed.set_image(url=resultado[1])
        except Exception: pass
        try: embed.add_field(name=BotConfig.t(interaction.guild_id, "sinopsis"), value=resultado[2], inline=False)
        except Exception: pass
        try: embed.add_field(name=BotConfig.t(interaction.guild_id, "lanzamiento"), value=resultado[3], inline=True)
        except Exception: pass
        try: embed.add_field(name=BotConfig.t(interaction.guild_id, "finalizacion"), value=resultado[4], inline=True)
        except Exception: pass
        try: embed.add_field(name=BotConfig.t(interaction.guild_id, "estado"), value=resultado[5], inline=True)
        except Exception: pass
        try: embed.add_field(name=BotConfig.t(interaction.guild_id, "tipo"), value=resultado[6], inline=True)
        except Exception: pass
        try: embed.add_field(name="Rating", value=resultado[7], inline=True)
        except Exception: pass
        try: embed.add_field(name=BotConfig.t(interaction.guild_id, "capitulos"), value=resultado[8], inline=True)
        except Exception: pass
        try: embed.add_field(name=BotConfig.t(interaction.guild_id, "serializacion"), value=resultado[9], inline=True)
        except Exception: pass
        try:
            if resultado[10] != "":
                embed.add_field(name=BotConfig.t(interaction.guild_id, "generos"), value=resultado[10], inline=True)
        except Exception: pass
        embed.set_footer(text="Obtenido de kitsu.io")
        await interaction.followup.send(embed=embed)
    except Exception as e:
        logger.error(f'manga_cmd error: {e}')
        await interaction.followup.send(str(resultado[0]))


async def _steam_autocomplete(interaction: discord.Interaction, current: str):
    if len(current) < 2:
        return []
    loop = asyncio.get_event_loop()
    items = await loop.run_in_executor(None, lambda: Scrapper.steamSuggest(current))
    return [app_commands.Choice(name=item["name"][:100], value=item["id"]) for item in items]


@tree.command(name="steam", description="Busca informacion de un juego en Steam")
@app_commands.describe(juego="Nombre del juego")
@app_commands.autocomplete(juego=_steam_autocomplete)
async def steam_cmd(interaction: discord.Interaction, juego: str):
    if not await _check_module(interaction, "entretenimiento"): return
    await interaction.response.defer()
    resultado = Scrapper.steamSearch(juego)
    if not resultado:
        await interaction.followup.send(BotConfig.t(interaction.guild_id, "juego_no_encontrado"))
        return
    embed = discord.Embed(title=resultado["name"], description=resultado["description"], color=0x1B2838)
    embed.set_image(url=resultado["image"])
    embed.add_field(name=BotConfig.t(interaction.guild_id, "desarrollador"), value=resultado["developer"] or "—", inline=True)
    embed.add_field(name=BotConfig.t(interaction.guild_id, "fecha_lanzamiento"), value=resultado["release_date"], inline=True)
    embed.add_field(name=BotConfig.t(interaction.guild_id, "genero"), value=resultado["genres"] or "—", inline=False)
    embed.add_field(name="Metacritic", value=resultado["metacritic"], inline=True)
    embed.add_field(name=BotConfig.t(interaction.guild_id, "precio"), value=resultado["price"], inline=True)
    embed.set_footer(text="Fuente: Steam Store")
    await interaction.followup.send(embed=embed)


@tree.command(name="vn", description="Busca una novela visual en VNDB")
@app_commands.describe(busqueda="Titulo de la novela visual")
async def vn_cmd(interaction: discord.Interaction, busqueda: str):
    if not await _check_module(interaction, "entretenimiento"): return
    await interaction.response.defer()
    resultado = Scrapper.vnSearch(busqueda)
    if not resultado:
        await interaction.followup.send(BotConfig.t(interaction.guild_id, "sin_resultados"))
        return
    titulo = resultado["title"]
    if resultado["alttitle"]:
        titulo += " / " + resultado["alttitle"]
    embed = discord.Embed(title=titulo, description=resultado["description"] or None, color=0x2B4C7E)
    if resultado["image"]:
        embed.set_image(url=resultado["image"])
    embed.add_field(name=BotConfig.t(interaction.guild_id, "vn_lanzamiento"), value=resultado["released"], inline=True)
    embed.add_field(name=BotConfig.t(interaction.guild_id, "vn_calificacion"), value=resultado["rating"], inline=True)
    embed.add_field(name=BotConfig.t(interaction.guild_id, "vn_duracion"), value=resultado["length"], inline=True)
    if resultado["platforms"]:
        embed.add_field(name=BotConfig.t(interaction.guild_id, "vn_plataformas"), value=", ".join(resultado["platforms"]), inline=True)
    if resultado["languages"]:
        embed.add_field(name=BotConfig.t(interaction.guild_id, "vn_idiomas"), value=", ".join(resultado["languages"]).upper(), inline=True)
    if resultado["tags"]:
        embed.add_field(name=BotConfig.t(interaction.guild_id, "vn_etiquetas"), value=", ".join(resultado["tags"]), inline=False)
    embed.set_footer(text="Fuente: VNDB (vndb.org)")
    await interaction.followup.send(embed=embed)






from Games import _Calculator, _Trivia, _RPS, _Minesweeper, _Hangman, _Game2048, _Dungeon, _TicTacToe, _calc_eval

class _ImageNav(discord.ui.View):
    def __init__(self, imagenes: list, busqueda: str, guild_id: int):
        super().__init__(timeout=120)
        self.imagenes = imagenes
        self.busqueda = busqueda
        self.guild_id = guild_id
        self.index = 0
        if len(imagenes) <= 1:
            for child in self.children:
                child.disabled = True

    def build_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title=BotConfig.t(self.guild_id, "imagen_encontrada"),
            description=self.busqueda,
        )
        embed.set_image(url=self.imagenes[self.index])
        embed.set_footer(text=f"{self.index + 1} / {len(self.imagenes)}")
        return embed

    @discord.ui.button(emoji="⬅️", style=discord.ButtonStyle.secondary)
    async def prev_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index = (self.index - 1) % len(self.imagenes)
        await interaction.response.edit_message(embed=self.build_embed())

    @discord.ui.button(emoji="➡️", style=discord.ButtonStyle.secondary)
    async def next_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index = (self.index + 1) % len(self.imagenes)
        await interaction.response.edit_message(embed=self.build_embed())


@tree.command(name="img", description="Busca una imagen (solo canales SFW)")
@app_commands.describe(busqueda="Termino de busqueda")
async def img_cmd(interaction: discord.Interaction, busqueda: str):
    if not await _check_module(interaction, "entretenimiento"): return
    if interaction.channel.is_nsfw():
        await interaction.response.send_message(BotConfig.t(interaction.guild_id, "solo_sfw"), ephemeral=True)
        return
    await interaction.response.defer()
    imagenes = Scrapper.imgSearch(busqueda)
    if not imagenes:
        await interaction.followup.send(BotConfig.t(interaction.guild_id, "sin_resultados"))
        return
    view = _ImageNav(imagenes, busqueda, interaction.guild_id)
    await interaction.followup.send(embed=view.build_embed(), view=view)


@tree.command(name="cc", description="Meme aleatorio de CuantoCabron")
async def cc_cmd(interaction: discord.Interaction):
    if not await _check_module(interaction, "entretenimiento"): return
    await interaction.response.defer()
    busqueda = Scrapper.ccSearch()
    embed = discord.Embed(title=busqueda[0], description=busqueda[2])
    embed.set_image(url=busqueda[1])
    await interaction.followup.send(embed=embed)


@tree.command(name="scp", description="Busca un SCP en la SCP Foundation Wiki")
@app_commands.describe(numero="Numero del SCP (ej: 173, 096)")
async def scp_cmd(interaction: discord.Interaction, numero: str):
    if not await _check_module(interaction, "entretenimiento"): return
    await interaction.response.defer()
    resultado = Scrapper.SCP_Search(numero)
    logger.info(f'scp_cmd resultado[0]={resultado[0]!r} len={len(resultado)}')
    try:
        embed = discord.Embed(
            title=f'SCP-{numero}',
            color=0x1B2631,
            url=f'https://scp-wiki.wikidot.com/scp-{numero}',
        )
        SCP_LOGO = 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/SCP_Foundation_(emblem).svg/200px-SCP_Foundation_(emblem).svg.png'
        thumbnail = resultado[0] if resultado[0] else SCP_LOGO
        embed.set_thumbnail(url=thumbnail)
        logger.info(f'scp_cmd set_thumbnail: {thumbnail!r}')
        for i in range(1, min(8, len(resultado))):
            try:
                partes = resultado[i].split(':', 1)
                raw_name = partes[0].strip()
                if len(raw_name) <= 80 and len(partes) > 1:
                    name = raw_name.upper()
                    value = partes[1].strip()[:1024]
                else:
                    name = '—'
                    value = resultado[i][:1024]
                if name and value:
                    embed.add_field(name=name, value=value, inline=False)
            except Exception as e:
                logger.warning(f'scp field {i} error: {e}')
        await interaction.followup.send(embed=embed)
    except Exception as e:
        logger.error(f'scp_cmd embed error: {e}')
        await interaction.followup.send('[DATA EXPUNGED]')


@tree.command(name="convert", description="Convierte divisas")
@app_commands.describe(monto="Monto a convertir", desde="Moneda origen (ej: CLP)", hasta="Moneda destino (ej: USD)")
async def convert_cmd(interaction: discord.Interaction, monto: float, desde: str, hasta: str):
    if not await _check_module(interaction, "entretenimiento"): return
    await interaction.response.defer()
    resultado = Scrapper.reporteDivisa(monto, desde.upper(), hasta.upper())
    try:
        embed = discord.Embed(title=BotConfig.t(interaction.guild_id, "conversion"), description=f"{desde.upper()} a {hasta.upper()}")
        embed.add_field(name=BotConfig.t(interaction.guild_id, "relacion_desde", desde=desde.upper()), value=resultado[0], inline=True)
        embed.add_field(name=BotConfig.t(interaction.guild_id, "relacion_hasta", hasta=hasta.upper()), value=resultado[1], inline=True)
        embed.add_field(name=BotConfig.t(interaction.guild_id, "valor_conversion", monto=monto, desde=desde.upper(), hasta=hasta.upper()), value=resultado[2], inline=False)
        embed.set_footer(text="Fuente: https://openexchangerates.org")
        await interaction.followup.send(embed=embed)
    except Exception as e:
        logger.error(f'convert_cmd error: {e}')
        await interaction.followup.send(str(resultado[2]))


# ──────────────────────────────────────────────
# REACCIONES — cooperativas (requieren @usuario)
# ──────────────────────────────────────────────

@tree.command(name="escobazo", description="Dale un escobazo a alguien")
@app_commands.describe(usuario="Usuario que recibira el escobazo")
async def escobazo_cmd(interaction: discord.Interaction, usuario: discord.Member):
    if not await _check_module(interaction, "reacciones"): return
    embed = _embed(BotConfig.t(interaction.guild_id, "escobazo", user=interaction.user.display_name, target=usuario.display_name), Feels.reactionImage("escobazo"), "Via Stick Horse")
    await interaction.response.send_message(embed=embed)


@tree.command(name="lick", description="Lame a alguien")
@app_commands.describe(usuario="Usuario a lamer")
async def lick_cmd(interaction: discord.Interaction, usuario: discord.Member):
    if not await _check_module(interaction, "reacciones"): return
    embed = _embed(BotConfig.t(interaction.guild_id, "lick", user=interaction.user.display_name, target=usuario.display_name), Feels.reactionImage("lamer"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="pat", description="Acaricia la cabeza de alguien")
@app_commands.describe(usuario="Usuario a acariciar")
async def pat_cmd(interaction: discord.Interaction, usuario: discord.Member):
    if not await _check_module(interaction, "reacciones"): return
    embed = _embed(BotConfig.t(interaction.guild_id, "pat", user=interaction.user.display_name, target=usuario.display_name), Feels.reactionImage("pat"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="slap", description="Cachetea a alguien")
@app_commands.describe(usuario="Usuario a cachetear")
async def slap_cmd(interaction: discord.Interaction, usuario: discord.Member):
    if not await _check_module(interaction, "reacciones"): return
    embed = _embed(BotConfig.t(interaction.guild_id, "slap", user=interaction.user.display_name, target=usuario.display_name), Feels.reactionImage("slap"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="feed", description="Alimenta a alguien")
@app_commands.describe(usuario="Usuario a alimentar")
async def feed_cmd(interaction: discord.Interaction, usuario: discord.Member):
    if not await _check_module(interaction, "reacciones"): return
    embed = _embed(BotConfig.t(interaction.guild_id, "feed", user=interaction.user.display_name, target=usuario.display_name), Feels.reactionImage("food"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="kick", description="Patea a alguien")
@app_commands.describe(usuario="Usuario a patear")
async def kick_cmd(interaction: discord.Interaction, usuario: discord.Member):
    if not await _check_module(interaction, "reacciones"): return
    embed = _embed(BotConfig.t(interaction.guild_id, "kick", user=interaction.user.display_name, target=usuario.display_name), Feels.reactionImage("kickbutt"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="baka", description="BAKA!! a alguien")
@app_commands.describe(usuario="Usuario BAKA")
async def baka_cmd(interaction: discord.Interaction, usuario: discord.Member):
    if not await _check_module(interaction, "reacciones"): return
    embed = _embed(BotConfig.t(interaction.guild_id, "baka", target=usuario.display_name), Feels.reactionImage("baka"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="bite", description="Muerde a alguien")
@app_commands.describe(usuario="Usuario a morder")
async def bite_cmd(interaction: discord.Interaction, usuario: discord.Member):
    if not await _check_module(interaction, "reacciones"): return
    embed = _embed(BotConfig.t(interaction.guild_id, "bite", user=interaction.user.display_name, target=usuario.display_name), Feels.reactionImage("bite"))
    await interaction.response.send_message(embed=embed)


# ──────────────────────────────────────────────
# REACCIONES — propias
# ──────────────────────────────────────────────

@tree.command(name="smug", description="Ponte creido(a)")
async def smug_cmd(interaction: discord.Interaction):
    if not await _check_module(interaction, "reacciones"): return
    embed = _embed(BotConfig.t(interaction.guild_id, "smug", user=interaction.user.display_name), Feels.reactionImage("smug"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="pout", description="Haz pucheros")
async def pout_cmd(interaction: discord.Interaction):
    if not await _check_module(interaction, "reacciones"): return
    embed = _embed(BotConfig.t(interaction.guild_id, "pout", user=interaction.user.display_name), Feels.reactionImage("pout"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="plaf", description="Haz plaf")
async def plaf_cmd(interaction: discord.Interaction):
    if not await _check_module(interaction, "reacciones"): return
    embed = _embed(BotConfig.t(interaction.guild_id, "plaf", user=interaction.user.display_name), Feels.reactionImage("plaf"), "Via Stick Horse")
    await interaction.response.send_message(embed=embed)


@tree.command(name="suicide", description="¿Estas bien?")
async def suicide_cmd(interaction: discord.Interaction):
    if not await _check_module(interaction, "reacciones"): return
    embed = _embed(
        BotConfig.t(interaction.guild_id, "suicide", user=interaction.user.display_name),
        Feels.reactionImage("suicide"),
        "Si realmente estas mal, busca ayuda: https://www.iasp.info/resources/Crisis_Centres/"
    )
    await interaction.response.send_message(embed=embed)


@tree.command(name="spin", description="Ponte a girar")
async def spin_cmd(interaction: discord.Interaction):
    if not await _check_module(interaction, "reacciones"): return
    embed = _embed(BotConfig.t(interaction.guild_id, "spin", user=interaction.user.display_name), Feels.reactionImage("spin"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="blush", description="Sonrojate")
async def blush_cmd(interaction: discord.Interaction):
    if not await _check_module(interaction, "reacciones"): return
    embed = _embed(BotConfig.t(interaction.guild_id, "blush", user=interaction.user.display_name), Feels.reactionImage("blush"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="shy", description="Hazte el/la timido(a)")
async def shy_cmd(interaction: discord.Interaction):
    if not await _check_module(interaction, "reacciones"): return
    embed = _embed(BotConfig.t(interaction.guild_id, "shy", user=interaction.user.display_name), Feels.reactionImage("shy"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="tsundere", description="Se una tsundere")
async def tsundere_cmd(interaction: discord.Interaction):
    if not await _check_module(interaction, "reacciones"): return
    embed = _embed(BotConfig.t(interaction.guild_id, "tsundere", user=interaction.user.display_name), Feels.reactionImage("tsundere"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="lewd", description="Pensamientos cochinos")
async def lewd_cmd(interaction: discord.Interaction):
    if not await _check_module(interaction, "reacciones"): return
    embed = _embed(BotConfig.t(interaction.guild_id, "lewd", user=interaction.user.display_name), Feels.reactionImage("lewd"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="jojo", description="Haz una JojoPose")
async def jojo_cmd(interaction: discord.Interaction):
    if not await _check_module(interaction, "reacciones"): return
    embed = _embed(BotConfig.t(interaction.guild_id, "jojo", user=interaction.user.display_name), Feels.reactionImage("jojo"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="cry", description="Llora")
async def cry_cmd(interaction: discord.Interaction):
    if not await _check_module(interaction, "reacciones"): return
    embed = _embed(BotConfig.t(interaction.guild_id, "cry", user=interaction.user.display_name), Feels.reactionImage("cry"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="smile", description="Sonrie")
async def smile_cmd(interaction: discord.Interaction):
    if not await _check_module(interaction, "reacciones"): return
    embed = _embed(BotConfig.t(interaction.guild_id, "smile", user=interaction.user.display_name), Feels.reactionImage("smile"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="escupefuego", description="Escupe fuego (menciona al bot para que responda)")
@app_commands.describe(usuario="Usuario objetivo (opcional)")
async def escupefuego_cmd(interaction: discord.Interaction, usuario: discord.Member = None):
    if not await _check_module(interaction, "reacciones"): return
    if usuario and usuario.id == client.user.id:
        titulo = BotConfig.t(interaction.guild_id, "firebreath_bot",
                             user=interaction.user.display_name, bot=client.user.display_name)
    elif usuario:
        titulo = BotConfig.t(interaction.guild_id, "firebreath_con",
                             user=interaction.user.display_name, target=usuario.display_name)
    else:
        titulo = BotConfig.t(interaction.guild_id, "firebreath", user=interaction.user.display_name)
    embed = _embed(titulo, Feels.reactionImage("firebreath"))
    await interaction.response.send_message(embed=embed)


# ──────────────────────────────────────────────
# REACCIONES — duales (usuario opcional)
# ──────────────────────────────────────────────

@tree.command(name="dance", description="Ponte a bailar (opcionalmente con alguien)")
@app_commands.describe(usuario="Con quien bailar (opcional)", tipo="Escribe 'caramelldansen' para el baile especial")
async def dance_cmd(interaction: discord.Interaction, usuario: discord.Member = None, tipo: str = None):
    if not await _check_module(interaction, "reacciones"): return
    feel = "caramelldansen" if tipo and tipo.lower() == "caramelldansen" else "dance"
    titulo = BotConfig.t(interaction.guild_id, "dance_con", user=interaction.user.display_name, target=usuario.display_name) if usuario else BotConfig.t(interaction.guild_id, "dance_solo", user=interaction.user.display_name)
    embed = _embed(titulo, Feels.reactionImage(feel))
    await interaction.response.send_message(embed=embed)


@tree.command(name="angry", description="Enojate (opcionalmente con alguien)")
@app_commands.describe(usuario="Con quien estas enojado(a) (opcional)")
async def angry_cmd(interaction: discord.Interaction, usuario: discord.Member = None):
    if not await _check_module(interaction, "reacciones"): return
    titulo = BotConfig.t(interaction.guild_id, "angry_con", user=interaction.user.display_name, target=usuario.display_name) if usuario else BotConfig.t(interaction.guild_id, "angry_solo", user=interaction.user.display_name)
    embed = _embed(titulo, Feels.reactionImage("angry"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="resucitar", description="Resucita a alguien (o a ti mismo)")
@app_commands.describe(usuario="Usuario a resucitar (opcional)")
async def resucitar_cmd(interaction: discord.Interaction, usuario: discord.Member = None):
    if not await _check_module(interaction, "reacciones"): return
    lang  = BotConfig.get_language(interaction.guild_id)
    dias  = (datetime.date.today() - _RESURRECCION).days
    label = BotConfig.t(interaction.guild_id, "resucitar_footer_es" if lang == "es" else "resucitar_footer_en")
    day_word = "D\u00eda" if lang == "es" else "Day"
    footer = f"{label} \u00b7 \u2620\ufe0f 7/9/2025 \u2192 \u2728 18/6/2026 \u00b7 {day_word} {dias}"
    titulo = (
        BotConfig.t(interaction.guild_id, "resucitar_con",
                    user=interaction.user.display_name, target=usuario.display_name)
        if usuario else
        BotConfig.t(interaction.guild_id, "resucitar_solo", user=interaction.user.display_name)
    )
    embed = discord.Embed(title=titulo)
    embed.set_image(url=Feels.reactionImage("resucitar"))
    embed.set_footer(text=footer)
    await interaction.response.send_message(embed=embed)


@tree.command(name="hug", description="Abraza a alguien o pide un abrazo")
@app_commands.describe(usuario="Usuario a abrazar (opcional)")
async def hug_cmd(interaction: discord.Interaction, usuario: discord.Member = None):
    if not await _check_module(interaction, "reacciones"): return
    titulo = BotConfig.t(interaction.guild_id, "hug_con", user=interaction.user.display_name, target=usuario.display_name) if usuario else BotConfig.t(interaction.guild_id, "hug_solo", user=interaction.user.display_name)
    embed = _embed(titulo, Feels.reactionImage("abrazo"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="run", description="Corre o escapa de alguien")
@app_commands.describe(usuario="Usuario de quien escapas (opcional)")
async def run_cmd(interaction: discord.Interaction, usuario: discord.Member = None):
    if not await _check_module(interaction, "reacciones"): return
    if usuario:
        embed = _embed(BotConfig.t(interaction.guild_id, "run_con", user=interaction.user.display_name, target=usuario.display_name), Feels.reactionImage("run"))
    else:
        embed = _embed(BotConfig.t(interaction.guild_id, "run_solo", user=interaction.user.display_name), Feels.reactionImage("escapar"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="kiss", description="Besa a alguien o pide un besito")
@app_commands.describe(usuario="Usuario a besar (opcional)")
async def kiss_cmd(interaction: discord.Interaction, usuario: discord.Member = None):
    if not await _check_module(interaction, "reacciones"): return
    titulo = BotConfig.t(interaction.guild_id, "kiss_con", user=interaction.user.display_name, target=usuario.display_name) if usuario else BotConfig.t(interaction.guild_id, "kiss_solo", user=interaction.user.display_name)
    embed = _embed(titulo, Feels.reactionImage("kiss"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="sleep", description="Duerme o duerme con alguien")
@app_commands.describe(usuario="Con quien dormiras (opcional)")
async def sleep_cmd(interaction: discord.Interaction, usuario: discord.Member = None):
    if not await _check_module(interaction, "reacciones"): return
    if usuario:
        embed = _embed(BotConfig.t(interaction.guild_id, "sleep_con", user=interaction.user.display_name, target=usuario.display_name), Feels.reactionImage("sleep"))
    else:
        embed = _embed(BotConfig.t(interaction.guild_id, "sleep_solo", user=interaction.user.display_name), Feels.reactionImage("sleepy"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="happy", description="Alegrate (opcionalmente por alguien)")
@app_commands.describe(usuario="Por quien estas feliz (opcional)")
async def happy_cmd(interaction: discord.Interaction, usuario: discord.Member = None):
    if not await _check_module(interaction, "reacciones"): return
    titulo = BotConfig.t(interaction.guild_id, "happy_con", user=interaction.user.display_name, target=usuario.display_name) if usuario else BotConfig.t(interaction.guild_id, "happy_solo", user=interaction.user.display_name)
    embed = _embed(titulo, Feels.reactionImage("happy"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="cookie", description="Dale una galleta a alguien o cometete una")
@app_commands.describe(usuario="Usuario a quien darle la galleta (opcional)")
async def cookie_cmd(interaction: discord.Interaction, usuario: discord.Member = None):
    if not await _check_module(interaction, "reacciones"): return
    titulo = BotConfig.t(interaction.guild_id, "cookie_con", user=interaction.user.display_name, target=usuario.display_name) if usuario else BotConfig.t(interaction.guild_id, "cookie_solo", user=interaction.user.display_name)
    embed = _embed(titulo, Feels.reactionImage("cookie"))
    await interaction.response.send_message(embed=embed)



# ──────────────────────────────────────────────
# POKÉMON
# ──────────────────────────────────────────────



async def _pokemon_autocomplete(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    if len(current) < 2:
        return []
    current_lower = current.lower().replace(" ", "-")
    en = BotConfig.get_language(interaction.guild_id) == "en"
    results = []
    for base_name, forms in D.POKEMON_FORMS.items():
        if current_lower in base_name:
            for es_label, en_label, api_value in forms:
                results.append(app_commands.Choice(
                    name=en_label if en else es_label,
                    value=api_value,
                ))
    return results[:25]


@tree.command(name="pokemon", description="Busca informacion de un Pokemon por nombre, numero de Pokedex o 'random'")
@app_commands.describe(busqueda="Nombre, numero nacional o 'random'")
@app_commands.autocomplete(busqueda=_pokemon_autocomplete)
async def pokemon_cmd(interaction: discord.Interaction, busqueda: str):
    if not await _check_module(interaction, "entretenimiento"): return
    await interaction.response.defer()
    resultado = Scrapper.pokemonSearch(busqueda, lang=BotConfig.get_language(interaction.guild_id))
    if not resultado:
        await interaction.followup.send(BotConfig.t(interaction.guild_id, "sin_resultados"))
        return
    await interaction.followup.send(embed=_pokemon_embed(resultado))


async def _tipo_autocomplete(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    current_lower = current.lower()
    en = BotConfig.get_language(interaction.guild_id) == "en"
    return [
        app_commands.Choice(name=nombre_en if en else nombre_es, value=valor)
        for nombre_es, nombre_en, valor in D.TYPES
        if current_lower in (nombre_en if en else nombre_es).lower() or current_lower in valor.lower()
    ][:25]


@tree.command(name="poketype", description="Pokemon aleatorio de un tipo especifico")
@app_commands.describe(tipo="Tipo de Pokemon")
@app_commands.autocomplete(tipo=_tipo_autocomplete)
async def poketype_cmd(interaction: discord.Interaction, tipo: str):
    if not await _check_module(interaction, "entretenimiento"): return
    await interaction.response.defer()
    resultado = Scrapper.pokemonByType(tipo, lang=BotConfig.get_language(interaction.guild_id))
    if not resultado:
        await interaction.followup.send(BotConfig.t(interaction.guild_id, "sin_resultados"))
        return
    await interaction.followup.send(embed=_pokemon_embed(resultado))


client.run(os.environ.get('DISCORD_TOKEN'))