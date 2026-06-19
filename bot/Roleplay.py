import random


def roll(cant_dados=1, cant_caras=20, bonificador=0, authorName=""):
    resultado = bonificador
    stringDados = ""
    if(cant_dados <= 10):
        # Simula el tiro de x dadod
        for x in range(1, (1+cant_dados)):
            # Tira el dado
            dado = random.randint(1, cant_caras)
            resultado = resultado + dado
            if(stringDados == ""):
                stringDados = "{}".format(str(dado))
            elif(stringDados != ""):
                stringDados = "{}+{}".format(stringDados, str(dado))

            
    elif(cant_dados > 10):
        return ("Ocurrio un error al intentar rolear")
    #Respuesta se compone de nombre de usuario, total = suma de tiros + bonificador
    respuesta = "El roll de {}: {} = ({})+{}".format(authorName,resultado,stringDados,bonificador)
    return respuesta

FATE_LADDER = {
    8: "Legendario", 7: "Épico", 6: "Fantástico",
    5: "Soberbio", 4: "Genial", 3: "Bueno",
    2: "Regular", 1: "Promedio", 0: "Mediocre",
    -1: "Pobre", -2: "Terrible"
}

def fateroll(cant_dados=4, mod=0, authorName=""):
    if int(cant_dados) > 10:
        return "Máximo 10 dados Fate."

    CARA = {1: "[+]", 0: "[ ]", -1: "[-]"}
    dados = [random.choice([-1, -1, 0, 0, 1, 1]) for _ in range(int(cant_dados))]
    suma = sum(dados)
    resultado = suma + int(mod)

    dados_str = " ".join(CARA[d] for d in dados)
    mod_str = f"{int(mod):+d}" if int(mod) != 0 else ""
    ladder = FATE_LADDER.get(resultado, "Legendario+" if resultado > 8 else "Terrible-")

    return (
        f"**{authorName}** tiró {cant_dados}dF{mod_str}\n"
        f"{dados_str}\n"
        f"**{suma}{mod_str} = {resultado} — {ladder}**"
    )
