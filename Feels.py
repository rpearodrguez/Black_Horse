import random

def reactionImage(feel=""):
    imagenes = [""]
    if feel == "escobazo":
        imagenes = ["https://media.giphy.com/media/l2Je4FbOimhxM6mE8/giphy.gif", "https://www.stickhorse.cl/wp-content/uploads/2020/01/SH-Escobazo-2.gif", "https://www.stickhorse.cl/wp-content/uploads/2020/01/SH-Escobazo-3.gif"]

    if feel == "abrazo":
        imagenes = ["https://media.tenor.com/images/9fe95432f2d10d7de2e279d5c10b9b51/tenor.gif"]

    randImage = random.randint(0, len(imagenes)-1)
return imagenes[randImage]