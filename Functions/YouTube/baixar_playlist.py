# Função para baixar playlist do YouTube em arquivos mp3

import _thread as th
from time import sleep
import os, sys, re 

from pytube import Playlist
from baixar_musica import main

# Pegando o path atual e adicionando nos arquivos de importação
path = os.path.dirname(os.path.realpath(__file__))
path = path[:path.index('Moon')+4]

sys.path.append(path)

from Functions.Sistema import mp4_to_mp3
from Manipulation.manipulation_audio import reproduction_audio
from Manipulation.manipulation_text import detection_much_words

def detection_baixar_musica(text: str, language: str) -> None:
    if detection_much_words(['baixar playlist', 'baixa playlist', 'playlist download'], text):
        Download(language)

# Função Principal
def Download(language: str) -> None:
    # Definindo a linguagem e as mensagens a serem enviadas nos prints
    if language == 'pt-br':
        message = ['Qual o link da playlist? ', 'Qual pasta deseja colocar (com o nome título da playlist)?', 'Começando o download',
                   'Download da playlist ', ' realizado com sucesso', 'Convertendo...', 'Finalizado!']
    else:
        message = ['What is the playlist link? ', 'Which folder?', 'Starting download', 'Playlist download ', ' successfully',
                   'Converting...', 'Finished!']

    reproduction_audio('playlist_baixar', language)  # Reproduzindo audio
    url = input(f'{message[0]}(Dê um espaço ao final para não entrar no link): ')  # Obtendo o link
    
    folder = input(message[1])  # Pegando o diretório a ser salvo

    try:
        playlist = Playlist(url)  # Capturando os tipos de downloads
        playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)") # Transformando a url em algo legível para a lib

        # Para cada vídeo, chama a função de baixar música, sem a opção fala
        for url in playlist.video_urls:
          main(url, folder, message, language, fator=False)
          sleep(0.2)
        
        # Removendo o arquivo de pasta temporário
        os.remove(folder+'\\tmp')

    except:
        reproduction_audio('erro', language)  # Aúdio de reprodução caso haja algum erro

# Teste
if __name__ == '__main__':
    Download('pt-br')
    sleep(20)
