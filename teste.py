import xlrd
from MLPBSA import MLPBSA
def lerExcel():
    amostras = []
    xls = xlrd.open_workbook("Tabela_Seção5.8_RNA.xls")
    plan = xls.sheets()[0]
    for i in range(1, plan.nrows):
        linha = plan.row_values(i)
        entradas = linha[0:3]
        saidas = linha[3:4]
        amostras.append([entradas,saidas])
    return amostras
neuronios = [10, 1] #NEURONIOS EM CADA CAMADA
amostras = lerExcel()
teste = MLPBSA(neuronios, amostras)
res = teste.execucao(8, 175,4, 0.8, 0.7, 0.3, 1, 0.5, 1, 4, -1)
print(res.avaliacao, res.melhorposicao)