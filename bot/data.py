# Constantes de datos usadas por Black_Kevin.py.
# Separadas aquí para mantener el archivo principal legible.

# ── Pokémon: colores por tipo y nombres de stats ──────────────────────────────

TYPE_COLORS = {
    "Fire": 0xF08030, "Water": 0x6890F0, "Grass": 0x78C850,
    "Electric": 0xF8D030, "Ice": 0x98D8D8, "Fighting": 0xC03028,
    "Poison": 0xA040A0, "Ground": 0xE0C068, "Flying": 0xA890F0,
    "Psychic": 0xF85888, "Bug": 0xA8B820, "Rock": 0xB8A038,
    "Ghost": 0x705898, "Dragon": 0x7038F8, "Dark": 0x705848,
    "Steel": 0xB8B8D0, "Fairy": 0xEE99AC, "Normal": 0xA8A878,
}

STAT_NAMES = {
    "hp": "HP",
    "attack": "Ataque",
    "defense": "Defensa",
    "special-attack": "Sp. Ataque",
    "special-defense": "Sp. Defensa",
    "speed": "Velocidad",
}

# ── Pokémon: 18 tipos (español, inglés, valor API) ────────────────────────────

TYPES = [
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

# ── Pokémon: formas alternativas verificadas en PokéAPI ───────────────────────
# Clave: nombre base que el usuario escribiría.
# Valor: lista de (label_es, label_en, api_name)

POKEMON_FORMS: dict[str, list[tuple[str, str, str]]] = {
    # ── Gen 3 ───────────────────────────────────────────────────────────────
    "castform": [
        ("Castform",             "Castform",             "castform"),
        ("Castform (Sol)",       "Castform (Sunny)",     "castform-sunny"),
        ("Castform (Lluvia)",    "Castform (Rainy)",     "castform-rainy"),
        ("Castform (Nieve)",     "Castform (Snowy)",     "castform-snowy"),
    ],
    "deoxys": [
        ("Deoxys (Normal)",      "Deoxys (Normal)",      "deoxys-normal"),
        ("Deoxys (Ataque)",      "Deoxys (Attack)",      "deoxys-attack"),
        ("Deoxys (Defensa)",     "Deoxys (Defense)",     "deoxys-defense"),
        ("Deoxys (Velocidad)",   "Deoxys (Speed)",       "deoxys-speed"),
    ],
    "wormadam": [
        ("Wormadam (Planta)",    "Wormadam (Plant)",     "wormadam-plant"),
        ("Wormadam (Arena)",     "Wormadam (Sandy)",     "wormadam-sandy"),
        ("Wormadam (Basura)",    "Wormadam (Trash)",     "wormadam-trash"),
    ],
    # ── Gen 4 ───────────────────────────────────────────────────────────────
    "rotom": [
        ("Rotom",                "Rotom",                "rotom"),
        ("Rotom (Calor)",        "Rotom (Heat)",         "rotom-heat"),
        ("Rotom (Lavadora)",     "Rotom (Wash)",         "rotom-wash"),
        ("Rotom (Frío)",         "Rotom (Frost)",        "rotom-frost"),
        ("Rotom (Ventilador)",   "Rotom (Fan)",          "rotom-fan"),
        ("Rotom (Cortadora)",    "Rotom (Mow)",          "rotom-mow"),
    ],
    "giratina": [
        ("Giratina (Alterada)",  "Giratina (Altered)",   "giratina-altered"),
        ("Giratina (Origen)",    "Giratina (Origin)",    "giratina-origin"),
    ],
    "shaymin": [
        ("Shaymin (Tierra)",     "Shaymin (Land)",       "shaymin-land"),
        ("Shaymin (Cielo)",      "Shaymin (Sky)",        "shaymin-sky"),
    ],
    # ── Gen 5 ───────────────────────────────────────────────────────────────
    "basculin": [
        ("Basculin (Rojo)",      "Basculin (Red)",       "basculin-red-striped"),
        ("Basculin (Azul)",      "Basculin (Blue)",      "basculin-blue-striped"),
    ],
    "darmanitan": [
        ("Darmanitan (Unova)",       "Darmanitan (Unova)",       "darmanitan-standard"),
        ("Darmanitan Zen (Unova)",   "Darmanitan Zen (Unova)",   "darmanitan-zen"),
        ("Darmanitan (Galar)",       "Darmanitan (Galar)",       "darmanitan-galar-standard"),
        ("Darmanitan Zen (Galar)",   "Darmanitan Zen (Galar)",   "darmanitan-galar-zen"),
    ],
    "tornadus": [
        ("Tornadus (Encarnado)",  "Tornadus (Incarnate)", "tornadus-incarnate"),
        ("Tornadus (Tótem)",      "Tornadus (Therian)",   "tornadus-therian"),
    ],
    "thundurus": [
        ("Thundurus (Encarnado)", "Thundurus (Incarnate)", "thundurus-incarnate"),
        ("Thundurus (Tótem)",     "Thundurus (Therian)",   "thundurus-therian"),
    ],
    "landorus": [
        ("Landorus (Encarnado)",  "Landorus (Incarnate)", "landorus-incarnate"),
        ("Landorus (Tótem)",      "Landorus (Therian)",   "landorus-therian"),
    ],
    "kyurem": [
        ("Kyurem",               "Kyurem",               "kyurem"),
        ("Kyurem Negro",         "Black Kyurem",         "kyurem-black"),
        ("Kyurem Blanco",        "White Kyurem",         "kyurem-white"),
    ],
    "keldeo": [
        ("Keldeo (Ordinario)",   "Keldeo (Ordinary)",    "keldeo-ordinary"),
        ("Keldeo (Resuelto)",    "Keldeo (Resolute)",    "keldeo-resolute"),
    ],
    "meloetta": [
        ("Meloetta (Aria)",      "Meloetta (Aria)",      "meloetta-aria"),
        ("Meloetta (Pirouette)", "Meloetta (Pirouette)", "meloetta-pirouette"),
    ],
    # ── Gen 6 ───────────────────────────────────────────────────────────────
    "aegislash": [
        ("Aegislash (Escudo)",   "Aegislash (Shield)",   "aegislash-shield"),
        ("Aegislash (Espada)",   "Aegislash (Blade)",    "aegislash-blade"),
    ],
    "zygarde": [
        ("Zygarde 10%",          "Zygarde 10%",          "zygarde-10"),
        ("Zygarde 50%",          "Zygarde 50%",          "zygarde-50"),
        ("Zygarde Completo",     "Zygarde Complete",     "zygarde-complete"),
    ],
    "hoopa": [
        ("Hoopa (Contenido)",    "Hoopa (Confined)",     "hoopa"),
        ("Hoopa (Desatado)",     "Hoopa (Unbound)",      "hoopa-unbound"),
    ],
    # ── Gen 7 ───────────────────────────────────────────────────────────────
    "oricorio": [
        ("Oricorio (Baile)",     "Oricorio (Baile)",     "oricorio-baile"),
        ("Oricorio (Pompón)",    "Oricorio (Pom-Pom)",   "oricorio-pom-pom"),
        ("Oricorio (Pa'u)",      "Oricorio (Pa'u)",      "oricorio-pau"),
        ("Oricorio (Sensu)",     "Oricorio (Sensu)",     "oricorio-sensu"),
    ],
    "lycanroc": [
        ("Lycanroc (Diurno)",    "Lycanroc (Midday)",    "lycanroc-midday"),
        ("Lycanroc (Nocturno)",  "Lycanroc (Midnight)",  "lycanroc-midnight"),
        ("Lycanroc (Crepúsculo)","Lycanroc (Dusk)",      "lycanroc-dusk"),
    ],
    "wishiwashi": [
        ("Wishiwashi (Solo)",    "Wishiwashi (Solo)",    "wishiwashi-solo"),
        ("Wishiwashi (Banco)",   "Wishiwashi (School)",  "wishiwashi-school"),
    ],
    "necrozma": [
        ("Necrozma",             "Necrozma",             "necrozma"),
        ("Necrozma (Alba)",      "Necrozma (Dawn Wings)", "necrozma-dawn"),
        ("Necrozma (Ocaso)",     "Necrozma (Dusk Mane)", "necrozma-dusk"),
        ("Necrozma Ultra",       "Ultra Necrozma",       "necrozma-ultra"),
    ],
    # ── Gen 8 ───────────────────────────────────────────────────────────────
    "toxtricity": [
        ("Toxtricity (Amplio)",  "Toxtricity (Amped)",   "toxtricity-amped"),
        ("Toxtricity (Grave)",   "Toxtricity (Low Key)", "toxtricity-low-key"),
    ],
    "urshifu": [
        ("Urshifu (Golpe Único)","Urshifu (Single Strike)", "urshifu-single-strike"),
        ("Urshifu (Golpe Rápido)","Urshifu (Rapid Strike)","urshifu-rapid-strike"),
    ],
    "zacian": [
        ("Zacian (Héroe)",       "Zacian (Hero)",        "zacian"),
        ("Zacian (Coronado)",    "Zacian (Crowned)",     "zacian-crowned"),
    ],
    "zamazenta": [
        ("Zamazenta (Héroe)",    "Zamazenta (Hero)",     "zamazenta"),
        ("Zamazenta (Coronado)", "Zamazenta (Crowned)",  "zamazenta-crowned"),
    ],
    "calyrex": [
        ("Calyrex",              "Calyrex",              "calyrex"),
        ("Calyrex (Hielo)",      "Calyrex (Ice Rider)",  "calyrex-ice"),
        ("Calyrex (Sombra)",     "Calyrex (Shadow Rider)","calyrex-shadow"),
    ],
    # ── Gen 9 ───────────────────────────────────────────────────────────────
    "tauros": [
        ("Tauros (Kanto)",       "Tauros (Kanto)",       "tauros"),
        ("Tauros (Combate)",     "Tauros (Combat)",      "tauros-paldea-combat-breed"),
        ("Tauros (Fuego)",       "Tauros (Blaze)",       "tauros-paldea-blaze-breed"),
        ("Tauros (Agua)",        "Tauros (Aqua)",        "tauros-paldea-aqua-breed"),
    ],
    "wooper": [
        ("Wooper (Johto)",       "Wooper (Johto)",       "wooper"),
        ("Wooper (Paldea)",      "Wooper (Paldea)",      "wooper-paldea"),
    ],
    "palafin": [
        ("Palafin (Cero)",       "Palafin (Zero)",       "palafin-zero"),
        ("Palafin (Héroe)",      "Palafin (Hero)",       "palafin-hero"),
    ],
    "tatsugiri": [
        ("Tatsugiri (Rizado)",   "Tatsugiri (Curly)",    "tatsugiri-curly"),
        ("Tatsugiri (Caído)",    "Tatsugiri (Droopy)",   "tatsugiri-droopy"),
        ("Tatsugiri (Estirado)", "Tatsugiri (Stretchy)", "tatsugiri-stretchy"),
    ],
    # ── Formas regionales ───────────────────────────────────────────────────
    "raichu": [
        ("Raichu (Kanto)",       "Raichu (Kanto)",       "raichu"),
        ("Raichu (Alola)",       "Raichu (Alola)",       "raichu-alola"),
    ],
    "sandshrew": [
        ("Sandshrew (Kanto)",    "Sandshrew (Kanto)",    "sandshrew"),
        ("Sandshrew (Alola)",    "Sandshrew (Alola)",    "sandshrew-alola"),
    ],
    "sandslash": [
        ("Sandslash (Kanto)",    "Sandslash (Kanto)",    "sandslash"),
        ("Sandslash (Alola)",    "Sandslash (Alola)",    "sandslash-alola"),
    ],
    "vulpix": [
        ("Vulpix (Kanto)",       "Vulpix (Kanto)",       "vulpix"),
        ("Vulpix (Alola)",       "Vulpix (Alola)",       "vulpix-alola"),
    ],
    "ninetales": [
        ("Ninetales (Kanto)",    "Ninetales (Kanto)",    "ninetales"),
        ("Ninetales (Alola)",    "Ninetales (Alola)",    "ninetales-alola"),
    ],
    "grimer": [
        ("Grimer (Kanto)",       "Grimer (Kanto)",       "grimer"),
        ("Grimer (Alola)",       "Grimer (Alola)",       "grimer-alola"),
    ],
    "muk": [
        ("Muk (Kanto)",          "Muk (Kanto)",          "muk"),
        ("Muk (Alola)",          "Muk (Alola)",          "muk-alola"),
    ],
    "exeggutor": [
        ("Exeggutor (Kanto)",    "Exeggutor (Kanto)",    "exeggutor"),
        ("Exeggutor (Alola)",    "Exeggutor (Alola)",    "exeggutor-alola"),
    ],
    "marowak": [
        ("Marowak (Kanto)",      "Marowak (Kanto)",      "marowak"),
        ("Marowak (Alola)",      "Marowak (Alola)",      "marowak-alola"),
    ],
    "ponyta": [
        ("Ponyta (Kanto)",       "Ponyta (Kanto)",       "ponyta"),
        ("Ponyta (Galar)",       "Ponyta (Galar)",       "ponyta-galar"),
    ],
    "rapidash": [
        ("Rapidash (Kanto)",     "Rapidash (Kanto)",     "rapidash"),
        ("Rapidash (Galar)",     "Rapidash (Galar)",     "rapidash-galar"),
    ],
    "slowpoke": [
        ("Slowpoke (Kanto)",     "Slowpoke (Kanto)",     "slowpoke"),
        ("Slowpoke (Galar)",     "Slowpoke (Galar)",     "slowpoke-galar"),
    ],
    "slowbro": [
        ("Slowbro (Kanto)",      "Slowbro (Kanto)",      "slowbro"),
        ("Slowbro (Galar)",      "Slowbro (Galar)",      "slowbro-galar"),
    ],
    "slowking": [
        ("Slowking (Johto)",     "Slowking (Johto)",     "slowking"),
        ("Slowking (Galar)",     "Slowking (Galar)",     "slowking-galar"),
    ],
    "farfetchd": [
        ("Farfetch'd (Kanto)",   "Farfetch'd (Kanto)",   "farfetchd"),
        ("Farfetch'd (Galar)",   "Farfetch'd (Galar)",   "farfetchd-galar"),
    ],
    "weezing": [
        ("Weezing (Kanto)",      "Weezing (Kanto)",      "weezing"),
        ("Weezing (Galar)",      "Weezing (Galar)",      "weezing-galar"),
    ],
    "mr-mime": [
        ("Mr. Mime (Kanto)",     "Mr. Mime (Kanto)",     "mr-mime"),
        ("Mr. Mime (Galar)",     "Mr. Mime (Galar)",     "mr-mime-galar"),
    ],
    "articuno": [
        ("Articuno (Kanto)",     "Articuno (Kanto)",     "articuno"),
        ("Articuno (Galar)",     "Articuno (Galar)",     "articuno-galar"),
    ],
    "zapdos": [
        ("Zapdos (Kanto)",       "Zapdos (Kanto)",       "zapdos"),
        ("Zapdos (Galar)",       "Zapdos (Galar)",       "zapdos-galar"),
    ],
    "moltres": [
        ("Moltres (Kanto)",      "Moltres (Kanto)",      "moltres"),
        ("Moltres (Galar)",      "Moltres (Galar)",      "moltres-galar"),
    ],
    "corsola": [
        ("Corsola (Johto)",      "Corsola (Johto)",      "corsola"),
        ("Corsola (Galar)",      "Corsola (Galar)",      "corsola-galar"),
    ],
    "zigzagoon": [
        ("Zigzagoon (Hoenn)",    "Zigzagoon (Hoenn)",    "zigzagoon"),
        ("Zigzagoon (Galar)",    "Zigzagoon (Galar)",    "zigzagoon-galar"),
    ],
    "linoone": [
        ("Linoone (Hoenn)",      "Linoone (Hoenn)",      "linoone"),
        ("Linoone (Galar)",      "Linoone (Galar)",      "linoone-galar"),
    ],
    "darumaka": [
        ("Darumaka (Unova)",     "Darumaka (Unova)",     "darumaka"),
        ("Darumaka (Galar)",     "Darumaka (Galar)",     "darumaka-galar"),
    ],
    "yamask": [
        ("Yamask (Unova)",       "Yamask (Unova)",       "yamask"),
        ("Yamask (Galar)",       "Yamask (Galar)",       "yamask-galar"),
    ],
    "stunfisk": [
        ("Stunfisk (Unova)",     "Stunfisk (Unova)",     "stunfisk"),
        ("Stunfisk (Galar)",     "Stunfisk (Galar)",     "stunfisk-galar"),
    ],
}

# ── Hora mundial ──────────────────────────────────────────────────────────────
# (es_nombre, en_nombre, tz_id, flag)
# Las primeras HORA_MAIN entradas se muestran en el embed sin parámetro.

TIMEZONES = [
    ("Santiago",          "Santiago",       "America/Santiago",               "🇨🇱"),
    ("Buenos Aires",      "Buenos Aires",   "America/Argentina/Buenos_Aires", "🇦🇷"),
    ("Montevideo",        "Montevideo",     "America/Montevideo",             "🇺🇾"),
    ("São Paulo",         "São Paulo",      "America/Sao_Paulo",             "🇧🇷"),
    ("Bogotá",            "Bogotá",         "America/Bogota",                "🇨🇴"),
    ("Lima",              "Lima",           "America/Lima",                  "🇵🇪"),
    ("Ciudad de México",  "Mexico City",    "America/Mexico_City",           "🇲🇽"),
    ("Madrid",            "Madrid",         "Europe/Madrid",                 "🇪🇸"),
    ("Nueva York",        "New York",       "America/New_York",              "🇺🇸"),
    ("Los Angeles",       "Los Angeles",    "America/Los_Angeles",           "🇺🇸"),
    ("Londres",           "London",         "Europe/London",                 "🇬🇧"),
    ("París",             "Paris",          "Europe/Paris",                  "🇫🇷"),
    ("Moscú",             "Moscow",         "Europe/Moscow",                 "🇷🇺"),
    ("Dubai",             "Dubai",          "Asia/Dubai",                    "🇦🇪"),
    ("Tokio",             "Tokyo",          "Asia/Tokyo",                    "🇯🇵"),
    ("Sidney",            "Sydney",         "Australia/Sydney",              "🇦🇺"),
]

HORA_MAIN = 8  # las primeras 8 (LATAM + España) van en el embed sin parámetro

DAYS = {
    "es": ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"],
    "en": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
}

# ── Trivia: categorías seleccionadas de Open Trivia DB ────────────────────────
# (id, nombre_es, nombre_en)
TRIVIA_CATEGORIES = [
    (9,  "Cultura General",      "General Knowledge"),
    (11, "Cine",                 "Film"),
    (12, "Música",               "Music"),
    (14, "Televisión",           "Television"),
    (15, "Videojuegos",          "Video Games"),
    (17, "Ciencia y Naturaleza", "Science & Nature"),
    (18, "Informática",          "Computers"),
    (20, "Mitología",            "Mythology"),
    (21, "Deportes",             "Sports"),
    (22, "Geografía",            "Geography"),
    (23, "Historia",             "History"),
    (27, "Animales",             "Animals"),
    (31, "Anime y Manga",        "Anime & Manga"),
]

TRIVIA_DIFFICULTY = {
    "easy":   {"es": "Fácil",  "en": "Easy"},
    "medium": {"es": "Media",  "en": "Medium"},
    "hard":   {"es": "Difícil","en": "Hard"},
}

# ── Ahorcado: lista de palabras en español (sin K, W ni tildes) ─────────────
HANGMAN_WORDS = [
    "elefante", "jirafa", "tiburon", "mariposa", "cocodrilo", "tortuga",
    "ballena", "caballo", "pantera", "loro", "cangrejo", "pulpo", "lagarto",
    "salmon", "volcan", "cascada", "desierto", "glaciar", "sabana",
    "telescopio", "brujula", "calendario", "paraguas", "bicicleta", "semaforo",
    "laberinto", "chocolate", "frambuesa", "mandarina", "espagueti", "hamburguesa",
    "almendra", "pistacho", "aguacate", "zanahoria", "berenjena", "biblioteca",
    "catedral", "aeropuerto", "laboratorio", "estadio", "cementerio", "coliseo",
    "aventura", "misterio", "fantasia", "leyenda", "galaxia", "universo",
    "nebulosa", "satelite", "cometa", "tsunami", "axolote", "camaleon",
    "dinosaurio", "pterodactilo", "triceratops", "diplodocus", "mamut",
    "pergamino", "laberinto", "castillo", "pirámide", "fortaleza",
    "piranha", "platipus", "escorpion", "medusa", "langosta",
    "obsidiana", "turquesa", "amatista", "esmeralda", "zafiro",
    "voleibol", "baloncesto", "ciclismo", "atletismo", "natacion",
]
