import discord
from discord import app_commands
import Scrapper
import Roleplay
import Feels
import BotConfig
import os
import datetime
import logging
from collections import deque

'''
Bot para Stick Horse
Version 3.1.0 - Slash Commands (app_commands) + BotConfig
Autor: Richard Pena (Vaalus)
Sin Message Content Intent.
'''

ADMIN_ID = int(os.environ.get('ADMIN_ID', 0))

# Buffer de logs en memoria
_log_buffer: deque[str] = deque(maxlen=50)

class _BufferHandler(logging.Handler):
    def emit(self, record):
        _log_buffer.append(self.format(record))

_fmt = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s', datefmt='%H:%M:%S')
_buf_handler = _BufferHandler()
_buf_handler.setFormatter(_fmt)

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s', datefmt='%H:%M:%S')
logging.getLogger('discord').addHandler(_buf_handler)
logging.getLogger('discord').setLevel(logging.WARNING)

logger = logging.getLogger('bot')
logger.addHandler(_buf_handler)

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


def _is_admin(interaction: discord.Interaction) -> bool:
    return interaction.user.id == ADMIN_ID


# ──────────────────────────────────────────────
# ADMIN
# ──────────────────────────────────────────────

@tree.command(name="servers", description="Lista los servidores donde esta activo el bot")
async def servers_cmd(interaction: discord.Interaction):
    if not _is_admin(interaction):
        await interaction.response.send_message(BotConfig.t(interaction.guild_id, "solo_admin"), ephemeral=True)
        return
    lines = [f"Bot activo en **{len(client.guilds)}** servidor(es):\n"]
    for guild in client.guilds:
        lines.append(f"• **{guild.name}** — {guild.member_count} miembros (id: `{guild.id}`)")
    await interaction.response.send_message("\n".join(lines), ephemeral=True)


@tree.command(name="logs", description="Muestra los ultimos logs del bot (solo admin)")
async def logs_cmd(interaction: discord.Interaction):
    if not _is_admin(interaction):
        await interaction.response.send_message(BotConfig.t(interaction.guild_id, "solo_admin"), ephemeral=True)
        return
    if not _log_buffer:
        await interaction.response.send_message(BotConfig.t(interaction.guild_id, "no_logs"), ephemeral=True)
        return
    texto = "\n".join(list(_log_buffer)[-20:])
    await interaction.response.send_message(f"```\n{texto[-1900:]}\n```", ephemeral=True)


@tree.command(name="sync", description="Sincroniza los slash commands con Discord (solo admin)")
async def sync_cmd(interaction: discord.Interaction):
    if not _is_admin(interaction):
        await interaction.response.send_message(BotConfig.t(interaction.guild_id, "solo_admin"), ephemeral=True)
        return
    await interaction.response.defer(ephemeral=True)
    await tree.sync()
    await interaction.followup.send(BotConfig.t(interaction.guild_id, "sync_ok"), ephemeral=True)


# ── /config ────────────────────────────────────

config_group = app_commands.Group(name="config", description="Configuracion del bot (solo admin)")
tree.add_command(config_group)


@config_group.command(name="idioma", description="Cambia el idioma en que responde el bot")
@app_commands.describe(idioma="Idioma del bot")
@app_commands.choices(idioma=[
    app_commands.Choice(name="Espanol", value="es"),
    app_commands.Choice(name="English", value="en"),
])
async def config_idioma_cmd(interaction: discord.Interaction, idioma: app_commands.Choice[str]):
    if not _is_admin(interaction):
        await interaction.response.send_message(BotConfig.t(interaction.guild_id, "solo_admin"), ephemeral=True)
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
    if not _is_admin(interaction):
        await interaction.response.send_message(BotConfig.t(interaction.guild_id, "solo_admin"), ephemeral=True)
        return
    enabled = estado.value == "on"
    BotConfig.set_module(interaction.guild_id, modulo.value, enabled)
    estado_str = BotConfig.t(interaction.guild_id, "config_modulo_on" if enabled else "config_modulo_off")
    await interaction.response.send_message(
        BotConfig.t(interaction.guild_id, "config_modulo_ok", modulo=modulo.value, estado=estado_str), ephemeral=True
    )


@config_group.command(name="estado", description="Muestra la configuracion actual del bot")
async def config_estado_cmd(interaction: discord.Interaction):
    if not _is_admin(interaction):
        await interaction.response.send_message(BotConfig.t(interaction.guild_id, "solo_admin"), ephemeral=True)
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
        "`/genshingift` Codigos de Genshin a links de canjeo\n"
        "`/epitafio` El epitafio de la Bruja Dorada\n"
        "`/invite` Invita al bot a tu servidor"
    ))
    embed.add_field(name="Entretenimiento", inline=False, value=(
        "`/anime` Informacion de un anime\n"
        "`/manga` Informacion de un manga\n"
        "`/steam` Informacion de un juego en Steam\n"
        "`/img` Busca una imagen (solo canales SFW)\n"
        "`/cc` Meme aleatorio de CuantoCabron\n"
        "`/scp` Entrada de la SCP Foundation Wiki\n"
        "`/convert` Conversion de divisas"
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
        "`/hug` `/kiss` `/dance` `/angry` `/run` `/sleep` `/happy` `/cookie`"
    ))
    if interaction.channel.is_nsfw():
        embed.add_field(name="NSFW", inline=False, value=(
            "`/patas` `/piernas` Imagenes de safebooru\n"
            "`/safebooru` Busqueda personalizada en safebooru\n"
            "`/danbooru` Busqueda en danbooru\n"
            "`/hanime` Busca en hentai-id"
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


@tree.command(name="genshingift", description="Convierte codigos de regalo de Genshin Impact en links de canjeo")
@app_commands.describe(codigos="Uno o mas codigos separados por espacios")
async def genshingift_cmd(interaction: discord.Interaction, codigos: str):
    if not await _check_module(interaction, "general"): return
    links = [
        f"https://genshin.mihoyo.com/en/gift?code={c}"
        for c in codigos.split()
        if len(c) == 12 and c.isalnum()
    ]
    if links:
        await interaction.response.send_message("\n".join(links))
    else:
        await interaction.response.send_message(BotConfig.t(interaction.guild_id, "codigo_invalido"))


@tree.command(name="say", description="Hace que el bot repita un mensaje")
@app_commands.describe(mensaje="El mensaje a repetir")
async def say_cmd(interaction: discord.Interaction, mensaje: str):
    if not await _check_module(interaction, "general"): return
    await interaction.response.send_message(mensaje)


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
    except Exception:
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
        except Exception:
            pass
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
    except Exception:
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
    except Exception:
        await interaction.followup.send(str(resultado[0]))


@tree.command(name="steam", description="Busca informacion de un juego en Steam")
@app_commands.describe(juego="Nombre del juego")
async def steam_cmd(interaction: discord.Interaction, juego: str):
    if not await _check_module(interaction, "entretenimiento"): return
    await interaction.response.defer()
    resultado = Scrapper.steamDataSearch(juego.replace(" ", "+"))
    try:
        if resultado[1] != "Nombre":
            embed = discord.Embed(title=BotConfig.t(interaction.guild_id, "nombre"), description=resultado[1])
            embed.set_image(url=resultado[0])
            embed.add_field(name=BotConfig.t(interaction.guild_id, "descripcion"), value=resultado[2], inline=False)
            embed.add_field(name=BotConfig.t(interaction.guild_id, "desarrollador"), value=resultado[3], inline=True)
            embed.add_field(name=BotConfig.t(interaction.guild_id, "fecha_lanzamiento"), value=resultado[4], inline=True)
            embed.add_field(name=BotConfig.t(interaction.guild_id, "genero"), value=resultado[5], inline=False)
            embed.add_field(name="Metacritic", value=resultado[6], inline=True)
            embed.add_field(name=BotConfig.t(interaction.guild_id, "precio"), value=resultado[7], inline=True)
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(BotConfig.t(interaction.guild_id, "juego_no_encontrado"))
    except Exception:
        await interaction.followup.send(BotConfig.t(interaction.guild_id, "juego_error"))


@tree.command(name="img", description="Busca una imagen (solo canales SFW)")
@app_commands.describe(busqueda="Termino de busqueda")
async def img_cmd(interaction: discord.Interaction, busqueda: str):
    if not await _check_module(interaction, "entretenimiento"): return
    if interaction.channel.is_nsfw():
        await interaction.response.send_message(BotConfig.t(interaction.guild_id, "solo_sfw"), ephemeral=True)
        return
    bloqueados = ["loli", "rape", "lolicon", "violacion", "violación", "genocidio", "genocide"]
    if any(w in busqueda.lower().split() for w in bloqueados):
        await interaction.response.send_message(
            "Se solicito la busqueda de un termino ilegal, se procedio a enviar su IP a las autoridades correspondientes. Feliz navidad uwu",
            ephemeral=True
        )
        return
    await interaction.response.defer()
    resultado = Scrapper.imgSearch(busqueda.replace(" ", "+"))
    embed = discord.Embed(title=BotConfig.t(interaction.guild_id, "imagen_encontrada"), description=busqueda)
    embed.set_image(url=resultado)
    await interaction.followup.send(embed=embed)


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
    try:
        embed = discord.Embed(title=BotConfig.t(interaction.guild_id, "busqueda_scp"), description=numero)
        try: embed.set_image(url=resultado[0])
        except Exception: pass
        for i in range(1, min(8, len(resultado))):
            try:
                partes = resultado[i].split(":", 1)
                embed.add_field(name=partes[0], value=partes[1] if len(partes) > 1 else resultado[i], inline=False)
            except Exception: pass
        await interaction.followup.send(embed=embed)
    except Exception:
        await interaction.followup.send(str(resultado[0]))


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
    except Exception:
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

_TYPE_COLORS = {
    "Fire": 0xF08030, "Water": 0x6890F0, "Grass": 0x78C850,
    "Electric": 0xF8D030, "Ice": 0x98D8D8, "Fighting": 0xC03028,
    "Poison": 0xA040A0, "Ground": 0xE0C068, "Flying": 0xA890F0,
    "Psychic": 0xF85888, "Bug": 0xA8B820, "Rock": 0xB8A038,
    "Ghost": 0x705898, "Dragon": 0x7038F8, "Dark": 0x705848,
    "Steel": 0xB8B8D0, "Fairy": 0xEE99AC, "Normal": 0xA8A878,
}
_STAT_NAMES = {
    "hp": "HP",
    "attack": "Ataque",
    "defense": "Defensa",
    "special-attack": "Sp. Ataque",
    "special-defense": "Sp. Defensa",
    "speed": "Velocidad",
}


# (español, inglés, valor API)
_TYPES = [
    ("Normal",    "Normal",    "normal"),
    ("Fuego",     "Fire",      "fire"),
    ("Agua",      "Water",     "water"),
    ("Eléctrico", "Electric",  "electric"),
    ("Planta",    "Grass",     "grass"),
    ("Hielo",     "Ice",       "ice"),
    ("Lucha",     "Fighting",  "fighting"),
    ("Veneno",    "Poison",    "poison"),
    ("Tierra",    "Ground",    "ground"),
    ("Volador",   "Flying",    "flying"),
    ("Psíquico",  "Psychic",   "psychic"),
    ("Bicho",     "Bug",       "bug"),
    ("Roca",      "Rock",      "rock"),
    ("Fantasma",  "Ghost",     "ghost"),
    ("Dragón",    "Dragon",    "dragon"),
    ("Siniestro", "Dark",      "dark"),
    ("Acero",     "Steel",     "steel"),
    ("Hada",      "Fairy",     "fairy"),
]


def _pokemon_embed(resultado: dict) -> discord.Embed:
    color = _TYPE_COLORS.get(resultado["types"][0], 0x5865F2)
    stats_str = "\n".join(f"{_STAT_NAMES.get(k, k)}: **{v}**" for k, v in resultado["stats"].items())
    embed = discord.Embed(
        title=f"#{resultado['dex']:04d} — {resultado['name']}",
        description=resultado["flavor"] or None,
        color=color,
    )
    if resultado["image"]:
        embed.set_thumbnail(url=resultado["image"])
    embed.add_field(name="Tipo", value=" / ".join(resultado["types"]), inline=True)
    embed.add_field(name="Altura / Peso", value=f"{resultado['height']}m / {resultado['weight']}kg", inline=True)
    if resultado["abilities"]:
        embed.add_field(name="Habilidades", value=", ".join(resultado["abilities"]), inline=True)
    if resultado["hidden"]:
        embed.add_field(name="Habilidad oculta", value=", ".join(resultado["hidden"]), inline=True)
    embed.add_field(name="Stats base", value=stats_str, inline=False)
    embed.set_footer(text="Fuente: PokéAPI (pokeapi.co)")
    return embed


@tree.command(name="pokemon", description="Busca informacion de un Pokemon por nombre, numero de Pokedex o 'random'")
@app_commands.describe(busqueda="Nombre, numero nacional o 'random'")
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
        for nombre_es, nombre_en, valor in _TYPES
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