import json
import os
import random
from Black_Kevin import get_secret

import requests


def reactionImage(feel=""):

    imagenes = [""]
    if feel == "escobazo":
        imagenes = ["https://media.giphy.com/media/l2Je4FbOimhxM6mE8/giphy.gif", 
                    "https://media.discordapp.net/attachments/476576031315066880/676602221571473418/tenor.gif",
                    "https://cdn.discordapp.com/attachments/441806502215548931/852009803684642876/doom-escobazos.gif",
                    "https://cdn.discordapp.com/attachments/441806502215548931/852009811188645888/neo-escobazo.gif"]
    
    if feel == "plaf":
        imagenes = ["http://stickhorse.cl/wp-content/uploads/2021/07/unknown.png",
                    "http://stickhorse.cl/wp-content/uploads/2021/07/Plaf.png"]


    if feel == "abrazo":
        search_term = "anime hug"

    if feel == "angry":
        search_term = "Angry Anime Girl"

    if feel == "pout":
        search_term = "Pouting anime Girl"

    if feel == "escapar":
        search_term = "anime run away"

    if feel == "run":
        search_term = "anime run"

    if feel == "smile":
        search_term = "anime smile"

    if feel == "lamer":
        search_term = "anime lick"

    if feel == "pat":
        search_term = "anime head pat"

    if feel == "jojo":
        search_term = "jojo pose"

    if feel == "suicide":
        search_term = "anime suicide"
    
    if feel == "slap":
        search_term = "anime slap"

    if feel == "kiss":
        search_term = "anime kiss"
    
    if feel == "food":
        search_term = "anime feed"

    if feel == "kickbutt":
        search_term = "anime kick"

    if feel == "smug":
        search_term = "anime smug"

    if feel == "spin":
        search_term = "anime spinning"

    if feel == "dance":
        search_term = "anime dance"
    
    if feel == "caramelldansen":
        search_term = "caramelldansen"

    if feel == "baka":
        search_term = "anime angry girl idiot"

    if feel == "blush":
        search_term = "anime girl blush"

    if feel == "shy":
        search_term = "anime shy"

    if feel == "tsundere":
        search_term = "tsundere"

    if feel == "lewd":
        search_term = "anime lewd"
    
    if feel == "bite":
        search_term = "anime bite"
    
    if feel == "sleep":
        search_term = "anime sleep"
    
    if feel == "sleepy":
        search_term = "anime sleepy"
        
    if feel == "cry":
        search_term = "anime sad cry"
        
    if feel == "happy":
        search_term = "anime happy"

    if feel == "cookie":
        search_term = "anime cookie eat"
    

    if feel !=  "escobazo":
        url = "https://api.tenor.com/v1/random?key={}&q={}&locale=en_US&contentfilter=off&media_filter=minimal&ar_range=wide&limit=1".format(get_secret('TENOR_KEY'), search_term)
        # open with GET method
        resp = requests.get(url)
        # http_respone 200 means OK status
        if resp.status_code == 200:
            gifs = json.loads(resp.content)
            print(gifs)
            imagenes[0] = gifs["results"][0]["media"][0]["gif"]["url"]
            print(imagenes[0])
        else:
            imagenes[0] = "https://media.tenor.com/images/ff8a2ea033a2f87a35d895eebd09cbe8/tenor.gif"
            
        
    randImage = random.randint(0, len(imagenes)-1)

    return imagenes[randImage]
