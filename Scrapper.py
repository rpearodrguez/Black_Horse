import random
import requests
from boto.s3.connection import S3Connection
from bs4 import BeautifulSoup
import re
import json
import os

#Anime Scrapping
def animeScrap(urlb=""):
    # url = the target we want to open
    if urlb in "accion , infantil , sobrenatural , josei , superpoderes , aventura , juegos , suspenso , carreras , magia , terror , mecha , vampiros , comedia , militar , yaoi , demencia , misterio , yuri , demonios , musica , deportes , parodia , drama , psicologico , ecchi , escolares , romance , espacial , samurai , fantasia , seinen , harem , shoujo , historico , shounen ":
        url = "https://animeflv.chrismichael.now.sh/api/v1/Genres/{}/rating/1".format(urlb)
        print(url)
    elif urlb == "artes+marciales":
        url = "https://animeflv.chrismichael.now.sh/api/v1/Genres/artes-marciales/rating/1"
        print(url)
    elif urlb == "ciencia+ficcion":
        url = "https://animeflv.chrismichael.now.sh/api/v1/Genres/ciencia-ficcion/rating/1"
        print(url)
    elif urlb == "recuentos+de+la+vida,":
        url = "https://animeflv.chrismichael.now.sh/api/v1/Genres/recuentos-de-la-vida/rating/1"
        print(url)
    else:
        url = "https://animeflv.chrismichael.now.sh/api/v1/Search/:{}".format(urlb)
        print(url)
    # open with GET method
    resp = requests.get(url)

    # http_respone 200 means OK status
    if resp.status_code == 200:
        
        # we need a parser,Python built-in HTML parser is enough .
        resultado = json.loads(resp.content)
        try:
            rand = random.randint(0,len(resultado["search"])-1)
            titulo = resultado["search"][rand]["title"]                
            portada = resultado["search"][rand]["poster"]
            sinopsis = resultado["search"][rand]["synopsis"]
            lanzamiento = resultado["search"][rand]["debut"]
            tipo = resultado["search"][rand]["type"]
            rating = resultado["search"][rand]["rating"]
            generos =  ", ".join(resultado["search"][rand]["genres"])
            episodios = resultado["search"][rand]["episodes"]
            try:
                episodios = resultado["search"][rand]["episodes"][1]["episode"]
            except:
                pass
            find = [titulo, portada, sinopsis, lanzamiento, tipo, rating, generos, episodios]
            print(find)
            return find
        except KeyError:
            rand = random.randint(0,len(resultado["animes"])-1)
            print(rand)
            titulo = resultado["animes"][rand]["title"]
            print(titulo)
            portada = resultado["animes"][rand]["poster"]
            print(portada)                
            sinopsis = resultado["animes"][rand]["synopsis"]
            print(sinopsis)
            lanzamiento = resultado["animes"][rand]["debut"]
            print(lanzamiento)
            tipo = resultado["animes"][rand]["type"]
            print(tipo)
            rating = resultado["animes"][rand]["rating"]
            print(rating)
            generos =  ", ".join(resultado["animes"][rand]["genres"])
            print(generos)
            episodios = resultado["animes"][rand]["episodes"]
            try:
                episodios = resultado["animes"][rand]["episodes"][1]["episode"]
            except:
                pass
            print(episodios)
            find = [titulo, portada, sinopsis, lanzamiento, tipo, rating, generos, episodios]
            print(find)
            return find
        except:
            find = ["Anime o genero no encontrado"]
            return resultado

            
    # Find posee los atributos (en el mismo orden) Título, Sumario, Puntaje, Episodios
    
#Manga Scrapping
def mangaScrap(urlb=""):
    # url = the target we want to open
    url = "https://animaifu.com/manga/search?q=" + urlb
    # open with GET method
    resp = requests.get(url)

    # http_respone 200 means OK status
    if resp.status_code == 200:
        print("Successfully opened the web page")
        print("Este es el sumario del manga solicitado :-\n")
        find = ["N/E", "N/E", "Ni idea", "Un Chingo", "N/E"]

        # we need a parser,Python built-in HTML parser is enough .
        soup = BeautifulSoup(resp.text, 'html.parser')
        style = soup.find("a", {"class": "unit"})['style']

        # l is the list which contains all the text i.e news
        l = soup.find("div", {"class": "anime-list-2"})
        ptr = re.search("http.*[)]", style)
        # now we want to print only the text part of the anchor.
        # find all the elements of a, i.e anchor
        find[4] = style[ptr.start():ptr.end() - 13]
        print(find[4])

        for i in l.findAll("p", {"class": "summary"}, limit=1):
            try:
                summary = i.text
                find[1] = summary[1:]
                print(find[1])
            except:
                pass

        for i in l.findAll("h3", {"class": "title"}, limit=1):
            try:
                title = i.text
                find[0] = title
                print(find[0])
            except:
                pass

        for i in l.findAll("p", {"class": "meta"}, limit=1):
            meta = i.text
            meta = meta.split()
            try:
                if len(meta[0]) == 3:
                    print(meta)
                    find[2] = meta[0]
                    print(find[2])
            except:
                pass

            try:
                episodes = meta[meta.index("Episodios") - 1]
                if (episodes):
                    find[3] = episodes
                    print("Espisodios" + find[3])
            except:
                pass

    # Find posee los atributos (en el mismo orden) Título, Sumario, Puntaje, Episodios, imagen de fondo
    print(find)
    return find

#Game Scrapping
def steamUrlSearch(urlb=""):
    # url = the target we want to open
    url = "https://store.steampowered.com/search/?term=" + urlb + "&category1=998"
    # open with GET method
    resp = requests.get(url)

    # http_respone 200 means OK status
    if resp.status_code == 200:
        # we need a parser,Python built-in HTML parser is enough .
        soup = BeautifulSoup(resp.text, 'html.parser')
        print(soup)
        #busca el estilo del objeto con la clase .search_result_row
        #l = soup.find("div", {"class": "search_pagination"})

        #style = soup.find("a", {"class": "search_pagination"})['style']
        for i in soup.findAll("a", {"class": "search_result_row"}, limit=1):
            try:
                print(i)
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
                        find[2] = titulo[8]

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
def nhentaiRandomSearch(urlb="https://nhentai.net"):
    # url = the target we want to open
    url = "https://nhentai.net"
    # open with GET method
    resp = requests.get(url)

    # http_respone 200 means OK status
    if resp.status_code == 200:
        print("Successfully opened the web page")
        print("Encontraron resultados :-\n")


        # we need a parser,Python built-in HTML parser is enough .
        soup = BeautifulSoup(resp.text, 'html.parser')
        #busca el estilo del objeto con la clase .search_result_row
        #l = soup.find("div", {"class": "search_pagination"})

        #style = soup.find("a", {"class": "search_pagination"})['style']
        for i in soup.findAll("a", {"class": "cover"}, limit=1):
            try:
                url = i.get('href').split('/')
                print(url)
                randnh = random.randint(1, int(url[2]))
                print(randnh)
                urlFull = "https://nhentai.net/g/"+str(randnh)


            except:
                pass

    # Find posee los atributos (en el mismo orden) Título, Sumario, Puntaje, Episodios, imagen de fondo
    return urlFull

def nhentaiTagSearch(tag="https://nhentai.net"):
    # url = the target we want to open
    url = 'https://nhentai.net/search/?q={}&sort=popular'.format(tag)
    #url = 'https://nhentai.net/search/?q=tag:"{}"&sort=popular'.format(tag)
    # open with GET method
    resp = requests.get(url)

    # http_respone 200 means OK status
    if resp.status_code == 200:
        print("Successfully opened the web page")
        print("Encontraron resultados :-\n")


        # we need a parser,Python built-in HTML parser is enough .
        soup = BeautifulSoup(resp.text, 'html.parser')
        #busca el estilo del objeto con la clase .search_result_row
        #l = soup.find("div", {"class": "search_pagination"})

        #style = soup.find("a", {"class": "search_pagination"})['style']
        if "No results found" in soup.text:
            return "No se encontraron resultados con el tag solicitado"
        
        lista = []

        for i in soup.findAll("a", {"class": "cover"}):
            try:

                url = i.get('href').split('/')
                print(url)
                urlFull = "https://nhentai.net/g/"+str(url[2])
                lista.append(urlFull)


            except:
                pass
        
        randtag = random.randint(0, len(lista)-1)
        return lista[randtag]

    # Find posee los atributos (en el mismo orden) Título, Sumario, Puntaje, Episodios, imagen de fondo

def imgSearch(search_term="busqueda"):

    try:
        imagenes = ["resultado no encontrado"]
        url = "https://www.googleapis.com/customsearch/v1?cx={}&key={}&q={}&searchType=image".format(os.environ.get('ID_BUSCADOR_GOOGLE'),os.environ.get('GOOGLE_CUSTOM_SEARCH'), search_term)
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
    busqueda = "thighs"
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

def hIdSearch(busqueda="oni+chichi"):
    url = "https://hentai-id.tv/?s={}".format(busqueda)
    resp = requests.get(url)
    print (resp)

    # http_respone 200 means OK status
    if resp.status_code == 200:
        print("Successfully opened the web page")
        print("Este es el sumario del meme solicitado :-\n")

        # we need a parser,Python built-in HTML parser is enough .
        soup = BeautifulSoup(resp.text, 'html.parser')
        # l is the list which contains all the text i.e news
        imagen = soup.find("div", {"class": "col-xs-12 col-md-12 col-lg-9 px-3"})
        # now we want to print only the text part of the anchor.
        # find all the elements of a, i.e anchor
        salsa = []
        try:
            for i in imagen.findAll("a", {"class": ""}, limit=10):
                try:
                    #Portada
                    salsa.append(i.get('href'))
                    
                except:
                    pass
        except:
            pass
        print(salsa)
        salsaFinal = salsa[random.randint(0,len(salsa)-1)]
        print(salsaFinal)
        return salsaFinal

def hIdShow(busqueda="oni+chichi"):
    try:
        url = hIdSearch(busqueda)
        resp = requests.get(url)
        print (resp)

        # http_respone 200 means OK status
        if resp.status_code == 200:
            print("Successfully opened the web page")
            print("Este es el sumario del meme solicitado :-\n")

            # we need a parser,Python built-in HTML parser is enough .
            soup = BeautifulSoup(resp.text, 'html.parser')
            # l is the list which contains all the text i.e news
            imagen = soup.find("img", {"class": "img-thumbnail"})
            imagen = imagen.get("src")
            contenido = soup.find("table", {"class": "table table-striped"})
            #el orden del contenido de la tabla es el siguiente: url, imagen, nombre, tags, Fansub, Extra, Secuela, Estudio, Estado, Sinopsis
            contenidoTabla = [url,imagen]
            keys = []
            values = []
            for i in contenido.findAll("td", {"class": "w30"}, limit=10):
                try:
                    keys.append("".join(("".join(i.text.split("\n"))).split("\r")))
                except:
                    pass
            for i in contenido.findAll("td", {"class": "w70"}, limit=10):
                try:
                    values.append("".join(("".join(i.text.split("\n"))).split("\r")))
                except:
                    pass
            
            tablaCompleta = [contenidoTabla,keys,values]
            return tablaCompleta
    except Exception as ex:
        print(ex)
        tablaCompleta = ["Serie no encontrada, soy un inutil, castígame ( ͡° ͜ʖ ͡°)"]
        return tablaCompleta