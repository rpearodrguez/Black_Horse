import discord
import random
import Scrapper
import Roleplay
import Feels
import os
import datetime
from boto.s3.connection import S3Connection



'''
Bot para Stick Horse
Versión 2.0.0 - Versión Operativa, adición comandos adicionales.
Autor: Richard Peña (Vaalus)
Desarrollado en Python 3.7 usando api Discord.py rewrite
'''
client = discord.Client()



    

@client.event
async def on_message(message):
    #print commands in console for logging purposes
    if message.content.find("sh.") != -1:
        print("{} - {}:{}".format(str(message.author).split("#")[0],message.author.guild.name, message.content)) # Now every message sent will be printed to the console


#General Module

    if message.content.find("sh.help") != -1 and not message.author.bot:
        embed = embed=discord.Embed(title="Ayuda", description="Prefijo sh. - Comandos basicos")
        embed.set_thumbnail(url="https://www.stickhorse.cl/wp-content/uploads/2019/11/SH.png")
        embed.add_field(name="<3", value="Debido a la limitación de carateres, puedes encontrar el listado de comandos en https://www.stickhorse.cl/bot-de-stick-horse-listado-de-comandos-prefijo-sh/", inline=True)
        embed.set_footer(text="Para más información visitanos en www.stickhorse.cl")
        await message.channel.send(content=None, embed=embed)

    if message.content.find("sh.help") != -1 and message.channel.is_nsfw() and not message.author.bot:
        embed = discord.Embed(title="Ayuda", description="Comandos NSFW")
        embed.set_thumbnail(url="https://www.stickhorse.cl/wp-content/uploads/2019/11/black_horse.png")
        embed.add_field(name="<3", value="Debido a la limitación de carateres, puedes encontrar el listado de comandos en https://www.stickhorse.cl/18-bot-de-stick-horse-listado-de-comandos-nsfwprefijo-sh/", inline=True)
        embed.set_footer(text="Para más información visitanos en www.stickhorse.cl")
        await message.channel.send(content=None, embed=embed)

    if message.content.find("sh.invite") != -1 and not message.author.bot:
        await message.channel.send("https://discordapp.com/api/oauth2/authorize?client_id=558102665695985674&permissions=92160&scope=bot")

    # If the user says !hello we will send you to eat dirt
    if message.content.find("sh.hola") != -1 and not message.author.bot:
        await message.channel.send("Come tierra") # If the user says !hello we will send you to eat dirt

    if message.content.find("sh.help") != -1 and not message.author.bot:
        embed = embed=discord.Embed(title="Ayuda", description="Prefijo sh. - Comandos basicos")
        embed.set_thumbnail(url="https://www.stickhorse.cl/wp-content/uploads/2019/11/SH.png")
        embed.add_field(name="<3", value="Debido a la limitación de carateres, puedes encontrar el listado de comandos en https://www.stickhorse.cl/bot-de-stick-horse-listado-de-comandos-prefijo-sh/", inline=True)
        embed.set_footer(text="Para más información visitanos en www.stickhorse.cl")
        await message.channel.send(content=None, embed=embed)
    
    if message.content.find("sh.jueves") != -1 and not message.author.bot:
        dia = datetime.datetime.today().weekday()
        if dia == 3:
            embed = embed=discord.Embed(title="Feliz jueves", description="hoy es jueves <3")
            embed.set_image(url="https://www.stickhorse.cl/wp-content/uploads/2020/08/Feliz-jueves.gif")
            await message.channel.send(content=None, embed=embed)
        else:
            await message.channel.send("Hoy no es jueves")

    

    if message.content.find("sh.say") != -1 and not message.author.bot:
        mensaje = message.content.split()
        mensaje2 = " ".join(mensaje[1:])
        await message.delete()
        if "sh." in mensaje2:
            await message.channel.send("{} no tan rapido maquinola".format(message.author.name))
        else:
            await message.channel.send(mensaje2)

#FRASES Module        
    elif message.content.find("TU SIGUES, JOTARO!") != -1 and not message.author.bot:
        await message.channel.send("BASTARDO... DIO")
        
    elif message.content.find("OH? TE ESTÁS ACERCANDO? EN LUGAR DE CORRER, VIENES DIRECTO A MÍ? AÚN CUANDO TU ABUELO JOSEPH, TE DIJO EL SECRETO DE THE WORLD") != -1 and not message.author.bot:
        await message.channel.send("NO PUEDO PARTIRTE LA MADRE SIN ACERCARME A TI")
        
    elif message.content.find("OH HO! ENTONCES ACERCATE TODO LO QUE QUIERAS")!= -1 and not message.author.bot:
        await message.channel.send("ORA!")
        
    elif message.content == "DIO" and not message.author.bot:
        await message.channel.send("OH? TE ESTÁS ACERCANDO? EN LUGAR DE CORRER, VIENES DIRECTO A MÍ? AÚN CUANDO TU ABUELO JOSEPH, TE DIJO EL SECRETO DE THE WORLD")
        
    elif message.content.find("NO PUEDO PARTIRTE LA MADRE SIN ACERCARME A TI")!= -1 and not message.author.bot:
        await message.channel.send("OH HO! ENTONCES ACERCATE TODO LO QUE QUIERAS")
        
    elif message.content.find("ORA! ORA! ORA! ORA! ORA!") != -1 and not message.author.bot:
        await message.channel.send("MUDA! MUDA! MUDA! MUDA! MUDA!")

    elif message.content.find("MUDA! MUDA! MUDA! MUDA! MUDA!") != -1 and not message.author.bot:
        await message.channel.send("ORA! ORA! ORA! ORA! ORA!")

    elif message.content.find("TENGO MUCHO MIEDO MAGINER") != -1 and not message.author.bot:
        await message.channel.send("TIENES QUE HACERLO POR MI, PIPO, POR MAGINER")

    elif message.content.find("TIENES QUE HACERLO POR MI, PIPO, POR MAGINER") != -1 and not message.author.bot:
        await message.channel.send("ESTÁ BIEN, POR TI... MAGINER")
        
    elif message.content.find("ESTÁ BIEN, POR TI... MAGINER") != -1 and not message.author.bot:
        await message.channel.send("BIEN MAGINER, PIPO ESTÁ MUERTO, LE CORTARON LA GARGANTA DE AQUI A ACÁ")
    
    elif message.content.find("BIEN MAGINER, PIPO ESTÁ MUERTO, LE CORTARON LA GARGANTA DE AQUI A ACÁ") != -1 and not message.author.bot:
        await message.channel.send("OIGA, ESTOY TRATANDO DE COMER MI ALMUERZO")
    
    elif message.content.find("PIPO ESTÁ MUERTO") != -1 and not message.author.bot:
        await message.channel.send("LE CORTARON LA GARGANTA DE AQUI A ACÁ")

    elif message.content == "ORA!" and not message.author.bot:
        await message.channel.send("MUDA!")
    
    elif message.content == "MUDA!" and not message.author.bot:
        await message.channel.send("ORA!")
    
    elif message.content == "KAZUMA! KAZUMA!" and not message.author.bot:
        randNum = random.randint(1, 2)
        if randNum == 1:
            await message.channel.send("KAZUMA DESU")
        if randNum == 2:
            await message.channel.send("KAZUMA DA YO")

    elif message.content == "OMAE WA MO SHINDEIRU" and not message.author.bot:
        embed = embed=discord.Embed(title="NANI!!", description="O-O")
        embed.set_image(url="https://media1.tenor.com/images/009d9801cc81b561927001cecb313d59/tenor.gif")
        await message.channel.send(content=None, embed=embed)


#NSFW Module

    #Si está en un canal NSFW, recibe codigo de nhentai y devuelve link a pagina (no es mucho más lo que se puede hacer, ya que murió su API
    elif message.content.find("sh.nh ") != -1 and message.channel.is_nsfw() and not message.author.bot:

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
    elif message.content.find("sh.nh ") != -1 and not message.channel.is_nsfw() and not message.author.bot:
        await message.delete()
        await message.channel.send("No sea marrano y pregunte en un canal NSFW")

    elif message.content.find("sh.patas") != -1 and message.channel.is_nsfw() and not message.author.bot:
        busqueda = Scrapper.safebooruSearch("feet")
        print(busqueda)
        if busqueda != "No se pudo encontrar resultado":
            embed = discord.Embed(title="Aquí está el resultado", description="Cochinón")
            embed.set_image(url = busqueda)
            embed.set_footer(text="Creditos a safebooru.org")
            await message.channel.send(content=None, embed=embed)
        else:
            await message.channel.send("No se pudo encontrar lo solicitado")
        
    
    elif message.content.find("sh.patas") != -1 and not message.channel.is_nsfw() and not message.author.bot:
        await message.delete()
        await message.channel.send("Debido a que puede salir contenido NSFW haz la consulta en algun canal de ese tipo")

    elif message.content.find("sh.piernas") != -1 and message.channel.is_nsfw() and not message.author.bot:
        busqueda = Scrapper.safebooruSearch("thighs")
        print(busqueda)
        if busqueda != "No se pudo encontrar resultado":
            embed = discord.Embed(title="Aquí está el resultado", description="Piernas")
            embed.set_image(url = busqueda)
            embed.set_footer(text="Creditos a safebooru.org")
            await message.channel.send(content=None, embed=embed)
        else:
            await message.channel.send("No se pudo encontrar lo solicitado")
        
    
    elif message.content.find("sh.piernas") != -1 and not message.channel.is_nsfw() and not message.author.bot:
        await message.delete()
        await message.channel.send("Debido a que puede salir contenido NSFW haz la consulta en algun canal de ese tipo")

    elif message.content.find("sh.safebooru") != -1 and message.channel.is_nsfw() and not message.author.bot:
        search = message.content.split()
        busqueda = Scrapper.safebooruSearch("+".join(search[1:]))
        print(busqueda)
        if busqueda != "No se pudo encontrar resultado":
            embed = discord.Embed(title="Aquí está el resultado de la busqueda", description=" ".join(search[1:]))
            embed.set_image(url = busqueda)
            embed.set_footer(text="Creditos a safebooru.org")
            await message.channel.send(content=None, embed=embed)
        else:
            await message.channel.send("No se pudo encontrar lo solicitado")

    elif message.content.find("sh.safebooru") != -1 and not message.channel.is_nsfw() and not message.author.bot:
        await message.delete()
        await message.channel.send("Debido a que puede salir contenido NSFW haz la consulta en algun canal de ese tipo")

    elif message.content.find("sh.danbooru ") != -1 and message.channel.is_nsfw() and not message.author.bot:
        danId = message.content.split()
        danBusqueda = "_".join(danId[1:]).split("/")
        danBusqueda2 = '{}2F'.format("%").join(danBusqueda)
        print(danBusqueda2)
        resultado = Scrapper.danbooruSearch(danBusqueda2)
        try:
            embed = discord.Embed(title="Búsqueda", description=" ".join(danId[1:]))
            embed.set_image(url = resultado[1])
            embed.add_field(name="Id en danbooru", value=resultado[0], inline=True)
            embed.add_field(name="Artista", value=resultado[2], inline=True)
            embed.add_field(name="Tags", value=resultado[3], inline=False)
            embed.set_footer(text="Creditos a https://danbooru.donmai.us")
            await message.channel.send(content=None, embed=embed)
        except Exception as ex:
            print(ex)
            await message.channel.send(resultado[0])
    
    elif message.content.find("sh.danbooru ") != -1 and not message.channel.is_nsfw() and not message.author.bot:
        await message.delete()
        await message.channel.send("No sea marrano y pregunte en un canal NSFW")

    elif message.content.find("sh.hanime ") != -1 and message.channel.is_nsfw() and not message.author.bot:
        danId = message.content.split()
        danBusqueda = "+".join(danId[1:])
        print(danBusqueda)
        resultado = Scrapper.hIdShow(danBusqueda)
        try:
            embed = discord.Embed(title="Búsqueda", description=" ".join(danId[1:]))
            embed.set_image(url = resultado[0][1])
            try:
                embed.add_field(name=resultado[1][0], value=resultado[2][0], inline=False)
            except:
                pass
            try:
                embed.add_field(name=resultado[1][1], value=resultado[2][1], inline=False)
            except:
                pass
            try:
                embed.add_field(name=resultado[1][2], value=resultado[2][2], inline=False)
            except:
                pass
            try:
                embed.add_field(name=resultado[1][3], value=resultado[2][3], inline=False)
            except:
                pass
            try:
                embed.add_field(name=resultado[1][4], value=resultado[2][4], inline=False)
            except:
                pass
            try:
                embed.add_field(name=resultado[1][5], value=resultado[2][5], inline=False)
            except:
                pass
            try:
                embed.add_field(name=resultado[1][6], value=resultado[2][6], inline=False)
            except:
                pass
            try:
                embed.add_field(name=resultado[1][7], value=resultado[2][7], inline=False)
            except:
                pass
            try:
                embed.add_field(name=resultado[1][8], value=resultado[2][8], inline=False)
            except:
                pass
            embed.set_footer(text="Puedes encontrarlo en: {}".format(resultado[0][0]))
            await message.channel.send(content=None, embed=embed)
        except Exception as ex:
            print(ex)
            await message.channel.send(resultado[0])

    elif message.content.find("sh.hanime ") != -1 and not message.channel.is_nsfw() and not message.author.bot:
        await message.delete()
        await message.channel.send("No sea marrano y pregunte en un canal NSFW")
#Roleplay Module

    # Dados
    elif message.content.find("sh.roll") != -1 and not message.author.bot:
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
    
    elif message.content.find("sh.fate") != -1 and not message.author.bot:

        dado = message.content.split()
        dado2 = dado[1].split("df")
        dados = dado2[0]
        modificador = dado2[1]
        usuario = str(message.author).split("#")
        resultado = Roleplay.fateroll(dados,modificador,usuario[0])
        await message.channel.send(resultado)

#Entertainment Module

    elif message.content.find("sh.anime ") != -1 and not message.author.bot:
        animeId = message.content.split()
        animeBusqueda = "+".join(animeId[1:])
        resultado = Scrapper.animeScrap(animeBusqueda)
        #find = [titulo, portada, sinopsis, lanzamiento,termino,terminado, tipo, rating ,episodios, generos]
        try:
            embed = discord.Embed(title="Titulo", description=resultado[0])
            embed.set_image(url = resultado[1])
            embed.add_field(name="Sinopsis", value=resultado[2], inline=False)
            embed.add_field(name="Lanzamiento", value=resultado[3], inline=True)
            embed.add_field(name="Finalizacion", value=resultado[4], inline=True)
            embed.add_field(name="Estado", value=resultado[5], inline=True)
            embed.add_field(name="Tipo", value=resultado[6], inline=True)
            embed.add_field(name="Rating", value=resultado[7], inline=True)
            embed.add_field(name="Episodios", value=resultado[8], inline=True)
            if resultado[9] != "":
                embed.add_field(name="Generos", value=resultado[9], inline=True)
            embed.set_footer(text="Obtenido de kitsu.io, traduccion con googletrans")
            await message.channel.send(content=None, embed=embed)
        except:

            await message.channel.send(resultado[0])

    elif message.content.find("sh.manga ") != -1 and not message.author.bot:
        mangaId = message.content.split()
        mangaBusqueda = "+".join(mangaId[1:])
        resultado = Scrapper.mangaScrap(mangaBusqueda)
        print(resultado)
        #find = [titulo, portada, sinopsis, lanzamiento,termino,terminado, tipo, rating ,episodios, serializacion, generos]
        try:
            embed = discord.Embed(title="Titulo", description=resultado[0])
            embed.set_image(url = resultado[1])
            embed.add_field(name="Sinopsis", value=resultado[2], inline=False)
            embed.add_field(name="Lanzamiento", value=resultado[3], inline=True)
            embed.add_field(name="Finalizacion", value=resultado[4], inline=True)
            embed.add_field(name="Estado", value=resultado[5], inline=True)
            embed.add_field(name="Tipo", value=resultado[6], inline=True)
            embed.add_field(name="Rating", value=resultado[7], inline=True)
            embed.add_field(name="Capitulos", value=resultado[8], inline=True)
            embed.add_field(name="Serializacion", value=resultado[9], inline=True)
            if resultado[10] != "":
                embed.add_field(name="Generos", value=resultado[10], inline=True)
            embed.set_footer(text="Obtenido de kitsu.io, traduccion con googletrans")
            await message.channel.send(content=None, embed=embed)
        except:

            await message.channel.send(resultado[0])

    elif message.content.find("sh.steam ") != -1 and not message.author.bot:

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
                embed.add_field(name="Descripción", value=resultado[2], inline=False)
                embed.add_field(name="Desarrollador", value=resultado[3], inline=True)
                embed.add_field(name="Fecha de lanzamiento", value=resultado[4], inline=True)
                embed.add_field(name="Género", value=resultado[5], inline=False)
                embed.add_field(name="Metacritic", value=resultado[6], inline=True)
                embed.add_field(name="Precio", value=resultado[7], inline=True)
                await message.channel.send(content=None, embed=embed)
    
            else:
    
                await message.channel.send("Juego no encontrado o con bloqueo de edad")
        except:
            pass

    elif message.content.find("sh.img ") != -1 and not message.author.bot:
        imageId = message.content.split()
        imageBusqueda = "+".join(imageId[1:])
        resultado = Scrapper.imgSearch(imageBusqueda)
        embed = discord.Embed(title="Imagen encontrada", description=" ".join(imageId[1:]))
        embed.set_image(url = resultado)
        await message.channel.send(content=None, embed=embed)

    elif message.content.find("sh.cc") != -1 and not message.author.bot:
        busqueda = Scrapper.ccSearch()
        embed = discord.Embed(title=busqueda[0], description=busqueda[2])
        embed.set_image(url = busqueda[1])
        await message.channel.send(content=None, embed=embed)

    elif message.content.find("sh.scp ") != -1 and not message.author.bot:
        scpId = message.content.split()
        scpBusqueda = scpId[1:]
        print(scpBusqueda)
        resultado = Scrapper.SCP_Search(scpBusqueda[0])
        try:
            embed = discord.Embed(title="Búsqueda: SCP-", description=" ".join(scpId[1:]))
            try:
                embed.set_image(url = resultado[0])
            except:
                pass
            try:
                embed.add_field(name=resultado[1].split(":")[0], value=resultado[1].split(":")[1], inline=False)
            except:
                pass
            try:
                embed.add_field(name=resultado[2].split(":")[0], value=resultado[2].split(":")[1], inline=False)
            except:
                pass
            try:
                embed.add_field(name=resultado[3].split(":")[0], value=resultado[3].split(":")[1], inline=False)
            except:
                pass
            try:
                embed.add_field(name=resultado[4].split(":")[0], value=resultado[4].split(":")[1], inline=False)
            except:
                pass
            try:
                embed.add_field(name=resultado[5].split(":")[0], value=resultado[5].split(":")[1], inline=False)
            except:
                pass
            try:
                embed.add_field(name=resultado[6].split(":")[0], value=resultado[6].split(":")[1], inline=False)
            except:
                pass
            try:
                embed.add_field(name=resultado[7].split(":")[0], value=resultado[7].split(":")[1], inline=False)
            except:
                pass
            await message.channel.send(content=None, embed=embed)
        except Exception as ex:
            print(ex)
            await message.channel.send(resultado[0])

    if message.content.find("sh.convert ") != -1 and not message.author.bot:
        consulta = message.content.split()
        try:
            monto = float(consulta[1])
            desde = consulta[2].upper()
            hasta = consulta[4].upper()
            resultado = Scrapper.reporteDivisa(monto, desde, hasta)
        except:
            await message.channel.send('Formato incorrecto, conversión debe ser en el siguiente formato:\nsh.convert [monto] [divisa base(ej: CLP)] to [divisa destino(ej: USD)] ')
        #find = [rate_desde,rate_hasta,resultado]
        try:
            embed = discord.Embed(title="Conversion", description="{} a {}".format(desde, hasta))
            embed.add_field(name="Relacion {} a 1 dolar".format(desde), value=resultado[0], inline=True)
            embed.add_field(name="Relacion {} a 1 dolar".format(hasta), value=resultado[1], inline=True)
            embed.add_field(name="Valor {} {} a {}".format(desde, monto, hasta), value=resultado[2], inline=False)
            embed.set_footer(text="Fuente: https://openexchangerates.org")
            await message.channel.send(content=None, embed=embed)
        except:
            await message.channel.send(resultado[2])

#Reactions Module
#Cooperative Reactions

    elif message.content.find("sh.escobazo") != -1 and not message.author.bot:
        try:            
            autor = str(message.author).split("#")[0]
            imagen = Feels.reactionImage("escobazo")
            try:
                victima = message.mentions[0].name
                embed = discord.Embed(title="{} dio un escobazo a {}".format(autor,victima))
            except IndexError:
                raise IndexError("Victima no existe")      
            embed.set_image(url = imagen)
            await message.channel.send(content=None, embed=embed)

        except IndexError:

            await message.channel.send("Debes mencionar un usuario para poder usar este comando")
    
    elif message.content.find("sh.lick") != -1 and not message.author.bot:
        try:
            autor = str(message.author).split("#")[0]
            imagen = Feels.reactionImage("lamer")
            try:
                victima = message.mentions[0].name
                embed = discord.Embed(title="{} lamió a {}".format(autor,victima))
            except IndexError:
                raise IndexError("Victima no existe")   
            embed.set_image(url = imagen)
            embed.set_footer(text="Via Tenor")
            await message.channel.send(content=None, embed=embed)

        except IndexError:

            await message.channel.send("Debes mencionar un usuario para poder usar este comando")

    elif message.content.find("sh.pat") != -1 and not message.author.bot:
        try:
            autor = str(message.author).split("#")[0]
            imagen = Feels.reactionImage("pat")
            try:
                victima = message.mentions[0].name
                embed = discord.Embed(title="{} acarició la cabeza de {}".format(autor,victima))
            except IndexError:
                raise IndexError("Victima no existe")  
            embed.set_image(url = imagen)
            embed.set_footer(text="Via Tenor")
            await message.channel.send(content=None, embed=embed)

        except IndexError:

            await message.channel.send("Debes mencionar un usuario para poder usar este comando")

    elif message.content.find("sh.slap") != -1 and not message.author.bot:
        try:
            autor = str(message.author).split("#")[0]
            imagen = Feels.reactionImage("slap")
            try:
                victima = message.mentions[0].name
                embed = discord.Embed(title="{} cacheteó a {}".format(autor,victima))
            except IndexError:
                raise IndexError("Victima no existe")  
            embed.set_image(url = imagen)
            embed.set_footer(text="Via Tenor")
            await message.channel.send(content=None, embed=embed)

        except IndexError:

            await message.channel.send("Debes mencionar un usuario para poder usar este comando")

    elif message.content.find("sh.feed") != -1 and not message.author.bot:
        try:
            autor = str(message.author).split("#")[0]
            imagen = Feels.reactionImage("food")
            try:
                victima = message.mentions[0].name
                embed = discord.Embed(title="{} alimentó a {}".format(autor,victima))
            except IndexError:
                raise IndexError("Victima no existe")  
            embed.set_image(url = imagen)
            embed.set_footer(text="Via Tenor")
            await message.channel.send(content=None, embed=embed)

        except IndexError:

            await message.channel.send("Debes mencionar un usuario para poder usar este comando")

    elif message.content.find("sh.kick") != -1 and not message.author.bot:
        try:
            autor = str(message.author).split("#")[0]
            imagen = Feels.reactionImage("kickbutt")
            try:
                victima = message.mentions[0].name
                embed = discord.Embed(title="{} pateó a {}".format(autor,victima))
            except IndexError:
                raise IndexError("Victima no existe")  
            embed.set_image(url = imagen)
            embed.set_footer(text="Via Tenor")
            await message.channel.send(content=None, embed=embed)

        except IndexError:

            await message.channel.send("Debes mencionar un usuario para poder usar este comando")

    elif message.content.find("sh.baka") != -1 and not message.author.bot:
        try:
            autor = str(message.author).split("#")[0]
            imagen = Feels.reactionImage("baka")
            try:
                victima = message.mentions[0].name
                embed = discord.Embed(title="{} BAKA!! BAKA!! BAKAAAA!!".format(victima))
            except IndexError:
                raise IndexError("Victima no existe") 
            embed.set_image(url = imagen)
            embed.set_footer(text="Via Tenor")
            await message.channel.send(content=None, embed=embed)

        except IndexError:

            await message.channel.send("Debes mencionar un usuario para poder usar este comando")

    elif message.content.find("sh.bite") != -1 and not message.author.bot:
        try:
            autor = str(message.author).split("#")[0]
            imagen = Feels.reactionImage("bite")
            try:
                victima = message.mentions[0].name
                embed = discord.Embed(title="{} muerde a {}".format(autor, victima))
            except IndexError:
                raise IndexError("Victima no existe") 
            embed.set_image(url = imagen)
            embed.set_footer(text="Via Tenor")
            await message.channel.send(content=None, embed=embed)

        except IndexError:

            await message.channel.send("Debes mencionar un usuario para poder usar este comando")
    

#Self Reactions

    elif message.content.find("sh.smug") != -1 and not message.author.bot:
        print(message.author)
        autor = str(message.author).split("#")[0]
        imagen = Feels.reactionImage("smug")
        embed = discord.Embed(title="{} es un(a) creido(a)".format(autor))
        embed.set_image(url = imagen)
        embed.set_footer(text="Via Tenor")
        await message.channel.send(content=None, embed=embed)

    elif message.content.find("sh.suicide") != -1 and not message.author.bot:
        print(message.author)
        autor = str(message.author).split("#")[0]
        imagen = Feels.reactionImage("suicide")
        embed = discord.Embed(title="{} se mató".format(autor))
        embed.set_image(url = imagen)
        embed.set_footer(text="Si realmente estas mal y necesitas ayuda visita https://www.stickhorse.cl/lineas-de-ayuda-psicologica-o-lineas-de-suicidio-en-hispano-america/")
        await message.channel.send(content=None, embed=embed)
    
    elif message.content.find("sh.spin") != -1 and not message.author.bot:
        print(message.author)
        autor = str(message.author).split("#")[0]
        imagen = Feels.reactionImage("spin")
        embed = discord.Embed(title="{} se puso a girar como pendejo".format(autor))
        embed.set_image(url = imagen)
        embed.set_footer(text="Via Tenor")
        await message.channel.send(content=None, embed=embed)

    elif message.content.find("sh.blush") != -1 and not message.author.bot:
        print(message.author)
        autor = str(message.author).split("#")[0]
        imagen = Feels.reactionImage("blush")
        embed = discord.Embed(title="{} se sonrojó".format(autor))
        embed.set_image(url = imagen)
        embed.set_footer(text="Via Tenor")
        await message.channel.send(content=None, embed=embed)
    
    elif message.content.find("sh.shy") != -1 and not message.author.bot:
        print(message.author)
        autor = str(message.author).split("#")[0]
        imagen = Feels.reactionImage("shy")
        embed = discord.Embed(title="{} se hace el tímido".format(autor))
        embed.set_image(url = imagen)
        embed.set_footer(text="Via Tenor")
        await message.channel.send(content=None, embed=embed)

    elif message.content.find("sh.tsundere") != -1 and not message.author.bot:
        print(message.author)
        autor = str(message.author).split("#")[0]
        imagen = Feels.reactionImage("tsundere")
        embed = discord.Embed(title="{} es una tsundere".format(autor))
        embed.set_image(url = imagen)
        embed.set_footer(text="Via Tenor")
        await message.channel.send(content=None, embed=embed)
    
    elif message.content.find("sh.lewd") != -1 and not message.author.bot:
        print(message.author)
        autor = str(message.author).split("#")[0]
        imagen = Feels.reactionImage("lewd")
        embed = discord.Embed(title="{} está teniendo pensamientos cochinos".format(autor))
        embed.set_image(url = imagen)
        embed.set_footer(text="Via Tenor")
        await message.channel.send(content=None, embed=embed)

    elif message.content.find("sh.jojo") != -1 and not message.author.bot:
        print(message.author)
        autor = str(message.author).split("#")[0]
        imagen = Feels.reactionImage("jojo")
        embed = discord.Embed(title="{} hizo una Jojopose".format(autor))
        embed.set_image(url = imagen)
        embed.set_footer(text="Via Tenor")
        await message.channel.send(content=None, embed=embed)
        
    elif message.content.find("sh.cry") != -1 and not message.author.bot:
        print(message.author)
        autor = str(message.author).split("#")[0]
        imagen = Feels.reactionImage("cry")
        embed = discord.Embed(title="{} está llorando".format(autor))
        embed.set_image(url = imagen)
        embed.set_footer(text="Via Tenor")
        await message.channel.send(content=None, embed=embed)

    elif message.content.find("sh.smile") != -1 and not message.author.bot:
        print(message.author)
        autor = str(message.author).split("#")[0]
        imagen = Feels.reactionImage("smile")
        embed = discord.Embed(title="{} se puso a sonreir".format(autor))
        embed.set_image(url = imagen)
        embed.set_footer(text="Via Tenor")
        await message.channel.send(content=None, embed=embed)
        
#Dual Reactions

    elif message.content.find("sh.dance") != -1 and not message.author.bot:
        mensaje = message.content.split()
        print(message.author)
        autor = str(message.author).split("#")[0]
        imagen = Feels.reactionImage("dance")
        try:
            if mensaje[1].lower() == "caramelldansen":
                imagen = Feels.reactionImage("caramelldansen")
        except:
            pass
        try:
            victima = message.mentions[0].name
            embed = discord.Embed(title="{} se puso a bailar con {}".format(autor,victima))
        except IndexError:
            embed = discord.Embed(title="{} se puso a bailar".format(autor))
            pass
        embed.set_image(url = imagen)
        embed.set_footer(text="Via Tenor")
        await message.channel.send(content=None, embed=embed)

    elif message.content.find("sh.hug") != -1 and not message.author.bot:
        autor = str(message.author).split("#")[0]
        imagen = Feels.reactionImage("abrazo")
        try:
            victima = message.mentions[0].name
            embed = discord.Embed(title="{} abrazó a {}".format(autor,victima))
        except IndexError:
            embed = discord.Embed(title="{} necesita un abrazo.".format(autor))
            pass
        embed.set_image(url = imagen)
        embed.set_footer(text="Via Tenor")
        await message.channel.send(content=None, embed=embed)

    elif message.content.find("sh.run") != -1 and not message.author.bot:
        autor = str(message.author).split("#")[0]
        try:
            imagen = Feels.reactionImage("run")
            victima = message.mentions[0].name
            embed = discord.Embed(title="{} escapó de {}".format(autor,victima))
        except IndexError:
            imagen = Feels.reactionImage("escapar")
            embed = discord.Embed(title="{} se echó a correr.".format(autor))
            pass
        embed.set_image(url = imagen)
        embed.set_footer(text="Via Tenor")
        await message.channel.send(content=None, embed=embed)

    elif message.content.find("sh.kiss ") != -1 and not message.author.bot:
        autor = str(message.author).split("#")[0]
        imagen = Feels.reactionImage("kiss")
        try:
            victima = message.mentions[0].name
            embed = discord.Embed(title="{} besó a {}".format(autor,victima))
        except IndexError:
            embed = discord.Embed(title="{} quiere un besito.".format(autor))
            pass
        embed.set_image(url = imagen)
        embed.set_footer(text="Via Tenor")
        await message.channel.send(content=None, embed=embed)

    elif message.content.find("sh.sleep") != -1 and not message.author.bot:
        autor = str(message.author).split("#")[0]
        try:
            victima = message.mentions[0].name
            imagen = Feels.reactionImage("sleep")
            embed = discord.Embed(title="{} se fue a dormir con {}".format(autor,victima))
        except IndexError:
            imagen = Feels.reactionImage("sleepy")
            embed = discord.Embed(title="{} tiene sueño".format(autor))
            pass
        embed.set_image(url = imagen)
        embed.set_footer(text="Via Tenor")
        await message.channel.send(content=None, embed=embed)

    elif message.content.find("sh.happy") != -1 and not message.author.bot:
        autor = str(message.author).split("#")[0]
        imagen = Feels.reactionImage("happy")
        try:
            victima = message.mentions[0].name
            embed = discord.Embed(title="{} está feliz por {}".format(autor,victima))
        except IndexError:
            embed = discord.Embed(title="{} está feliz".format(autor))
            pass
        embed.set_image(url = imagen)
        embed.set_footer(text="Via Tenor")
        await message.channel.send(content=None, embed=embed)
        
client.run(os.environ.get('DISCORD_TOKEN'))
