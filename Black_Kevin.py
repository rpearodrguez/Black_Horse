import discord
import Setup
import random
import Scrapper


'''
Bot para Stick Horse
Versión 1.0.1 - Versión Operativa, adición comandos adicionales.
Autor: Richard Peña (Vaalus)
Desarrollado en Python 3.7 usando api Discord.py rewrite
'''
client = discord.Client()

    

@client.event
async def on_message(message):
    #entrega información de comandos
    print(message.content) # Now every message sent will be printed to the console
    if message.content.find("sh.help") != -1:
        embed = discord.Embed(title="Ayuda", description="Prefijo sh. - Comandos basicos")
        embed.set_image(url = "https://www.stickhorse.cl/wp-content/uploads/2019/11/SH.png")
        embed.add_field(name="hola", value="Saluda al más puro estilo de Stick Horse")
        embed.add_field(name="invite", value="Link de invitación")
        embed.add_field(name="steam", value="Busca enlace a juego en steam")
        embed.add_field(name="anime", value="Busca información de un anime solicitado")
        embed.add_field(name="manga", value="Busca información de un manga solicitado")
        embed.add_field(name="escobazo", value="Dale un buen escobazo a alguien más, o ti mismo, no te juzgo")
        embed.add_field(name="roll x n +", value="Tira x cantidad de dados de n caras + el bonificador")
        embed.add_field(name="web", value="Para más información visitanos en www.stickhorse.cl")
        await message.channel.send(content=None, embed=embed)

    if message.content.find("sh.help") != -1 and message.channel.is_nsfw():
        embed = discord.Embed(title="Ayuda", description="Comandos NSFW")
        embed.set_image(url="https://www.stickhorse.cl/wp-content/uploads/2019/11/black_horse.png")
        embed.add_field(name="nh <codigo>", value="Devuelve link de nhentai relacionado con el codigo entregado")
        embed.add_field(name="nh <random>", value="Entrega un link aleatorio desde nhentai")
        embed.add_field(name="ts <codigo>", value="Lo mismo que nh pero para tsumino.com")
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

    # Dados
    if message.content.find("sh.roll") != -1:
        # Separa la cantidad de dados y de caras del mensaje.
        dado = message.content.split()
        usuario = str(message.author).split("#")
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
                    await message.channel.send("Tiro de: {} dado {} de {} caras: {}, bonificador {} incluido".format(usuario[0], x, caras, result, bonificador))
            elif(cant_dados>10):
                await message.channel.send("Se quiere morir ese?")


        except:
            await message.channel.send("Formato invalido, debes ingresar dos valores cantidad-de-dados, caras y el bonificador")
            pass

    if message.content.find("sh.anime ") != -1:
        animeId = message.content.split()
        animeBusqueda = "+".join(animeId[1:])
        resultado = Scrapper.animeScrap(animeBusqueda)
        embed = discord.Embed(title="Titulo", description=resultado[0])
        embed.set_image(url = resultado[4])
        embed.add_field(name="Sumario", value=resultado[1])
        embed.add_field(name="Puntaje", value=resultado[2])
        embed.add_field(name="Episodios", value=resultado[3])
        await message.channel.send(content=None, embed=embed)

    if message.content.find("sh.manga ") != -1:
        mangaId = message.content.split()
        mangaBusqueda = "+".join(mangaId[1:])
        resultado = Scrapper.mangaScrap(mangaBusqueda)
        embed = discord.Embed(title="Titulo", description=resultado[0])
        embed.set_image(url = resultado[4])
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
                await message.channel.send(resultado[0])
            
            elif resultado[1] != "Nombre" or resultado[2] != "Descripcion" or resultado[3] != "Desarrollador" or resultado[4] != "Lanzamiento" or resultado[5] != "Genero" or resultado[6] != "Metacritic" or resultado[7] != "Precio":
                embed = discord.Embed(title="Nombre", description=resultado[1])
                embed.set_image(url = resultado[0])
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

    if message.content.find("sh.invite") != -1:
        await message.channel.send("https://discordapp.com/oauth2/authorize?client_id=558102665695985674&permissions=0&scope=bot")

    if message.content.find("sh.ts ") != -1 and message.channel.is_nsfw():

        #Recibe información del manga, rescata el codigo y genera el enlace al manga.
        ts_number = message.content.split()
        '''
        if(ts_number[1]=="random"):
            await message.channel.send(Scrapper.tsuminoRandomSearch())
        elif(ts_number[1]!="random" and not ts_number[1].isdigit()):
            pass
            #await message.channel.send(Scrapper.tsuminoTagSearch(ts_number[1].capitalize()))
        '''
        if(int(ts_number[1])):
            await message.channel.send("https://www.tsumino.com/entry/{}".format(ts_number[1]))
        elif(not ts_number[1].isdigit()):
            await message.channel.send("Formato incorrecto, ingrese numero o escriba random como parametro")
    #En caso de que esté en un canal SFW da está respuesta
    elif message.content.find("sh.ts ") != -1 and not message.channel.is_nsfw():
        await message.channel.send("No sea marrano y pregunte en un canal NSFW")

    if message.content.find("sh.escobazo ") != -1:
        victima = message.content.split()
        embed = discord.Embed(title="Alerta de escobazo")
        embed.set_image(url = "https://media.giphy.com/media/l2Je4FbOimhxM6mE8/giphy.gif")
        embed.add_field(name="D:", value="{} dio un escobazo a {}".format(message.author,victima[1]))
        await message.channel.send(content=None, embed=embed)

client.run(Setup.token)
