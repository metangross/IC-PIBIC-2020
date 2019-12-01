from random import random
class PSO(object):
    class Individuo(object):
        def __init__(self, posicao, velocidade = 0, valAptidao = 0, melhorValor = 0,melhorPosicao = 0):
            self.posicao = posicao #Posicao da Particula
            self.velocidade = velocidade #Velocidade da Particula
            self.valAptidao = valAptidao #Valor de Aptidão da Particula
            self.melhorValor = melhorValor #Melhor valor de aptidão que a particula ja teve
            self.melhorPosicao = melhorPosicao #Melhor posição que a particula ja teve
    
    
    def __init__(self, vMax, numPop, cognitivo, social):
        self.vMax = vMax
        self.numPop = numPop
        self.cognitivo = cognitivo
        self.social = social
    
    def inicializaPopulacao(self):
        self.populacao = [self.Individuo(random()) for i in range(self.numPop)]
    
    
    def aptidao(self, particula):
        #AQUI É ONDE SERÁ REALIZADO O CALCULO DE APTIDÃO QUE DEPENDERÁ DO PROBLEMA
        return random()
    
    
    def execucao(self):
        self.inicializaPopulacao()
        vInicial = random()
        for i in self.populacao:
            i.velocidade = vInicial
        while True:
            for i in self.populacao:
                i.valAptidao = self.aptidao(i.pInicial)
                if i.valAptidao > i.melhorValor:
                    i.melhorValor = i.valAptidao
                    i.melhorPosicao = i.posicao
            melhorParticula = None
            melhorValor = 0
            for i in self.populacao:
                if i.valAptidao > melhorValor:
                    melhorValor = i.valAptidao
                    melhorParticula = i
            for i in self.populacao:
                variacao = self.cognitivo*(i.melhorPosicao - (-i.posicao)) + self.social*(melhorParticula.posicao - (-i.posicao))
                i.velocidade = i.velocidade + variacao
                i.posicao = i.posicao + i.velocidade
            #if condicao = alcançada:
            #   break

