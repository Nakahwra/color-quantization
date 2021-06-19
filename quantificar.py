#!/usr/bin/env python3

"""Quantificador de cores de imagens utilizando algoritmos de busca local"""

import sys, buscas
from problemas import ProblemaQuantificacao
from PIL import Image

__author__ = "Nome do aluno"
__copyright__ = "Copyleft"
__credits__ = ["Ricardo Inácio Álvares e Silva"]
__license__ = "GPLv3"
__version__ = "1.0"
__maintainer__ = "Ricardo Inácio Álvares e Silva"
__email__ = "ricardo.silva@unifil.br"
__status__ = "Desenvolvimento"


def quantificar_subida_encosta(**kwargs):
    """
    Funcao que inicializa estruturas de dados e invoca algoritmo de busca local
    por subida de encosta.
    """
    ### Após iniciar estruturas de dados, remova o comentario da linha abaixo
    buscas.subida_encosta(ProblemaQuantificacao.paleta_inicial(qtd_cores=kwargs.get('cores'), img=kwargs.get('pixels')))

def quantificar_feixe_local(**kwargs):
    """
    Funcao que inicializa estruturas de dados e invoca algoritmo de busca em
    feixe local.
    """
    ### Após iniciar estruturas de dados, remova o comentario da linha abaixo
    
    k = kwargs.get('argumento')
    problema = [ProblemaQuantificacao.paleta_inicial(qtd_cores=kwargs.get('cores'), img=kwargs.get('pixels')) for _ in range(k)]
    buscas.feixe_local(problema=problema, k=k)
    
def quantificar_geneticamente(**kwargs):
    """
    Funcao que inicializa estruturas de dados e invoca algoritmo de busca local
    por por algoritmo genético.
    """
    ### Após iniciar estruturas de dados, remova o comentario da linha abaixo
    #buscas.busca_genetica(populacao, fitness)
    k = kwargs.get('argumento')
    populacao = [ProblemaQuantificacao.paleta_inicial(qtd_cores=kwargs.get('cores'), img=kwargs.get('pixels')) for _ in range(k)]
    buscas.busca_genetica(populacao=populacao)

if __name__ == "__main__":
    # Leitura e verificacao dos argumentos de linha de comando
    if len(sys.argv) < 5:
        print("Modo de usar: python3 quantificar.py algoritmo argumento cores imagem\n"
            + "algoritmo: nome do algoritmo a ser utilizado\n"
            + "argumento: valor de 'k' para feixe local ou tamanho da populacao\n"
            + "cores: quantidade de cores (número)\n"
            + "imagem: caminho e nome do arquivo com a imagem a ser processada.") 
        exit()
    
    algoritmo = sys.argv[1]
    argumento = int(sys.argv[2])
    cores = int(sys.argv[3])
    nome_arquivo = sys.argv[4]


    # Define algoritmo a ser aplicado
    if algoritmo == "subida":
        algoritmo = quantificar_subida_encosta
    elif algoritmo == "feixe":
        algoritmo = quantificar_feixe_local
    elif algoritmo == "genetico":
        algoritmo = quantificar_geneticamente
    else:
        print("Algoritmo especificado inválido: {0}".format(algoritmo))
        print("Algoritmos válidos são: {0}, {1}, {2}"
              .format("subida", "feixe", "genetico"))
        exit()
        
    
    if cores < 1:
        print("Quantidade de cores pós-quantizacão deve ser no mínimo 1.")
        exit()
    
    # Abrir a imagem especificada
    try:
        original = Image.open(nome_arquivo)
    except IOError as err:
        print("Erro ao acessar arquivo: {0}".format(err))
    
    # print(original.width)
    # print(original.height)

    # Copiar imagem para poder comparar ambas ao final.    
    reduzida = original.copy()
    
    # Obtendo acesso aos pixels da cópia. Cada posicao é uma tupla (R, G, B)
    # R, G e B tem domínio em [0,255], ou seja, 0 <= x <= 255
    # pixels = reduzida.load()


    algoritmo(argumento=argumento, cores=cores, pixels=reduzida)
    
    original.show()
    reduzida.show()
    reduzida.save(nome_arquivo.split(".")[0] + ".png")
    
    exit()

else:
    raise ImportError("Este módulo só pode funcionar como o principal.")
