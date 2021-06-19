#!/usr/bin/env python3

"""Módulo com implementacao da modelagem do problema abordado"""

__author__ = "Lucas Nakahara e Gabriel Rodrigues"
__copyright__ = "Copyleft"
__credits__ = ["Ricardo Inácio Álvares e Silva"]
__license__ = "GPLv3"
__version__ = "0.1"
__maintainer__ = "Lucas Nakahara e Gabriel Rodrigues"
__email__ = "seu@email.com"
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
    
    @property
    def resultado(self):
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
        # print(random())
        cores = self.paleta
        largura, altura = self.tamanho

        hist = {}
        for i in range(largura):
            for j in range(altura):
                hist[self.imagem[i,j]] = hist.get(self.imagem[i,j], 0) + 1

        valor_h = 0
        for linha in range(largura):
            for coluna in range(altura):
                for cor in cores:
                    cr, cg, cb = cor
                    ir, ig, ib = self.imagem[linha, coluna]
                    # dist_euclid = sqrt((ir-cr)**2 + (ig-cg)**2 + (ib-cb)**2)
                    dist_euclid = abs(ir-cr) + abs(ig-cg) + abs(ib-cb)
                    valor_h += dist_euclid
        return valor_h

        # valor_h = 0
        # for cor in cores:
        #     for pixel in hist:
        #         dist_euclid = abs(pixel[0]-cor[0]) + abs(pixel[1]-cor[1]) + abs(pixel[2]-cor[2])
        #         valor_h += dist_euclid       
        # return valor_h
    
    @property
    def acoes(self):
        adjacentes = list()
        for i, tupla_cor in enumerate(self.paleta):
            for j, cor in enumerate(tupla_cor):
                for variacao in range(2):
                    print(f"tupla:{i} - cor:{j} - variacao:{variacao+1}")
                    nova_paleta = deepcopy(self.paleta)
                    nova_tupla_cor = list(deepcopy(tupla_cor))
                    nova_cor = deepcopy(cor)

                    nova_cor = (nova_cor + (variacao + 1)) if nova_cor < 255 else (nova_cor + (variacao + 1)) - 255
                    # print(f"cor: {cor} - nova_cor: {nova_cor}")

                    nova_tupla_cor[j] = nova_cor
                    # print(f"tupla_cor: {tupla_cor} - nova_tupla_cor: {nova_tupla_cor}")

                    nova_paleta[i] = tuple(nova_tupla_cor)
                    # print(f"paleta: {self.paleta} - nova_paleta: {nova_paleta}")

                    # adjacente = self.adjacente(nova_paleta)
                    adjacentes.append(ProblemaQuantificacao(self.qtd_cores, nova_paleta, self.imagem, self.tamanho))
        
        return adjacentes

if __name__ == "__main__":
    print("Este módulo não deve ser utilizado como o principal ou inicial")
    exit()
