from random import random, gauss, choice, uniform
from math import exp
from sys import float_info
import xlwt
menornum = 2.2250738585072014e-308
peso = 500
class BSA(object):
    class individuo(object):
        def __init__(self, posicao):
            self.posicao = posicao
            self.melhorPosicao = 0
            self.fitness = 0
            self.melhorFitness = -99999999999999999
        def printPosicao(self):
            print(f"{self.posicao}")
    def inicializaPop(self):
        self.populacao = [self.individuo([random(),random()]) for i in range(0, self.numPop)]          
    def __init__(self, numPop, maxIter, freqVoo, probForage, cognitivo, social, a1, a2, FL, limsup, liminf):
        self.numPop = numPop
        self.maxIter = maxIter
        self.freqVoo = freqVoo
        self.probForage = probForage
        self.cognitivo = cognitivo
        self.social = social
        self.a1 = a1
        self.a2 = a2
        self.FL = FL
        self.limsup = limsup
        self.liminf = liminf
    def aptidao(self, individuo):
        #individuo.posicao[1] = 1100 - individuo.posicao[0] #Substituição
        #func = 0.01*pow(individuo.posicao[0],2) - 10*individuo.posicao[0] + 5000 + 0.005*pow(individuo.posicao[1],2) - 3*(individuo.posicao[1]) + 500
        func = 0.01*pow(individuo.posicao[0],2) - 10*individuo.posicao[0] + 5000 + 0.005*pow(individuo.posicao[1],2) - 3*(individuo.posicao[1]) + 500 + (abs(1100 - individuo.posicao[0] - individuo.posicao[1])) * peso
        fitness = 1/func
        individuo.fitness = fitness
        if individuo.fitness > individuo.melhorFitness:
            individuo.melhorFitness = individuo.fitness
            individuo.melhorPosicao = individuo.posicao.copy()
    def avaliaPopilacao(self):
        bestFitness = -99999999999999
        for i in self.populacao:
            self.aptidao(i)
            if i.fitness > bestFitness:
                bestFitness = i.fitness
                bestIndividual = i
        
        return bestFitness, bestIndividual
    def execucao(self):
        t = 0
        self.inicializaPop()
        bestFitness, bestIndividual = self.avaliaPopilacao()
        
        while(t < self.maxIter):
            sumFit = 0
            media = [0 for i in range(len(bestIndividual.posicao))]
            for j in self.populacao:
                sumFit += j.melhorFitness
                for i in range(len(bestIndividual.posicao)):
                    media[i] += j.posicao[i]
            
            for i in range(len(bestIndividual.posicao)):
                    media[i] = media[i]/self.numPop
            sumFit += menornum
            if (t % (self.freqVoo) is not 0):
                for i in self.populacao:
                    if random() < self.probForage:
                        for j in range(len(i.posicao)):
                            i.posicao[j] = i.posicao[j] + (i.melhorPosicao[j] - i.posicao[j]) * self.cognitivo * random() + (bestIndividual.posicao[j] - i.posicao[j]) * self.social * random()
                            if self.limsup is not None and i.posicao[j] > self.limsup[j]:
                                i.posicao[j] = self.limsup[j]
                            if self.liminf is not None and i.posicao[j] < self.liminf[j]:
                                i.posicao[j] = self.liminf[j]
                    else:
                        pFit = i.melhorFitness
                        pFitK = choice(self.populacao).melhorFitness
                        
                        while pFitK is pFit:
                            pFitK = choice(self.populacao).melhorFitness
                        A1 = self.a1 * exp( -(pFit/sumFit) * self.numPop) 
                        A2 = self.a2 * exp((pFit - pFitK)/(abs(pFitK - pFit)+menornum)*((self.numPop * pFitK)/(sumFit + menornum)))
                        for j in range(len(i.posicao)):
                            i.posicao[j] = i.posicao[j] + A1 * (media[j] - i.posicao[j]) * random() + A2 * (i.melhorPosicao[j] - i.posicao[j]) * uniform(-1, 1)
                            if self.limsup is not None and i.posicao[j] > self.limsup[j]:
                                i.posicao[j] = self.limsup[j]
                            if self.liminf is not None and i.posicao[j] < self.liminf[j]:
                                i.posicao[j] = self.liminf[j]
            else:
                best = -99999999999
                bestIndex = 0
                worst = float("Inf")
                worstIndex = 0
                for i in range(len(self.populacao)):
                    if self.populacao[i].melhorFitness > best:
                        best = self.populacao[i].melhorFitness
                        bestIndex = i
                    elif self.populacao[i].melhorFitness < worst:
                        worst = self.populacao[i].melhorFitness
                        worstIndex = i
                for i in range(len(self.populacao)):
                    if i is bestIndex:
                        Gauss = gauss(0, 1)*1
                        for j in range(len(self.populacao[i].posicao)):
                            self.populacao[i].posicao[j] = self.populacao[i].posicao[j] + Gauss*self.populacao[i].posicao[j]
                            if self.limsup is not None and self.populacao[i].posicao[j] > self.limsup[j]:
                                self.populacao[i].posicao[j] = self.limsup[j]
                            if self.liminf is not None and self.populacao[i].posicao[j] < self.liminf[j]:
                                self.populacao[i].posicao[j] = self.liminf[j]
                    elif i is worstIndex or random() > 0.5:
                        Random = random()
                        k = choice(self.populacao)
                        while k is self.populacao[i]:
                            k = choice(self.populacao)
                        for j in range(len(self.populacao[i].posicao)):
                            self.populacao[i].posicao[j] = self.populacao[i].posicao[j] + (k.posicao[j] - self.populacao[i].posicao[j]) * self.FL * Random
                            if self.limsup is not None and self.populacao[i].posicao[j] > self.limsup[j]:
                                self.populacao[i].posicao[j] = self.limsup[j]
                            if self.liminf is not None and self.populacao[i].posicao[j] < self.liminf[j]:
                                self.populacao[i].posicao[j] = self.liminf[j]
            
            bestFitness, bestIndividual = self.avaliaPopilacao()
            t += 1
#Execução
N = [3, 5, 10, 20]
M = [10, 50, 100, 200, 500, 1000]
FQ = [5, 10, 20, 50, 100]
P = [0.7,0.8,0.9,1]
wb = xlwt.Workbook()
ws = wb.add_sheet("Resultados")
colunas = ["N", "M", "FQ", "P", "Melhor Fitness", "Melhor Posicao", "Média dos Fitness"]
for i in range(len(colunas)):
    ws.write(0, i, colunas[i])
linha = 1
for fq in FQ:
    for p in P:
        for n in N:
            for m in M:
                teste = BSA(n,m,fq,p,1.5,1.5,1,1,0.5, [1000, 700], None)
                teste.execucao()
                #for pop in teste.populacao:
                #    print(f"Melhor Pos = {pop.melhorPosicao}")
                #    print(f"Melhor Fit = {pop.melhorFitness}")
                #input()
                i = 1
                melhor = None
                posicao = None
                media = 0
                for individuo in teste.populacao:
                    media += individuo.melhorFitness
                    if melhor is None:
                        melhor = individuo.melhorFitness
                        posicao = individuo.melhorPosicao
                    elif individuo.melhorFitness > melhor:
                        melhor = individuo.melhorFitness
                        posicao = individuo.melhorPosicao
                media = media / len(teste.populacao)
                melhor = str(melhor)
                melhor = melhor.replace(".",",")
                media = str(media)
                media = media.replace(".",",")
                elementos = [n, m, fq, p, melhor, posicao, media]
                for col in range(len(colunas)):
                    ws.write(linha, col, str(elementos[col]))
                linha = linha + 1
wb.save(f"Resultados(Punição peso {peso}).xls")