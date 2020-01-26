import json
import os
import random

import requests
from boto.s3.connection import S3Connection


def reactionImage(feel=""):

    imagenes = [""]
    if feel == "escobazo":
        imagenes = ["https://media.giphy.com/media/l2Je4FbOimhxM6mE8/giphy.gif", "https://www.stickhorse.cl/wp-content/uploads/2020/01/SH-Escobazo-2.gif", "https://www.stickhorse.cl/wp-content/uploads/2020/01/SH-Escobazo-3.gif"]

    if feel == "abrazo":
        search_term = "anime+hug"

    if feel == "lamer":
        search_term = "anime+lick"

    if feel == "pat":
        search_term = "anime+head+pat"

    if feel !=  "escobazo":
        url = "https://api.tenor.com/v1/random?key={}&q={}&locale=en_US&contentfilter=off&media_filter=minimal&ar_range=wide&limit=1".format(os.environ.get('TENOR_KEY'), search_term)
        # open with GET method
        resp = requests.get(url)
        # http_respone 200 means OK status
        if resp.status_code == 200:
            gifs = json.loads(resp.content)
            imagenes[0] = gifs["results"][0]["media"][0]["gif"]["url"]
            print(imagenes[0])
        else:
            imagenes[0] = "https://media.tenor.com/images/ff8a2ea033a2f87a35d895eebd09cbe8/tenor.gif"
            
        
    randImage = random.randint(0, len(imagenes)-1)

    return imagenes[randImage]
