# Função para carregar uma playist previamente colocada, localizada nas pastas de arquivo de texto

import webbrowser as browser
import random, os, sys, time
from unidecode import unidecode

# Pegando o path atual e adicionando nos arquivos de importação
path = os.path.dirname(os.path.realpath(__file__))
path = path[:path.index('Moon')+4]

sys.path.append(path)

from Manipulation.manipulation_text import detection_much_words
from Manipulation.manipulation_audio import reproduction_audio

def detection_playist(text: str, language: str) -> None:
    if detection_much_words(['playlist'], text):  # Tocando uma playist definida ou aleatória
        reproduction_audio('playist_web', language)
        Main(text, language)

# Função para acréscimo de leituras no arquivo .txt das playlists
def acrescimo(line: int, backup: list) -> None:  # Acréscimo no número de vezes que a playist foi tocada
    vezes_tocadas = int(backup[line][1])
    backup[line][1] = vezes_tocadas + 1
    with open(f'{path}\\Texts\\Musics\\playlists.txt', 'w') as source:
        for linha in backup:
            # print(f'{linha[0]};{linha[1]};{linha[2]}')
            source.write(f'{linha[0]};{linha[1]};{linha[2]}' + '\n')

# Função principal
def Main(text: str, language: str) -> None:
    try:
        text = unidecode(text) # Retirando caracteres especiais
        with open(f'{path}\\Texts\\Musics\\playlists.txt', 'r') as source:  # Abrindo o arquivo
            playist = []
            # Para cada linha, adiciona os dados na lista
            for line in source:
                line = line.strip()
                playist_aux = line.split(';')
                playist.append(playist_aux)
            # As linhas foram adicionadas no vetor de playist para a manipulação

        linha = -1  # Definindo variável de seleção da playist
        for x in range(0, len(playist)):
            if playist[x][0] in text:  # Verificando se a playist foi escolhida
                linha = x

        if linha != -1:  # Se for diferente de -', quer dizer que uma playist foi escolhida na frase
            url = playist[linha][2]
            acrescimo(linha, playist)
        else:  # Se uma playist não tiver sido escolhida
            size = 0
            quant_cada_play = []  # Variável para saber quanto cada playist foi tocada
            for line in playist:  # Descobrindo o total de vezes em que a playist foi tocada
                size = int(line[1]) + size
                aux_play = []  # Variável auxiliar
                for x in range(0, int(line[1])):
                    aux_play.append(x + 1)  # Adicionando na variável auxiliar x vezes que a playist foi tocada
                quant_cada_play.append(aux_play)

            random_num = random.randint(1, size - 1)  # Randorizando um número inteiro
            factor = 1  # O objetivo a partir daqui é aleatorizar uma playist de acordo com o número de vezes tocadas
            count = 0  # Ou seja, quanto mais vezes tocadas, maior a chance de cair ela
            for x in range(0, len(quant_cada_play)):
                for _ in range(0, len(quant_cada_play[x])):
                    if factor == random_num:
                        count = x  # Definindo a playist a ser tocada pela randorização
                    factor = factor + 1
            url = playist[count][2]

        browser.open(url)  # Abrindo na web

    except Exception as e:
        print(e)
        reproduction_audio('erro', language) # Reproduz o aúdio de erros

# Teste
if __name__ == '__main__':
    detection_playist('playlist eletronica', 'pt-br')
    time.sleep(5)
    

