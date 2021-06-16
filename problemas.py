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
from typing import List

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
        
@dataclass
class Paleta():
    cores: List
    qtd_cores: int

class ProblemaQuantificacao(ProblemaLocal):
    """Aqui você implementará a modelagem da busca local em quantizacao de
    imagens"""
    def __init__(self, qtd_cores):
        self.qtd_cores = qtd_cores
    
    def paleta_inicial(self):
        cores = [tuple(int(random()*256) for _ in range(3)) for _ in range(self.qtd_cores)]
        return Paleta(cores, self.qtd_cores)

    @staticmethod
    def heuristica(self, paleta: Paleta, image: Image):
        cores = paleta.cores
        img = image.load()

        valor_h = 0
        for linha in range(img.width):
            for coluna in range(img.height):
                for cor in cores:
                    cr, cg, cb = cor
                    ir, ig, ib = img[linha, coluna]
                    dist_euclid = sqrt((ir-cr)**2 + (ig-cg)**2 + (ib-cb)**2)
                    valor_h += dist_euclid
        return valor_h





if __name__ == "__main__":
    print("Este módulo não deve ser utilizado como o principal ou inicial")
    exit()
