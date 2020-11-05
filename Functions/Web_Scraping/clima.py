# Capturando as informações do clima atual a partir de Web Scraping da página de clima do Google

import time
import os, sys

from bs4 import BeautifulSoup
from requests import get
from googletrans import Translator
from playsound import playsound as ps

# Pegando o path atual e adicionando nos arquivos de importação
path = os.path.dirname(os.path.realpath(__file__))
path = path[:path.index('Moon')+4]

sys.path.append(path)

from Manipulation.manipulation_audio import cria_audio
from Manipulation.manipulation_audio import reproduction_audio
from Manipulation.manipulation_text import detection_much_words


def detection_clima(text: str, language: str) -> None:
    if detection_much_words(['tempo', 'clima', 'temperatura', 'weather', 'climate', 'temperature'], text):
        reproduction_audio('capturando_web', language)
        clima(language)

# Função principal
def clima(language: str) -> None:
    try:
        # URL da página de pesquisa do clima do Google
        url = "https://www.google.com/search?sxsrf=ALeKk03XRgXBBQ0xMOdRKjfYMz17naVuJQ%3A1586300662125&ei=9gaNXumgB5Ke5OUPlcCEwAQ&q=temperatura+agora+governador+valadares&oq=temperatura+atual+de+gover&gs_lcp=CgZwc3ktYWIQAxgAMgYIABAWEB4yBQgAEM0CMgUIABDNAjIFCAAQzQIyBQgAEM0COgQIABBHOgcIIxDqAhAnOgQIIxAnOgQIABBDOgUIABCDAToCCAA6BAgAEAo6BwgAEEYQgAJKNQgXEjEwZzQ4NWczMDdnMjUwZzI1M2cyNDdnMzM0ZzI1MmcyNjRnNDM2ZzMzNGcyNDJnMjM0Sh0IGBIZMGcxZzFnMWcxZzFnMWcxZzFnMWc1ZzVnOVDbljVYsbc1YKjANWgCcAR4AYAB7QOIAco-kgEIMi0xNC4zLjiYAQCgAQGqAQdnd3Mtd2l6sAEK&sclient=psy-ab"

        site = get(url) # Realizando a requisição

        # Transformando a resposta em um HTML legível com BeautifulSoup
        soup = BeautifulSoup(site.text, 'html.parser')

        # Procurando o elemento de descrição do tempo a partir de outros que tem a mesma das suas classes
        descricao = soup.findAll(attrs={'class': 'BNeawe tAd8D AP7Wnd'})
        descricao = descricao[len(descricao) - 1].text # Texto do último elemento (dia atual)
        
        # Retirando a data e o horário, sobrando somente a descrição do tempo
        descricao = descricao.split('\n')[1]
        
        # Procurando os elementos informativos de temperatura
        temperatura = soup.findAll(attrs={'class': 'BNeawe iBp4i AP7Wnd'})
        temperatura = temperatura[1].text # Texto do segundo elemento

        # Criação do áudio informativo dependendo da linguagem
        if language == 'pt-br':
            cria_audio(f'A temperatura atual é de {temperatura} e está {descricao}', 'clima', language)
        else:
            # Se for em inglês, como as informações são em português, é utilizado a lib do Google Translator
            # para traduzir em inglês

            translate = Translator()
            descricao = translate.translate(descricao).text
            cria_audio(f'The current temperature is {temperatura} and is {descricao}', 'clima', language)

        ps(f'{path}/audios_{language}/clima.mp3') # Reproduzindo o áudio criado
        os.remove(f'{path}/audios_{language}/clima.mp3') # Excluindo o áudio

    except:
        reproduction_audio('erro', language) # Reproduz áudio de erro


if __name__ == '__main__':
    detection_clima('clima', 'pt-br')
    time.sleep(5)
