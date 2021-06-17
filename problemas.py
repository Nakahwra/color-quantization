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
    
    @classmethod
    def paleta_inicial(cls, qtd_cores, imagem):
        paleta = [tuple(int(random()*256) for _ in range(3)) for _ in range(qtd_cores)]
        return cls(qtd_cores, paleta, imagem)

    @property
    def heuristica(self):
        cores = self.paleta
        imagem = self.imagem

        valor_h = 0
        for linha in range(imagem.width):
            for coluna in range(imagem.height):
                for cor in cores:
                    cr, cg, cb = cor
                    ir, ig, ib = imagem[linha, coluna]
                    dist_euclid = sqrt((ir-cr)**2 + (ig-cg)**2 + (ib-cb)**2)
                    valor_h += dist_euclid
        return valor_h
    
    @property
    def acoes(self):

        # paleta = [(),(),()] i=0
        # tupla_cor = (1,2,3) i=0
        # cor = 1
        # variacao [0] ~ 255
            # if 0 != 1:
                # nova_tupla_cor = (0,2,3)
                # nova_paleta = [(0,2,3),(),()]

        for i, tupla_cor in enumerate(self.paleta):
            for j, cor in enumerate(tupla_cor):
                for variacao in range(255):
                    nova_paleta = self.paleta
                    nova_tupla_cor = tupla_cor

                    if variacao != cor:
                        nova_tupla_cor[j] = variacao
                        nova_paleta[i] = nova_tupla_cor
                        yield ProblemaQuantificacao(self.qtd_cores, nova_paleta, self.imagem)

if __name__ == "__main__":
    print("Este módulo não deve ser utilizado como o principal ou inicial")
    exit()
