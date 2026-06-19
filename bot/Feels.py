import os
import random

import requests


def reactionImage(feel=""):

    ESCOBAZO_CLASSIC = "https://media.giphy.com/media/l2Je4FbOimhxM6mE8/giphy.gif"

    imagenes = [""]
    if feel == "escobazo":
        search_term = "broom hit anime"

    if feel == "plaf":
        search_term = "anime slap face"


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
    

    if feel == "escobazo" and random.randint(1, 7) == 1:
        imagenes[0] = ESCOBAZO_CLASSIC
    else:
        resp = requests.get("https://api.giphy.com/v1/gifs/search", params={
            "api_key": os.environ.get('GIPHY_KEY'),
            "q": search_term,
            "limit": 10,
            "rating": "pg-13"
        })
        if resp.status_code == 200:
            data = resp.json().get("data", [])
            if data:
                imagenes[0] = random.choice(data)["images"]["original"]["url"]
        if not imagenes[0]:
            imagenes[0] = "https://media.giphy.com/media/3o7TKMt1VVNkHV2PaE/giphy.gif"
            
        
    randImage = random.randint(0, len(imagenes)-1)

    return imagenes[randImage]
