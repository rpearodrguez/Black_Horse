import json
import os
import random
import re
import urllib.parse
import conversion
from googletrans import Translator

import requests
from Black_Kevin import get_secret
from bs4 import BeautifulSoup

translator = Translator()


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
                portada = "https://www.stickhorse.cl/wp-content/uploads/2019/11/SH.png"
            sinopsis = re.sub('\n'," ",resultado["data"][0]["attributes"]["synopsis"])
            sinopsis = re.sub(r'\[.*?\]'," ",sinopsis)
            sinopsis = re.sub('\r'," ",sinopsis)
            if sinopsis == 'No synopsis has been added for this manga yet.Click here to update this information.':
                sinopsis = "Sinopsis no encontrada"
            else:
                sinopsis = translator.translate(sinopsis,dest='es').text[:1020]+"..."
            lanzamiento = resultado["data"][0]["attributes"]["startDate"]
            if str(lanzamiento) == "" or str(lanzamiento) == "None":
                lanzamiento = "No hay fecha de lanzamiento"
            termino = resultado["data"][0]["attributes"]["endDate"]
            if str(termino) == "" or str(termino) == "None":
                termino = "No hay fecha de termino"
            terminado = translator.translate(resultado["data"][0]["attributes"]["status"],dest='es').text
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
                    generos += translator.translate(genero["attributes"]["name"],dest='es').text+", " 
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
                portada = "https://www.stickhorse.cl/wp-content/uploads/2019/11/SH.png"
            sinopsis = re.sub('\n'," ",resultado["data"][0]["attributes"]["synopsis"])
            sinopsis = re.sub(r'\[.*?\]'," ",sinopsis)
            sinopsis = re.sub('\r'," ",sinopsis)
            if sinopsis == 'No synopsis has been added for this manga yet.Click here to update this information.' or sinopsis == '':
                sinopsis = "Sinopsis no encontrada"
            else:
                sinopsis = translator.translate(sinopsis,dest='es').text[:1020]+"..."
            lanzamiento = resultado["data"][0]["attributes"]["startDate"]
            if str(lanzamiento) == "" or str(lanzamiento) == "None":
                lanzamiento = "Lanzamiento no encontrado"
            termino = resultado["data"][0]["attributes"]["endDate"]
            if str(termino) == "" or str(termino) == "None":
                termino = "Fecha de termino no encontrada"
            terminado = translator.translate(resultado["data"][0]["attributes"]["status"],dest='es').text
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
                    generos += translator.translate(genero["attributes"]["name"],dest='es').text+", "
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
                        
                        find[2] = translator.translate(titulo[8],dest='es').text
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
        url = "https://www.googleapis.com/customsearch/v1?cx={}&key={}&q={}&searchType=image&safe=active".format(get_secret('ID_BUSCADOR_GOOGLE'),get_secret('GOOGLE_CUSTOM_SEARCH'), search_term)
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
    url = "https://danbooru.donmai.us/posts.json?login={}&api_key={}&limit=1&tags={}&random=true".format(get_secret('DANBOORU_LOGIN'),get_secret('DANBOORU_KEY'),busqueda)
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
    if busqueda.lower() in ["ahegao","anal","ashikoki","bakunyuu","bukkake","bestiality","bondage","chikan","comedia","escolar","fantasia","futanari","gangbang","harem","hipnosis","incesto","milf","lolicon","nakadashi","netorare","netorase","netori","orgia","paizuri","romance","shota","tentaculos","terror","trap","virgenes","violacion","yuri","yaoi"]:
        url = "https://hentai-id.tv/category/{}/?archivos=h1".format(busqueda)
    elif busqueda.lower() == "degeneracion+mental":
        url = "https://hentai-id.tv/category/degeneracion-mental/?archivos=h1"
    else:
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
            for i in scpText.findAll("p", {"class": ""}, limit=5):
                try:
                    if "\n" in i.text:
                        contenido = i.text.split("\n")
                        scpResult.append(translator.translate(contenido[0],dest='es').text)
                        scpResult.append(translator.translate(contenido[2],dest='es').text)
                    else:
                        scpResult.append(translator.translate(i.text,dest='es').text)
                except:
                    pass
            print("Revisión 3: Contenido encontrado {}".format(scpResult))
        except:
            pass
        
        return scpResult
    
    elif resp.status_code == 404:
        return ["[DATA EXPUNGED]","[DATA EXPUNGED]:[DATA EXPUNGED]","[DATA EXPUNGED]:PARA UNA VERSION ACTUALIZADA DEL INFORME CONTACTA CON EL DOCTOR [REDACTED]"]

def reporteDivisa(monto = 1, desde = "USD", hasta = "CLP"):
    url = "https://openexchangerates.org/api/latest.json?app_id={}".format(get_secret('OPEN_EXCHANGE'))
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
        return find