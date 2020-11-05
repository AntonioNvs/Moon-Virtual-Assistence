# Função com a funcionalidade de acessar determinados sites

import time, os, sys
import webbrowser

# Pegando o path atual e adicionando nos arquivos de importação
path = os.path.dirname(os.path.realpath(__file__))
path = path[:path.index('Moon')+4]

sys.path.append(path)

from Manipulation.manipulation_audio import reproduction_audio
from Manipulation.manipulation_text import detection_much_words

def detection_acessar(text: str, language: str) -> None:
    if detection_much_words(['acesse', 'acessar', 'access'], text):
        Main(text, language)

# Função principal
def Main(text: str, language: str) -> None:
    """
        Listagem de sites possíveis com suas respectivas URL'S, se algum site pedido não
        estiver na lista, reproduz o aúdio de erro
    """
    sites = {
        'google drive': "https://drive.google.com/drive/u/0/my-drive",
        'youtube': "https://www.youtube.com/",
        'gmail': "https://mail.google.com/mail/u/0/#inbox",
        'plural': 'https://maestro.plurall.net/?state=14795553868286406#/home',
        'notas': 'http://prados101.fiemg.com.br/Corpore.Net/Login.aspx?autoload=false&ReturnUrl=%2fCorpore.Net%2fMain'
                 '.aspx%3fSelectedMenuIDKey%3d%26ShowMode%3d2',
        'sesi': 'https://sesieducacao.com.br/publico/index.php',
        'what': 'https://web.whatsapp.com/',
        'alura': 'https://cursos.alura.com.br/dashboard',
        'descomplica': 'https://descomplica.com.br/cursos/medicina-extensivo-completo-2020-A/inicio/',
        'tradutor': 'https://www.google.com/search?q=translate&oq=tra&aqs=chrome.0.69i59l2j69i57j69i59j0j69i61l3'
                    '.991j0j7&sourceid=chrome&ie=UTF-8 '
    }

    try:
        url = '' # Definindo variável de url

        # Verificando se existe o site pedido na lista de URL'S
        for web in sites:
            if web in text:
                url = sites[web] # Se existe, define a url como a do respectivo site
        # Se a URL não tiver vazia, abre no navegador
        if url != '':
            webbrowser.open(url)
            reproduction_audio('acessar_site', language)
        
        # Se tiver vazia, reproduz o aúdio de "erro"
        else:
            reproduction_audio('desculpa_site', language)
    except:
        reproduction_audio('erro', language) # Reproduz aúdio de erro

# Teste
if __name__ == "__main__":
    Main('acessar google drive', 'pt-br')
    time.sleep(3)
