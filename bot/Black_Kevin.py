import discord
from discord import app_commands
import Scrapper
import Roleplay
import Feels
import os
import datetime

'''
Bot para Stick Horse
Versión 3.0.0 - Slash Commands (app_commands)
Autor: Richard Peña (Vaalus)
Sin Message Content Intent — no requiere verificación de Privileged Intents.
'''

ADMIN_ID = int(os.environ.get('ADMIN_ID', 0))

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    await tree.sync()
    print(f'Bot conectado como {client.user} (id: {client.user.id})')
    print(f'Activo en {len(client.guilds)} servidor(es):')
    for guild in client.guilds:
        print(f'  [{guild.id}] {guild.name} — {guild.member_count} miembros')
    print('Slash commands sincronizados.')


# ──────────────────────────────────────────────
# HELPER
# ──────────────────────────────────────────────

def _embed(titulo: str, imagen: str, footer: str = "Via Giphy") -> discord.Embed:
    embed = discord.Embed(title=titulo)
    embed.set_image(url=imagen)
    embed.set_footer(text=footer)
    return embed


# ──────────────────────────────────────────────
# ADMIN
# ──────────────────────────────────────────────

@tree.command(name="servers", description="Lista los servidores donde está activo el bot")
async def servers_cmd(interaction: discord.Interaction):
    if interaction.user.id != ADMIN_ID:
        await interaction.response.send_message("No tienes permisos para usar este comando.", ephemeral=True)
        return
    lines = [f"Bot activo en **{len(client.guilds)}** servidor(es):\n"]
    for guild in client.guilds:
        lines.append(f"• **{guild.name}** — {guild.member_count} miembros (id: `{guild.id}`)")
    await interaction.response.send_message("\n".join(lines), ephemeral=True)


@tree.command(name="sync", description="Sincroniza los slash commands con Discord (solo admin)")
async def sync_cmd(interaction: discord.Interaction):
    if interaction.user.id != ADMIN_ID:
        await interaction.response.send_message("No tienes permisos para usar este comando.", ephemeral=True)
        return
    await tree.sync()
    await interaction.response.send_message("Slash commands sincronizados con Discord.", ephemeral=True)


# ──────────────────────────────────────────────
# GENERAL
# ──────────────────────────────────────────────

@tree.command(name="help", description="Muestra la lista de comandos disponibles")
async def help_cmd(interaction: discord.Interaction):
    embed = discord.Embed(title="Kevin, la deidad primordial", description="Comandos disponibles")
    embed.add_field(name="General", inline=False, value=(
        "`/hola` Saluda al bot\n"
        "`/jueves` ¿Hoy es jueves?\n"
        "`/say` El bot repite tu mensaje\n"
        "`/genshingift` Códigos de Genshin a links de canjeo\n"
        "`/epitafio` El epitafio de la Bruja Dorada\n"
        "`/invite` Invita al bot a tu servidor"
    ))
    embed.add_field(name="Entretenimiento", inline=False, value=(
        "`/anime` Información de un anime\n"
        "`/manga` Información de un manga\n"
        "`/steam` Información de un juego en Steam\n"
        "`/img` Busca una imagen (solo canales SFW)\n"
        "`/cc` Meme aleatorio de CuantoCabrón\n"
        "`/scp` Entrada de la SCP Foundation Wiki\n"
        "`/convert` Conversión de divisas"
    ))
    embed.add_field(name="Roleplay", inline=False, value=(
        "`/roll` Tira dados estándar (ej: `/roll 2 20 3` = 2d20+3)\n"
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
            "`/nh` Busca en nhentai\n"
            "`/patas` `/piernas` Imágenes de safebooru\n"
            "`/safebooru` Búsqueda personalizada en safebooru\n"
            "`/danbooru` Búsqueda en danbooru\n"
            "`/hanime` Busca en hentai-id"
        ))
    await interaction.response.send_message(embed=embed)


@tree.command(name="invite", description="Obtén el link para invitar al bot a tu servidor")
async def invite_cmd(interaction: discord.Interaction):
    await interaction.response.send_message(
        "https://discord.com/api/oauth2/authorize?client_id=558102665695985674&permissions=92160&scope=bot+applications.commands"
    )


@tree.command(name="hola", description="Saluda al bot")
async def hola_cmd(interaction: discord.Interaction):
    await interaction.response.send_message("Come tierra")


@tree.command(name="epitafio", description="El epitafio de la Bruja Dorada")
async def epitafio_cmd(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Epitafio de la Bruja Dorada",
        color=0xFFD700
    )
    embed.add_field(name="​", inline=False, value=(
        "*Elogia mi nombre, reverencia a la Tierra Dorada.\n"
        "Mi amada tierra natal, resucitada por la llave del oro.*"
    ))
    embed.add_field(name="​", inline=False, value=(
        "En el primer crepúsculo, ofrece a los seis elegidos por la llave.\n"
        "En el segundo crepúsculo, los dos que están cerca serán separados.\n"
        "En el tercer crepúsculo, los dos que están cerca serán alabados.\n"
        "En el cuarto crepúsculo, perfora la cabeza y mata.\n"
        "En el quinto crepúsculo, perfora el pecho y mata.\n"
        "En el sexto crepúsculo, perfora el estómago y mata.\n"
        "En el séptimo crepúsculo, perfora las rodillas y mata.\n"
        "En el octavo crepúsculo, perfora los pies y mata.\n"
        "En el noveno crepúsculo, la bruja revivirá y no quedará nadie.\n"
        "En el décimo crepúsculo, el viaje terminará y llegarás a la Tierra Dorada."
    ))
    embed.add_field(name="​", inline=False, value=(
        "La bruja elogiará al sabio y le otorgará cuatro tesoros.\n"
        "Uno será todo el oro de la Tierra Dorada.\n"
        "Uno será la resurrección de las almas de todos los muertos.\n"
        "Uno será la realización de un milagro que es imposible.\n"
        "Uno será poner a la bruja a dormir por toda la eternidad."
    ))
    embed.set_footer(text="Duerme en paz, mi más amada bruja, Beatrice.")
    await interaction.response.send_message(embed=embed)


@tree.command(name="jueves", description="¿Hoy es jueves?")
async def jueves_cmd(interaction: discord.Interaction):
    if datetime.datetime.today().weekday() == 3:
        embed = discord.Embed(title="Feliz jueves", description="hoy es jueves <3")
        embed.set_image(url="https://c.tenor.com/-W6QXc36TfQAAAAd/asuka-eva.gif")
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("Hoy no es jueves")


@tree.command(name="genshingift", description="Convierte códigos de regalo de Genshin Impact en links de canjeo")
@app_commands.describe(codigos="Uno o más códigos separados por espacios")
async def genshingift_cmd(interaction: discord.Interaction, codigos: str):
    links = [
        f"https://genshin.mihoyo.com/en/gift?code={c}"
        for c in codigos.split()
        if len(c) == 12 and c.isalnum()
    ]
    if links:
        await interaction.response.send_message("\n".join(links))
    else:
        await interaction.response.send_message("No se encontraron códigos válidos (deben ser de 12 caracteres alfanuméricos).")


@tree.command(name="say", description="Hace que el bot repita un mensaje")
@app_commands.describe(mensaje="El mensaje a repetir")
async def say_cmd(interaction: discord.Interaction, mensaje: str):
    await interaction.response.send_message(mensaje)


# ──────────────────────────────────────────────
# NSFW
# ──────────────────────────────────────────────

@tree.command(name="nh", description="Busca en nhentai (solo canales NSFW)")
@app_commands.describe(busqueda="Número, 'random', o tag de búsqueda")
async def nh_cmd(interaction: discord.Interaction, busqueda: str):
    if not interaction.channel.is_nsfw():
        await interaction.response.send_message("No sea marrano y pregunte en un canal NSFW", ephemeral=True)
        return
    if busqueda == "random":
        await interaction.response.send_message(Scrapper.nhentaiRandomSearch())
    elif busqueda.isdigit():
        await interaction.response.send_message(f"https://nhentai.net/g/{busqueda}")
    else:
        tag = "+".join(busqueda.split())
        await interaction.response.send_message(Scrapper.nhentaiTagSearch(tag))


@tree.command(name="patas", description="Imagen aleatoria de patas en safebooru (solo canales NSFW)")
async def patas_cmd(interaction: discord.Interaction):
    if not interaction.channel.is_nsfw():
        await interaction.response.send_message("Haz la consulta en un canal NSFW", ephemeral=True)
        return
    await interaction.response.defer()
    busqueda = Scrapper.safebooruSearch("feet")
    if busqueda != "No se pudo encontrar resultado":
        embed = discord.Embed(title="Aquí está el resultado", description="Cochinón")
        embed.set_image(url=busqueda)
        embed.set_footer(text="Creditos a safebooru.org")
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send("No se pudo encontrar lo solicitado")


@tree.command(name="piernas", description="Imagen aleatoria de piernas en safebooru (solo canales NSFW)")
async def piernas_cmd(interaction: discord.Interaction):
    if not interaction.channel.is_nsfw():
        await interaction.response.send_message("Haz la consulta en un canal NSFW", ephemeral=True)
        return
    await interaction.response.defer()
    busqueda = Scrapper.safebooruSearch("thighs")
    if busqueda != "No se pudo encontrar resultado":
        embed = discord.Embed(title="Aquí está el resultado", description="Piernas")
        embed.set_image(url=busqueda)
        embed.set_footer(text="Creditos a safebooru.org")
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send("No se pudo encontrar lo solicitado")


@tree.command(name="safebooru", description="Busca imágenes en safebooru (solo canales NSFW)")
@app_commands.describe(tags="Tags de búsqueda separados por espacios")
async def safebooru_cmd(interaction: discord.Interaction, tags: str):
    if not interaction.channel.is_nsfw():
        await interaction.response.send_message("Haz la consulta en un canal NSFW", ephemeral=True)
        return
    await interaction.response.defer()
    busqueda = Scrapper.safebooruSearch("+".join(tags.split()))
    if busqueda != "No se pudo encontrar resultado":
        embed = discord.Embed(title="Resultado de búsqueda", description=tags)
        embed.set_image(url=busqueda)
        embed.set_footer(text="Creditos a safebooru.org")
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send("No se pudo encontrar lo solicitado")


@tree.command(name="danbooru", description="Busca imágenes en danbooru (solo canales NSFW)")
@app_commands.describe(tags="Tags de búsqueda")
async def danbooru_cmd(interaction: discord.Interaction, tags: str):
    if not interaction.channel.is_nsfw():
        await interaction.response.send_message("No sea marrano y pregunte en un canal NSFW", ephemeral=True)
        return
    await interaction.response.defer()
    busqueda = "_".join(tags.split()).replace("/", "%2F")
    resultado = Scrapper.danbooruSearch(busqueda)
    try:
        embed = discord.Embed(title="Búsqueda", description=tags)
        embed.set_image(url=resultado[1])
        embed.add_field(name="Id en danbooru", value=resultado[0], inline=True)
        embed.add_field(name="Artista", value=resultado[2], inline=True)
        embed.add_field(name="Tags", value=resultado[3], inline=False)
        embed.set_footer(text="Creditos a https://danbooru.donmai.us")
        await interaction.followup.send(embed=embed)
    except Exception:
        await interaction.followup.send(resultado[0])


@tree.command(name="hanime", description="Busca en hentai-id (solo canales NSFW)")
@app_commands.describe(titulo="Título o tags de búsqueda")
async def hanime_cmd(interaction: discord.Interaction, titulo: str):
    if not interaction.channel.is_nsfw():
        await interaction.response.send_message("No sea marrano y pregunte en un canal NSFW", ephemeral=True)
        return
    await interaction.response.defer()
    resultado = Scrapper.hIdShow("+".join(titulo.split()))
    try:
        embed = discord.Embed(title="Búsqueda", description=titulo)
        embed.set_image(url=resultado[0][1])
        for i in range(min(9, len(resultado[1]))):
            try:
                embed.add_field(name=resultado[1][i], value=resultado[2][i], inline=False)
            except Exception:
                pass
        embed.set_footer(text=f"Puedes encontrarlo en: {resultado[0][0]}")
        await interaction.followup.send(embed=embed)
    except Exception:
        await interaction.followup.send(str(resultado[0]))


# ──────────────────────────────────────────────
# ROLEPLAY
# ──────────────────────────────────────────────

@tree.command(name="roll", description="Tira dados — /roll 2 20 para 2d20")
@app_commands.describe(dados="Cantidad de dados", caras="Caras por dado", bonificador="Bonificador opcional")
async def roll_cmd(interaction: discord.Interaction, dados: int, caras: int, bonificador: int = 0):
    resultado = Roleplay.roll(dados, caras, bonificador, interaction.user.display_name)
    await interaction.response.send_message(resultado)


@tree.command(name="fate", description="Tira dados de Fate (dF)")
@app_commands.describe(dados="Cantidad de dados Fate", modificador="Modificador numérico")
async def fate_cmd(interaction: discord.Interaction, dados: int, modificador: int = 0):
    resultado = Roleplay.fateroll(dados, modificador, interaction.user.display_name)
    await interaction.response.send_message(resultado)


# ──────────────────────────────────────────────
# ENTRETENIMIENTO
# ──────────────────────────────────────────────

@tree.command(name="anime", description="Busca información de un anime")
@app_commands.describe(nombre="Nombre del anime")
async def anime_cmd(interaction: discord.Interaction, nombre: str):
    await interaction.response.defer()
    resultado = Scrapper.animeScrap(nombre.replace(" ", "+"))
    try:
        embed = discord.Embed(title="Título", description=resultado[0])
        try: embed.set_image(url=resultado[1])
        except Exception: pass
        try: embed.add_field(name="Sinopsis", value=resultado[2], inline=False)
        except Exception: pass
        try: embed.add_field(name="Lanzamiento", value=resultado[3], inline=True)
        except Exception: pass
        try: embed.add_field(name="Finalización", value=resultado[4], inline=True)
        except Exception: pass
        try: embed.add_field(name="Estado", value=resultado[5], inline=True)
        except Exception: pass
        try: embed.add_field(name="Tipo", value=resultado[6], inline=True)
        except Exception: pass
        try: embed.add_field(name="Rating", value=resultado[7], inline=True)
        except Exception: pass
        try: embed.add_field(name="Episodios", value=resultado[8], inline=True)
        except Exception: pass
        try:
            if resultado[9] != "":
                embed.add_field(name="Géneros", value=resultado[9], inline=True)
        except Exception: pass
        embed.set_footer(text="Obtenido de kitsu.io")
        await interaction.followup.send(embed=embed)
    except Exception:
        await interaction.followup.send(str(resultado[0]))


@tree.command(name="manga", description="Busca información de un manga")
@app_commands.describe(nombre="Nombre del manga")
async def manga_cmd(interaction: discord.Interaction, nombre: str):
    await interaction.response.defer()
    resultado = Scrapper.mangaScrap(nombre.replace(" ", "+"))
    try:
        embed = discord.Embed(title="Título", description=resultado[0])
        try: embed.set_image(url=resultado[1])
        except Exception: pass
        try: embed.add_field(name="Sinopsis", value=resultado[2], inline=False)
        except Exception: pass
        try: embed.add_field(name="Lanzamiento", value=resultado[3], inline=True)
        except Exception: pass
        try: embed.add_field(name="Finalización", value=resultado[4], inline=True)
        except Exception: pass
        try: embed.add_field(name="Estado", value=resultado[5], inline=True)
        except Exception: pass
        try: embed.add_field(name="Tipo", value=resultado[6], inline=True)
        except Exception: pass
        try: embed.add_field(name="Rating", value=resultado[7], inline=True)
        except Exception: pass
        try: embed.add_field(name="Capítulos", value=resultado[8], inline=True)
        except Exception: pass
        try: embed.add_field(name="Serialización", value=resultado[9], inline=True)
        except Exception: pass
        try:
            if resultado[10] != "":
                embed.add_field(name="Géneros", value=resultado[10], inline=True)
        except Exception: pass
        embed.set_footer(text="Obtenido de kitsu.io")
        await interaction.followup.send(embed=embed)
    except Exception:
        await interaction.followup.send(str(resultado[0]))


@tree.command(name="steam", description="Busca información de un juego en Steam")
@app_commands.describe(juego="Nombre del juego")
async def steam_cmd(interaction: discord.Interaction, juego: str):
    await interaction.response.defer()
    resultado = Scrapper.steamDataSearch(juego.replace(" ", "+"))
    try:
        if resultado[1] != "Nombre":
            embed = discord.Embed(title="Nombre", description=resultado[1])
            embed.set_image(url=resultado[0])
            embed.add_field(name="Descripción", value=resultado[2], inline=False)
            embed.add_field(name="Desarrollador", value=resultado[3], inline=True)
            embed.add_field(name="Fecha de lanzamiento", value=resultado[4], inline=True)
            embed.add_field(name="Género", value=resultado[5], inline=False)
            embed.add_field(name="Metacritic", value=resultado[6], inline=True)
            embed.add_field(name="Precio", value=resultado[7], inline=True)
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send("Juego no encontrado o con bloqueo de edad")
    except Exception:
        await interaction.followup.send("No se pudo obtener información del juego")


@tree.command(name="img", description="Busca una imagen (solo canales SFW)")
@app_commands.describe(busqueda="Término de búsqueda")
async def img_cmd(interaction: discord.Interaction, busqueda: str):
    if interaction.channel.is_nsfw():
        await interaction.response.send_message("Comando exclusivo para canales safe for work", ephemeral=True)
        return
    bloqueados = ["loli", "rape", "lolicon", "violacion", "violación", "genocidio", "genocide"]
    if any(t in busqueda.lower().split() for t in bloqueados):
        await interaction.response.send_message(
            "Se solicitó la búsqueda de un término ilegal, se procedió a enviar su IP a las autoridades correspondientes. Feliz navidad uwu",
            ephemeral=True
        )
        return
    await interaction.response.defer()
    resultado = Scrapper.imgSearch(busqueda.replace(" ", "+"))
    embed = discord.Embed(title="Imagen encontrada", description=busqueda)
    embed.set_image(url=resultado)
    await interaction.followup.send(embed=embed)


@tree.command(name="cc", description="Meme aleatorio de CuantoCabrón")
async def cc_cmd(interaction: discord.Interaction):
    await interaction.response.defer()
    busqueda = Scrapper.ccSearch()
    embed = discord.Embed(title=busqueda[0], description=busqueda[2])
    embed.set_image(url=busqueda[1])
    await interaction.followup.send(embed=embed)


@tree.command(name="scp", description="Busca un SCP en la SCP Foundation Wiki")
@app_commands.describe(numero="Número del SCP (ej: 173, 096)")
async def scp_cmd(interaction: discord.Interaction, numero: str):
    await interaction.response.defer()
    resultado = Scrapper.SCP_Search(numero)
    try:
        embed = discord.Embed(title="Búsqueda: SCP-", description=numero)
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
    await interaction.response.defer()
    resultado = Scrapper.reporteDivisa(monto, desde.upper(), hasta.upper())
    try:
        embed = discord.Embed(title="Conversión", description=f"{desde.upper()} a {hasta.upper()}")
        embed.add_field(name=f"Relación {desde.upper()} a 1 dólar", value=resultado[0], inline=True)
        embed.add_field(name=f"Relación {hasta.upper()} a 1 dólar", value=resultado[1], inline=True)
        embed.add_field(name=f"Valor {monto} {desde.upper()} a {hasta.upper()}", value=resultado[2], inline=False)
        embed.set_footer(text="Fuente: https://openexchangerates.org")
        await interaction.followup.send(embed=embed)
    except Exception:
        await interaction.followup.send(str(resultado[2]))


# ──────────────────────────────────────────────
# REACCIONES — cooperativas (requieren @usuario)
# ──────────────────────────────────────────────

@tree.command(name="escobazo", description="Dale un escobazo a alguien")
@app_commands.describe(usuario="Usuario que recibirá el escobazo")
async def escobazo_cmd(interaction: discord.Interaction, usuario: discord.Member):
    embed = _embed(f"{interaction.user.display_name} dio un escobazo a {usuario.display_name}", Feels.reactionImage("escobazo"), "Via Stick Horse")
    await interaction.response.send_message(embed=embed)


@tree.command(name="lick", description="Lame a alguien")
@app_commands.describe(usuario="Usuario a lamer")
async def lick_cmd(interaction: discord.Interaction, usuario: discord.Member):
    embed = _embed(f"{interaction.user.display_name} lamió a {usuario.display_name}", Feels.reactionImage("lamer"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="pat", description="Acaricia la cabeza de alguien")
@app_commands.describe(usuario="Usuario a acariciar")
async def pat_cmd(interaction: discord.Interaction, usuario: discord.Member):
    embed = _embed(f"{interaction.user.display_name} acarició la cabeza de {usuario.display_name}", Feels.reactionImage("pat"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="slap", description="Cachetea a alguien")
@app_commands.describe(usuario="Usuario a cachetear")
async def slap_cmd(interaction: discord.Interaction, usuario: discord.Member):
    embed = _embed(f"{interaction.user.display_name} cacheteó a {usuario.display_name}", Feels.reactionImage("slap"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="feed", description="Alimenta a alguien")
@app_commands.describe(usuario="Usuario a alimentar")
async def feed_cmd(interaction: discord.Interaction, usuario: discord.Member):
    embed = _embed(f"{interaction.user.display_name} alimentó a {usuario.display_name}", Feels.reactionImage("food"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="kick", description="Patea a alguien")
@app_commands.describe(usuario="Usuario a patear")
async def kick_cmd(interaction: discord.Interaction, usuario: discord.Member):
    embed = _embed(f"{interaction.user.display_name} pateó a {usuario.display_name}", Feels.reactionImage("kickbutt"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="baka", description="BAKA!! a alguien")
@app_commands.describe(usuario="Usuario BAKA")
async def baka_cmd(interaction: discord.Interaction, usuario: discord.Member):
    embed = _embed(f"{usuario.display_name} BAKA!! BAKA!! BAKAAAA!!", Feels.reactionImage("baka"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="bite", description="Muerde a alguien")
@app_commands.describe(usuario="Usuario a morder")
async def bite_cmd(interaction: discord.Interaction, usuario: discord.Member):
    embed = _embed(f"{interaction.user.display_name} muerde a {usuario.display_name}", Feels.reactionImage("bite"))
    await interaction.response.send_message(embed=embed)


# ──────────────────────────────────────────────
# REACCIONES — propias
# ──────────────────────────────────────────────

@tree.command(name="smug", description="Ponte creído(a)")
async def smug_cmd(interaction: discord.Interaction):
    embed = _embed(f"{interaction.user.display_name} es un(a) creido(a)", Feels.reactionImage("smug"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="pout", description="Haz pucheros")
async def pout_cmd(interaction: discord.Interaction):
    embed = _embed(f"{interaction.user.display_name} está haciendo pucheros", Feels.reactionImage("pout"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="plaf", description="Haz plaf")
async def plaf_cmd(interaction: discord.Interaction):
    embed = _embed(f"{interaction.user.display_name} hizo plaf", Feels.reactionImage("plaf"), "Via Stick Horse")
    await interaction.response.send_message(embed=embed)


@tree.command(name="suicide", description="¿Estás bien?")
async def suicide_cmd(interaction: discord.Interaction):
    embed = _embed(
        f"{interaction.user.display_name} se mató",
        Feels.reactionImage("suicide"),
        "Si realmente estás mal, busca ayuda: https://www.iasp.info/resources/Crisis_Centres/"
    )
    await interaction.response.send_message(embed=embed)


@tree.command(name="spin", description="Ponte a girar")
async def spin_cmd(interaction: discord.Interaction):
    embed = _embed(f"{interaction.user.display_name} se puso a girar como pendejo", Feels.reactionImage("spin"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="blush", description="Sonrójate")
async def blush_cmd(interaction: discord.Interaction):
    embed = _embed(f"{interaction.user.display_name} se sonrojó", Feels.reactionImage("blush"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="shy", description="Hazte el/la tímido(a)")
async def shy_cmd(interaction: discord.Interaction):
    embed = _embed(f"{interaction.user.display_name} se hace el/la tímido(a)", Feels.reactionImage("shy"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="tsundere", description="Sé una tsundere")
async def tsundere_cmd(interaction: discord.Interaction):
    embed = _embed(f"{interaction.user.display_name} es una tsundere", Feels.reactionImage("tsundere"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="lewd", description="Pensamientos cochinos")
async def lewd_cmd(interaction: discord.Interaction):
    embed = _embed(f"{interaction.user.display_name} está teniendo pensamientos cochinos", Feels.reactionImage("lewd"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="jojo", description="Haz una JojoPose")
async def jojo_cmd(interaction: discord.Interaction):
    embed = _embed(f"{interaction.user.display_name} hizo una JojoPose", Feels.reactionImage("jojo"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="cry", description="Llora")
async def cry_cmd(interaction: discord.Interaction):
    embed = _embed(f"{interaction.user.display_name} está llorando", Feels.reactionImage("cry"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="smile", description="Sonríe")
async def smile_cmd(interaction: discord.Interaction):
    embed = _embed(f"{interaction.user.display_name} se puso a sonreír", Feels.reactionImage("smile"))
    await interaction.response.send_message(embed=embed)


# ──────────────────────────────────────────────
# REACCIONES — duales (usuario opcional)
# ──────────────────────────────────────────────

@tree.command(name="dance", description="Ponte a bailar (opcionalmente con alguien)")
@app_commands.describe(usuario="Con quien bailar (opcional)", tipo="Escribe 'caramelldansen' para el baile especial")
async def dance_cmd(interaction: discord.Interaction, usuario: discord.Member = None, tipo: str = None):
    feel = "caramelldansen" if tipo and tipo.lower() == "caramelldansen" else "dance"
    titulo = f"{interaction.user.display_name} se puso a bailar con {usuario.display_name}" if usuario else f"{interaction.user.display_name} se puso a bailar"
    embed = _embed(titulo, Feels.reactionImage(feel))
    await interaction.response.send_message(embed=embed)


@tree.command(name="angry", description="Enójate (opcionalmente con alguien)")
@app_commands.describe(usuario="Con quien estás enojado(a) (opcional)")
async def angry_cmd(interaction: discord.Interaction, usuario: discord.Member = None):
    titulo = f"{interaction.user.display_name} está molesto(a) con {usuario.display_name}" if usuario else f"{interaction.user.display_name} está molesto(a)"
    embed = _embed(titulo, Feels.reactionImage("angry"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="hug", description="Abraza a alguien o pide un abrazo")
@app_commands.describe(usuario="Usuario a abrazar (opcional)")
async def hug_cmd(interaction: discord.Interaction, usuario: discord.Member = None):
    titulo = f"{interaction.user.display_name} abrazó a {usuario.display_name}" if usuario else f"{interaction.user.display_name} necesita un abrazo."
    embed = _embed(titulo, Feels.reactionImage("abrazo"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="run", description="Corre o escapa de alguien")
@app_commands.describe(usuario="Usuario de quien escapas (opcional)")
async def run_cmd(interaction: discord.Interaction, usuario: discord.Member = None):
    if usuario:
        embed = _embed(f"{interaction.user.display_name} escapó de {usuario.display_name}", Feels.reactionImage("run"))
    else:
        embed = _embed(f"{interaction.user.display_name} se echó a correr.", Feels.reactionImage("escapar"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="kiss", description="Besa a alguien o pide un besito")
@app_commands.describe(usuario="Usuario a besar (opcional)")
async def kiss_cmd(interaction: discord.Interaction, usuario: discord.Member = None):
    titulo = f"{interaction.user.display_name} besó a {usuario.display_name}" if usuario else f"{interaction.user.display_name} quiere un besito."
    embed = _embed(titulo, Feels.reactionImage("kiss"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="sleep", description="Duerme o duerme con alguien")
@app_commands.describe(usuario="Con quien dormirás (opcional)")
async def sleep_cmd(interaction: discord.Interaction, usuario: discord.Member = None):
    if usuario:
        embed = _embed(f"{interaction.user.display_name} se fue a dormir con {usuario.display_name}", Feels.reactionImage("sleep"))
    else:
        embed = _embed(f"{interaction.user.display_name} tiene sueño", Feels.reactionImage("sleepy"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="happy", description="Alégrate (opcionalmente por alguien)")
@app_commands.describe(usuario="Por quien estás feliz (opcional)")
async def happy_cmd(interaction: discord.Interaction, usuario: discord.Member = None):
    titulo = f"{interaction.user.display_name} está feliz por {usuario.display_name}" if usuario else f"{interaction.user.display_name} está feliz"
    embed = _embed(titulo, Feels.reactionImage("happy"))
    await interaction.response.send_message(embed=embed)


@tree.command(name="cookie", description="Dale una galleta a alguien o cómete una")
@app_commands.describe(usuario="Usuario a quien darle la galleta (opcional)")
async def cookie_cmd(interaction: discord.Interaction, usuario: discord.Member = None):
    titulo = f"{interaction.user.display_name} le dio una galleta a {usuario.display_name}" if usuario else f"{interaction.user.display_name} se comió una galleta"
    embed = _embed(titulo, Feels.reactionImage("cookie"))
    await interaction.response.send_message(embed=embed)


client.run(os.environ.get('DISCORD_TOKEN'))
