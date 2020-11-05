# Função para pesquisar uma música no YouTube e abrir o navegador com tal escolha

from requests import get
import lxml.html
import os, sys
import webbrowser

# Pegando o path atual e adicionando nos arquivos de importação
path = os.path.dirname(os.path.realpath(__file__))
path = path[:path.index('Moon')+4]

sys.path.append(path)

from Manipulation.manipulation_text import detection_much_words, removing_words
from Manipulation.manipulation_audio import reproduction_audio

def detection_acessar_musica(text: str, language: str) -> None:
    if detection_much_words(['song', 'música', 'músicas'], text):
        reproduction_audio('musica', language)
        Main(text, language)

# Função principal
def Main(text: str, language: str) -> None:
    try:
        # Removendo possíveis palavras que não são parte do nome da música
        text = removing_words(text, ['song', 'música', 'acessar', 'na', 'músicas'])

        # Definindo a URL de pesquisa
        url = f'https://youtube.com/search?q={text}'
        
        source = get(url).text # Requisição GET a partir da URL montada

        # Salvando o resultado em .txt para poder ler as variáveis JavaScript geradas
        open("video.txt", "w", encoding='utf-8').write(source)

        # Lendo o arquivo resultante, identificando a primeira referência para um vídeo
        with open("video.txt", "r", encoding="utf-8") as src:
            text = src.read() # Lendo o arquivo

            """
                Procurando a primeira referência para um vídeo, localizada em um objeto JavaScript
                que contém todas as informações dos vídeos a serem listados. Tal referência, tem como propriedade
                "url" e a URL sempre começa com "/watch?v"
            """
            init = text.index('"url":"/watch?v') # Primeiro index
            fin = text[init+7:].index('"') + init+7 # Último index, eliminando a parte da propriedade ("url": ")
            url_video = f'www.youtube.com{text[init+7:fin]}' # Definindo a url do vídeo

        # Abrindo o vídeo no navegador padrão
        webbrowser.open(url_video)
    except:
        reproduction_audio('erro', language) # Reproduz áudio de erro


# Teste
if __name__ == '__main__':
    Main('doeu', 'pt-br')
