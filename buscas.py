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

def subida_encosta(problema):
    """
    Busca local por subida de encosta.
    
    :param problema: objeto da classe ProblemaLocal
    :return: estado final de um pico do problema (global ou local).
    """
    raise NotImplementedError

def feixe_local(problema, k=8):
    """
    Busca por feixe local.
    
    :param problema: objeto da classe ProblemaLocal
    :param k: quantidade de estados a passarem de uma geracão à outra
    :return: estado final de um pico do problema (global ou local).
    """
    raise NotImplementedError

def busca_genetica(populacao, fn_fitness):
    """
    Busca local por algoritmo genético.
    
    :param populacao: lista de strings, cada string são os "genes" de um individuo
    :param fn_fitness: funcao capaz de avaliar a qualidade de um individuo
    :return: um individuo com a funcao_fitness desejada
    """    
    raise NotImplementedError

if __name__ == "__main__":
    print("Este módulo não deve ser utilizado como o principal ou inicial")
    exit()
