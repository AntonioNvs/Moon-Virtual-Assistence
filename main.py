import _thread as th
import sys
from Manipulation.manipulation_audio import reproduction_audio
from Manipulation.manipulation_text import detection_much_words
import speech_recognition as sr
from controll_functions import controll_function
import keyboard
from time import sleep


class Speech:
    def __init__(self):
        self.r: classmethod = sr.Recognizer()
        self.language: str = 'pt-br' # Definindo a linguagem
        self.detection_audio: bool = True # Se é para ficar reajustando o aúdio de acordo com o ambiente
        self.duration_adjust: int = 0.5 # Tempo de duração desse reajustamento
        self.translate: list = []  # Lista de palavras já reconhecidas
        self.keys = 'Home' # Tecla de acionamento do reconhecimento de voz
        self.ajust_audio() # Ativando a thread de ajuste de aúdio
        self.detection_keyboard() # Ativando a thread de detectar a tecla apertada
    
    # Função de ajuste de aúdio
    def ajust_audio(self):
        def thread(_, __):
            while True:
                if self.detection_audio:
                    with sr.Microphone() as source:
                        self.r.adjust_for_ambient_noise(source, duration=self.duration_adjust)
                sleep(30)

        th.start_new_thread(thread, (0, 0))

    def detection_keyboard(self):
        while True:
            keyboard.wait(self.keys)
            with sr.Microphone() as source:
                print('Fale: ')
                audio = self.r.listen(source)
                try:
                    text = self.r.recognize_google(audio, language=self.language)
                    self.translate.append(text)
                except:
                    self.translate.append('Sorry, speak again')
            text_atual = self.translate[-1]
            print(f'Você disse: {text_atual}')
            text_atual = text_atual.lower()  # Transformando todas as letras em minúsculas
            self.functions(text_atual)

    def functions(self, text):
        if not self.config_functions(text):  # Se foi chamado, verifica-se se a função não é de configuração
            result = controll_function(text,
                                       self.language)  # Se a função não for de configuração, é realizado as normais
            if not result:
                pass

    def config_functions(self, text) -> bool:
        factor_return: bool = False  # Criando a variável de retorno da função
        if self.language == 'pt-br':
            # Caso quero mudar de língua
            if detection_much_words(['mudar língua', 'língua', 'quero inglês'], text):
                reproduction_audio('mudanca_lingua', self.language)
                self.language = 'en'
                factor_return = True

            # Caso eu queira que o programa seja encerrado
            elif detection_much_words(['descansada', 'dormir', 'encerra programa'], text):
                reproduction_audio('saida', 'pt-br')
                sys.exit()  # Encerrando o programa

            # Caso eu queira escrever manualmente o comando
            elif detection_much_words(['para texto', 'input', 'entrada de texto'], text):
                reproduction_audio('input', self.language)
                entrada = input('Escreva o comando: ')  # Pegando o comando na entrada do cmd
                entrada = entrada.lower().strip()  # Manipulando a string, deixando minúscula e sem espaços finais
                self.functions(entrada)  # Mandando o texto para realização do comando descrito
                factor_return = True

        elif self.language == 'en':
            # Caso quero mudar de língua
            if detection_much_words(['change language', 'language like portuguese'], text):
                reproduction_audio('language_change', self.language)
                self.language = 'pt-br'
                factor_return = True

            # Caso eu queira que o programa seja encerrado
            elif detection_much_words(['quit', 'out', 'quitting'], text):
                reproduction_audio('quit', 'en')
                sys.exit()  # Encerrando o programa

            # Caso eu queira escrever manualmente o comando
            elif detection_much_words(['for text', 'text input'], text):
                reproduction_audio('input', self.language)
                entrada = input('Escreva o comando: ')  # Pegando o comando na entrada do cmd
                entrada = entrada.lower().strip()  # Manipulando a string, deixando minúscula e sem espaços finais
                self.functions(entrada)  # Mandando o texto para realização do comando descrito
                factor_return = True

        return factor_return


if __name__ == '__main__':
    Speech()
