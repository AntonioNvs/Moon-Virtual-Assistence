# Função para pesquisa profunda no google, com o auxílio da lib googlesearch

import webbrowser as browser
import re, sys, os

from googlesearch import search

# Pegando o path atual e adicionando nos arquivos de importação
path = os.path.dirname(os.path.realpath(__file__))
path = path[:path.index('Moon')+4]

sys.path.append(path)

from Manipulation.manipulation_audio import reproduction_audio
from Manipulation.manipulation_text import removing_words, detection_much_words

# Função principal
def Main(text: str, language: str) -> None:
    reproduction_audio('acessar_pesquisa', language)

    padrao = "[0-9]{1,2}"  # Descobrindo o número de guias por expressões regulares
    retorno = re.findall(padrao, text)  # Achando todos os números, sendo que o último será o número de abas
    num_guias = int(retorno[len(retorno)-1])  # Defifindo o número de guias

    list_words = ['abas', 'aba', 'guias', 'guia']  # Lista de palavras com o significado de abas
    list_artigos = ['no', 'em', 'na']  # Artigos
    for word in list_words:
        if word in text:
            source_index = text.index(word)  # Saber qual indice da string está a palavra abas, para separa em duas

    text = text[:source_index]  # Separando o text em duas
    source = text[source_index:]  # Parte da fonte do text
    text = text.replace(str(num_guias), '').strip()  # Remodulando a variável text
    source = removing_words(source, list_words)
    source = removing_words(source, list_artigos)  # Descobrindo a fonte pedida

    if detection_much_words(list_artigos, text[len(text)-3:]):  # Caso a ultima palavra seja um artigo, ela é retirada
        text = removing_words(text, list_artigos)

    if source == '':       # Caso não tenha informado a fonte, será o google
        source = 'google'

    for url in search(f'"{text}"{source}', stop=num_guias):  # Descobrindo os sites pela lib
        browser.open(url)  # Acessando as url's

# Teste
if __name__ == '__main__':
    Main('carros elétricos em 5 abas no google', 'pt-br')