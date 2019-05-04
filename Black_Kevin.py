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
    if message.content.find("sh.help") != -1:
        embed = discord.Embed(title="Ayuda", description="Prefijo sh. - Comandos basicos")
        embed.add_field(name="hola", value="Saluda al más puro estilo de Stick Horse")
        embed.add_field(name="anime", value="Busca anime solicitado")
        embed.add_field(name="roll x n", value="Tira x cantidad de dados de n caras")
        await message.channel.send(content=None, embed=embed)

    if message.content.find("sh.help") != -1 and message.channel.is_nsfw():
        embed = discord.Embed(title="Ayuda", description="Comandos NSFW")
        embed.add_field(name="nh <codigo>", value="Devuelve link de nhentai relacionado con el codigo entregado")
        embed.add_field(name="nhrandom", value="Entrega un link aleatorio desde nhentai")
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

    # Dados
    if message.content.find("sh.roll") != -1:
        # Separa la cantidad de dados y de caras del mensaje.
        dado = message.content.split()
        caras = int(dado[-1])
        cant_dados = int(dado[1])
        cant_dados = cant_dados+1
        # Simula el tiro de x dadod
        if(cant_dados>4):
            await message.channel.send("Se quiere morir ese?")
        elif:
            for x in range(1, cant_dados):
                # Tira el dado
                result = random.randint(1, caras)
                # Muestra el resultado como mensaje
                await message.channel.send("dado {} de {} caras: {}".format(x, caras, result))





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

client.run(Setup.token)