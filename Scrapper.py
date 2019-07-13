import random
import requests
from bs4 import BeautifulSoup
import re

def animeScrap(urlb=""):
    # url = the target we want to open
    url = "https://animaifu.com/anime/search?q=" + urlb
    # open with GET method
    resp = requests.get(url)

    # http_respone 200 means OK status
    if resp.status_code == 200:
        print("Successfully opened the web page")
        print("Este es el sumario del anime solicitado :-\n")
        find = ["N/E", "N/E", "Ni idea", "Un Chingo", "N/E"]

        # we need a parser,Python built-in HTML parser is enough .
        soup = BeautifulSoup(resp.text, 'html.parser')
        style = soup.find("a", {"class": "unit"})['style']

        # l is the list which contains all the text i.e news
        l = soup.find("div", {"class": "anime-list-2"})
        ptr = re.search("http.*[)]", style)
        # now we want to print only the text part of the anchor.
        # find all the elements of a, i.e anchor
        find[4] = style[ptr.start():ptr.end()-13]
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
                if len(meta[0])==3:
                    print(meta)
                    find[2] = meta[0]
                    print(find[2])
            except:
                pass

            try:
                episodes = meta[meta.index("Episodios") - 1]
                if (episodes):
                    find[3] = episodes
                    print("Espisodios"+find[3])
            except:
                pass



    # Find posee los atributos (en el mismo orden) Título, Sumario, Puntaje, Episodios
    print(find)
    return find


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

def steamUrlSearch(urlb=""):
    # url = the target we want to open
    url = "https://store.steampowered.com/search/?term=" + urlb + "&category1=998"
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
        for i in soup.findAll("a", {"class": "search_result_row"}, limit=1):
            try:
                url = i.get('href')
                print(url)
            except:
                pass

    # Find posee los atributos (en el mismo orden) Título, Sumario, Puntaje, Episodios, imagen de fondo
    return url

def steamDataSearch(busqueda):
    url = steamUrlSearch(busqueda)
    resp = requests.get(url)

    # http_respone 200 means OK status
    if resp.status_code == 200:
        print("Successfully opened the web page")
        print("Este es el sumario del juego solicitado :-\n")
        find = ["Portada", "Nombre", "Descripcion", "Desarrollador", "Lanzamiento", "Genero", "Puntaje Metacritic", "Precio"]

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
                    #Nombre
                    find[1] = titulo[1][7:]
                    #Desarrollador
                    find[3] = titulo[5]
                    # Fecha de lanzamiento
                    find[4] = titulo[11][14:]
                    #Genero
                    find[5] = titulo[2][7:]

                except:
                    pass

            for i in meta.findAll("div", {"id": "game_area_metascore"}, limit=1):
                try:
                    titulo = i.text.split("\t")
                    print(titulo)
                    #Metascore
                    find[6] = titulo[10]

                except:
                    pass

            for i in glance.findAll("div", {"class": "game_description_snippet"}, limit=1):
                try:
                    titulo = i.text.split("\t")
                    print(titulo)
                    #Descripcion
                    find[2] = titulo[8]

                except:
                    pass

            for i in price.findAll("div", {"class": "game_purchase_price"}, limit=1):
                try:
                    titulo = i.text.split("\t")
                    print(titulo)
                    #Descripcion
                    find[7] = titulo[7]

                except:
                    pass

        except:
            find[0] = url
        # Find posee los atributos (en el mismo orden) Título, Sumario, Puntaje, Episodios
        print(find)
        return find

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