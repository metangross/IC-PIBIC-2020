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
        self.vMax = vMax #VELOCIDADE MAXIMA
        self.numPop = numPop #NUMERO DE PARTICULAS
        self.cognitivo = cognitivo #COMPONENTE COGNITIVO
        self.social = social #COMPONENTE SOCIAL
    
    def inicializaPopulacao(self):
        self.populacao = [self.Individuo(random()) for i in range(self.numPop)] #INICIALIZA OS INDIVIDUOS COM VELOCIDADES ALÉATORIAS
    
    
    def aptidao(self, particula):
        #AQUI É ONDE SERÁ REALIZADO O CALCULO DE APTIDÃO QUE DEPENDERÁ DO PROBLEMA
        return random()
    
    
    def execucao(self):
        self.inicializaPopulacao() #CRIA E INICIALIZA A POPULAÇÃO
        vInicial = random() #DEFINE UMA VELOCIDADE INICIAL RANDÔMICA
        for i in self.populacao:
            i.velocidade = vInicial #DEFINE A VELOCIDADE INICIAL DE CADA PARTICULA IGUALMENTE
        while True: #CONDIÇÃO DE PARADA
            for i in self.populacao:
                i.valAptidao = self.aptidao(i.pInicial) #CALCULA A APTIDÃO DA PARTICULA
                if i.valAptidao > i.melhorValor: #VERIFICA SE A APTIDÃO DA PARTICULA É MAIOR QUE O MELHOR DA PARTICULA
                    i.melhorValor = i.valAptidao #ATUALIZA O MELHOR VALOR DE APTIDÃO
                    i.melhorPosicao = i.posicao #ATUALIZA A MELHOR POSIÇÃO 
            melhorParticula = None #VARIAVEL QUE SERÁ ARMAZENADA A MELHOR PARTICULA GLOBAL
            melhorValor = 0 #MELHOR VALOR DE APTIDÃO
            for i in self.populacao: 
                if i.valAptidao > melhorValor: #VERIFICA SE A APTIDÃO DA PARTICULA É MAIOR QUE O MELHOR GLOBAL
                    melhorValor = i.valAptidao # ARMAZENA O MELHOR VALOR DE APTIDÃO
                    melhorParticula = i #ARMAZENA A MELHOR PARTICULA
            for i in self.populacao:
                variacao = self.cognitivo*(i.melhorPosicao - (-i.posicao)) + self.social*(melhorParticula.posicao - (-i.posicao)) #VARIAÇÃO DA VELOCIDADE
                i.velocidade = i.velocidade + variacao #ATUALIZA A VELOCIDADE DA PARTICULA
                i.posicao = i.posicao + i.velocidade #ATUALIZA A POSIÇÃO DA PARTICULA
            if True:#CONDIÇÃO DE PARADA
                break 

