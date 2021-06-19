#!/usr/bin/env python3

"""Módulo com implementacao da modelagem do problema abordado"""

__author__ = "Lucas Nakahara e Gabriel Rodrigues"
__copyright__ = "Copyleft"
__credits__ = ["Ricardo Inácio Álvares e Silva"]
__license__ = "GPLv3"
__version__ = "0.1"
__maintainer__ = "Lucas Nakahara e Gabriel Rodrigues"
__status__ = "Desenvolvimento"

from math import sqrt
from random import random
from PIL.Image import Image
from copy import deepcopy
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class ProblemaLocal():
    """Classe abstrata com interfaces para implementacao de busca local"""
    @property
    def heuristica(self):
        raise NotImplementedError()
    
    @property
    def acoes(self):
        raise NotImplementedError()

@dataclass
class ProblemaQuantificacao(ProblemaLocal):
    """Aqui você implementará a modelagem da busca local em quantizacao de
    imagens"""
    qtd_cores: int
    paleta: List[Tuple]
    imagem: List[Tuple]
    tamanho: Tuple
    
    @classmethod
    def paleta_inicial(cls, qtd_cores, img):
        paleta = [tuple(int(random()*256) for _ in range(3)) for _ in range(qtd_cores)]
        imagem = img.load()
        tamanho = (img.width, img.height)
        return cls(qtd_cores, paleta, imagem, tamanho)

    @property
    def heuristica(self):
        valor_h = 0
        for linha in range(self.largura):
            for coluna in range(self.altura):
                for cor in self.paleta:
                    cr, cg, cb = cor
                    ir, ig, ib = self.imagem[linha, coluna]
                    # distancia = sqrt((ir-cr)**2 + (ig-cg)**2 + (ib-cb)**2) # Euclidiana
                    distancia = abs(ir-cr) + abs(ig-cg) + abs(ib-cb) # Manhattan
                    valor_h += distancia
        return valor_h
    
    @property
    def acoes(self):
        adjacentes = list()
        for i, tupla_cor in enumerate(self.paleta):
            for j, cor in enumerate(tupla_cor):
                for variacao in range(2):
                    nova_paleta = deepcopy(self.paleta)
                    nova_tupla_cor = list(deepcopy(tupla_cor))
                    nova_cor = deepcopy(cor)

                    nova_cor = (nova_cor + (variacao + 1)) if nova_cor < 255 else (nova_cor + (variacao + 1)) - 255
                    nova_tupla_cor[j] = nova_cor
                    nova_paleta[i] = tuple(nova_tupla_cor)
                    adjacentes.append(ProblemaQuantificacao(self.qtd_cores, nova_paleta, self.imagem, self.tamanho))
        return adjacentes
    
    @property
    def largura(self):
        return self.tamanho[0]
    
    @property
    def altura(self):
        return self.tamanho[1]

    def quantificar_cores(self):
        print("Quantificando imagem...")

        for linha in range(self.tamanho[0]):
            for coluna in range(self.tamanho[1]):
                de = list()
                for cor in self.paleta:
                    cr, cg, cb = cor
                    ir, ig, ib = self.imagem[linha, coluna]
                    # distancia = sqrt((ir-cr)**2 + (ig-cg)**2 + (ib-cb)**2) # Euclidiana
                    distancia = abs(ir-cr) + abs(ig-cg) + abs(ib-cb) # Manhattan
                    de.append((cor, distancia))
                
                melhor_cor = min(de, key=lambda tuplas: tuplas[1])
                self.imagem[linha,coluna] = melhor_cor[0]

        print("Imagem quantificada!")

if __name__ == "__main__":
    print("Este módulo não deve ser utilizado como o principal ou inicial")
    exit()
