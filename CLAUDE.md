# Black Horse Bot — CLAUDE.md

## Qué es este proyecto
Bot de Discord para el servidor **Stick Horse** (stickhorse.cl). Funciona con slash commands (`/comando`) usando `discord.py 2.x` con `app_commands`. No requiere el Privileged Intent de Message Content.

## Stack
- **Python 3.11** — runtime (ver `runtime.txt`)
- **discord.py ≥ 2.3.2** — framework principal, slash commands via `app_commands.CommandTree`
- **deep-translator** — traducción automática al español (no requiere API key propia)
- **beautifulsoup4 + requests** — web scraping y consumo de APIs REST

## Estructura de archivos

```
Black_Horse/
├── bot/                  # Código fuente del bot
│   ├── Black_Kevin.py    # Punto de entrada. Define todos los slash commands y on_ready
│   ├── Scrapper.py       # Búsqueda externa: anime, manga, steam, SCP, booru, nhentai, divisas
│   ├── Feels.py          # GIFs de reacción desde Tenor API v2
│   ├── Roleplay.py       # Lógica de dados: roll (estándar) y fateroll (FATE)
│   └── conversion.py     # Fórmula matemática de conversión de divisas
├── Dockerfile            # Imagen Docker del bot
├── docker-compose.yml    # Orquestador de servicios
├── Procfile              # Config Railway: sh -c 'cd bot && python Black_Kevin.py'
├── requirements.txt      # Dependencias Python
├── runtime.txt           # Versión de Python
└── .env.example          # Referencia de variables de entorno
```

## Variables de entorno

Críticas (el bot no inicia sin ellas):
- `DISCORD_TOKEN` — token del bot desde el Discord Developer Portal
- `ADMIN_ID` — ID numérico de Discord del owner (para `/servers` y `/sync`)

Opcionales (el bot inicia, pero esos comandos específicos fallarán):
- `TENOR_KEY` — Google Cloud API key con Tenor API v2 habilitada (para `/escobazo`, `/hug`, etc.)
- `GOOGLE_CUSTOM_SEARCH` + `ID_BUSCADOR_GOOGLE` — para `/img`
- `DANBOORU_LOGIN` + `DANBOORU_KEY` — para `/danbooru`
- `OPEN_EXCHANGE` — para `/convert`

## Cómo correr localmente
```bash
pip install -r requirements.txt
cp .env.example bot/.env   # y rellenar los valores
cd bot && python Black_Kevin.py
```

## Deployment
Docker (recomendado): ver `docker-compose.yml`. El `.env` va en la raíz del repo (mismo nivel que `docker-compose.yml`).
Railway: conectar el repo, configurar variables de entorno en el panel. El `Procfile` es compatible.

## Patrones importantes al editar el código

### Agregar un nuevo slash command
```python
@tree.command(name="nombre", description="Descripción visible en Discord")
@app_commands.describe(param="Descripción del parámetro")
async def nombre_cmd(interaction: discord.Interaction, param: str):
    await interaction.response.send_message("respuesta")
```
Después de agregar un comando, ejecutar `/sync` en Discord (como ADMIN_ID) para registrarlo. Los cambios globales pueden tardar hasta 1 hora en propagarse en todos los servidores.

### Comandos con llamadas lentas a APIs externas
Usar `defer()` + `followup` para no exceder el timeout de 3 segundos de Discord:
```python
await interaction.response.defer()
resultado = Scrapper.alguna_funcion()
await interaction.followup.send(resultado)
```

### Comandos solo NSFW
```python
if not interaction.channel.is_nsfw():
    await interaction.response.send_message("Solo en canales NSFW", ephemeral=True)
    return
```

### Helper `_embed()`
Para comandos de reacción con GIF (definido al inicio de `Black_Kevin.py`):
```python
embed = _embed("Título del embed", url_imagen, "Texto del footer (opcional)")
```

### Traducción en Scrapper.py
```python
from deep_translator import GoogleTranslator
# Usar el helper local:
texto_es = translate(texto_en)  # función definida al inicio de Scrapper.py
```
