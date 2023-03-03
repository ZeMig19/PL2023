import re
from pathlib import Path
from datetime import datetime
import math
import json

# Usar como referencia o caminho do script para descobrir onde estao os ficheiros que sao inseridos por argumento
file_path = str(Path( __file__ ).parent.absolute())

# Funcao: processos_read
# Input: f_name, o nome do ficheiro a abrir
# Output: Lista de listas correspondente a cada linha e argumento delimitado por ::
def processos_read(f_name):
    processos_list = []
    # Abrir ficheiro usando como base o caminho onde esta o script
    with open(file_path + "\\" + f_name,"r") as f:
        # Por cada linha, criar uma lista em que cada elemento corresponde a delimitacao
        for line in f:
            processos_list.append(line.split("::"))
    return processos_list

# Funcao: processos_get_elem -> Tenta ler elemento de uma lista de processo. Se elemento nao existir, retorna string vazia
# Input: processo, Recebe uma lista que corresponde a um processo. Cada elemento do processo é um campo da lista.
# Input: elem, index do elemento a tentar ler
# Output: Recebe o elemento apontado por index. Se nao existir, retorna string vazia
def processos_get_elem(processo,elem):
    if elem > len(processo):
        return ""
    return processo[elem]

# Funcao: processos_to_dict -> Converte uma lista de processos (gerada pela funcao processos_read()) para um dicionario
# Input: processos_list, Recebe uma lista de processos (string)
# Output: Retorna um lista de dicionarios garantindo os tipos de dados correspondentes
def processos_to_dict(processos_list):
    processos_dict = {}
    for p in processos_list:
        if len(p) >= 4:
            id = int(processos_get_elem(p, 0))
            processos_dict[id] = {
                'data_nasc' : datetime.strptime(processos_get_elem(p, 1), '%Y-%m-%d'),
                'nome' : processos_get_elem(p, 2),
                'pai' : processos_get_elem(p, 3),
                'mae' : processos_get_elem(p, 4),
                'detalhes' : processos_get_elem(p, 5),
                'relativos' : processo_get_relativos(processos_get_elem(p, 5))
            }
    return processos_dict

# Funcao: processos_year_limits -> Em um dicionario de processos, descobre qual o ano mais antigo e o mais recentes (limites)
# Input: p_d, Recebe uma lista de dicionarios de processos
# Output: Retorna um array, em que o primeiro elemento e o ano mais antigo e o segundo, o ano mais recente
def processos_year_limits(p_d):
    min = None
    max = None
    for p in p_d:
        if min == None or min > p_d[p]['data_nasc']:
            min = p_d[p]['data_nasc']
        if max == None or max < p_d[p]['data_nasc']:
            max = p_d[p]['data_nasc']

    return [min.year, max.year]

# Funcao: processos_seculo_limits -> Descobre o seculo mais antigo e o seculo mais recente de uma lista de dicionarios de processos
# Input: p_d, Recebe uma lista de dicionarios de processos
# Output: Retorna um array, em que o primeiro elemento e o seculo mais antigo e o segundo, o seculo mais recente
def processos_seculo_limits(p_d):
    min = None
    max = None
    for p in p_d:
        if min == None or min > math.ceil(p_d[p]['data_nasc'].year/100):
            min = math.ceil(p_d[p]['data_nasc'].year/100)
        if max == None or max < math.ceil(p_d[p]['data_nasc'].year/100):
            max = math.ceil(p_d[p]['data_nasc'].year/100)

    return [min, max]

# Funcao: processos_get_per_year -> Retorna todos os processos de um determinado ano
# Input: p_d, Recebe uma lista de dicionarios de processos
# Input: y, Ano a pesquisar
# Output: Retorna uma lista de dicionarios de processos do ano correspondente a pesquisar
def processos_get_per_year(p_d,y):
    c = []
    for p in p_d:
        if p_d[p]['data_nasc'].year == y:
            c.append(p_d[p])
    return c

# Funcao: processos_get_por_seculo -> Retorna todos os processos de um determinado seculo
# Input: p_d, Recebe uma lista de dicionarios de processos
# Input: s, seculo a pesquisar
# Output: Retorna uma lista de dicionarios de processos do seculo correspondente a pesquisar
def processos_get_por_seculo(p_d,s):
    c = []
    for p in p_d:
        if math.ceil(p_d[p]['data_nasc'].year/100) == s:
            c.append(p_d[p])
    return c

# Funcao: processos_freq_processos_por_ano -> Retorna quantos processos existem por ano (dos limites existentes)
# Input: p_d, Recebe uma lista de dicionarios de processos
# Output: Retorna um dicionario, e que a chave de cada elemento e o ano e o valor a soma de todos os processos 
def processos_freq_processos_por_ano(p_d):
    processos_freq_dict = {}
    [y_min, y_max] = processos_year_limits(p_d)
    for y in range(y_min, y_max):
        if len(processos_get_per_year(p_d,y)) > 0:
            processos_freq_dict[y] = len(processos_get_per_year(p_d,y))
    return processos_freq_dict

# Funcao: processos_freq_nomes_seculo -> Retorna quantos processos existem por seculo (dos limites existentes)
# Input: p_d, Recebe uma lista de dicionarios de processos
# Output: Retorna um dicionario, e que a chave de cada elemento e o seculo e o valor a soma de todos os processos desse seculo
def processos_freq_nomes_seculo(p_d):
    primeiros_nomes = {}
    ultimos_nomes = {}
    [y_min, y_max] = processos_year_limits(p_d)
    [c_min, c_max] = processos_seculo_limits(p_d)
    # Percorrer seculo a seculo
    for c in range(c_min, c_max):
        # Percorrer ano a ano 
        for y in range(y_min, y_max):
            # Verificar se o ano pertence ao securo
            if math.ceil(y/100) == c:
                # Pesquisar todos os processos do ano em questao
                for py in processos_get_per_year(p_d,y):
                    # Split do nome para saber nome proprio e apelido
                    nomes = py['nome'].split(" ")
                    # Nome proprio
                    p_nome = nomes[0]
                    # Apelido
                    u_nome = nomes[len(nomes) - 1]

                    # Contabilizar nome proprio. Se nao existir, cria
                    if p_nome in primeiros_nomes:
                        primeiros_nomes[p_nome] = primeiros_nomes[p_nome] + 1
                    else:
                        primeiros_nomes[p_nome] = 1

                    # Contabilizar ultimo nome. Se nao existir, cria
                    if u_nome in ultimos_nomes:
                        ultimos_nomes[u_nome] = ultimos_nomes[u_nome] + 1
                    else:
                        ultimos_nomes[u_nome] = 1
        return [primeiros_nomes, ultimos_nomes]

# Funcao: processos_freq_nomes_seculo_ultimos_5 -> Retorna os 5 nomes mais frequentes por seculo
# Input: p_d, Recebe uma lista de dicionarios de processos
# Output: Retorna um dicionario, e que a chave de cada elemento e o seculo e o valor e uma lista de dicionarios de nomes de pessoas e frequencia
def processos_freq_nomes_seculo_ultimos_5(p_d):
    [p_nomes, u_nomes] = processos_freq_nomes_seculo(p_d)
    return [
        dict(sorted(p_nomes.items(), key=lambda x:x[1],reverse=True)[0:5]),  
        dict(sorted(u_nomes.items(), key=lambda x:x[1],reverse=True)[0:5])
            ]

# Funcao: processo_get_relativos -> Retorna os familiares com base no campo dos detalhes
# Input: detalhes, String com o campo dos familiares
# Output: Retorna lista de dicionarios com os familiares
def processo_get_relativos(detalhes):
    relativos = []
    for relativo in re.findall(r"([^,;.]+),([^,;.]+). Proc.([0-9]+).",detalhes):
        try:
            nome = relativo[0].strip()
            tipo = relativo[1].lower()
            num = int(relativo[2])
            relativos.append({"nome" : nome, "tipo" : tipo, "num" : num})
        except:
            pass
    return relativos

# Funcao: processo_calcula_relacoes -> Calcula os diferentes relacionamentos de uma pessoa.
# Input: p_d, Recebe uma lista de dicionarios de processos
# Output: Retorna um dicionario com a contabilidade dos tipos de relacao
def processo_calcula_relacoes(p_d):
    rel = {}
    for p in p_d:
        for r in p_d[p]['relativos']:
            if r["tipo"] in rel:
                rel[r["tipo"]] = rel[r["tipo"]] + 1
            else:
                rel[r["tipo"]] = 1
    return dict(sorted(rel.items(), key=lambda x:x[1],reverse=True)),  

# Funcao: primeiros_20_to_json -> Converte os 20 primeiros registos para ficheiro json
# Input: f_name, Nome do ficheiro json a escrever
# Input: p_d, Recebe uma lista de dicionarios de processos
# Output: nada
def primeiros_20_to_json(f_name,p_d):
    jsonString = json.dumps({k: p_d[k] for k in list(p_d)[:20]},indent=2,default=str)
    with open(file_path + "\\" + f_name,"w") as f:
        f.write(jsonString)
 
# Funcao main
# Explicacao: 
#   1 - Carrega do ficheiro processos.txt
#   2 - Converte ficheiro para dicionario
#   3 - Executa perguntas do enunciado
def main():
    # Carregar ficheiro de texto para uma lista, separando com o caracter delimitador ::
    p_l = processos_read("processos.txt")
    # Imprimir quantas linhas foram carregadas
    print(len(p_l))
    # Converter lista com parametros, para dicionario garantindo os tipos de dados
    p_d = processos_to_dict(p_l)

    # Alinea a) Calcula a frequência de processos por ano (primeiro elemento da data)
    print("------------------------ Alinea a) ---------------------------")
    p_d_f = processos_freq_processos_por_ano(p_d)
    # Alinea a) Resultados
    print(p_d_f)
    print("---------------------- Fim Alinea a) -------------------------")

    # Alinea b) Calcula a frequência de nomes próprios (o primeiro em cada nome) e apelidos (o ultimo em cada nome) por séculos e apresenta os 5 mais usados
    print("------------------------ Alinea b) ---------------------------")
    [p_nomes, u_nomes] = processos_freq_nomes_seculo_ultimos_5(p_d)
    print(p_nomes)
    print(u_nomes)
    print("---------------------- Fim Alinea b) -------------------------")
    
    # Alinea c) Calcula a frequência dos vários tipos de relação: irmão, sobrinho, etc.;
    print("------------------------ Alinea c) ---------------------------")
    r = processo_calcula_relacoes(p_d)
    print(r)
    print("---------------------- Fim Alinea c) -------------------------")

    # Alinea d) Converta os 20 primeiros registos num novo ficheiro de output mas em formato **Json**.
    print("------------------------ Alinea d) ---------------------------")
    primeiros_20_to_json("primeiros20.json",p_d)
    print("Criado ficheiro 'primeiros20.json'")
    print("---------------------- Fim Alinea d) -------------------------")

# Inicio de execucao do programa, chama a funcao main
if __name__ == "__main__":
    main()