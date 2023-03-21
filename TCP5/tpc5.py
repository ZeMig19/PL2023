import re, sys, math
from functools import reduce

def estado_levantar(res):
    print("maq: \"Introduza moedas.\"")
    return 0

def estado_pousar(res):
    print(f'maq: \"troco= {moeda_to_string(res["saldo"])}; Volte sempre!\"')
    return 0

def moeda_to_string(m):
    return f"{int(math.modf(m)[1])}e{int(math.modf(m)[0]*100)}c"

def estado_moeda(res):
    err = ""
    moedas = re.findall("\d+[e|c]",res["line"])
    
    for m in moedas:
        if m in maquina_estados["MOEDA"]["moedas"]:
            res["saldo"] = res["saldo"] + maquina_estados["MOEDA"]["moedas"][m]
        else:
            err = f"{err}{m} - moeda inválida; "
    
    print(f'maq: \"{err}saldo = {moeda_to_string(res["saldo"])}\"')
    return res["saldo"]

def estado_t(res):
    ext = res["estado_input"].groups()[0]
    num = res["estado_input"].groups()[1]
    
    if ext in maquina_estados["T=numero"]["numeros"]:
        if maquina_estados["T=numero"]["numeros"][ext] == -1:
            print(f'maq: \"Esse número não é permitido neste telefone. Queira discar novo número!\"')
        elif maquina_estados["T=numero"]["numeros"][ext] > res["saldo"]:
            print(f'maq: \"Nao dispoe Saldo suficiente. Custo chamada = {maquina_estados["T=numero"]["numeros"][ext]}, saldo = {res["saldo"]} \"')
        else:
            res["saldo"] = res["saldo"] - maquina_estados["T=numero"]["numeros"][ext]
            print(f'maq: \"saldo = {moeda_to_string(res["saldo"])}\"')
    return res["saldo"]

def estado_abortar(res):
    return estado_pousar(res)

maquina_estados = {
    "LEVANTAR": {
        "depende" : [
                    "POUSAR"
        ],
        "regex" : "^LEVANTAR$",
        "funcao" : estado_levantar
    },
    "POUSAR": {
        "depende" : [
            "LEVANTAR",
            "MOEDA",
            "T=numero",
            "ABORTAR"
        ],
        "regex" : "^POUSAR$",
        "funcao" : estado_pousar
    },
    "MOEDA" : {
        "depende" : [
            "LEVANTAR",
            "MOEDA",
            "T=numero"
        ],
        "regex": "^MOEDA( (\d{1,2})[c|e][,|.])+$",
        "funcao" : estado_moeda,
        "moedas" : {
            "10c" : 0.1,
            "20c" : 0.2,
            "50c" : 0.5,
            "1e"  : 1,
            "2e"  : 2,
        }
    },
    "T=numero": {
        "depende": [
            "LEVANTAR",
            "T=numero",
            "MOEDA",
        ],
        "regex" : "^T=(601|641|00|2|800|808)(\d{6,10})$",
        "funcao" : estado_t,
        "numeros" : {
            "601" : -1,
            "641" : -1,
            "00"  : 1.5,
            "2"   : 0.25,
            "800" : 0,
            "808" : 0.1
        }
    },
    "ABORTAR": {
        "depende": [
            "LEVANTAR"
        ],
        "regex" : "^ABORTAR$",
        "funcao" : estado_abortar
    }

}

def main():
    estado_atual = "POUSAR"
    saldo  = 0
    for line in sys.stdin:
        
        for prox_estado in maquina_estados:
            regex = maquina_estados[prox_estado]["regex"]
            estado_input = re.search(regex,line)
            if estado_input != None:
                if estado_atual not in maquina_estados[prox_estado]["depende"] :
                    print(f'maq: \"Transicao de estados invalida. Maquina no estado {estado_atual}. Para ir para {prox_estado} tenho de vir de : {str( maquina_estados[prox_estado]["depende"])} \"')
                else:
                    estado_atual = prox_estado
                    saldo = maquina_estados[estado_atual]["funcao"](
                        {
                        "estado_input": estado_input, 
                        "line": line,
                        "saldo": saldo
                        }
                        )
                break
    
if __name__ == "__main__":
    main()