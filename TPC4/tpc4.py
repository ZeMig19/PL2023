import re
from pathlib import Path
import math
import json
from functools import reduce

# Usar como referencia o caminho do script para descobrir onde estao os ficheiros que sao inseridos por argumento
file_path = str(Path( __file__ ).parent.absolute())

# csv_read permite ler de um ficheiro csv, linha a linha em que cada campo tem delimitador e retorna uma lista
# de listas correspondendo a cada elemento de uma linha. Atencao, este resultado nao e o final
def csv_read(f_name, separador=","):
    csv_list = []
    with open(file_path + "\\" + f_name,"r",encoding="utf-8") as f:
        for line in f:
            for fix in re.findall(r'{\d,\d}', line):
                line = line.replace(fix,fix.replace(",",";"))

            csv_list.append(list(map(lambda elem: elem.replace('\n', ''), line.split(separador))))
    return csv_list

# csv_list_parse_colunas permite fazer parsing da estrutura retornada pela funcao csv_read, e ,
# permite faz parsing de todos os campos definidos no enunciado. Esta funcao retorna um objecto json
def csv_list_parse_colunas(csv_list_c):
    ret = []
    for c in csv_list_c:
        elem = {}
        n_t_lim_fixo = re.match(r"(.+){(\d)}",c)
        n_t_lim_fixo_f = re.match(r"(.+){(\d)}::(.+)",c)
        n_t = re.match(r"(.+){(\d);(\d)}",c)
        n_t_f = re.match(r"(.+){(\d);(\d)}::(.+)",c)
        if n_t_f:
            elem["coluna"] = n_t_f[1]
            elem["lim_in"] = int(n_t_f[2])
            elem["lim_sup"] = int(n_t_f[3])
            elem["func"] = str(n_t_f[4])
        elif n_t:
            elem["coluna"] = n_t[1]
            elem["lim_in"] = int(n_t[2])
            elem["lim_sup"] = int(n_t[3])
        elif n_t_lim_fixo_f:
            elem["coluna"] = n_t_lim_fixo_f[1]
            elem["lim_in"] = int(n_t_lim_fixo_f[2])
            elem["lim_sup"] = int(n_t_lim_fixo_f[2])
            elem["func"] = str(n_t_lim_fixo_f[3])
        elif n_t_lim_fixo:
            elem["coluna"] = n_t_lim_fixo[1]
            elem["lim_in"] = int(n_t_lim_fixo[2])
            elem["lim_sup"] = int(n_t_lim_fixo[2])
        elif c != '':
            elem["coluna"] = c

        ret.append(elem)

    return ret
    
# csv_list_parse_linha permite executar todos os comandos definidos pelo objecto json retornado pela funcao
# csv_list_parse_colunas.  Ele permite executar os campos dinamicos (::, sum, media, ...)
def csv_list_parse_linha(linha, colunas):
    if len(linha) > len(colunas):
        print(len(linha))
        print(len(colunas))
        print("ERRO")
        print(linha)
        exit(0)

    ret = {}
    lista_ler = None
    j = 0
    for i in range(len(linha)):
        coluna = colunas[i]
        campo = linha[i]
        
        if lista_ler != None:
            j = j + 1

            if campo == '' and j < lista_ler['lim_in']:
                print(f"ERRO: Lista invalida - lim_in :: {linha}")
                exit(1)
            
            if campo != '' and j > lista_ler['lim_sup']:
                print(f"ERRO: Lista invalida - lim_sup :: {linha}")
                exit(1)
            
            if campo != '':
                ret[lista_ler['coluna']].append(int(campo))

            if 'func' in lista_ler:
                if lista_ler['func'].lower() == "media":
                    ret[lista_ler['func']] = reduce(lambda a, b: a + b,  ret[lista_ler['coluna']]) / len( ret[lista_ler['coluna']])
                if lista_ler['func'].lower() == "sum":
                    ret[lista_ler['func']] = reduce(lambda a, b: a + b,  ret[lista_ler['coluna']])
        else:
            if 'coluna' in coluna:
                ret[coluna['coluna']] = campo
            if 'lim_sup' in coluna and 'lim_in' in coluna:
                ret[coluna['coluna']] = []
                lista_ler = coluna
    return ret

# csv_list_to_json permite converter um objecto csv_list para uma string json
def csv_list_to_json(csv_list):
    i = 0
    colunas = []
    linha_json = []
    for c in csv_list:
        if i == 0:
            colunas = csv_list_parse_colunas(c)
        else:
            linha_json.append(csv_list_parse_linha(c,colunas))
        i = i  + 1
    return linha_json

# main, funcao onde inicia todo o programa. Tenta abrir os diferentes ficheiros csv e converte
# para json
def main():
    for i in range(1,6):
        print(f"alunos{i}.csv -> alunos{i}.json")
        alunos_csv = csv_read(f"alunos{i}.csv")
        j = csv_list_to_json(alunos_csv)
        with open(f"alunos{i}.json", "w", encoding="utf8") as outfile:
            json.dump(j, outfile,indent=4,ensure_ascii=False)


if __name__ == "__main__":
    main()