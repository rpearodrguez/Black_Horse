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
