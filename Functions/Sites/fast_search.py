# Função que realiza uma pesquisa simples no google

import webbrowser
import os, sys

# Pegando o path atual e adicionando nos arquivos de importação
path = os.path.dirname(os.path.realpath(__file__))
path = path[:path.index('Moon')+4]

sys.path.append(path)

from Manipulation.manipulation_audio import reproduction_audio

# Função principal
def Main(text: str, language: str):
    reproduction_audio('acessar_pesquisa', language)
    url = "https://www.google.com/search?q=" # Inicial da URL
    text_search = f'{url}{text}' # Juntando com o texto a ser pesquisado
    webbrowser.open(text_search) # Abrindo no navegador

# Teste
if __name__ == '__main__':
    Main('carros autônomos', 'pt-br')