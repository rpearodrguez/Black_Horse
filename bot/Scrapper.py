import html
import json
import logging
import os
import random
import re
import urllib.parse
import conversion

import cloudscraper
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

logger = logging.getLogger('bot.scrapper')
_scraper = cloudscraper.create_scraper()


def translate(text, dest='es'):
    try:
        return GoogleTranslator(source='auto', target=dest).translate(text) or text
    except Exception:
        return text


# Abreviaciones de cocina que Google Translate no maneja bien.
# Las que pueden llevar punto final usan lookahead (?=\s|,|$) en vez de \b
# para que el punto sea consumido sin problema de word-boundary.
_COOKING_SUBS = [
    (r'\bfl\.?\s*oz\.?(?=\s|,|$)',  'onza fluida'),   # antes que \boz
    (r'\btbsp?\.?(?=\s|,|$)',       'cucharada'),      # tbsp, tbs
    (r'\btsp\.?(?=\s|,|$)',         'cucharadita'),
    (r'\bcups?(?=\s|,|$)',          'taza'),
    (r'\boz\.?(?=\s|,|$)',          'onza'),
    (r'\blbs?\.?(?=\s|,|$)',        'libra'),
    (r'\bpkgs?\.?(?=\s|,|$)',       'paquete'),
    (r'\bpinch(?:es)?\b',           'pizca'),
    (r'\bdash(?:es)?\b',            'chorrito'),
    (r'\bto\s+taste\b',             'al gusto'),
    (r'\bas\s+needed\b',            'al gusto'),
    (r'\bqts?\.?(?=\s|,|$)',        'cuarto de litro'),
    (r'\bpts?\.?(?=\s|,|$)',        'pinta'),
]


def _norm_cooking(text: str) -> str:
    for pat, rep in _COOKING_SUBS:
        text = re.sub(pat, rep, text, flags=re.IGNORECASE)
    return text


def translate_ingredients(ings: list, dest: str = 'es') -> list:
    if not ings or dest == 'en':
        return ings
    processed = [_norm_cooking(i) for i in ings]
    try:
        # Una sola llamada al traductor; Google preserva saltos de línea
        result = translate('\n'.join(processed), dest=dest)
        parts = [p.strip() for p in result.split('\n') if p.strip()]
        if len(parts) == len(ings):
            return parts
    except Exception:
        pass
    # Fallback: traducción individual
    return [translate(i, dest=dest) for i in processed]


#Anime Scrapping
def animeScrap(urlb=""):
    # url = the target we want to open
    url = 'https://kitsu.io/api/edge/anime?filter[text]={}'.format(urllib.parse.quote(urlb))
    print(url)
    # open with GET method
    resp = requests.get(url)

    # http_respone 200 means OK status
    if resp.status_code == 200:
        
        # we need a parser,Python built-in HTML parser is enough .
        resultado = json.loads(resp.content)        
        try:
            titulo = resultado["data"][0]["attributes"]["canonicalTitle"]
            if str(titulo) == "" or str(titulo) == "None":
                titulo = "Titulo no encontrado"
            portada = resultado["data"][0]["attributes"]["posterImage"]["large"]
            if portada == "" or portada == "None":
                portada = ""
            sinopsis = re.sub('\n'," ",resultado["data"][0]["attributes"]["synopsis"])
            sinopsis = re.sub(r'\[.*?\]'," ",sinopsis)
            sinopsis = re.sub('\r'," ",sinopsis)
            if sinopsis == 'No synopsis has been added for this manga yet.Click here to update this information.':
                sinopsis = "Sinopsis no encontrada"
            else:
                sinopsis = translate(sinopsis)[:1020]+"..."
            lanzamiento = resultado["data"][0]["attributes"]["startDate"]
            if str(lanzamiento) == "" or str(lanzamiento) == "None":
                lanzamiento = "No hay fecha de lanzamiento"
            termino = resultado["data"][0]["attributes"]["endDate"]
            if str(termino) == "" or str(termino) == "None":
                termino = "No hay fecha de termino"
            terminado = translate(resultado["data"][0]["attributes"]["status"])
            if str(terminado) == "" or str(terminado) == "None":
                terminado = "No se encontro estado de termino"
            tipo = resultado["data"][0]["attributes"]["showType"]
            if str(tipo) == "" or str(tipo) == "None":
                tipo = "No se encontró tipo"
            rating = resultado["data"][0]["attributes"]["ageRatingGuide"]
            if str(rating) == "" or str(rating) == "None":
                rating = "No se encontro rating de edad"
            episodios = resultado["data"][0]["attributes"]["episodeCount"]
            if str(episodios) == "" or str(episodios) == "None":
                episodios = "No se encontró cantidad de episodios"
            try:
                generos = ""
                link_generos =  resultado["data"][0]["relationships"]["genres"]["links"]["related"]
                generos_content = json.loads(requests.get(link_generos).content)
                for genero in generos_content["data"]:
                    generos += translate(genero["attributes"]["name"])+", "
                find = [titulo, portada, sinopsis, lanzamiento,termino,terminado, tipo, rating ,episodios, generos]
                print(find)
            except:
                find = [titulo, portada, sinopsis, lanzamiento,termino,terminado, tipo, rating, episodios]
                print(find)
            return find
        except:
            resultado = "Anime o genero no encontrado"
            return resultado

            
    # Find posee los atributos (en el mismo orden) Título, Sumario, Puntaje, Episodios
    
#Manga Scrapping
def mangaScrap(urlb=""):
    # url = the target we want to open
    url = 'https://kitsu.io/api/edge/manga?filter[text]={}'.format(urllib.parse.quote(urlb))
    print(url)
    # open with GET method
    resp = requests.get(url)
    #print(url)
    #print(resp.status_code)
    
    # http_respone 200 means OK status
    if resp.status_code == 200:
        # we need a parser,Python built-in HTML parser is enough .
        resultado = json.loads(resp.content)
        try:
            titulo = resultado["data"][0]["attributes"]["canonicalTitle"]
            if str(titulo) == "" or str(titulo) == "None":
                titulo = "Titulo no encontrado"
            portada = resultado["data"][0]["attributes"]["posterImage"]["large"]
            if portada == "" or portada == "None":
                portada = ""
            sinopsis = re.sub('\n'," ",resultado["data"][0]["attributes"]["synopsis"])
            sinopsis = re.sub(r'\[.*?\]'," ",sinopsis)
            sinopsis = re.sub('\r'," ",sinopsis)
            if sinopsis == 'No synopsis has been added for this manga yet.Click here to update this information.' or sinopsis == '':
                sinopsis = "Sinopsis no encontrada"
            else:
                sinopsis = translate(sinopsis)[:1020]+"..."
            lanzamiento = resultado["data"][0]["attributes"]["startDate"]
            if str(lanzamiento) == "" or str(lanzamiento) == "None":
                lanzamiento = "Lanzamiento no encontrado"
            termino = resultado["data"][0]["attributes"]["endDate"]
            if str(termino) == "" or str(termino) == "None":
                termino = "Fecha de termino no encontrada"
            terminado = translate(resultado["data"][0]["attributes"]["status"])
            if str(terminado) == "" or str(terminado) == "None":
                terminado = "Estado de termino no encontrado"
            tipo = resultado["data"][0]["attributes"]["subtype"]
            if str(tipo) == "" or str(tipo) == "None":
                tipo = "Tipo de producción no encontrado"
            rating = resultado["data"][0]["attributes"]["ageRatingGuide"]
            if str(rating) == "" or str(rating) == "None":
                rating = "Rating no encontrado"
            episodios = resultado["data"][0]["attributes"]["chapterCount"]
            if str(episodios) == "" or str(episodios) == "None":
                episodios = "Cantidad de capitulos no encontrado"
            serializacion = resultado["data"][0]["attributes"]["serialization"]
            if str(serializacion) == "" or str(serializacion) == "None":
                serializacion = "Revista de serializacion no encontrado"
            try:
                generos = ""
                link_generos =  resultado["data"][0]["relationships"]["genres"]["links"]["related"]
                generos_content = json.loads(requests.get(link_generos).content)
                for genero in generos_content["data"]:
                    generos += translate(genero["attributes"]["name"])+", "
                find = [titulo, portada, sinopsis, lanzamiento,termino,terminado, tipo, rating ,episodios, serializacion, generos]
            except:
                find = [titulo, portada, sinopsis, lanzamiento,termino,terminado, tipo, rating, episodios, serializacion]
            return find             
            
        except:
            resultado = "Anime o genero no encontrado"
            return resultado

    else:
        print(resp.content)

# ── Steam ─────────────────────────────────────────────────────────────────────

def steamSearch(busqueda: str):
    if busqueda.isdigit():
        appid = int(busqueda)
    else:
        search = requests.get(
            "https://store.steampowered.com/api/storesearch/",
            params={"term": busqueda, "l": "english", "cc": "US"},
            timeout=10,
        )
        if search.status_code != 200:
            return None
        items = search.json().get("items", [])
        if not items:
            return None
        appid = items[0]["id"]

    detail = requests.get(
        "https://store.steampowered.com/api/appdetails",
        params={"appids": appid, "cc": "cl", "l": "spanish"},
        timeout=10,
    )
    if detail.status_code != 200:
        return None
    app = detail.json().get(str(appid), {})
    if not app.get("success"):
        return None
    d = app["data"]

    price = "Gratis" if d.get("is_free") else "—"
    po = d.get("price_overview")
    if po:
        final = po.get("final_formatted", "—")
        discount = po.get("discount_percent", 0)
        if discount:
            price = f"~~{po.get('initial_formatted')}~~ {final} (-{discount}%)"
        else:
            price = final

    return {
        "name": d.get("name", "—"),
        "description": html.unescape(d.get("short_description", "—")),
        "developer": ", ".join(d.get("developers") or []),
        "release_date": (d.get("release_date") or {}).get("date", "—"),
        "genres": ", ".join(g["description"] for g in (d.get("genres") or [])),
        "metacritic": str((d.get("metacritic") or {}).get("score", "—")),
        "price": price,
        "image": d.get("header_image", ""),
    }


def steamSuggest(busqueda: str) -> list:
    try:
        resp = requests.get(
            "https://store.steampowered.com/api/storesearch/",
            params={"term": busqueda, "l": "english", "cc": "US"},
            timeout=5,
        )
        if resp.status_code != 200:
            return []
        return [
            {"id": str(item["id"]), "name": item["name"]}
            for item in resp.json().get("items", [])
            if item.get("type") == "app"
        ][:10]
    except Exception:
        return []


#Hentai Scrapping
NH_REST = "https://nhentai.rest"
NH_EXT = {"j": "jpg", "p": "png", "g": "gif"}

def _nh_parse(data):
    media_id = data["media_id"]
    cover_ext = NH_EXT.get(data["images"]["cover"]["t"], "jpg")
    tags_by_type = {}
    for tag in data.get("tags", []):
        tags_by_type.setdefault(tag["type"], []).append(tag["name"])
    return {
        "id": data["id"],
        "title": data.get("title", {}).get("pretty") or data.get("title", {}).get("english", "Sin título"),
        "cover": f"https://t.nhentai.net/galleries/{media_id}/cover.{cover_ext}",
        "pages": data.get("num_pages", "?"),
        "artists": tags_by_type.get("artist", []),
        "groups": tags_by_type.get("group", []),
        "languages": tags_by_type.get("language", []),
        "parodies": tags_by_type.get("parody", []),
        "characters": tags_by_type.get("character", []),
        "tags": tags_by_type.get("tag", []),
        "url": f"https://nhentai.net/g/{data['id']}/"
    }

def nhentaiInfo(id):
    try:
        resp = requests.get(f"{NH_REST}/api/gallery/{id}")
        if resp.status_code != 200:
            logger.warning(f"nhentaiInfo {id}: HTTP {resp.status_code}")
            return None
        return _nh_parse(resp.json())
    except Exception as e:
        logger.error(f"nhentaiInfo {id}: {e}")
        return None

def nhentaiRandom():
    try:
        resp = requests.get(f"{NH_REST}/api/gallery/random")
        if resp.status_code == 200:
            return str(resp.json()["id"])
        logger.warning(f"nhentaiRandom: HTTP {resp.status_code}")
    except Exception as e:
        logger.error(f"nhentaiRandom: {e}")
    return None

def nhentaiTagSearch(tag):
    try:
        resp = requests.get(f"{NH_REST}/api/gallery/search",
                            params={"query": tag, "sort": "popular"})
        if resp.status_code == 200:
            results = resp.json().get("result", [])
            if results:
                return str(random.choice(results)["id"])
            logger.warning(f"nhentaiTagSearch '{tag}': sin resultados")
        else:
            logger.warning(f"nhentaiTagSearch '{tag}': HTTP {resp.status_code}")
    except Exception as e:
        logger.error(f"nhentaiTagSearch '{tag}': {e}")
    return None

def imgSearch(busqueda: str, count: int = 5) -> list:
    key = os.environ.get('GOOGLE_CUSTOM_SEARCH')
    cx = os.environ.get('ID_BUSCADOR_GOOGLE')
    if not key or not cx:
        return []
    try:
        resp = requests.get(
            "https://www.googleapis.com/customsearch/v1",
            params={"cx": cx, "key": key, "q": busqueda, "searchType": "image", "safe": "active", "num": count},
            timeout=10,
        )
        if resp.status_code != 200:
            return []
        return [item["link"] for item in resp.json().get("items", [])]
    except Exception:
        return []

def ccSearch():
    url = "https://www.cuantocabron.com/aleatorio/p/1"
    resp = requests.get(url)

    # http_respone 200 means OK status
    if resp.status_code == 200:
        print("Successfully opened the web page")
        print("Este es el sumario del meme solicitado :-\n")
        find = ["Titulo","Imagen","Creditos a Cuantocabron.com"]

        # we need a parser,Python built-in HTML parser is enough .
        soup = BeautifulSoup(resp.text, 'html.parser')
        # l is the list which contains all the text i.e news
        titulo = soup.find("h2", {"class": "storyTitle"})
        find[0] = titulo.text
        imagen = soup.find("a", {"class": "cclink"})
        print(imagen)
        # now we want to print only the text part of the anchor.
        # find all the elements of a, i.e anchor
        try:
            for i in imagen.findAll("img", {"class": ""}, limit=1):
                try:
                    #Portada
                    find[1] = i.get('src')
                    print(find[1])
                except:
                    pass
        except:
            pass
        print(find)
        return find

def safebooruSearch(busqueda=""):
    #busqueda = "thighs"
    url = "https://safebooru.org/index.php?page=dapi&s=post&q=index&limit=100&tags={}".format(busqueda)
    # open with GET method
    resp = requests.get(url)
    root = resp.content.decode('UTF-8')
    # http_respone 200 means OK status
    if resp.status_code == 200:
        count = root.split("<")
        #print("Count 1 : {}".format(count))
        count2 = count[2].split()
        print("Count 2 : {}".format(count2))
        count3 = count2[1].split("=")
        print(count3)
        count4 = count3[1].split('"')
        print("count4 = {}".format(count4))
        #randpata = random.randint(1, int(count4))
        if int(count4[1]) > 100:
            count4[1] = 100
        randpata = random.randint(1, int(count4[1]))
        lista = root.split("file_url=")
        resultado = lista[randpata].split()[0].split('"')[1]
        return resultado
        
    else:
        return "No se pudo encontrar resultado"

def danbooruSearch(busqueda=""):
    url = "https://danbooru.donmai.us/posts.json?login={}&api_key={}&limit=1&tags={}&random=true".format(os.environ.get('DANBOORU_LOGIN'),os.environ.get('DANBOORU_KEY'),busqueda)
    # open with GET method
    resp = requests.get(url)
    print(resp.status_code)

    # http_respone 200 means OK status
    if resp.status_code == 200:
        find = ["id no identificada","imagen no identificada","Artista no identificado","Tags no identificados"]
        # we need a parser,Python built-in HTML parser is enough .
        resultado = json.loads(resp.content)
        print(resultado)
        try:
            id_post = resultado[0]["id"]
            if id_post == "":
                id_post = "id no identificada"
            imagen = resultado[0]["file_url"]
            if imagen == "":
                imagen = "imagen no identificada"
            artista = resultado[0]["tag_string_artist"]
            if artista == "":
                artista = "Artista no identificado"
            tags = resultado[0]["tag_string"]
            tags2 = " ".join(tags.split()[:15])
            if tags == "":
                tags2 = "Tags no identificados"
            find = [id_post, imagen, artista, tags2]
            print(find)
            return find          
            
        except Exception as ex:
            print(ex)
            find[0] = "Tag no encontrado, prueba verificando parentesis, (ej: (series)) o barras (ej: /)"
            return find

HID_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def _hid_trailing_num(title):
    m = re.search(r'\s+(\d+)\s*$', title)
    return int(m.group(1)) if m else 0

def hIdSearch(busqueda):
    try:
        query = busqueda.replace('+', ' ').strip()
        resp = requests.get(f"https://hentai-id.tv/?s={busqueda}", headers=HID_HEADERS)
        if resp.status_code != 200:
            logger.warning(f"hIdSearch '{busqueda}': HTTP {resp.status_code}")
            return None
        soup = BeautifulSoup(resp.text, 'html.parser')
        container = soup.find('div', class_='col-lg-9')
        if not container:
            logger.warning(f"hIdSearch '{busqueda}': contenedor de resultados no encontrado")
            return None
        results = [
            (a.get('href'), a.get_text(strip=True))
            for a in container.find_all('a', href=True)
            if 'hentai-id.tv' in a.get('href', '') and a.get_text(strip=True)
        ]
        if not results:
            return None
        if len(results) == 1:
            return results[0][0]
        # Ordena: sin número = primero (0), luego 2, 3, 4...
        results.sort(key=lambda x: _hid_trailing_num(x[1]))
        # Si la búsqueda termina en número, busca el resultado con ese número
        m = re.search(r'\s+(\d+)\s*$', query)
        if m:
            target = int(m.group(1))
            for url, title in results:
                if _hid_trailing_num(title) == target:
                    return url
        return results[0][0]
    except Exception as e:
        logger.error(f"hIdSearch '{busqueda}': {e}")
        return None

def hIdShow(busqueda):
    try:
        url = hIdSearch(busqueda)
        if not url:
            return None
        resp = requests.get(url, headers=HID_HEADERS)
        if resp.status_code != 200:
            logger.warning(f"hIdShow '{url}': HTTP {resp.status_code}")
            return None
        soup = BeautifulSoup(resp.text, 'html.parser')
        cover = ""
        box = soup.find('div', class_='box-entry-body')
        if box:
            img = box.find('img')
            if img:
                cover = img.get('src', '')
        keys, values = [], []
        table = soup.find('table', class_='table-striped')
        if table:
            for row in table.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) >= 2:
                    keys.append(cells[0].get_text(strip=True).rstrip(':'))
                    values.append(cells[1].get_text(strip=True))
        return [[url, cover], keys, values]
    except Exception as e:
        logger.error(f"hIdShow '{busqueda}': {e}")
        return None

def SCP_Search(busqueda: str = "173") -> list:
    url = f'https://scp-wiki.wikidot.com/scp-{busqueda}'
    logger.info(f'SCP GET {url}')
    try:
        resp = requests.get(url, timeout=12)
    except Exception as e:
        logger.error(f'SCP request error: {e}')
        return ['', '[DATA EXPUNGED]:[DATA EXPUNGED]']
    logger.info(f'SCP status {resp.status_code} | final url: {resp.url}')
    if resp.status_code == 404:
        return ['', '[DATA EXPUNGED]:[DATA EXPUNGED]',
                '[DATA EXPUNGED]:PARA UNA VERSION ACTUALIZADA CONTACTA CON EL DOCTOR [REDACTED]']
    if resp.status_code != 200:
        logger.error(f'SCP unexpected status {resp.status_code}')
        return ['', '[DATA EXPUNGED]:[DATA EXPUNGED]']

    soup = BeautifulSoup(resp.text, 'html.parser')
    result = []

    # Imagen: buscar en scp-image-block, luego cualquier img del contenido
    def _norm_url(src: str) -> str:
        if src.startswith('//'):
            return 'https:' + src
        if src.startswith('http://'):
            return 'https://' + src[7:]
        if src.startswith('/'):
            return 'https://scp-wiki.wikidot.com' + src
        return src

    img_url = ''
    content = soup.find('div', id='page-content')

    img_block = soup.find('div', class_='scp-image-block')
    if img_block:
        img_tag = img_block.find('img')
        logger.info(f'SCP image-block found, img tag: {img_tag}')
        if img_tag:
            src = img_tag.get('src') or img_tag.get('data-src', '')
            if src:
                img_url = _norm_url(src)

    if not img_url and content:
        for img in content.find_all('img'):
            src = img.get('src') or img.get('data-src', '')
            if src and not src.endswith('.gif'):
                img_url = _norm_url(src)
                logger.info(f'SCP image fallback: {img_url!r}')
                break

    SCP_LOGO = 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/SCP_Foundation_%28emblem%29.svg/200px-SCP_Foundation_%28emblem%29.svg.png'
    if not img_url or 'wdfiles.com' in img_url:
        img_url = SCP_LOGO
    logger.info(f'SCP image final: {img_url!r}')
    result.append(img_url)

    # Campos de texto del artículo
    if content:
        for p in content.find_all('p', limit=8):
            text = re.sub(r'\s+', ' ', p.get_text(' ', strip=True)).strip()
            if text:
                result.append(translate(text))
    logger.info(f'SCP result count: {len(result)} items')
    return result if len(result) > 1 else ['', '[DATA EXPUNGED]:[DATA EXPUNGED]']

def reporteDivisa(monto = 1, desde = "USD", hasta = "CLP"):
    url = "https://openexchangerates.org/api/latest.json?app_id={}".format(os.environ.get('OPEN_EXCHANGE'))
    resp = requests.get(url)
    print(resp.status_code)

    # http_respone 200 means OK status
    if resp.status_code == 200:
        resultado = json.loads(resp.content)
        try:
            if desde == "USD":
                rate_desde = 1
            else:
                rate_desde = resultado["rates"][desde]
            if hasta == "USD":
                rate_hasta = 1
            else:
                rate_hasta = resultado["rates"][hasta]
            
            resultado = conversion.divisa(monto,float(rate_desde),float(rate_hasta))
            find = [round(rate_desde,2),round(rate_hasta,2),resultado]
            print(find)
            return find
        except:
            find = [desde,hasta,"No se encontró moneda consultada"]
            print(find)
            return find
    else:
        find = [desde,hasta,"No se pudo acceder al conversor"]
        print(find)


# ── PokéAPI ──────────────────────────────────────────────────────────────────

_POKEAPI = "https://pokeapi.co/api/v2"
_POKEMON_COUNT = 1025  # Gen 9 (Paldea)

def pokemonSearch(busqueda: str, lang: str = "es"):
    query = busqueda.strip().lower()
    if query == "random":
        query = str(random.randint(1, _POKEMON_COUNT))
    query = query.replace(" ", "-")

    resp = requests.get(f"{_POKEAPI}/pokemon/{query}", timeout=10)
    if resp.status_code == 404:
        # Algunos Pokémon requieren el nombre de forma exacto (ej: giratina-altered).
        # Consultamos la especie para obtener la variedad por defecto.
        species_fallback = requests.get(f"{_POKEAPI}/pokemon-species/{query}", timeout=10)
        if species_fallback.status_code != 200:
            return None
        varieties = species_fallback.json().get("varieties", [])
        default = next((v["pokemon"]["name"] for v in varieties if v["is_default"]), None)
        if not default:
            return None
        resp = requests.get(f"{_POKEAPI}/pokemon/{default}", timeout=10)
    if resp.status_code != 200:
        return None
    data = resp.json()

    flavor = ""
    species_resp = requests.get(data["species"]["url"], timeout=10)
    if species_resp.status_code == 200:
        entries = species_resp.json().get("flavor_text_entries", [])
        # Busca primero en el idioma del servidor, luego en inglés como fallback
        for target_lang in (lang, "en"):
            for entry in entries:
                if entry["language"]["name"] == target_lang:
                    flavor = entry["flavor_text"].replace("\n", " ").replace("\f", " ")
                    break
            if flavor:
                break
        # Si no había entrada nativa pero hay texto en inglés, traduce
        if flavor and lang != "en" and all(
            entry["language"]["name"] != lang
            for entry in entries
        ):
            flavor = translate(flavor, dest=lang)

    image = (
        (data["sprites"].get("other") or {})
        .get("official-artwork", {})
        .get("front_default")
        or data["sprites"].get("front_default", "")
    )

    return {
        "name": data["name"].replace("-", " ").title(),
        "dex": data["id"],
        "types": [t["type"]["name"].capitalize() for t in data["types"]],
        "abilities": [a["ability"]["name"].replace("-", " ").title() for a in data["abilities"] if not a["is_hidden"]],
        "hidden": [a["ability"]["name"].replace("-", " ").title() for a in data["abilities"] if a["is_hidden"]],
        "stats": {s["stat"]["name"]: s["base_stat"] for s in data["stats"]},
        "image": image,
        "flavor": flavor,
        "height": data["height"] / 10,
        "weight": data["weight"] / 10,
    }


def pokemonByType(api_type: str, lang: str = "es"):
    type_resp = requests.get(f"{_POKEAPI}/type/{api_type}", timeout=10)
    if type_resp.status_code != 200:
        return None
    pokemon_list = type_resp.json().get("pokemon", [])
    base = []
    for p in pokemon_list:
        url = p["pokemon"]["url"].rstrip("/")
        try:
            pid = int(url.split("/")[-1])
            if 1 <= pid <= _POKEMON_COUNT:
                base.append(p["pokemon"]["name"])
        except (ValueError, IndexError):
            pass
    if not base:
        return None
    return pokemonSearch(random.choice(base), lang=lang)


# ── VNDB ──────────────────────────────────────────────────────────────────────

_VNDB_API = "https://api.vndb.org/kana"

_VN_PLATFORMS = {
    "win": "Windows", "lin": "Linux", "mac": "macOS", "web": "Web",
    "and": "Android", "ios": "iOS", "xbo": "Xbox", "ps5": "PS5",
    "ps4": "PS4", "ps3": "PS3", "psv": "PS Vita", "swi": "Switch",
    "nds": "DS", "mob": "Mobile",
}

def _strip_vndb_markup(text: str) -> str:
    text = re.sub(r'\[spoiler\].*?\[/spoiler\]', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'\[url=[^\]]*\](.*?)\[/url\]', r'\1', text, flags=re.DOTALL)
    text = re.sub(r'\[[^\]]*\]', '', text)
    return text.strip()


def vnSearch(busqueda: str):
    resp = requests.post(
        f"{_VNDB_API}/vn",
        json={
            "filters": ["search", "=", busqueda],
            "fields": "title, alttitle, image.url, image.sexual, description, released, rating, length_minutes, tags.name, platforms, languages",
            "results": 1,
            "sort": "searchrank",
        },
        headers={"Content-Type": "application/json"},
        timeout=10,
    )
    if resp.status_code != 200:
        return None
    results = resp.json().get("results", [])
    if not results:
        return None
    vn = results[0]

    length = vn.get("length_minutes")
    if length:
        h, m = divmod(length, 60)
        length_str = f"{h}h {m}m" if h else f"{m}m"
    else:
        length_str = "—"

    desc = vn.get("description") or ""
    desc = _strip_vndb_markup(desc)
    if len(desc) > 500:
        desc = desc[:497] + "..."

    rating = vn.get("rating")
    rating_str = f"{rating / 10:.1f}/10" if rating else "—"

    image_obj = vn.get("image") or {}
    image_url = image_obj.get("url", "") if image_obj.get("sexual", 1) == 0 else ""

    return {
        "title": vn.get("title", "—"),
        "alttitle": vn.get("alttitle") or "",
        "image": image_url,
        "description": desc,
        "released": vn.get("released") or "—",
        "rating": rating_str,
        "length": length_str,
        "tags": [t["name"] for t in (vn.get("tags") or [])[:8]],
        "platforms": [_VN_PLATFORMS.get(p, p) for p in (vn.get("platforms") or [])],
        "languages": vn.get("languages") or [],
    }

def triviaQuestion(category_id: int = None) -> dict | None:
    params = {"amount": 1, "type": "multiple", "encode": "url3986"}
    if category_id:
        params["category"] = category_id
    try:
        r = requests.get("https://opentdb.com/api.php", params=params, timeout=10)
        data = r.json()
    except Exception as e:
        logger.error(f'triviaQuestion error: {e}')
        return None
    if data.get("response_code") != 0 or not data.get("results"):
        return None
    q = data["results"][0]
    decode = lambda s: html.unescape(urllib.parse.unquote(s))
    return {
        "question":   decode(q["question"]),
        "correct":    decode(q["correct_answer"]),
        "incorrect":  [decode(a) for a in q["incorrect_answers"]],
        "difficulty": q["difficulty"],
        "category":   decode(q["category"]),
    }


def horoscopoSearch(sign: str) -> dict | None:
    try:
        r = requests.get(
            'https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily',
            params={'sign': sign, 'day': 'today'},
            timeout=10,
        )
        data = r.json()
        if not data.get('success'):
            return None
        return {'sign': sign, 'date': data['data']['date'], 'text': data['data']['horoscope_data']}
    except Exception as e:
        logger.error(f'horoscopoSearch error: {e}')
        return None


def personajeSearch(query: str) -> dict | None:
    try:
        r = requests.get(
            'https://api.jikan.moe/v4/characters',
            params={'q': query, 'limit': 1},
            timeout=10,
        )
        data = r.json()
        if not data.get('data'):
            return None
        c = data['data'][0]
        anime_list = [a['anime']['title'] for a in c.get('anime', [])[:4]]
        return {
            'name':  c['name'],
            'kanji': c.get('name_kanji', ''),
            'image': c['images']['jpg']['image_url'],
            'url':   c['url'],
            'favs':  c.get('favorites', 0),
            'anime': anime_list,
            'about': (c.get('about') or '')[:400],
        }
    except Exception as e:
        logger.error(f'personajeSearch error: {e}')
        return None


def peliculaSearch(titulo: str) -> dict | None:
    key = os.getenv('OMDB_KEY', '')
    if not key:
        return None
    try:
        r = requests.get(
            'http://www.omdbapi.com/',
            params={'t': titulo, 'apikey': key, 'plot': 'short'},
            timeout=10,
        )
        d = r.json()
        if d.get('Response') == 'False':
            return None
        clean = lambda v: v if v and v != 'N/A' else ''
        return {
            'title':    clean(d.get('Title')),
            'year':     clean(d.get('Year')),
            'genre':    clean(d.get('Genre')),
            'director': clean(d.get('Director')),
            'actors':   clean(d.get('Actors')),
            'plot':     clean(d.get('Plot')),
            'poster':   clean(d.get('Poster')),
            'imdb':     clean(d.get('imdbRating')),
            'runtime':  clean(d.get('Runtime')),
            'country':  clean(d.get('Country')),
        }
    except Exception:
        return None


def spoonacularSearch(busqueda: str, number: int = 5) -> list | None:
    key = os.getenv('SPOONACULAR_KEY', '')
    if not key:
        return None
    try:
        query = busqueda
        try:
            en = translate(busqueda, dest='en')
            if en.strip():
                query = en
        except Exception:
            pass
        r = requests.get(
            'https://api.spoonacular.com/recipes/findByIngredients',
            params={'ingredients': query, 'number': number, 'ranking': 1,
                    'ignorePantry': True, 'apiKey': key},
            timeout=10,
        )
        data = r.json()
        if not isinstance(data, list) or not data:
            return None
        return [{'id': m['id'], 'title': m['title'], 'image': m.get('image', '')}
                for m in data]
    except Exception:
        return None


def spoonacularDetail(recipe_id: int) -> dict | None:
    key = os.getenv('SPOONACULAR_KEY', '')
    if not key:
        return None
    try:
        r = requests.get(
            f'https://api.spoonacular.com/recipes/{recipe_id}/information',
            params={'apiKey': key},
            timeout=10,
        )
        d = r.json()
        seen_ids: set = set()
        ings: list = []
        for i in d.get('extendedIngredients', []):
            iid = i.get('id')
            if iid in seen_ids:
                continue
            seen_ids.add(iid)
            text = i.get('original') or i.get('originalString') or ''
            if text:
                ings.append(text)
        # Fuente primaria: texto crudo de la página (más fiable para blogs/fuentes no estándar)
        raw_html = d.get('instructions') or ''
        if raw_html:
            raw_text = BeautifulSoup(raw_html, 'html.parser').get_text('\n', strip=True).strip()
            raw_text = re.sub(r'\n{3,}', '\n\n', raw_text)
        else:
            raw_text = ''
        # Fuente secundaria: pasos analizados por Spoonacular (bueno para recetas de sitios conocidos)
        steps = []
        for block in d.get('analyzedInstructions', []):
            for step in block.get('steps', []):
                s = step.get('step', '').strip()
                if s:
                    steps.append(f"{step['number']}. {s}")
        analyzed = '\n'.join(steps)
        instructions = (raw_text or analyzed)[:900]
        return {
            'title':        d.get('title', ''),
            'image':        d.get('image', ''),
            'readyIn':      d.get('readyInMinutes', 0),
            'servings':     d.get('servings', 0),
            'ingredients':  ings,
            'instructions': instructions,
            'url':          d.get('sourceUrl', ''),
        }
    except Exception:
        return None


def raeSearch(palabra: str) -> dict | None:
    try:
        _headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'es-ES,es;q=0.9',
            'Referer': 'https://dle.rae.es/',
        }
        # Normalizar a la forma canónica con tildes vía autocomplete
        keys_r = requests.get('https://dle.rae.es/srv/keys', params={'q': palabra.strip().lower()},
                              headers={**_headers, 'Accept': 'application/json',
                                       'X-Requested-With': 'XMLHttpRequest'}, timeout=8)
        if keys_r.status_code == 200 and keys_r.text.strip().startswith('['):
            suggestions = json.loads(keys_r.text)
            if suggestions:
                palabra = suggestions[0].split('|')[0]
        url = f'https://dle.rae.es/{urllib.parse.quote(palabra)}'
        r = requests.get(url, headers={**_headers, 'Accept': 'text/html,application/xhtml+xml'}, timeout=10)
        if r.status_code != 200:
            return None
        soup = BeautifulSoup(r.text, 'html.parser')
        h1 = soup.find('h1', class_='c-page-header__title')
        titulo = h1.get_text(strip=True) if h1 else palabra
        defs = []
        for div in soup.find_all('div', class_='c-definitions__item'):
            texto = div.get_text(' ', strip=True)
            if texto:
                defs.append(texto)
        if not defs:
            return None
        return {'palabra': titulo, 'definiciones': defs[:5], 'url': url}
    except Exception:
        return None
