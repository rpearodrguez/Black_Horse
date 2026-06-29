# Black Horse — Bot de Discord para Stick Horse

Bot oficial del servidor [Stick Horse](https://www.stickhorse.cl). Desarrollado en Python con `discord.py 2.x` usando **slash commands** (`/comando`). No requiere el Privileged Intent de Message Content.

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

### Utilidades
| Comando | Descripción |
|---|---|
| `/diccionario [palabra]` | Definición en el Diccionario de la lengua española (RAE) |
| `/hora` | Hora actual en múltiples zonas horarias del mundo |
| `/calcular [expresion]` | Evalúa una expresión matemática directamente (ej: `2+2`, `(5+3)*2`, `2**8`) |
| `/calc` | Calculadora interactiva con botones |

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
| `/pokemon [nombre\|número\|random]` | Info de un Pokémon; autocompletado muestra formas alternativas |
| `/poketype [tipo]` | Pokémon aleatorio de un tipo (autocompletado bilingüe con los 18 tipos) |
| `/vn [título]` | Información de una novela visual (VNDB) |
| `/horoscopo [signo]` | Horóscopo del día (autocompletado bilingüe con los 12 signos) |
| `/personaje [nombre]` | Información de un personaje de anime o manga (Jikan/MAL) |
| `/pelicula [título]` | Información de una película — rating IMDb, reparto, sinopsis (requiere `OMDB_KEY`) |
| `/receta [ingrediente]` | Recetas que usan ese ingrediente — elige de hasta 5 resultados (Spoonacular, requiere `SPOONACULAR_KEY`) |
| `/caracola [pregunta]` | Consulta a la Caracola Mágica de Bob Esponja |

### Listas colaborativas
| Comando | Descripción |
|---|---|
| `/lista ver [nombre]` | Muestra la lista con filtros (Todos / Alguno lo tiene / Yo lo tengo) y paginación de 10 items |
| `/lista agregar [nombre] [item]` | Agrega un item; campo `enlace` opcional |
| `/lista tengo [nombre] [número]` | Marca o desmarca que tienes ese item |
| `/lista buscar [nombre]` | Selector múltiple de usuarios — muestra items que todos ellos tienen |
| `/lista quitar [nombre] [número]` | Quita un item por número |
| `/lista crear [nombre] [@rol]` | Crea una lista con rol de acceso opcional (solo admins del servidor) |
| `/lista borrar [nombre]` | Elimina una lista completa (solo admins del servidor) |
| `/lista rol [nombre] [@rol]` | Cambia el rol de acceso de una lista (solo admins del servidor) |

### Juegos
| Comando | Descripción |
|---|---|
| `/gato [@oponente]` | Tic-tac-toe 3×3 — contra otro usuario o contra el bot (minimax) |
| `/ppt [@oponente]` | Piedra Papel Tijeras — contra otro usuario (elección secreta) o contra el bot |
| `/trivia [categoría]` | Pregunta de trivia con 4 opciones (Open Trivia DB, 13 categorías) |
| `/dungeon` | Dungeon crawler ASCII de 3 niveles |
| `/ahorcado` | Adivina la palabra letra por letra |
| `/dosmil` | 2048 — combina fichas hasta llegar a 2048 |
| `/buscaminas` | Buscaminas 5×5 — no pises las minas |

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
| `/resucitar [@usuario]` | Resucita a alguien (o a ti mismo) — GIF anime + referencia a la resurrección de Kevin |
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
| `/config idioma [es\|en]` | Cambia el idioma del bot en este servidor |
| `/config modulo [nombre] [activar\|desactivar]` | Activa o desactiva un módulo de comandos |
| `/config estado` | Muestra la configuración actual del servidor |

### Kavita (solo el owner del bot)
| Comando | Descripción |
|---|---|
| `/kavita status` | Estado del poller: canal configurado, servidor, último poll |
| `/kavita canal #canal` | Configura el canal donde se publican las notificaciones |
| `/kavita check` | Fuerza un ciclo de polling inmediato |
| `/kavita reset` | Limpia el cache de series vistas (el siguiente check re-anuncia todo) |
| `/kavita series [cantidad]` | Lista las series agregadas recientemente en Kavita (default: 15, máx: 30) |

---

## Setup

### Requisitos
- Python 3.11+ (o Docker)
- Cuenta en [Discord Developer Portal](https://discord.com/developers/applications)

### Variables de entorno
Copia `.env.example` a `.env` y completa los valores:

```env
DISCORD_TOKEN=          # Token del bot (Developer Portal → Bot → Token)
ADMIN_ID=               # Tu ID de usuario de Discord
GIPHY_KEY=              # API key de Giphy (para comandos de reacción con GIF)
GOOGLE_CUSTOM_SEARCH=   # Google API key (para /img)
ID_BUSCADOR_GOOGLE=     # ID del Custom Search Engine (para /img)
DANBOORU_LOGIN=         # Usuario de Danbooru (para /danbooru)
DANBOORU_KEY=           # API key de Danbooru (para /danbooru)
OPEN_EXCHANGE=          # API key de OpenExchangeRates (para /convert)
SPOONACULAR_KEY=        # API key de Spoonacular (para /receta, 150 req/día gratis)
OMDB_KEY=               # API key de OMDB (para /pelicula, 1000 req/día gratis)

# Kavita (opcional — solo para notificaciones de manga)
KAVITA_URL=             # URL base del servidor Kavita (sin barra final)
KAVITA_USER=            # Usuario de Kavita
KAVITA_PASSWORD=        # Contraseña de Kavita
KAVITA_POLL_INTERVAL=30 # Intervalo de polling en minutos (default: 30)
KAVITA_LIBRARIES=       # IDs de bibliotecas a monitorear, separados por coma (vacío = todas)
KAVITA_LIBRARY_NAMES=   # Mapeo id:nombre, ej: 1:Manga,2:Novelas Ligeras
```

`DISCORD_TOKEN` y `ADMIN_ID` son obligatorias. El resto son opcionales — el bot arranca sin ellas, solo esos comandos específicos fallarán.

### Correr con Docker (recomendado)
```bash
cp .env.example .env   # rellenar los valores
docker compose up -d --build
```

### Correr localmente
```bash
pip install -r requirements.txt
cp .env.example bot/.env   # rellenar los valores
cd bot && python Black_Kevin.py
```

### Actualizar el bot (si está corriendo en Docker)
```bash
git pull && docker compose up -d --build
```

---

## Deployment — Google Cloud Free Tier

El bot corre en una VM `e2-micro` de Google Cloud (siempre gratuita):

1. Crear VM `e2-micro` en `us-central1`, `us-east1` o `us-west1` con Ubuntu 24.04 LTS y disco Standard de 30 GB
2. Conectarse por SSH e instalar Docker:
   ```bash
   curl -fsSL https://get.docker.com | sudo sh && sudo usermod -aG docker $USER
   ```
3. Reconectar SSH, clonar el repo y crear el `.env`:
   ```bash
   git clone https://github.com/rpearodrguez/Black_Horse.git && cd Black_Horse
   nano .env
   ```
4. Levantar el bot:
   ```bash
   docker compose up -d --build
   ```

---

## Configuración en Discord Developer Portal

En [discord.com/developers/applications](https://discord.com/developers/applications) → tu app → **Bot**:

- **Message Content Intent**: NO requerido (el bot usa slash commands)
- **Server Members Intent**: NO requerido
- Scopes al generar el link de invitación: `bot` + `applications.commands`
- Permisos mínimos: `Send Messages`, `Embed Links`, `Read Message History`

---

## Tareas pendientes

- **`/scp` — imagen del artículo no carga en Discord**: La imagen se extrae correctamente de `scp-wiki.wdfiles.com` y la URL es válida (verificado con embed generators externos), pero Discord no la renderiza en el embed. Se intentó `set_image` y `set_thumbnail`; el problema parece ser específico de cómo Discord resuelve URLs de `wdfiles.com` desde su proxy de imágenes. Requiere investigación adicional.
- **`/scp` — logo de la Fundación SCP como fallback**: El logo de Wikipedia Commons (`.svg.png`) tampoco carga en Discord. Alternativa: hostear el logo en un CDN compatible (ej. Fandom/Wikia) o en el propio repositorio.
- **Música**: Integración de reproducción de audio desde YouTube pendiente de implementar (`yt-dlp` + FFmpeg + cola por servidor).

---

## Créditos
- Desarrollado por **Richard Peña (Vaalus)**
- Imágenes de reacción vía [Tenor](https://tenor.com) / [Giphy](https://giphy.com)
- Información de anime/manga vía [kitsu.io](https://kitsu.io)
- Sugerencias: [stickhorse.cl](https://www.stickhorse.cl)
