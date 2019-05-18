import requests
from bs4 import BeautifulSoup

def animeScrap(urlb=""):
    # url = the target we want to open
    url = "https://animaifu.com/anime/search?q=" + urlb
    # open with GET method
    resp = requests.get(url)

    # http_respone 200 means OK status
    if resp.status_code == 200:
        print("Successfully opened the web page")
        print("Este es el sumario del anime solicitado :-\n")
        find = ["", "", "", ""]

        # we need a parser,Python built-in HTML parser is enough .
        soup = BeautifulSoup(resp.text, 'html.parser')

        # l is the list which contains all the text i.e news
        l = soup.find("div", {"class": "anime-list-2"})
        # now we want to print only the text part of the anchor.
        # find all the elements of a, i.e anchor

        for i in l.findAll("p", {"class": "summary"}, limit=1):
            summary = i.text
            find[1] = summary

        for i in l.findAll("h3", {"class": "title"}, limit=1):
            title = i.text
            find[0] = title

        for i in l.findAll("p", {"class": "meta"}, limit=1):
            meta = i.text
            points = meta[1:4]
            episodes = meta[12:]
            find[2] = points
            find[3] = episodes

    # Find posee los atributos (en el mismo orden) Título, Sumario, Puntaje, Episodios
    return find