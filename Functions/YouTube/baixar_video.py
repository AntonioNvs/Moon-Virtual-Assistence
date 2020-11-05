# Função para baixar vídeo do YouTube em arquivos mp3

import time
import _thread as th
import sys, os

from pytube import YouTube

# Pegando o path atual e adicionando nos arquivos de importação
path = os.path.dirname(os.path.realpath(__file__))
path = path[:path.index('Moon')+4]

sys.path.append(path)

from Manipulation.manipulation_text import detection_much_words
from Manipulation.manipulation_audio import reproduction_audio

def detection_video(text: str, language: str) -> None:
    if detection_much_words(['baixar vídeo', 'video download'], text):
        Download(language)

# Função principal
def Download(language: str) -> None:
    # Definindo a linguagem e as mensagens a serem enviadas nos prints
    if language == 'pt-br':
        message = ['Qual o link do vídeo?  ', 'Qual pasta?','Começando o download', 'Download do vídeo ', ' realizado com sucesso']
    else:
        message = ['What is the video link?  ', 'What folder?', 'Starting download', 'Video download ', ' successfully']

    reproduction_audio('video_baixar', language)  # Reproduzindo audio
    url = input(message[0])  # Obtendo o link
    position = url.replace(' ', '')  # Tirando o espaço final
    folder = input(message[1])
    try:
        yt = YouTube(position)  # Capturando os tipos de downloads
        title = yt.title  # Pegando o título do vídeo
        tipos_downloads = yt.streams.filter(progressive=True) # Pegando todos os tipos de downloads
        stream = None  # Definindo o meu tipo de download
        # Escolhendo a melhor qualidade e o melhor FPS
        qualidade = 0
        fps = 0
        for link in tipos_downloads:
            # Verifcando se existe resolução e fps
            if link.resolution is not None and link.fps is not None and link.mime_type == 'video/mp4':
                # Verificando se a qualidade ou o fps eh melhor que o anterior
                if int(link.resolution.replace('p', '')) >= qualidade and int(link.fps) >= fps:
                    stream = link  # Atribuindo o novo tipo de download
                    qualidade = int(link.resolution.replace('p', ''))  # Mudando a resolução
                    fps = int(link.fps)  # Mudando o fps
                    
        # Thread para baixar a música enquanto as ações são executadas normalmente
        def thread():
            print(message[2])
            stream.download(folder)  # Realizando o download
            print(f'{message[3]}{title}{message[3]}')  # Escrevendo o download finalizado

        th.start_new_thread(thread, ())  # Inicializando a thread de download
        reproduction_audio('baixar_video', language)
    except:
        reproduction_audio('erro', language)  # Aúdio de reprodução caso haja algum erro


if __name__ == '__main__':
    Download('pt-br')
    time.sleep(90)
