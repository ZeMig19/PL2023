import re,itertools
from prettytable import PrettyTable

# Class Pessoa
# Atributos:
#   i -> idade
#   s -> sexo
#   t -> tensao
#   c -> colesterol
#   b -> batimento
#   td -> tem doenca
class Pessoa:
    def __init__(self, i, s, t, c, b, td):
        self.i = int(i)
        self.s = s
        self.t = int(t)
        self.c = int(c)
        self.b = int(b)
        self.td = int(td)

    # Redefinir funcao de representacao, para os objectos serem convertidos para string quando as listas sao escritas
    def __repr__(self):
        return str(self)
    # Funcao toString
    def __str__(self):
        return f"{self.i}|{self.s}|{self.t}|{self.c}|{self.b}|{self.td}"

#Class Db (Database)
#Atributos:
#   -> lp (lista de pessoas, da classe Pessoa)
class Db:
    def __init__(self, lp):
        self.lp = lp

    def filtra_sexo(self,s,td):
        ret = []
        for p in self.lp:
            if s == p.s and td == p.td:
                ret.append(p)
        return Db(ret)

    def filtra_escaloes(self,r):
        ret = []
        for p in self.lp:
            if p.i in list(r):
                ret.append(p)
        return Db(ret)
    
    def filtra_colestrol(self,v):
        ret = []
        for c in range(v-5,v+5):
            for p in self.lp:
                if p.c == c:
                    ret.append(p)
        return Db(ret)

    def printTabela(self):
        t = PrettyTable(['idade', 'sexo','tensao','colesterol','batimento','temDoenca'])
        for p in self.lp:
           t.add_row([p.i,p.s,p.t,p.c,p.b,p.td])
        print(t)

    # Funcao que permite calcular o numero de pessoas da db. Usado quando se chama len()
    def __len__(self):
        return len(self.lp)

    # Funcao que permite converter esta class para string
    def __str__(self):
        return str(self.lp)
    
# Funcao que permite fazer o parsing do csv com os dados
def parse(f):
    lp = []
    with open(f,"r") as fp:
        ln = 1
        for line in fp.readlines():
            if ln != 1:
                # Expressao regular para validar linha e leitura
                x = re.search("^(\d+),(M|F),(\d+),(\d+),(\d+),(\d+)$", line)
                if x != None:
                    lp.append(Pessoa(x.group(1),x.group(2),x.group(3),x.group(4),x.group(5),x.group(6)))
                else:
                    pass
            ln = ln + 1
    return lp
 
def main():
    f = "myheart.csv"
    db = Db(parse(f))
    
    print(len(db.filtra_sexo("F",0)))
    print(len(db.filtra_escaloes(range(30,34))))
    print(len(db.filtra_escaloes(range(35,39))))
    print(len(db.filtra_escaloes(range(40,44))))

    print((db.filtra_colestrol(180)))

    db.filtra_sexo("F",0).filtra_colestrol(180).printTabela()

if __name__ == "__main__":
    main()