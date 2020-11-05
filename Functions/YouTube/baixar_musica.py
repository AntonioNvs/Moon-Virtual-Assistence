# Função para baixar músicas a partir do YouTube em arquivos mp3

import _thread as th
from time import sleep
import os, sys, re

from pytube import YouTube
from unidecode import unidecode 
from moviepy.editor import *

# Pegando o path atual e adicionando nos arquivos de importação
path = os.path.dirname(os.path.realpath(__file__))
path = path[:path.index('Moon')+4]

sys.path.append(path)

from Functions.Sistema import mp4_to_mp3
from Manipulation.manipulation_audio import reproduction_audio
from Manipulation.manipulation_text import detection_much_words, removing_caracters_specials

def detection_baixar_musica(text: str, language: str) -> None:
    if detection_much_words(['baixar música', 'baixa música', 'song download'], text):
        Download(language)

# Função principal
def Download(language: str) -> None:
    # Definindo a linguagem e as mensagens a serem enviadas nos prints
    if language == 'pt-br':
        message = ['Qual o link da música? ', 'Qual pasta deseja colocar?', 'Começando o download',
                   'Download da música ', ' realizado com sucesso', 'Convertendo...', 'Finalizado!']
    else:
        message = ['What is the song link? ', 'Which folder?', 'Starting download', 'Song download ', ' successfully',
                   'Converting...', 'Finished!']

    reproduction_audio('musica_baixar', language)  # Reproduzindo audio
    url = input(f'{message[0]}(Dê um espaço ao final para não entrar no link): ')  # Obtendo o link

    folder = input(message[1])  # Pegando o diretório a ser salvo
    
    main(url, folder, message, language)

def main(url: str, folder: str, message: list, language: str, speak = True) -> None:
    # A variável 'speak' serve para informar se é para acionar os áudios ou não
    try:
        yt = YouTube(url)  # Capturando os tipos de downloads

        title = yt.title # Pegando o título do vídeo
        title = removing_caracters_specials(title).replace(' ', '-')

        stream = yt.streams.first()  # Pegando todos os tipos de downloads
        time = yt.length # Descobrindo o tamanho do vídeo em segundos
        
        if(speak): reproduction_audio('baixar_musica', language)
        print(message[2])
        stream.download(folder+'/tmp', filename=title)  # Realizando o download
        print(f'{message[3]}{title}{message[4]}')  # Escrevendo o download finalizado

        def _thread():
            # Começando a conversão de MP4 para MP3
            print(message[5])
            video_to_audio(folder, time, title)  # Convertendo...
            print(message[6])
            if(speak): reproduction_audio('musica_terminada', language)  # Reprodução de aúdio de sucessp

        # Começando a thread de conversão de mp4 para mp3
        th.start_new_thread(_thread, ())
    except:
        reproduction_audio('erro', language)  # Aúdio de reprodução caso haja algum erro

# Função para transformar o vídeo baixado em áudio
def video_to_audio(folder: str, time: int, title: str) -> None:
    # Capturando todo o caminho do arquivo de vídeo
    full_path = os.path.join(folder+'\\tmp', title+'.mp4')
    
    # Caminho para o arquivo de áudio
    output_path = os.path.join(folder, os.path.splitext(title+'.mp4')[0] + '.mp3')

    # Convertendo o vídeo em áudio
    clip = VideoFileClip(full_path)

    # Salvando no arquivo
    clip.audio.write_audiofile(output_path)

    # Na conversão, é acrescentado 5 segundos no final do arquivo, tal parte serve para retirar-lo
    # com o auxílio do software ffmpeg
    try:
        # Cortando o arquivo e copiando a outro
        os.system(f'ffmpeg -ss {0} -t {time-5} -i {folder}/{title}.mp3 {folder}/{title[:len(title)-1]}.mp3')

        # Removendo o arquivo antigo
        os.remove(folder+'\\'+title+'.mp3')

    # Exceção caso o corte dê errado, imprimindo o erro
    except Exception as e:
        print(e)

# Teste
if __name__ == '__main__':
    Download('pt-br')
    sleep(20)
