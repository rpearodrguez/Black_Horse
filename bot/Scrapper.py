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

#Game Scrapping
def steamUrlSearch(urlb=""):
    # url = the target we want to open
    url = "https://store.steampowered.com/search/?term=" + urlb + "&category1=998&ignore_preferences=1"
    # open with GET method
    resp = requests.get(url)

    # http_respone 200 means OK status
    if resp.status_code == 200:
        # we need a parser,Python built-in HTML parser is enough .
        soup = BeautifulSoup(resp.text, 'html.parser')
        #busca el estilo del objeto con la clase .search_result_row
        #l = soup.find("div", {"class": "search_pagination"})
        #style = soup.find("a", {"class": "search_pagination"})['style']
        #print("Contenido de la pagina: {}".format(soup.contents))
        
        for i in soup.findAll("a", {"class": "search_result_row"}, limit=1):
            #print("objeto de la clase search_result_row: {}".format(i))
            try:
                urla = i.get('href')
                print(urla)
                return urla
            except:
                print("No se pudo rescatar información de la pagina")
                return url

    # Find posee los atributos (en el mismo orden) Título, Sumario, Puntaje, Episodios, imagen de fondo
    return url

def steamDataSearch(busqueda):
    url = steamUrlSearch(busqueda)
    resp = requests.get(url)

    # http_respone 200 means OK status
    if resp.status_code == 200:
        print("Successfully opened the web page")
        print("Este es el sumario del juego solicitado :-\n")
        find = ["Portada", "Nombre", "Descripcion", "Desarrollador", "Algun día", "Genero", "Demasiado malo para ser puntuado", "No es gratis, pero no tengo idea"]

        # we need a parser,Python built-in HTML parser is enough .
        soup = BeautifulSoup(resp.text, 'html.parser')
        #print(soup.contents)
        # l is the list which contains all the text i.e news
        glance = soup.find("div", {"class": "glance_ctn"})
        meta = soup.find("div", {"class": "game_meta_data"})
        price = soup.find("div", {"id": "game_area_purchase"})
        # now we want to print only the text part of the anchor.
        # find all the elements of a, i.e anchor
        try:
            for i in glance.findAll("img", {"class": "game_header_image_full"}, limit=1):
                try:
                    #Portada
                    find[0] = i.get('src')
                    print(find[0])
                except:
                    pass




            for i in meta.findAll("div", {"class": "details_block"}, limit=1):
                try:
                    titulo = i.text.split("\n")
                    print(titulo)
                    if titulo[1][7:] != "":
                        #Nombre
                        find[1] = titulo[1][7:]

                    if titulo[5] != "":
                        #Desarrollador
                        find[3] = titulo[5]

                    if titulo[11][14:] != "":
                        #Fecha de lanzamiento
                        find[4] = titulo[11][14:]

                    if titulo[2][7:] != "":
                        #Genero
                        find[5] = titulo[2][7:]

                except:
                    pass

            for i in meta.findAll("div", {"id": "game_area_metascore"}, limit=1):
                try:
                    titulo = i.text.split("\t")
                    print(titulo)
                    if titulo[10] != "":
                        #Metascore
                        find[6] = titulo[10]

                except:
                    pass

            for i in glance.findAll("div", {"class": "game_description_snippet"}, limit=1):
                try:
                    titulo = i.text.split("\t")
                    print(titulo)
                    if titulo[8] != "":
                        #Descripcion
                        
                        find[2] = translate(titulo[8])
                        print(find[2])

                except:
                    pass

            for i in price.findAll("div", {"class": "game_purchase_price"}, limit=1):
                try:
                    titulo = i.text.split("\t")
                    print(titulo)
                    if titulo[7] != "":
                        #Precio
                        find[7] = titulo[7]

                except:
                    pass

        except:
            find[0] = url
        # Find posee los atributos (en el mismo orden) 0=Portada, 1=Nombre, 2=Descripcion , 3=Desarrollador, 4=Lanzamiento, 5=Genero, 6=Metacritic, 7=Precio
        print(find)
        return find

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

def imgSearch(search_term="busqueda"):
    try:
        imagenes = ["resultado no encontrado"]
        url = "https://www.googleapis.com/customsearch/v1?cx={}&key={}&q={}&searchType=image&safe=active".format(os.environ.get('ID_BUSCADOR_GOOGLE'),os.environ.get('GOOGLE_CUSTOM_SEARCH'), search_term)
        # open with GET method
        resp = requests.get(url)
        # http_respone 200 means OK status
        if resp.status_code == 200:
            gifs = json.loads(resp.content)
            imagenes[0] = gifs["items"][0]["link"]
            print(imagenes[0])
        return imagenes[0]
    except:
        pass

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

def SCP_Search(busqueda="5998"):
    url = "http://www.scp-wiki.net/scp-{}".format(busqueda)
    print(url)
    resp = requests.get(url)
    print (resp)

    # http_respone 200 means OK status
    if resp.status_code == 200:
        print("Successfully opened the web page")
        print("Este es el sumario del meme solicitado :-\n")

        # we need a parser,Python built-in HTML parser is enough .
        soup = BeautifulSoup(resp.text, 'html.parser')
        # l is the list which contains all the text i.e news
        scpImage = soup.find("div", {"class": "scp-image-block"})
        scpText = soup.find("div", {"id": "page-content"})
        # now we want to print only the text part of the anchor.
        # find all the elements of a, i.e anchor
        scpResult = []
        try:
            print("inicia busqueda de contenido")
            try:
                for i in scpImage.findAll("a", {"class": ""}, limit=10):
                    try:
                        #Portada
                        scpResult.append(i.get('href'))
                        print(scpResult[0])
                        
                    except:
                        pass
                print("Revisión 1: Imagen encontrada {}".format(scpResult))
                if scpResult == []:
                    try: 
                        for i in scpImage.findAll("img", {"class": "image"}):
                            scpResult.append(i['src'])
                            print(scpResult[0])
                    except:
                        pass
            except:
                scpResult.append("http://scp-wiki.wdfiles.com/local--files/component%3Atheme/logo.png")
                pass
            
            print("Revisión 2: Imagen encontrada {}".format(scpResult))
            for i in scpText.find_all("p", limit=5):
                try:
                    if "\n" in i.text:
                        contenido = i.text.split("\n")
                        scpResult.append(translate(contenido[0]))
                        scpResult.append(translate(contenido[2]))
                    else:
                        scpResult.append(translate(i.text))
                except:
                    pass
            print("Revisión 3: Contenido encontrado {}".format(scpResult))
        except:
            pass
        
        return scpResult
    
    elif resp.status_code == 404:
        return ["[DATA EXPUNGED]","[DATA EXPUNGED]:[DATA EXPUNGED]","[DATA EXPUNGED]:PARA UNA VERSION ACTUALIZADA DEL INFORME CONTACTA CON EL DOCTOR [REDACTED]"]

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