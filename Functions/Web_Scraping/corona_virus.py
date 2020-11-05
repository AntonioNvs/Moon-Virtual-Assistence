# Capturando as informações globais do coronavirus a partir de Web Scraping da página do World Meters

import os, sys

from requests import get
from bs4 import BeautifulSoup
from playsound import playsound as ps

# Pegando o path atual e adicionando nos arquivos de importação
path = os.path.dirname(os.path.realpath(__file__))
path = path[:path.index('Moon')+4]

sys.path.append(path)

from Manipulation.manipulation_text import detection_much_words
from Manipulation.manipulation_audio import cria_audio, reproduction_audio


def detection_corona_virus(text: str, language: str) -> None:
    if detection_much_words(['coronavirus', 'corona'], text):  # Casos de coronavírus
        reproduction_audio('capturando_web', language)
        corona_virus(language)

# Função principal
def corona_virus(language: str) -> None:
    try:
        # URL do World Meters com os dados do Corona Virus
        url = "https://www.worldometers.info/coronavirus/"

        site = get(url) # Realizando a requisição

        # Transformando a resposta em um HTML legível com BeautifulSoup
        soup = BeautifulSoup(site.text, 'html.parser')

        # Lista com as informações
        array = soup.findAll(attrs={'class': 'maincounter-number'})
        
        array_formated = []
        
        # Como as informações são em inglês, transforma-se as vírgulas em pontos e acrescentado em um novo array
        for text in array:
            array_formated.append(text.span.text.replace(',', '.')) # Trocando a vírgula por um ponto

        # Criação da variável de áudio informativo dependendo da linguagem
        if language == 'pt-br':
            audio = f'Casos {array_formated[0]}, Mortes {array_formated[1]}, Recuperados {array_formated[2]}'
        elif language == 'en':
            audio = f'Cases {array_formated[0]}, Death {array_formated[1]}, Recovered {array_formated[2]}'

        cria_audio(audio, 'cases', language) # Criação do áudio
        ps(f'{path}/audios_{language}/cases.mp3') # Reprodução

        os.remove(f'{path}/audios_{language}/cases.mp3') # Exclusão do áudio para evitar sopreposição

    except:
        reproduction_audio('erro', language) # Reproduz áudio de erro

# Teste
if __name__ == '__main__':
    detection_corona_virus('corona', 'pt-br')
