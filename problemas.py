#!/usr/bin/env python3

"""Módulo com implementacao da modelagem do problema abordado"""

__author__ = "Nome do aluno"
__copyright__ = "Copyleft"
__credits__ = ["Ricardo Inácio Álvares e Silva"]
__license__ = "GPLv3"
__version__ = "0.1"
__maintainer__ = "Aluno"
__email__ = "seu@email.com"
__status__ = "Desenvolvimento"


class ProblemaLocal():
    """Classe abstrata com interfaces para implementacao de busca local"""
    
    def __init__(self, s):
        self.estado_inicial = s
    
    def heuristica(self, s):
        raise NotImplementedError()
    
    def acoes(self, s):
        raise NotImplementedError()
    
    def resultado(self, s, a):
        raise NotImplementedError()


class ProblemaQuantificacao(ProblemaLocal):
    """Aqui você implementará a modelagem da busca local em quantizacao de
    imagens"""
    pass


if __name__ == "__main__":
    print("Este módulo não deve ser utilizado como o principal ou inicial")
    exit()
