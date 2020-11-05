# Controle da pesquisa do google, definindo qual tipo de pesquisa será realizada

import sys, os

# Pegando o path atual e adicionando nos arquivos de importação
path = os.path.dirname(os.path.realpath(__file__))
path = path[:path.index('Moon')+4]

sys.path.append(path)

from Functions.Sites import fast_search, deep_search
from Manipulation.manipulation_text import removing_words, detection_much_words


def detection_search(text: str, language: str) -> None:
    if detection_much_words(['pesquisar', 'pesquise', 'search'], text):
        Main(text, language)

# Função principal
def Main(text: str, language: str) -> None:
    # Removendo as palavras de indício de pesquisa para pegar somente o texto a ser pesquisado 
    text = removing_words(text, ['pesquisar', 'pesquise'])

    # Se na frase tiver palavras significando número de abas e guias, aciona a pesquisa profunda
    if detection_much_words(['aba', 'abas', 'guias', 'guia'], text):
        deep_search.Main(text, language)

    # Se não tiver, aciona a pesquisa simples
    else:
        fast_search.Main(text, language)

# Teste
if __name__ == '__main__':
    Main('pesquisar carros no google', 'pt-br')
