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

    #Si está en un canal NSFW, recibe codigo de nhentai y devuelve link a pagina (no es mucho más lo que se puede hacer, ya que murió su API
    if message.content.find("sh.nh ") != -1 and message.channel.is_nsfw():

        # Check if in correct channel
        nh_number = message.content[6:]
        await message.channel.send("https://nhentai.net/g/{}".format(nh_number))
    elif message.content.find("sh.nh ") != -1 and not message.channel.is_nsfw():
        await message.channel.send("No sea marrano y pregunte en un canal NSFW")


    
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
