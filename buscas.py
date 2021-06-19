#!/usr/bin/env python3

"""Módulo que abriga os algoritmos de quantificacao de imagens"""

__author__ = "Nome do aluno"
__copyright__ = "Copyleft"
__credits__ = ["Ricardo Inácio Álvares e Silva"]
__license__ = "GPLv3"
__version__ = "0.1"
__maintainer__ = "Aluno"
__email__ = "seu@email.com"
__status__ = "Desenvolvimento"

from math import sqrt
from random import random, choices, randint
from problemas import ProblemaQuantificacao


def subida_encosta(problema):
    """
    Busca local por subida de encosta.
    
    :param problema: objeto da classe ProblemaLocal
    :return: estado final de um pico do problema (global ou local).
    """
    melhor_atual = problema
    adjacentes = list()
    contador = 0
    while True:
        adjacentes = melhor_atual.acoes

        melhor_adjacente = min(adjacentes, key=lambda problema: problema.heuristica)

        print(melhor_atual.heuristica)
        print(melhor_adjacente.heuristica)
        if melhor_adjacente.heuristica < melhor_atual.heuristica:
            contador += 1
            melhor_atual = melhor_adjacente
        else:
            quantificar_cores(melhor_atual)
            break
            # return melhor_atual

def feixe_local(problema, k=8):
    """
    Busca por feixe local.
    
    :param problema: objeto da classe ProblemaLocal
    :param k: quantidade de estados a passarem de uma geracão à outra
    :return: estado final de um pico do problema (global ou local).
    """
    k_atuais = problema
    while True:
        k_adjacentes = list()
        for k_atual in k_atuais:
            k_adjacentes += list(k_atual.acoes)
        k_adjacentes.sort(key=lambda estado: estado.heuristica)
        
        if k_adjacentes[0].heuristica < k_atuais[0].heuristica:
            print(k_adjacentes[0].heuristica)
            k_atuais = k_adjacentes[:k]
        else:
            quantificar_cores(k_atuais[0])
            break

def busca_genetica(populacao):
    """
    Busca local por algoritmo genético.
    
    :param populacao: lista de strings, cada string são os "genes" de um individuo
    :return: um individuo com a funcao_fitness desejada
    """    
    alfa = .1
    geracoes = 50
    geracao_atual = populacao
    for count_geracao in range(geracoes):
        # fitness
        fitness_populacao = sum(individuo.heuristica for individuo in geracao_atual)
        fitnesses_weights = [individuo.heuristica/fitness_populacao for individuo in geracao_atual]
        print(f'{count_geracao},\n'
            f'{fitness_populacao} total fitness,\n'
            f'{min(individuo.heuristica for individuo in geracao_atual)} menor fitness,\n'
            f'{min(geracao_atual, key=lambda individuo: individuo.heuristica)}')

        if min(individuo.heuristica for individuo in geracao_atual) == 0:
            break

        # selecao
        selecionados = choices(geracao_atual, fitnesses_weights, k=len(geracao_atual))

        # crossover
        geracao_atual = []
        for n in range(0, len(selecionados), 2):
            pai1, pai2 = selecionados[n].paleta, selecionados[n+1].paleta
            assert len(pai1) == len(pai2)

            crosscut = randint(1, len(pai1) - 1)
            geracao_atual.append(ProblemaQuantificacao(selecionados[n].qtd_cores, pai1[:crosscut] + pai2[crosscut:], selecionados[n].imagem, selecionados[n].tamanho))
            geracao_atual.append(ProblemaQuantificacao(selecionados[n].qtd_cores, pai2[:crosscut] + pai1[crosscut:], selecionados[n].imagem, selecionados[n].tamanho))

        # mutacao
        for individuo in geracao_atual:
            individuo.paleta = [gene if random() > alfa else tuple([int(random()*256) for _ in range(3)])
                                    for gene in individuo.paleta]
    
    # print(geracao_atual)
    quantificar_cores(min(geracao_atual, key=lambda individuo: individuo.heuristica))

def kmedias():
    pass

def quantificar_cores(melhor_atual):
    for linha in range(melhor_atual.tamanho[0]):
        for coluna in range(melhor_atual.tamanho[1]):
            de = list()
            for cor in melhor_atual.paleta:
                cr, cg, cb = cor
                ir, ig, ib = melhor_atual.imagem[linha, coluna]
                dist_euclid = sqrt((ir-cr)**2 + (ig-cg)**2 + (ib-cb)**2)
                de.append((cor, dist_euclid))
            
            melhor_cor = min(de, key=lambda tuplas: tuplas[1])
            print(melhor_cor)
            melhor_atual.imagem[linha,coluna] = melhor_cor[0]

if __name__ == "__main__":
    print("Este módulo não deve ser utilizado como o principal ou inicial")
    exit()
