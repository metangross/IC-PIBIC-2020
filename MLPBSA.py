from random import random, gauss,choice, randrange
from math import exp, e
from copy import deepcopy
from decimal import getcontext, Decimal
getcontext().prec = 100

#trainingset = [[[entradas], [saidas esperadas]],
#               [[entradas], [saidas esperadas]]]
#pesos = [[CAMADA[LISTA]]
#pesos = [[[0.2,0.3],[0.4,0.9]],[[],[],[]],[[],[],[],[]]]
neuronios = [2, 1] #NEURONIOS EM CADA CAMADA
trainingset = [[[0, 0],[1]],
               [[0, 1],[0]],
               [[1, 0],[0]],
               [[1, 1],[1]]]


class MLPBSA(object):
    class individuo(object):
        def __init__(self, posicao = None):
            self.posicao = posicao
            self.melhorposicao = None
            self.avaliacao = -99999999999999
            self.melhoravaliacao = -999999999999999

        def geradorPesos(self, neuronios, entradas):
            #Param neuronios:configuração da RNA, entradas: quantidade de entradas
            self.posicao = []
            for i in range(len(neuronios)): #Para cada camada
                self.posicao.append([]) 
                if i is 0:
                    for j in range(neuronios[i]): #Para cada neuronio daquela camada
                        self.posicao[i].append([]) 
                        for k in range(entradas + 1): # Para cada entrada da camada de entrada
                            self.posicao[i][j].append(random())
                else:
                    for j in range(neuronios[i]): #Para cada neuronio daquela camada
                        self.posicao[i].append([])
                        for k in range(neuronios[i-1]+1): # Para cada entrada da camada oculta ou de saida
                            self.posicao[i][j].append(random())
    def __init__(self, neuronios, trainingset, testset = None):
        self.neuronios = neuronios
        self.trainingset = trainingset
        self.testset = testset
        self.bestFitness = -9999999
        self.bestIndividual = None
        self.worstFitness = 99999999
        self.worstIndividual = None
        self.menornum = 2.2250738585072014e-308
    def funcAtiv(self, val):
        return 1/(1 + pow(e,-2*val))

    def forward(self, entradas, pesos):
        resultadosTotal = []
        for i in range(len(self.neuronios)): #Para cada camada
            resultadosCamada = [] 
            if i is 0:
                for j in range(self.neuronios[i]): #Para cada neuronio daquela camada:
                    resultado = 0
                    for k in range(len(pesos[i][j])):
                        if k is 0:
                            resultado += -1 * pesos[i][j][k]
                        else:
                            resultado += entradas[k-1] * pesos[i][j][k]
                    resultado = self.funcAtiv(resultado)
                    resultadosCamada.append(resultado)
            else:
                for j in range(self.neuronios[i]): #Para cada neuronio daquela camada:
                    resultado = 0
                    for k in range(len(pesos[i][j])):
                        if k is 0:
                            resultado += -1 * pesos[i][j][k]
                        else:
                            resultado += resultadosTotal[i-1][k-1] * pesos[i][j][k]
                    resultado = self.funcAtiv(resultado)

                    resultadosCamada.append(resultado)
            resultadosTotal.append(resultadosCamada)
        return resultadosTotal[len(neuronios)-1] #retorna o resultado da camada de saida
    def erro(self, pesos):
        erroTotal = 0
        for i in self.trainingset:
            entradas = i[0]
            esperado = i[1]
            res = self.forward(entradas, pesos)
            erroTeste = 0
            for val in range(len(esperado)):
                erroTeste += abs(esperado[val] - res[val])
            erroTeste = erroTeste/len(esperado)
            erroTotal += erroTeste
        erroTotal = erroTotal/len(self.trainingset)
        return erroTotal
    def inicializaPop(self, numPop, neuronios):
        self.populacao = []
        for i in range(numPop):
            individuo = self.individuo()
            individuo.geradorPesos(neuronios, self.qtdEntradas)
            self.populacao.append(individuo)

    def avaliaPopulacao(self):
        for i in self.populacao:
            erro = self.erro(i.posicao)
            erro = erro + self.menornum
            i.avaliacao = 1/erro

            #input()
            if i.avaliacao > self.bestFitness:
                self.bestFitness = i.avaliacao
                self.bestIndividual = deepcopy(i)
                #print(f"NOVO BEST = {i.avaliacao}")

            if i.avaliacao < self.worstFitness:
                self.worstFitness = i.avaliacao
                self.worstIndividual = deepcopy(i)
            if i.melhoravaliacao is None:
                i.melhoravaliacao = i.avaliacao
                i.melhorposicao = deepcopy(i.posicao)
            elif i.melhoravaliacao is not None and i.avaliacao > i.melhoravaliacao:
                i.melhoravaliacao = i.avaliacao
                i.melhorposicao = deepcopy(i.posicao)
        #input()
    def inicializaMedia(self):
        self.media = []
        for i in range(len(self.neuronios)):
            self.media.append([])
            if i is 0:
                for j in range(self.neuronios[i]):
                    self.media[i].append([])
                    for k in range(self.qtdEntradas+1):
                        self.media[i][j].append(0)
            else:
                for j in range(self.neuronios[i]):
                    self.media[i].append([])
                    for k in range(self.neuronios[i-1]+1):
                        self.media[i][j].append(0)
    def calculaSomaFitnessMedia(self):
        self.sumFit = 0
        for i in self.populacao:
            self.sumFit += i.avaliacao
            for j in range(len(self.neuronios)):
                if j is 0:
                    for k in range(self.neuronios[j]):
                        for l in range(self.qtdEntradas+1):
                            self.media[j][k][l] += i.posicao[j][k][l]
                else:
                    for k in range(self.neuronios[j]):
                        for l in range(self.neuronios[j-1]+1):
                            self.media[j][k][l] += i.posicao[j][k][l]
        self.sumFit += self.menornum #Evitar divisão por 0
        for j in range(len(self.neuronios)):
                if j is 0:
                    for k in range(self.neuronios[j]):
                        for l in range(self.qtdEntradas+1):
                            self.media[j][k][l] /= len(self.populacao)
                else:
                    for k in range(self.neuronios[j]):
                        for l in range(self.neuronios[j-1]+1):
                            self.media[j][k][l] /= len(self.populacao)
    def forage(self, individuo, cognitivo, social):
        for i in range(len(self.neuronios)):
                if i is 0:
                    for j in range(self.neuronios[i]):
                        for k in range(self.qtdEntradas+1):
                            individuo.posicao[i][j][k] += (individuo.melhorposicao[i][j][k] - individuo.posicao[i][j][k]) * cognitivo * random() + (self.bestIndividual.posicao[i][j][k] - individuo.posicao[i][j][k]) * social * random()
                            
                            individuo.posicao[i][j][k] = self.verificaVal(individuo.posicao[i][j][k])
                            
                else:
                    for j in range(self.neuronios[i]):
                        for k in range(self.neuronios[i-1]+1):
                            #print(self.neuronios[i-1]+1)
                            #print(f"Peso {k}")
                            #input()
                            
                            individuo.posicao[i][j][k] += (individuo.melhorposicao[i][j][k] - individuo.posicao[i][j][k]) * cognitivo * random() + (self.bestIndividual.posicao[i][j][k] - individuo.posicao[i][j][k]) * social * random()
                            
                            individuo.posicao[i][j][k] = self.verificaVal(individuo.posicao[i][j][k])
                            
    def vigilance(self,individuo, a1, a2):
        A1 = a1 * exp(-(individuo.melhoravaliacao/self.sumFit) * len(self.populacao))
        m = choice(self.populacao)
        while m is individuo:
            m = choice(self.populacao)
        A2 = a2 * exp(((individuo.melhoravaliacao - m.melhoravaliacao)/(abs(m.melhoravaliacao - individuo.melhoravaliacao) + self.menornum)) * len(self.populacao) * m.melhoravaliacao / self.sumFit)
        for i in range(len(self.neuronios)):
                if i is 0:
                    for j in range(self.neuronios[i]):
                        for k in range(self.qtdEntradas+1):
                            individuo.posicao[i][j][k] += A1 * (self.media[i][j][k] - individuo.posicao[i][j][k]) * random() + A2 * (m.melhorposicao[i][j][k] - individuo.posicao[i][j][k]) * randrange(-1, 1)
                            individuo.posicao[i][j][k] = self.verificaVal(individuo.posicao[i][j][k])
                            
                else:
                    for j in range(self.neuronios[i]):
                        for k in range(self.neuronios[i-1]+1):
                            individuo.posicao[i][j][k] += A1 * (self.media[i][j][k] - individuo.posicao[i][j][k]) * random() + A2 * (m.melhorposicao[i][j][k] - individuo.posicao[i][j][k]) * randrange(-1, 1)
                            individuo.posicao[i][j][k] = self.verificaVal(individuo.posicao[i][j][k])
                            
    def producer(self, individuo):
        for i in range(len(self.neuronios)):
                if i is 0:
                    for j in range(self.neuronios[i]):
                        for k in range(self.qtdEntradas+1):
                            individuo.posicao[i][j][k] += gauss(0,1) * individuo.posicao[i][j][k]
                            individuo.posicao[i][j][k] = self.verificaVal(individuo.posicao[i][j][k])
                            
                else:
                    for j in range(self.neuronios[i]):
                        for k in range(self.neuronios[i-1]+1):
                            individuo.posicao[i][j][k] += gauss(0,1) * individuo.posicao[i][j][k]
                            individuo.posicao[i][j][k] = self.verificaVal(individuo.posicao[i][j][k])
                            
    def scrounger(self, individuo, FL):
        m = choice(self.populacao)
        while m is individuo:
            m = choice(self.populacao)
        for i in range(len(self.neuronios)):
                if i is 0:
                    for j in range(self.neuronios[i]):
                        for k in range(self.qtdEntradas+1):
                            individuo.posicao[i][j][k] += (m.posicao[i][j][k] - 0) * FL * random()
                            individuo.posicao[i][j][k] = self.verificaVal(individuo.posicao[i][j][k])
                            
                else:
                    for j in range(self.neuronios[i]):
                        for k in range(self.neuronios[i-1]+1):
                            individuo.posicao[i][j][k] += (m.posicao[i][j][k] - 0) * FL * random()
                            individuo.posicao[i][j][k] = self.verificaVal(individuo.posicao[i][j][k])
                            
    def verificaVal(self, peso):
        if peso > self.limSup:
            peso = self.limSup
        if peso < self.limInf:
            peso = self.limInf
        return peso
    def execucao(self, numPop, maxIter, freqVoo, probForage, cognitivo, social, a1, a2, FL, limSup, limInf):
        self.qtdEntradas = len(self.trainingset[0][0])
        self.inicializaPop(numPop, self.neuronios)
        self.avaliaPopulacao()
        self.limSup = limSup
        self.limInf = limInf
        t = 0
        while (t < maxIter):
            self.inicializaMedia()    
            self.calculaSomaFitnessMedia()
            #print(t)
            if (t % freqVoo is not 0):#Não irá voar
                for i in self.populacao: #Para cada individuo
                    if random() < probForage: #Forage for Food
                        self.forage(i,cognitivo,social)
                    else:
                        self.vigilance(i, a1, a2)
            else:
                for i in self.populacao:
                    if i is self.bestIndividual or (random() > 0.5 and i is not self.worstIndividual):
                        self.producer(i)
                    else:
                        self.scrounger(i, FL)
            self.avaliaPopulacao()
            t = t + 1
            #print(f"Best = {self.bestIndividual.avaliacao}")
        return self.bestIndividual
