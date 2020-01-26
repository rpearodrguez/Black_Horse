import discord
import random
import Scrapper
import Feels
import os
from boto.s3.connection import S3Connection
#s3 = S3Connection(os.environ['S3_KEY'], os.environ['S3_SECRET'])


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

#General Module

    if message.content.find("sh.help") != -1:
        embed = embed=discord.Embed(title="Ayuda", description="Prefijo sh. - Comandos basicos")
        embed.set_thumbnail(url="https://www.stickhorse.cl/wp-content/uploads/2019/11/SH.png")
        embed.add_field(name="MODULO", value="GENERAL", inline=False)
        embed.add_field(name="hola", value="Saluda al más puro estilo de Stick Horse", inline=True)
        embed.add_field(name="invite", value="Link de invitación", inline=True)
        embed.add_field(name="MODULO", value="ENTRETENIMIENTO", inline=False)
        embed.add_field(name="steam", value="Busca enlace a juego en steam", inline=True)
        embed.add_field(name="anime", value="Busca información de un anime solicitado", inline=True)
        embed.add_field(name="manga", value="Busca información de un manga solicitado", inline=True)
        embed.add_field(name="MODULO", value="ROL", inline=False)
        embed.add_field(name="roll x n +", value="Tira x cantidad de dados de n caras + el bonificador", inline=True)
        embed.add_field(name="MODULO", value="FEELS", inline=False)
        embed.add_field(name="escobazo", value="Dale un buen escobazo a alguien más, o ti mismo, no te juzgo", inline=True)
        embed.add_field(name="hug", value="Reparte abrazos por el mundo", inline=True)
        embed.add_field(name="lick", value="Si tienes complejo de rana allá tu", inline=True)
        embed.set_footer(text="Para más información visitanos en www.stickhorse.cl")
        await message.channel.send(content=None, embed=embed)

    if message.content.find("sh.help") != -1 and message.channel.is_nsfw():
        embed = discord.Embed(title="Ayuda", description="Comandos NSFW")
        embed.set_image(url="https://www.stickhorse.cl/wp-content/uploads/2019/11/black_horse.png")
        embed.add_field(name="nh <codigo>", value="Devuelve link de nhentai relacionado con el codigo entregado")
        embed.add_field(name="nh <random>", value="Entrega un link aleatorio desde nhentai")
        embed.add_field(name="ts <codigo>", value="Lo mismo que nh pero para tsumino.com")
        await message.channel.send(content=None, embed=embed)

    if message.content.find("sh.invite") != -1:
        await message.channel.send("https://discordapp.com/api/oauth2/authorize?client_id=558102665695985674&permissions=92160&scope=bot")

    #saluda a quien lo salude
    if message.content.find("sh.hola") != -1:
        await message.channel.send("Come tierra") # If the user says !hello we will send back hi

    if message.content.find("sh.say") != -1:
        mensaje = message.content.split()
        mensaje2 = " ".join(mensaje[1:])
        await message.channel.send(mensaje2)

#NSFW Module

    #Si está en un canal NSFW, recibe codigo de nhentai y devuelve link a pagina (no es mucho más lo que se puede hacer, ya que murió su API
    if message.content.find("sh.nh ") != -1 and message.channel.is_nsfw():

        #Recibe información del manga, rescata el codigo y genera el enlace al manga.
        nh_number = message.content.split()
        if(nh_number[1]=="random"):
            await message.channel.send(Scrapper.nhentaiRandomSearch())
        elif(nh_number[1]!="random" and not nh_number[1].isdigit()):
            busqueda = "+".join(nh_number[1:])
            await message.channel.send(Scrapper.nhentaiTagSearch(busqueda))
        elif(int(nh_number[1])):
            await message.channel.send("https://nhentai.net/g/{}".format(nh_number[1]))
        elif(not int(nh_number[1])):
            await message.channel.send("Formato incorrecto, ingrese numero o escriba random como parametro")
    #En caso de que esté en un canal SFW da está respuesta
    elif message.content.find("sh.nh ") != -1 and not message.channel.is_nsfw():
        await message.channel.send("No sea marrano y pregunte en un canal NSFW")

#Roleplay Module

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

#Entertainment Module

    if message.content.find("sh.anime ") != -1:
        animeId = message.content.split()
        animeBusqueda = "+".join(animeId[1:])
        resultado = Scrapper.animeScrap(animeBusqueda)
        #find = [titulo, portada, sinopsis, lanzamiento, tipo, rating, generos, episodios]
        embed = discord.Embed(title="Titulo", description=resultado[0])
        embed.set_image(url = resultado[1])
        embed.add_field(name="Sinopsis", value=resultado[2], inline=False)
        embed.add_field(name="Lanzamiento", value=resultado[3], inline=True)
        embed.add_field(name="Tipo", value=resultado[4], inline=True)
        embed.add_field(name="Puntaje", value=resultado[5], inline=True)
        embed.add_field(name="Genero(s)", value=resultado[6], inline=False)
        embed.add_field(name="Episodios", value=resultado[7], inline=True)
        embed.set_footer(text="Creditos a animeflv.net")
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

    if message.content.find("sh.img ") != -1:
        imageId = message.content.split()
        imageBusqueda = "+".join(imageId[1:])
        resultado = Scrapper.imgSearch(imageBusqueda)
        embed = discord.Embed(title="Imagen encontrada", description=" ".join(imageId[1:]))
        embed.set_image(url = resultado)
        await message.channel.send(content=None, embed=embed)

#Reactions Module

    if message.content.find("sh.escobazo ") != -1:
        victima = message.content.split()
        autor = str(message.author).split("#")[0]
        imagen = Feels.reactionImage("escobazo")
        embed = discord.Embed(title="Alerta de escobazo")
        embed.set_image(url = imagen)
        embed.add_field(name="D:", value="{} dio un escobazo a {}".format(autor,victima[1]))
        await message.channel.send(content=None, embed=embed)
    
    if message.content.find("sh.hug ") != -1:
        victima = message.content.split()
        print(message.author)
        autor = str(message.author).split("#")[0]
        imagen = Feels.reactionImage("abrazo")
        embed = discord.Embed(title="Alerta de abrazo")
        embed.set_image(url = imagen)
        embed.add_field(name=":D", value="{} dio un abrazo a {}".format(autor,victima[1]))
        embed.set_footer(text="Creditos a tenor.com")
        await message.channel.send(content=None, embed=embed)
    
    if message.content.find("sh.lick ") != -1:
        victima = message.content.split()
        print(message.author)
        autor = str(message.author).split("#")[0]
        imagen = Feels.reactionImage("lamer")
        embed = discord.Embed(title="Alerta de lamida")
        embed.set_image(url = imagen)
        embed.add_field(name=";A;", value="{} lamió a {}".format(autor,victima[1]))
        embed.set_footer(text="Creditos a tenor.com")
        await message.channel.send(content=None, embed=embed)

    if message.content.find("sh.pat ") != -1:
        victima = message.content.split()
        print(message.author)
        autor = str(message.author).split("#")[0]
        imagen = Feels.reactionImage("pat")
        embed = discord.Embed(title="Alerta de pateo")
        embed.set_image(url = imagen)
        embed.add_field(name="*-*", value="{} acarició la cabeza de {}".format(autor,victima[1]))
        embed.set_footer(text="Creditos a tenor.com")
        await message.channel.send(content=None, embed=embed)

    if message.content.find("sh.jojo") != -1:
        victima = message.content.split()
        print(message.author)
        autor = str(message.author).split("#")[0]
        imagen = Feels.reactionImage("jojo")
        embed = discord.Embed(title="{} hizo una Jojopose".format(autor))
        embed.set_image(url = imagen)
        embed.set_footer(text="Creditos a tenor.com")
        await message.channel.send(content=None, embed=embed)

    if message.content.find("sh.slap ") != -1:
        victima = message.content.split()
        print(message.author)
        autor = str(message.author).split("#")[0]
        imagen = Feels.reactionImage("slap")
        embed = discord.Embed(title="{} golpeó a ".format(autor))
        embed.set_image(url = imagen)
        embed.set_footer(text="Creditos a tenor.com")
        await message.channel.send(content=None, embed=embed)

    if message.content.find("sh.kiss ") != -1:
        victima = message.content.split()
        print(message.author)
        autor = str(message.author).split("#")[0]
        imagen = Feels.reactionImage("kiss")
        embed = discord.Embed(title="{} besó a ".format(autor))
        embed.set_image(url = imagen)
        embed.set_footer(text="Creditos a tenor.com")
        await message.channel.send(content=None, embed=embed)

    if message.content.find("sh.suicide") != -1:
        victima = message.content.split()
        print(message.author)
        autor = str(message.author).split("#")[0]
        imagen = Feels.reactionImage("suicide")
        embed = discord.Embed(title="{} se mató".format(autor))
        embed.set_image(url = imagen)
        embed.set_footer(text="Si realmente estas mal y necesitas ayuda visita http://www.asulac.org/necesitas-ayuda/")
        await message.channel.send(content=None, embed=embed)

client.run(os.environ.get('DISCORD_TOKEN'))
