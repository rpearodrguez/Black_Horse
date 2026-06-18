# Black Horse — Bot de Discord para Stick Horse

Bot oficial del servidor [Stick Horse](https://www.stickhorse.cl). Desarrollado en Python con `discord.py 2.x` usando **slash commands** (`/comando`).

---

## Comandos disponibles

### General
| Comando | Descripción |
|---|---|
| `/help` | Lista de comandos disponibles |
| `/invite` | Link de invitación al bot |
| `/hola` | Saluda al bot |
| `/jueves` | ¿Hoy es jueves? |
| `/say [mensaje]` | El bot repite tu mensaje |
| `/genshingift [codigos]` | Convierte códigos de regalo de Genshin Impact en links de canjeo |

### Entretenimiento
| Comando | Descripción |
|---|---|
| `/anime [nombre]` | Información detallada de un anime (kitsu.io) |
| `/manga [nombre]` | Información detallada de un manga (kitsu.io) |
| `/steam [juego]` | Información de un juego en Steam |
| `/img [búsqueda]` | Busca una imagen (solo canales SFW) |
| `/cc` | Meme aleatorio de CuantoCabrón |
| `/scp [número]` | Entrada de la SCP Foundation Wiki |
| `/convert [monto] [desde] [hasta]` | Conversión de divisas (ej: `/convert 1000 CLP USD`) |

### Roleplay
| Comando | Descripción |
|---|---|
| `/roll [dados] [caras] [bonificador]` | Tira dados (ej: `/roll 2 20 3` = 2d20+3) |
| `/fate [dados] [modificador]` | Tira dados de Fate dF (ej: `/fate 4 2`) |

### Reacciones — sobre otros (requieren mencionar usuario)
| Comando | Descripción |
|---|---|
| `/escobazo @usuario` | Dale un escobazo |
| `/pat @usuario` | Acaricia la cabeza |
| `/slap @usuario` | Cachetea |
| `/lick @usuario` | Lame |
| `/feed @usuario` | Alimenta |
| `/kick @usuario` | Patea |
| `/baka @usuario` | BAKA!! |
| `/bite @usuario` | Muerde |

### Reacciones — sobre ti mismo
| Comando | Descripción |
|---|---|
| `/smug` | Eres un creído(a) |
| `/pout` | Haces pucheros |
| `/plaf` | Haces plaf |
| `/spin` | Te pones a girar |
| `/blush` | Te sonrojas |
| `/shy` | Te haces el/la tímido(a) |
| `/tsundere` | Modo tsundere activado |
| `/lewd` | Pensamientos cochinos |
| `/jojo` | JojoPose |
| `/cry` | Lloras |
| `/smile` | Sonríes |
| `/suicide` | (si realmente lo necesitas, busca ayuda) |

### Reacciones — duales (usuario opcional)
| Comando | Descripción |
|---|---|
| `/hug [@usuario]` | Abraza a alguien o pide un abrazo |
| `/kiss [@usuario]` | Besa a alguien o pide un besito |
| `/dance [@usuario] [tipo]` | Baila solo o con alguien (`tipo: caramelldansen`) |
| `/angry [@usuario]` | Enójate o enójate con alguien |
| `/run [@usuario]` | Corre o escapa de alguien |
| `/sleep [@usuario]` | Tienes sueño o te vas a dormir con alguien |
| `/happy [@usuario]` | Estás feliz o feliz por alguien |
| `/cookie [@usuario]` | Te comes una galleta o le das una a alguien |

### NSFW (solo en canales marcados como NSFW)
| Comando | Descripción |
|---|---|
| `/nh [número\|random\|tag]` | Busca en nhentai por número, random o tag |
| `/patas` | Imagen aleatoria de safebooru (feet) |
| `/piernas` | Imagen aleatoria de safebooru (thighs) |
| `/safebooru [tags]` | Búsqueda personalizada en safebooru |
| `/danbooru [tags]` | Búsqueda en danbooru |
| `/hanime [título]` | Busca en hentai-id |

### Admin (solo el owner del bot)
| Comando | Descripción |
|---|---|
| `/servers` | Lista los servidores donde está activo el bot |
| `/sync` | Registra los slash commands en Discord |

---

## Setup

### Requisitos
- Python 3.11+
- Cuenta en [Discord Developer Portal](https://discord.com/developers/applications)

### Variables de entorno
Copia `.env.example` a `.env` y completa los valores:

```env
DISCORD_TOKEN=          # Token del bot (Developer Portal → Bot → Token)
ADMIN_ID=               # Tu ID de usuario de Discord
TENOR_KEY=              # Google Cloud API key con Tenor API habilitada
GOOGLE_CUSTOM_SEARCH=   # Google API key (para /img)
ID_BUSCADOR_GOOGLE=     # ID del Custom Search Engine (para /img)
DANBOORU_LOGIN=         # Usuario de Danbooru (para /danbooru)
DANBOORU_KEY=           # API key de Danbooru (para /danbooru)
OPEN_EXCHANGE=          # API key de OpenExchangeRates (para /convert)
```

### Correr localmente
```bash
pip install -r requirements.txt
python Black_Kevin.py
```

### Deployment gratuito — Railway (recomendado)
1. Crear cuenta en [railway.app](https://railway.app)
2. Conectar este repositorio de GitHub
3. Configurar las variables de entorno en el panel de Railway
4. Railway detecta el `Procfile` automáticamente y lanza el bot como worker

---

## Configuración en Discord Developer Portal

En [discord.com/developers/applications](https://discord.com/developers/applications) → tu app → **Bot**:

- **Message Content Intent**: NO requerido (el bot usa slash commands)
- **Server Members Intent**: NO requerido
- Permisos mínimos al generar el link de invitación: `Send Messages`, `Embed Links`, `Read Message History`

---

## Créditos
- Desarrollado por **Richard Peña (Vaalus)**
- Imágenes de reacción vía [Tenor](https://tenor.com)
- Información de anime/manga vía [kitsu.io](https://kitsu.io)
- Sugerencias: [stickhorse.cl](https://www.stickhorse.cl)
