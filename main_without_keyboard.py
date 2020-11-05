import time
import speech_recognition as sr
import _thread as th
from controll_functions import functions
from Manipulation.manipulation_text import detection_much_words
from Manipulation.manipulation_audio import reproduction_audio
import sys


class Speech:
    def __init__(self):
        self.language: str = 'pt-br' # Definindo a lingugaem
        self.x: int = 0 # Qual é 
        self.cont: int = 0
        self.r: classmethod = sr.Recognizer()
        self.controll: list = [False] * 500
        self.translate: list = []  # Lista de palavras já reconhecidas
        self.duration_adjust: int = 0.5
        self.detection_audio = True
        self.att_hotword()
        th.start_new_thread(self.verification, (2, 3))

    def att_hotword(self):
        if self.language == 'pt-br':
            self.hotword = 'lua'
        elif self.language == 'en':
            self.hotword = 'moon'

    def verification(self, n_sei, nsei) -> None:
        while True:
            try:
                if self.controll[self.x]:
                    text = self.translate[self.x]
                    text = text.lower()
                    print(f'You say: {text}')
                    self.x = self.x + 1
                    self.hotword_detect(text)
                time.sleep(0.1)
            except IndexError:
                print('a')
                self.controll = []
                self.controll = [False] * 500
                self.x = 0
                self.cont = 0
                self.translate = []

    def translate_audio(self, text, cont) -> None:
        try:
            text = self.r.recognize_google(text, language=self.language)
            self.translate.append(text)
        except:
            self.translate.append('Sorry')

        self.controll[cont] = True

    # Função para detecção de fala
    def detection(self) -> None:
        if self.detection_audio:  # Se estiver realizando alguma função, o reconhecimento de voz é desativado
            with sr.Microphone() as source:
                self.r.adjust_for_ambient_noise(source,
                                                duration=self.duration_adjust)  # Ajustando com o ruído ambiente
                print('Speak: ')
                audio = self.r.listen(source)
            th.start_new_thread(self.translate_audio, (audio, self.cont))
            self.cont = self.cont + 1
        else:  # Caso esteja realizando alguma função
            pass

    # Função de controle de chamada do assistente e de funções a ser realizadas
    def hotword_detect(self, text) -> None:
        if self.hotword in text:  # Verificando se foi chamado o assistente
            self.detection_audio = False
            if not self.config_functions(text):  # Se foi chamado, verifica-se se a função não é de configuração
                result = functions(text, self.language)  # Se a função não for de configuração, é realizado as normais
                if not result:  # Caso nenhuma função tenha sido realizada
                    pass
            self.detection_audio = True

    # Função para configuração do próprio assistente por comando de voz
    def config_functions(self, text) -> bool:
        factor_return: bool = False  # Criando a variável de retorno da função
        if self.language == 'pt-br':
            # Caso quero mudar de língua
            if detection_much_words(['mudar língua', 'língua', 'quero inglês'], text):
                reproduction_audio('mudanca_lingua', self.language)
                self.language = 'en'
                self.att_hotword()
                factor_return = True

            # Caso eu queira que o programa seja encerrado
            if detection_much_words(['descansada', 'dormir', 'encerra programa'], text):
                reproduction_audio('saida', 'pt-br')
                sys.exit()  # Encerrando o programa
        elif self.language == 'en':
            # Caso quero mudar de língua
            if detection_much_words(['change language', 'language like Portuguese'], text):
                reproduction_audio('language_change', self.language)
                self.language = 'pt-br'
                self.att_hotword()
                factor_return = True

            # Caso eu queira que o programa seja encerrado
            if detection_much_words(['quit', 'out', 'quitting'], text):
                reproduction_audio('quit', 'en')
                sys.exit()  # Encerrando o programa
        return factor_return


if __name__ == '__main__':
    # Moon().run()  # Inicializando o meu assistente
    assistence = Speech()
    while True:
        assistence.detection()
