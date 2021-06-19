#!/usr/bin/env python3

"""Quantificador de cores de imagens utilizando algoritmos de busca local"""

__author__ = "Lucas Nakahara e Gabriel Rodrigues"
__copyright__ = "Copyleft"
__credits__ = ["Ricardo Inácio Álvares e Silva"]
__license__ = "GPLv3"
__version__ = "1.0"
__maintainer__ = "Lucas Nakahara e Gabriel Rodrigues"
__status__ = "Desenvolvimento"

import sys, buscas
from problemas import ProblemaQuantificacao
from PIL import Image

def quantificar_subida_encosta(**kwargs):
    """
    Funcao que inicializa estruturas de dados e invoca algoritmo de busca local
    por subida de encosta.
    """
    cores = kwargs.get('cores')
    imagem = kwargs.get('reduzida')
    buscas.subida_encosta(ProblemaQuantificacao.paleta_inicial(cores, imagem))

def quantificar_feixe_local(**kwargs):
    """
    Funcao que inicializa estruturas de dados e invoca algoritmo de busca em
    feixe local.
    """
    cores = kwargs.get('cores')
    imagem = kwargs.get('reduzida')
    k = kwargs.get('argumento')
    problema = [ProblemaQuantificacao.paleta_inicial(cores, imagem) for _ in range(k)]
    buscas.feixe_local(problema=problema, k=k)
    
def quantificar_geneticamente(**kwargs):
    """
    Funcao que inicializa estruturas de dados e invoca algoritmo de busca local
    por por algoritmo genético.
    """
    cores = kwargs.get('cores')
    imagem = kwargs.get('reduzida')
    k = kwargs.get('argumento')
    populacao = [ProblemaQuantificacao.paleta_inicial(cores, imagem) for _ in range(k)]
    buscas.busca_genetica(populacao=populacao)

def quantificar_kmedias(**kwargs):
    """
    Funcao que inicializa estruturas de dados e invoca algoritmo de busca k-médias
    """
    cores = kwargs.get('cores')
    img = kwargs.get('reduzida')
    tamanho = (img.width, img.height)
    buscas.kmedias(ProblemaQuantificacao(cores, None, img.load(), tamanho))

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
        print(f"Inicializando algoritmo: subida de encosta.")
        algoritmo = quantificar_subida_encosta
    elif algoritmo == "feixe":
        print(f"Inicializando algoritmo: feixe local.")
        algoritmo = quantificar_feixe_local
    elif algoritmo == "genetico":
        print(f"Inicializando algoritmo: genético.")
        algoritmo = quantificar_geneticamente
    elif algoritmo == "kmedias":
        print(f"Inicializando algoritmo: k-médias.")
        algoritmo = quantificar_kmedias
    else:
        print("Algoritmo especificado inválido: {0}".format(algoritmo))
        print("Algoritmos válidos são: {0}, {1}, {2}, {3}"
              .format("subida", "feixe", "genetico", "kmedias"))
        exit()
    
    if cores < 1:
        print("Quantidade de cores pós-quantizacão deve ser no mínimo 1.")
        exit()
    
    # Abrir a imagem especificada
    try:
        original = Image.open(nome_arquivo)
    except IOError as err:
        print("Erro ao acessar arquivo: {0}".format(err))

    # Copiar imagem para poder comparar ambas ao final.    
    reduzida = original.copy()

    algoritmo(argumento=argumento, cores=cores, reduzida=reduzida)
    
    original.show()
    reduzida.show()
    reduzida.save(nome_arquivo.split(".")[0] + "-quantified.png")
    exit()
else:
    raise ImportError("Este módulo só pode funcionar como o principal.")
