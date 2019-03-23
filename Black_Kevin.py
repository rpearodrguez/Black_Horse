from random import randint
import discord
import Setup



client = discord.Client()
'''
Bot para Stick Horse
Versión 0.0.1 - Ingreso comandos básicos, puesta en marcha
Autor: Richard Peña (Vaalus)
Desarrollado en Python 3.7 usando api Discord.py rewrite
'''
@client.event
async def on_message(message):
    print(message.content) # Now every message sent will be printed to the console

@client.event
async def on_message(message):
    #entrega información de comandos
    if message.content.find("sh.help") != -1:
        await message.channel.send("Ayuda Stick Horse - Beta:\n prefijo sh.\n hola = Devuelve tu saludo al estilo Stick Horse \n nh <codigo manga nhentai> = entrega enlace a pagina de nhentai") # If the user says !hello we will send back hi

    #saluda a quien lo salude
    if message.content.find("sh.hola") != -1:
        await message.channel.send("Come tierra") # If the user says !hello we will send back hi

    #recibe codigo de nhentai y devuelve link a pagina (no es mucho más lo que se puede hacer, ya que murió su API
    if message.content.find("sh.nh ") != -1:
        nh_number = message.content[6:]
        await message.channel.send("https://nhentai.net/g/{}".format(nh_number))


    
    if message.content.find("sh.anime ") != -1:
        #tag = on_message[9:]
        await message.channel.send("desarrollo en proceso)
        
    
    #frases random de jojos
    if message.content.find("sh.jojos") != -1:
        #a = randint(1, 5)
        #if a == 1:
        #    await message.channel.send("Yare yare daze ")
        #if a == 2:
        await message.channel.send("desarrollo en proceso")





client.run(Setup.token)