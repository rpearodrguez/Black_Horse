import discord
import Setup
import random
import Scrapper


'''
Bot para Stick Horse
Versión 0.0.1 - Ingreso comandos básicos, puesta en marcha
Autor: Richard Peña (Vaalus)
Desarrollado en Python 3.7 usando api Discord.py rewrite
'''
client = discord.Client()


@client.event
async def on_message(message):
    print(message.content) # Now every message sent will be printed to the console

@client.event
async def on_message(message):
    #entrega información de comandos
    if message.content.find("sh.help") != -1:
        embed = discord.Embed(title="Ayuda", description="Prefijo sh. - Comandos basicos")
        embed.add_field(name="hola", value="Saluda al más puro estilo de Stick Horse")
        embed.add_field(name="steam", value="Busca enlace a juego en steam")
        embed.add_field(name="anime", value="Busca información de un anime solicitado")
        embed.add_field(name="manga", value="Busca información de un manga solicitado")
        embed.add_field(name="roll x n +", value="Tira x cantidad de dados de n caras + el bonificador")
        await message.channel.send(content=None, embed=embed)

    if message.content.find("sh.help") != -1 and message.channel.is_nsfw():
        embed = discord.Embed(title="Ayuda", description="Comandos NSFW")
        embed.add_field(name="nh <codigo>", value="Devuelve link de nhentai relacionado con el codigo entregado")
        embed.add_field(name="nh <random>", value="Entrega un link aleatorio desde nhentai")
        await message.channel.send(content=None, embed=embed)

    #saluda a quien lo salude
    if message.content.find("sh.hola") != -1:
        await message.channel.send("Come tierra") # If the user says !hello we will send back hi

    #Si está en un canal NSFW, recibe codigo de nhentai y devuelve link a pagina (no es mucho más lo que se puede hacer, ya que murió su API
    if message.content.find("sh.nh ") != -1 and message.channel.is_nsfw():

        #Recibe información del manga, rescata el codigo y genera el enlace al manga.
        nh_number = message.content.split()
        if(nh_number[1]=="random"):
            await message.channel.send(Scrapper.nhentaiRandomSearch())
        elif(int(nh_number[1])):
            await message.channel.send("https://nhentai.net/g/{}".format(nh_number[1]))
        elif(not int(nh_number[1])):
            await message.channel.send("Formato incorrecto, ingrese numero o escriba random como parametro")
    #En caso de que esté en un canal SFW da está respuesta
    elif message.content.find("sh.nh ") != -1 and not message.channel.is_nsfw():
        await message.channel.send("No sea marrano y pregunte en un canal NSFW")

    '''
    if message.content.find("sh.nhrandom") != -1 and message.channel.is_nsfw():
        #Genera un numero random que será utilizado como indice de busqueda en nhentai
        #Este numero es el maximo posible al día 23 de marzo del 2019 - 23:34 (GTM-4).
        nhrnd = random.randint(1, 266905)
        #Recibe información del manga, rescata el codigo y genera el enlace al manga.
        await message.channel.send("https://nhentai.net/g/{}".format(nhrnd))
    #En caso de que esté en un canal SFW da está respuesta
    elif message.content.find("sh.nhrandom") != -1 and not message.channel.is_nsfw():
        await message.channel.send("No sea marrano y pregunte en un canal NSFW")
    '''

    # Dados
    if message.content.find("sh.roll") != -1:
        # Separa la cantidad de dados y de caras del mensaje.
        dado = message.content.split()
        # Limita la cantidad de dados para no abusar del spam, la cantidad de dados simultaneos es una condición arbitraria.
        try:
            caras = int(dado[2])
            cant_dados = int(dado[1])
            bonificador = int(dado[3])
            #Limita la cantidad de dados para no abusar del spam, la cantidad de dados simultaneos es una condición arbitraria.

            if(cant_dados<10 or cant_dados==10):
                # Simula el tiro de x dadod
                for x in range(1, (1+cant_dados)):
                    # Tira el dado
                    result = random.randint(1, caras) + bonificador
                    # Muestra el resultado como mensaje
                    await message.channel.send("dado {} de {} caras: {}, bonificador {} incluido".format(x, caras, result, bonificador))
            elif(cant_dados>10):
                await message.channel.send("Se quiere morir ese?")


        except:
            await message.channel.send("Formato invalido, debes ingresar dos valores cantidad-de-dados, caras y el bonificador")
            pass

    if message.content.find("sh.anime ") != -1:
        animeId = message.content.split()
        animeBusqueda = "+".join(animeId[1:])
        resultado = Scrapper.animeScrap(animeBusqueda)
        await message.channel.send(resultado[4])
        embed = discord.Embed(title="Titulo", description=resultado[0])
        embed.add_field(name="Sumario", value=resultado[1])
        embed.add_field(name="Puntaje", value=resultado[2])
        embed.add_field(name="Episodios", value=resultado[3])
        await message.channel.send(content=None, embed=embed)


    if message.content.find("sh.manga ") != -1:
        mangaId = message.content.split()
        mangaBusqueda = "+".join(mangaId[1:])
        resultado = Scrapper.mangaScrap(mangaBusqueda)
        await message.channel.send(resultado[4])
        embed = discord.Embed(title="Titulo", description=resultado[0])
        embed.add_field(name="Sumario", value=resultado[1])
        embed.add_field(name="Puntaje", value=resultado[2])
        embed.add_field(name="Volumenes", value=resultado[3])
        await message.channel.send(content=None, embed=embed)

    if message.content.find("sh.steam ") != -1:

        juegoID = message.content.split()
        juegoBusqueda = "+".join(juegoID[1:])
        resultado = Scrapper.steamDataSearch(juegoBusqueda)

        try:
            #"Portada", "Nombre", "Descripcion", "Desarrollador", "Lanzamiento", "Genero", "Metacritic", "Precio"
            if resultado[0] != "Portada" and resultado[1] == "Nombre" and resultado[2] == "Descripcion" and resultado[3] == "Desarrollador" and resultado[4] == "Lanzamiento" and resultado[5] == "Genero" and resultado[6] == "Metacritic" and resultado[7] != "Precio":
                await message.channel.send(resultado[1])
            
            elif resultado[1] != "Nombre" or resultado[2] != "Descripcion" or resultado[3] != "Desarrollador" or resultado[4] != "Lanzamiento" or resultado[5] != "Genero" or resultado[6] != "Metacritic" or resultado[7] != "Precio":
                await message.channel.send(resultado[0])
                embed = discord.Embed(title="Nombre", description=resultado[1])
                embed.add_field(name="Descripción", value=resultado[2])
                embed.add_field(name="Desarrollador", value=resultado[3])
                embed.add_field(name="Fecha de lanzamiento", value=resultado[4])
                embed.add_field(name="Género", value=resultado[5])
                embed.add_field(name="Metacritic", value=resultado[6])
                embed.add_field(name="Precio", value=resultado[7])
                await message.channel.send(content=None, embed=embed)
            else:
                await message.channel.send("Juego no encontrado o con bloqueo de edad")
        except:
            pass

client.run(Setup.token)
