import discord
import Setup
import random
from Pymoe import Kitsu

'''
Bot para Stick Horse
Versión 0.0.1 - Ingreso comandos básicos, puesta en marcha
Autor: Richard Peña (Vaalus)
Desarrollado en Python 3.7 usando api Discord.py rewrite
'''
client = discord.Client()
instance = Kitsu(Setup.kitsu_client_id, Setup.kitsu_client_secret)

@client.event
async def on_message(message):
    print(message.content) # Now every message sent will be printed to the console

@client.event
async def on_message(message):
    #entrega información de comandos
    if message.content == "sh.help":
        embed = discord.Embed(title="Ayuda", description="prefijo sh. - Comandos variados")
        embed.add_field(name="hola", value="Te manda a comer tierra")
        embed.add_field(name="anime", value="Aun en desarrollo, te dará información de un anime solicitado")
        embed.add_field(name="jojos", value="Aun en desarrollo (a petición del público), Jojokes")
        await message.channel.send(content=None, embed=embed)

    if message.content == "sh.help":
        embed = discord.Embed(title="Comandos NSFW", description="prefijo sh. - Comandos variados")
        embed.add_field(name="nh <codigo del manga>", value="Devuelve el link para visualizar esa obra de arte")
        embed.add_field(name="nhrandom", value="Genera un link aleatorio de nhentai")
        await message.channel.send(content=None, embed=embed)

    #saluda a quien lo salude
    if message.content.find("sh.hola") != -1:
        await message.channel.send("Come tierra") # If the user says !hello we will send back hi

    #Si está en un canal NSFW, recibe codigo de nhentai y devuelve link a pagina (no es mucho más lo que se puede hacer, ya que murió su API
    if message.content.find("sh.nh ") != -1 and message.channel.is_nsfw():

        #Recibe información del manga, rescata el codigo y genera el enlace al manga.
        nh_number = message.content.split()
        await message.channel.send("https://nhentai.net/g/{}".format(nh_number[1]))
    #En caso de que esté en un canal SFW da está respuesta
    elif message.content.find("sh.nh ") != -1 and not message.channel.is_nsfw():
        await message.channel.send("No sea marrano y pregunte en un canal NSFW")

    if message.content.find("sh.nhrandom") != -1 and message.channel.is_nsfw():
        #Genera un numero random que será utilizado como indice de busqueda en nhentai
        #Este numero es el maximo posible al día 23 de marzo del 2019 - 23:34 (GTM-4).
        nhrnd = random.randint(1, 266905)
        #Recibe información del manga, rescata el codigo y genera el enlace al manga.
        await message.channel.send("https://nhentai.net/g/{}".format(nhrnd))
    #En caso de que esté en un canal SFW da está respuesta
    elif message.content.find("sh.nhrandom") != -1 and not message.channel.is_nsfw():
        await message.channel.send("No sea marrano y pregunte en un canal NSFW")

    if message.content.find("sh.anime ") != -1:
        anime = message.content.split()
        search = instance.anime.search(anime[1:])  # Search anime by term
        try:
            await message.channel.send(search[1]['attributes']['posterImage']['small'])
            embed = discord.Embed(title="", description=search[1]['attributes']['titles']['en_jp'])
            embed.add_field(name="Nombre Inglés", value=search[1]['attributes']['titles']['en'])
            embed.add_field(name="Sinopsis", value=search[1]['attributes']['synopsis'])
            embed.add_field(name="Fecha de Emisión", value=search[1]['attributes']['startDate'])
            embed.add_field(name="Fecha de Término", value=search[1]['attributes']['endDate'])
            embed.add_field(name="Rating", value=search[1]['attributes']['ageRatingGuide'])
            embed.add_field(name="Estado", value=search[1]['attributes']['status'])
            await message.channel.send(content=None, embed=embed)

        except:

            await message.channel.send("No se encontró el anime solicitado")
            pass

    
    #frases random de jojos
    if message.content.find("sh.jojos") != -1:
        #a = randint(1, 5)
        #if a == 1:
        #    await message.channel.send("Yare yare daze ")
        #if a == 2:
        await message.channel.send("desarrollo en proceso")


client.run(Setup.token)