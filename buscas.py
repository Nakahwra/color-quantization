#!/usr/bin/env python3

"""Módulo que abriga os algoritmos de quantificacao de imagens"""

__author__ = "Lucas Nakahara e Gabriel Rodrigues"
__copyright__ = "Copyleft"
__credits__ = ["Ricardo Inácio Álvares e Silva"]
__license__ = "GPLv3"
__version__ = "0.1"
__maintainer__ = "Lucas Nakahara e Gabriel Rodrigues"
__status__ = "Desenvolvimento"

from copy import deepcopy
from dataclasses import dataclass
from math import dist, sqrt
from random import random, choices, randint
from typing import List, Tuple, Set
from problemas import ProblemaQuantificacao

def subida_encosta(problema):
    """
    Busca local por subida de encosta.

    :param problema: objeto da classe ProblemaLocal
    """
    melhor_atual = problema
    adjacentes = list()
    contador = 0

    print("Calculando adjacentes...")
    while True:
        adjacentes = melhor_atual.acoes
        melhor_adjacente = min(adjacentes, key=lambda problema: problema.heuristica)

        if melhor_adjacente.heuristica < melhor_atual.heuristica:
            contador += 1
            melhor_atual = melhor_adjacente
        else:
            melhor_atual.quantificar_cores()
            break

def feixe_local(problema, k=8):
    """
    Busca por feixe local.
    
    :param problema: objeto da classe ProblemaLocal
    :param k: quantidade de estados a passarem de uma geracão à outra
    """
    k_atuais = problema

    print("Calculando adjacentes...")
    while True:
        k_adjacentes = list()

        for k_atual in k_atuais:
            k_adjacentes += list(k_atual.acoes)

        k_adjacentes.sort(key=lambda estado: estado.heuristica)
        
        if k_adjacentes[0].heuristica < k_atuais[0].heuristica:
            k_atuais = k_adjacentes[:k]
        else:
            k_atuais[0].quantificar_cores()
            break

def busca_genetica(populacao):
    """
    Busca local por algoritmo genético.
    
    :param populacao: lista de strings, cada string são os "genes" de um individuo
    """    
    alfa = .1
    geracoes = 4
    geracao_atual = populacao

    print("Processando operações genéticas...")
    for count_geracao in range(geracoes):
        # fitness
        fitness_populacao = sum(individuo.heuristica for individuo in geracao_atual)
        fitnesses_weights = [individuo.heuristica/fitness_populacao for individuo in geracao_atual]

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
    
    melhor_atual = min(geracao_atual, key=lambda individuo: individuo.heuristica)
    melhor_atual.quantificar_cores()

def kmedias(problema):
    """
    Busca por algotimo k-médias.
    
    :param problema: objeto da classe ProblemaLocal
    """  
    cluster_list = gerar_clusters(problema.qtd_cores, problema.tamanho, problema.imagem)

    print("Processando clusters...")
    while True:
        alteracao = False
        for linha in range(problema.largura):
            for coluna in range(problema.altura):
                min_distancia = 0
                cluster_selecionado = None
                cor = problema.imagem[linha, coluna]

                for i, cluster in enumerate(cluster_list):
                    cr, cg, cb = cluster.centro
                    ir, ig, ib = cor
                    # distancia = sqrt((ir-cr)**2 + (ig-cg)**2 + (ib-cb)**2) # Euclidiana
                    distancia = abs(ir-cr) + abs(ig-cg) + abs(ib-cb) # Manhattan

                    if distancia < min_distancia or min_distancia == 0:
                        min_distancia = distancia
                        cluster_selecionado = i

                for i, cluster in enumerate(cluster_list):
                    if cor in cluster.elementos and i != cluster_selecionado:
                        cluster.elementos.discard(cor)

                if cor not in cluster_list[cluster_selecionado].elementos:
                    cluster_list[cluster_selecionado].elementos.add(cor)
                    alteracao = True
        
        if alteracao == False:
            break
        
        for i, cluster in enumerate(cluster_list):
            srgb = [0,0,0]

            for elemento in cluster.elementos:
                srgb = [srgb[i] + elemento[i] for i in range(3)]

            qtd_elementos = len(cluster.elementos) if len(cluster.elementos) > 0 else 1
            srgb = [srgb[i]//qtd_elementos for i in range(3)]
            cluster_list[i].centro = tuple(srgb)
    
    paleta = [cluster.centro for cluster in cluster_list]
    problema.paleta = paleta
    problema.quantificar_cores()

def gerar_clusters(qtd_clusters, tamanho, imagem):
    print("Gerando clusters...")
    largura, altura = tamanho
    clusters = list()

    for _ in range(qtd_clusters):
        i = int(random() * largura)
        j = int(random() * altura)
        clusters.append(Cluster(imagem[i,j], set()))
    return clusters
    
@dataclass
class Cluster():
    centro: Tuple
    elementos: Set[Tuple]

if __name__ == "__main__":
    print("Este módulo não deve ser utilizado como o principal ou inicial")
    exit()
