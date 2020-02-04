import random

def roll (cant_dados = 1, cant_caras = 20):
    pass

def fateroll (cant_dados=1, mod=0, authorName=""):
    try:
        if int(cant_dados)<20:
            textopositivo = ""
            textonegativo = ""
            contador = 0
            positivos = 0
            negativos = 0
            for x in range(1, (1+int(cant_dados))):
                result = random.randint(1, 2)
                if result == 1:
                    textopositivo += "+"
                    contador += 1
                    positivos += 1
                        
                if result == 2:
                    textonegativo += "-"
                    contador -= 1
                    negativos += 1
            resultado = contador+int(mod)

            finalRoll = "El roll de {} es ({}{}) ({}{}) ({})".format(authorName,textopositivo,textonegativo,contador,mod,resultado)
            return finalRoll
        else:
            return ("Intentas rolear una cantidad muy grande de dados")
    except:
        return ("Ocurrio un error al intentar rolear")