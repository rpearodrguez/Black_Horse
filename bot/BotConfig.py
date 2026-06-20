import json
import os

_PATH = os.path.join(os.path.dirname(__file__), "config.json")

MODULES = ["general", "utilidades", "entretenimiento", "roleplay", "reacciones", "nsfw"]
LANGUAGES = ["es", "en"]

_GUILD_DEFAULT = {
    "language": "es",
    "modules": {m: True for m in MODULES},
}

_STRINGS = {
    "es": {
        "solo_admin": "No tienes permisos para usar este comando.",
        "solo_bot_admin": "Este comando es exclusivo del propietario del bot.",
        "solo_server_admin": "Necesitas permisos de administrador en este servidor.",
        "modulo_desactivado": "Este modulo esta desactivado.",
        "solo_nsfw": "Haz la consulta en un canal NSFW",
        "solo_sfw": "Comando exclusivo para canales safe for work",
        "sin_resultados": "No se encontraron resultados.",
        "config_idioma_ok": "Idioma cambiado a **{lang}**.",
        "config_modulo_ok": "Modulo **{modulo}** {estado}.",
        "config_modulo_on": "activado",
        "config_modulo_off": "desactivado",
        "config_estado_titulo": "Configuracion del bot",
        "config_idioma_label": "Idioma",
        "config_modulos_label": "Modulos",
        "sync_ok": "Slash commands sincronizados con Discord.",
        "no_logs": "No hay logs disponibles.",
        "codigo_invalido": "No se encontraron codigos validos (deben ser de 12 caracteres alfanumericos).",
        "link_invalido": "El link no parece ser de Twitter/X.",
        "hola": "Come tierra",
        "jueves_si": "Feliz jueves",
        "jueves_si_desc": "hoy es jueves <3",
        "jueves_no": "Hoy no es jueves",
        "celacanto": "🐟 ¡**{user}** se ha encontrado con un celacanto!\nhttps://youtu.be/0UI6Rt3Tl0A",
        "twitter_compartio": "{user} compartio:\n{url}",
        "escobazo": "{user} dio un escobazo a {target}",
        "lick": "{user} lamio a {target}",
        "pat": "{user} acaricio la cabeza de {target}",
        "slap": "{user} cacheteo a {target}",
        "feed": "{user} alimento a {target}",
        "kick": "{user} pateo a {target}",
        "baka": "{target} BAKA!! BAKA!! BAKAAAA!!",
        "bite": "{user} muerde a {target}",
        "smug": "{user} es un(a) creido(a)",
        "pout": "{user} esta haciendo pucheros",
        "plaf": "{user} hizo plaf",
        "suicide": "{user} se mato",
        "spin": "{user} se puso a girar como pendejo",
        "blush": "{user} se sonrojo",
        "shy": "{user} se hace el/la timido(a)",
        "tsundere": "{user} es una tsundere",
        "lewd": "{user} esta teniendo pensamientos cochinos",
        "jojo": "{user} hizo una JojoPose",
        "cry": "{user} esta llorando",
        "smile": "{user} se puso a sonreir",
        "dance_con": "{user} se puso a bailar con {target}",
        "dance_solo": "{user} se puso a bailar",
        "angry_con": "{user} esta molesto(a) con {target}",
        "angry_solo": "{user} esta molesto(a)",
        "resucitar_con": "{user} resucito a {target}",
        "resucitar_solo": "{user} ha resucitado",
        "resucitar_footer_es": "Kevin tambien lo vivio",
        "resucitar_footer_en": "Kevin knows this.",
        "resucitar_con": "{user} resucito a {target}",
        "resucitar_solo": "{user} ha resucitado",
        "resucitar_footer_es": "Kevin tambien lo vivio",
        "resucitar_footer_en": "Kevin knows this.",
        "juego_ajeno": "Esta partida no es tuya.",
        "hug_con": "{user} abrazo a {target}",
        "hug_solo": "{user} necesita un abrazo.",
        "run_con": "{user} escapo de {target}",
        "run_solo": "{user} se echo a correr.",
        "kiss_con": "{user} beso a {target}",
        "kiss_solo": "{user} quiere un besito.",
        "sleep_con": "{user} se fue a dormir con {target}",
        "sleep_solo": "{user} tiene sueno",
        "happy_con": "{user} esta feliz por {target}",
        "happy_solo": "{user} esta feliz",
        "cookie_con": "{user} le dio una galleta a {target}",
        "cookie_solo": "{user} se comio una galleta",
        "firebreath": "{user} escupio fuego",
        "firebreath_con": "{user} le escupio fuego a {target}",
        "firebreath_bot": "{bot} escupe fuego por la boca 🔥",
        "titulo": "Titulo",
        "sinopsis": "Sinopsis",
        "lanzamiento": "Lanzamiento",
        "finalizacion": "Finalizacion",
        "estado": "Estado",
        "tipo": "Tipo",
        "episodios": "Episodios",
        "capitulos": "Capitulos",
        "serializacion": "Serializacion",
        "generos": "Generos",
        "nombre": "Nombre",
        "descripcion": "Descripcion",
        "desarrollador": "Desarrollador",
        "fecha_lanzamiento": "Fecha de lanzamiento",
        "genero": "Genero",
        "precio": "Precio",
        "imagen_encontrada": "Imagen encontrada",
        "busqueda": "Busqueda",
        "busqueda_scp": "Busqueda: SCP-",
        "conversion": "Conversion",
        "relacion_desde": "Relacion {desde} a 1 dolar",
        "relacion_hasta": "Relacion {hasta} a 1 dolar",
        "valor_conversion": "Valor {monto} {desde} a {hasta}",
        "resultado_imagen": "Aqui esta el resultado",
        "sin_resultado": "No se pudo encontrar lo solicitado",
        "juego_no_encontrado": "Juego no encontrado o con bloqueo de edad",
        "juego_error": "No se pudo obtener informacion del juego",
        "hora_titulo": "Hora Mundial",
        "hora_fecha": "Fecha",
        "vn_calificacion": "Calificacion",
        "vn_duracion": "Duracion aprox.",
        "vn_lanzamiento": "Lanzamiento",
        "vn_plataformas": "Plataformas",
        "vn_idiomas": "Idiomas",
        "vn_etiquetas": "Etiquetas",
        "help_config_titulo": "Configuracion del servidor",
        "help_config_idioma": "Cambia el idioma del bot",
        "help_config_modulo": "Activa o desactiva un modulo",
        "help_config_estado": "Muestra la configuracion actual",
        "gato_titulo": "Juego del Gato",
        "gato_turno": "{sym} Turno de {user}",
        "gato_gana": "🎉 ¡{user} gana!",
        "gato_empate": "🤝 ¡Empate!",
        "gato_no_turno": "No es tu turno.",
        "gato_ocupada": "Esa celda ya esta ocupada.",
        "gato_vs_si": "No puedes jugar contra ti mismo.",
        "gato_vs_bot": "No puedes jugar contra un bot.",
        "trivia_correcto": "Correcto",
        "trivia_incorrecto": "Incorrecto",
        "trivia_timeout": "Tiempo agotado",
        "trivia_respuesta": "Respuesta correcta",
        "help_bot_admin_titulo": "Admin del bot",
        "help_bot_servers": "Lista los servidores donde esta el bot",
        "help_bot_logs": "Ultimos logs del bot",
        "help_bot_sync": "Sincroniza los slash commands",
    },
    "en": {
        "solo_admin": "You don't have permission to use this command.",
        "solo_bot_admin": "This command is exclusive to the bot owner.",
        "solo_server_admin": "You need administrator permissions in this server.",
        "modulo_desactivado": "This module is disabled.",
        "solo_nsfw": "Please use an NSFW channel for this command.",
        "solo_sfw": "This command is only available in SFW channels.",
        "sin_resultados": "No results found.",
        "config_idioma_ok": "Language changed to **{lang}**.",
        "config_modulo_ok": "Module **{modulo}** {estado}.",
        "config_modulo_on": "enabled",
        "config_modulo_off": "disabled",
        "config_estado_titulo": "Bot configuration",
        "config_idioma_label": "Language",
        "config_modulos_label": "Modules",
        "sync_ok": "Slash commands synced with Discord.",
        "no_logs": "No logs available.",
        "codigo_invalido": "No valid codes found (must be 12 alphanumeric characters).",
        "link_invalido": "The link doesn't seem to be from Twitter/X.",
        "hola": "Eat dirt",
        "jueves_si": "Happy Thursday",
        "jueves_si_desc": "today is Thursday <3",
        "jueves_no": "Today is not Thursday",
        "celacanto": "🐟 **{user}** encountered a coelacanth!\nhttps://youtu.be/0UI6Rt3Tl0A",
        "twitter_compartio": "{user} shared:\n{url}",
        "escobazo": "{user} hit {target} with a broom",
        "lick": "{user} licked {target}",
        "pat": "{user} patted {target}'s head",
        "slap": "{user} slapped {target}",
        "feed": "{user} fed {target}",
        "kick": "{user} kicked {target}",
        "baka": "{target} BAKA!! BAKA!! BAKAAAA!!",
        "bite": "{user} bit {target}",
        "smug": "{user} is being smug",
        "pout": "{user} is pouting",
        "plaf": "{user} went plaf",
        "suicide": "{user} died",
        "spin": "{user} started spinning",
        "blush": "{user} is blushing",
        "shy": "{user} is being shy",
        "tsundere": "{user} went tsundere",
        "lewd": "{user} is having lewd thoughts",
        "jojo": "{user} struck a JojoPose",
        "cry": "{user} is crying",
        "smile": "{user} smiled",
        "dance_con": "{user} is dancing with {target}",
        "dance_solo": "{user} started dancing",
        "angry_con": "{user} is angry at {target}",
        "angry_solo": "{user} is angry",
        "resucitar_con": "{user} resurrected {target}",
        "resucitar_solo": "{user} has been resurrected",
        "resucitar_footer_es": "Kevin tambien lo vivio",
        "resucitar_footer_en": "Kevin knows this.",
        "resucitar_con": "{user} resurrected {target}",
        "resucitar_solo": "{user} has been resurrected",
        "resucitar_footer_es": "Kevin tambien lo vivio",
        "resucitar_footer_en": "Kevin knows this.",
        "juego_ajeno": "This is not your game.",
        "hug_con": "{user} hugged {target}",
        "hug_solo": "{user} needs a hug.",
        "run_con": "{user} ran away from {target}",
        "run_solo": "{user} ran away.",
        "kiss_con": "{user} kissed {target}",
        "kiss_solo": "{user} wants a kiss.",
        "sleep_con": "{user} went to sleep with {target}",
        "sleep_solo": "{user} is sleepy",
        "happy_con": "{user} is happy for {target}",
        "happy_solo": "{user} is happy",
        "cookie_con": "{user} gave a cookie to {target}",
        "cookie_solo": "{user} ate a cookie",
        "firebreath": "{user} breathed fire",
        "firebreath_con": "{user} breathed fire at {target}",
        "firebreath_bot": "{bot} breathes fire 🔥",
        "titulo": "Title",
        "sinopsis": "Synopsis",
        "lanzamiento": "Release Date",
        "finalizacion": "End Date",
        "estado": "Status",
        "tipo": "Type",
        "episodios": "Episodes",
        "capitulos": "Chapters",
        "serializacion": "Serialization",
        "generos": "Genres",
        "nombre": "Name",
        "descripcion": "Description",
        "desarrollador": "Developer",
        "fecha_lanzamiento": "Release Date",
        "genero": "Genre",
        "precio": "Price",
        "imagen_encontrada": "Image found",
        "busqueda": "Search",
        "busqueda_scp": "Search: SCP-",
        "conversion": "Conversion",
        "relacion_desde": "{desde} to 1 USD",
        "relacion_hasta": "{hasta} to 1 USD",
        "valor_conversion": "Value of {monto} {desde} in {hasta}",
        "resultado_imagen": "Here's your result",
        "sin_resultado": "Nothing found.",
        "juego_no_encontrado": "Game not found or age-locked.",
        "juego_error": "Could not retrieve game information.",
        "hora_titulo": "World Clock",
        "hora_fecha": "Date",
        "vn_calificacion": "Rating",
        "vn_duracion": "Approx. Duration",
        "vn_lanzamiento": "Released",
        "vn_plataformas": "Platforms",
        "vn_idiomas": "Languages",
        "vn_etiquetas": "Tags",
        "help_config_titulo": "Server configuration",
        "help_config_idioma": "Change the bot language",
        "help_config_modulo": "Enable or disable a module",
        "help_config_estado": "Show current configuration",
        "gato_titulo": "Tic-Tac-Toe",
        "gato_turno": "{sym} {user}'s turn",
        "gato_gana": "🎉 {user} wins!",
        "gato_empate": "🤝 Draw!",
        "gato_no_turno": "It's not your turn.",
        "gato_ocupada": "That cell is already taken.",
        "gato_vs_si": "You can't play against yourself.",
        "gato_vs_bot": "You can't play against a bot.",
        "trivia_correcto": "Correct",
        "trivia_incorrecto": "Wrong",
        "trivia_timeout": "Time's up",
        "trivia_respuesta": "Correct answer",
        "help_bot_admin_titulo": "Bot admin",
        "help_bot_servers": "List all servers the bot is in",
        "help_bot_logs": "Show recent bot logs",
        "help_bot_sync": "Sync slash commands with Discord",
    },
}

# { "guild_id_str": { "language": "es", "modules": {...} } }
_guilds: dict = {}


def _load():
    global _guilds
    if os.path.exists(_PATH):
        try:
            with open(_PATH, encoding="utf-8") as f:
                _guilds = json.load(f).get("guilds", {})
            return
        except Exception:
            pass
    _guilds = {}


def _save():
    with open(_PATH, "w", encoding="utf-8") as f:
        json.dump({"guilds": _guilds}, f, indent=2, ensure_ascii=False)


def _guild(guild_id: int) -> dict:
    key = str(guild_id)
    if key not in _guilds:
        _guilds[key] = {
            "language": _GUILD_DEFAULT["language"],
            "modules": dict(_GUILD_DEFAULT["modules"]),
        }
    return _guilds[key]


def module_enabled(guild_id: int, name: str) -> bool:
    return _guild(guild_id)["modules"].get(name, True)


def get_language(guild_id: int) -> str:
    return _guild(guild_id).get("language", "es")


def set_language(guild_id: int, lang: str):
    _guild(guild_id)["language"] = lang
    _save()


def set_module(guild_id: int, name: str, enabled: bool):
    _guild(guild_id)["modules"][name] = enabled
    _save()


def get_modules(guild_id: int) -> dict:
    return dict(_guild(guild_id)["modules"])


def t(guild_id: int, key: str, **kwargs) -> str:
    lang = get_language(guild_id)
    strings = _STRINGS.get(lang, _STRINGS["es"])
    text = strings.get(key, _STRINGS["es"].get(key, key))
    if kwargs:
        text = text.format(**kwargs)
    return text


_load()