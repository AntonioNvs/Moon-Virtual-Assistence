from gtts import gTTS as gt
from playsound import playsound as ps
import _thread as th
import os, sys


# Pegando o path atual e adicionando nos arquivos de importação
path = os.path.dirname(os.path.realpath(__file__))
path = path[:path.index('Moon')+4]

sys.path.append(path)

def cria_audio(audio, save, language):
    tts = gt(audio, lang=language)
    gt.save(tts, f'{path}\\audios_{language}\\{save}.mp3')

# {os.path.dirname(os.path.realpath(__file__))}/
def reproduction_audio(save, language):
    def theard():
        ps(f'{path}\\audios_{language}\\{save}.mp3')

    th.start_new_thread(theard, ())


if __name__ == '__main__':
    cria_audio('Título, hora, e se e hoje ou amanha', 'agenda', 'pt-br')
