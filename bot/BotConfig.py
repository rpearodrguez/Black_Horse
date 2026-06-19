import json
import os

_PATH = os.path.join(os.path.dirname(__file__), "config.json")

MODULES = ["general", "entretenimiento", "roleplay", "reacciones", "nsfw"]
LANGUAGES = ["es", "en"]

_DEFAULT = {
    "language": "es",
    "modules": {m: True for m in MODULES},
}

_STRINGS = {
    "es": {
        "solo_admin": "No tienes permisos para usar este comando.",
        "modulo_desactivado": "Este módulo está desactivado.",
        "solo_nsfw": "Haz la consulta en un canal NSFW",
        "solo_sfw": "Comando exclusivo para canales safe for work",
        "sin_resultados": "No se encontraron resultados.",
        "config_idioma_ok": "Idioma cambiado a **{lang}**.",
        "config_modulo_ok": "Módulo **{modulo}** {estado}.",
        "config_modulo_on": "activado ✅",
        "config_modulo_off": "desactivado ❌",
        "config_estado_titulo": "Configuración del bot",
        "config_idioma_label": "Idioma",
        "config_modulos_label": "Módulos",
        "sync_ok": "Slash commands sincronizados con Discord.",
        "no_logs": "No hay logs disponibles.",
        "codigo_invalido": "No se encontraron códigos válidos (deben ser de 12 caracteres alfanuméricos).",
        "link_invalido": "El link no parece ser de Twitter/X.",
        "hola": "Come tierra",
        "jueves_si": "Feliz jueves",
        "jueves_si_desc": "hoy es jueves <3",
        "jueves_no": "Hoy no es jueves",
        "celacanto": "🐟 ¡**{user}** se ha encontrado con un celacanto!\nhttps://youtu.be/0UI6Rt3Tl0A",
        "twitter_compartio": "{user} compartió:\n{url}",
        # Reacciones — sobre otros
        "escobazo": "{user} dio un escobazo a {target}",
        "lick": "{user} lamió a {target}",
        "pat": "{user} acarició la cabeza de {target}",
        "slap": "{user} cacheteó a {target}",
        "feed": "{user} alimentó a {target}",
        "kick": "{user} pateó a {target}",
        "baka": "{target} BAKA!! BAKA!! BAKAAAA!!",
        "bite": "{user} muerde a {target}",
        # Reacciones — propias
        "smug": "{user} es un(a) creido(a)",
        "pout": "{user} está haciendo pucheros",
        "plaf": "{user} hizo plaf",
        "suicide": "{user} se mató",
        "spin": "{user} se puso a girar como pendejo",
        "blush": "{user} se sonrojó",
        "shy": "{user} se hace el/la tímido(a)",
        "tsundere": "{user} es una tsundere",
        "lewd": "{user} está teniendo pensamientos cochinos",
        "jojo": "{user} hizo una JojoPose",
        "cry": "{user} está llorando",
        "smile": "{user} se puso a sonreír",
        # Reacciones — duales
        "dance_con": "{user} se puso a bailar con {target}",
        "dance_solo": "{user} se puso a bailar",
        "angry_con": "{user} está molesto(a) con {target}",
        "angry_solo": "{user} está molesto(a)",
        "hug_con": "{user} abrazó a {target}",
        "hug_solo": "{user} necesita un abrazo.",
        "run_con": "{user} escapó de {target}",
        "run_solo": "{user} se echó a correr.",
        "kiss_con": "{user} besó a {target}",
        "kiss_solo": "{user} quiere un besito.",
        "sleep_con": "{user} se fue a dormir con {target}",
        "sleep_solo": "{user} tiene sueño",
        "happy_con": "{user} está feliz por {target}",
        "happy_solo": "{user} está feliz",
        "cookie_con": "{user} le dio una galleta a {target}",
        "cookie_solo": "{user} se comió una galleta",
        # Embeds
        "titulo": "Título",
        "sinopsis": "Sinopsis",
        "lanzamiento": "Lanzamiento",
        "finalizacion": "Finalización",
        "estado": "Estado",
        "tipo": "Tipo",
        "episodios": "Episodios",
        "capitulos": "Capítulos",
        "serializacion": "Serialización",
        "generos": "Géneros",
        "nombre": "Nombre",
        "descripcion": "Descripción",
        "desarrollador": "Desarrollador",
        "fecha_lanzamiento": "Fecha de lanzamiento",
        "genero": "Género",
        "precio": "Precio",
        "imagen_encontrada": "Imagen encontrada",
        "busqueda": "Búsqueda",
        "busqueda_scp": "Búsqueda: SCP-",
        "conversion": "Conversión",
        "relacion_desde": "Relación {desde} a 1 dólar",
        "relacion_hasta": "Relación {hasta} a 1 dólar",
        "valor_conversion": "Valor {monto} {desde} a {hasta}",
        "resultado_imagen": "Aquí está el resultado",
        "sin_resultado": "No se pudo encontrar lo solicitado",
        "juego_no_encontrado": "Juego no encontrado o con bloqueo de edad",
        "juego_error": "No se pudo obtener información del juego",
    },
    "en": {
        "solo_admin": "You don't have permission to use this command.",
        "modulo_desactivado": "This module is disabled.",
        "solo_nsfw": "Please use an NSFW channel for this command.",
        "solo_sfw": "This command is only available in SFW channels.",
        "sin_resultados": "No results found.",
        "config_idioma_ok": "Language changed to **{lang}**.",
        "config_modulo_ok": "Module **{modulo}** {estado}.",
        "config_modulo_on": "enabled ✅",
        "config_modulo_off": "disabled ❌",
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
        # Reactions — targeting others
        "escobazo": "{user} hit {target} with a broom",
        "lick": "{user} licked {target}",
        "pat": "{user} patted {target}'s head",
        "slap": "{user} slapped {target}",
        "feed": "{user} fed {target}",
        "kick": "{user} kicked {target}",
        "baka": "{target} BAKA!! BAKA!! BAKAAAA!!",
        "bite": "{user} bit {target}",
        # Reactions — self
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
        # Reactions — dual
        "dance_con": "{user} is dancing with {target}",
        "dance_solo": "{user} started dancing",
        "angry_con": "{user} is angry at {target}",
        "angry_solo": "{user} is angry",
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
        # Embeds
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
    },
}

_config = None


def _load():
    global _config
    if os.path.exists(_PATH):
        try:
            with open(_PATH, encoding="utf-8") as f:
                loaded = json.load(f)
            _config = dict(_DEFAULT)
            _config.update(loaded)
            _config["modules"] = {**_DEFAULT["modules"], **loaded.get("modules", {})}
            return
        except Exception:
            pass
    _config = {"language": _DEFAULT["language"], "modules": dict(_DEFAULT["modules"])}


def _save():
    with open(_PATH, "w", encoding="utf-8") as f:
        json.dump(_config, f, indent=2, ensure_ascii=False)


def module_enabled(name: str) -> bool:
    return _config["modules"].get(name, True)


def get_language() -> str:
    return _config.get("language", "es")


def set_language(lang: str):
    _config["language"] = lang
    _save()


def set_module(name: str, enabled: bool):
    _config["modules"][name] = enabled
    _save()


def get_modules() -> dict:
    return dict(_config["modules"])


def t(key: str, **kwargs) -> str:
    lang = get_language()
    strings = _STRINGS.get(lang, _STRINGS["es"])
    text = strings.get(key, _STRINGS["es"].get(key, key))
    if kwargs:
        text = text.format(**kwargs)
    return text


_load()