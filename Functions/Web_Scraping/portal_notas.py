# Capturando no portal de notas da minha escola

import time, os, sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Pegando o path atual e adicionando nos arquivos de importação
path = os.path.dirname(os.path.realpath(__file__))
path = path[:path.index('Moon')+4]

sys.path.append(path)

from Manipulation.manipulation_audio import reproduction_audio
from Manipulation.manipulation_text import detection_much_words

def detection_portal_notas(text: str, language: str) -> None:
    if detection_much_words(['resultado escola', 'notas', 'nota', 'notes', 'notes in portal', 'note'], text):
        reproduction_audio('notas', language)
        Portal_de_Notas(language)
        reproduction_audio('notas_capturadas', language)

# Função principal
def Portal_de_Notas(language: str) -> None:
    try:
        # Definindo configurações de login
        login = {
            'user': 'xxxxxxxx',
            'password': 'xxxxxxx'
        }

        # URL inicial
        url = "https://prados101.fiemg.com.br/Corpore.Net/Login.aspx"

        # URL para identificar qual contexto educacional o aluno está, ou seja, a série
        url_contexto_educacional = "http://prados101.fiemg.com.br/Corpore.Net/Source/Edu-Educacional/RM.EDU.CONTEXTO/EduSelecionarContextoModalWebForm.aspx?Qs=ActionID%3dEduNotaAvaliacaoActionWeb%26SelectedMenuIDKey%3dmnNotasAval"

        # URL com as notas de cada etapa do aluno naquela série
        url_notas_etapa = "http://prados101.fiemg.com.br/Corpore.Net/Main.aspx?ActionID=EduNotaEtapaActionWeb&SelectedMenuIDKey=mnNotasEtapa"

        # Inicialização do driver de execução
        driver = webdriver.Chrome(executable_path=f"{path}\\Functions\\Web_Scraping\\chromedriver.exe")

        driver.get(url) # Primeira requisição ao site de login

        driver.find_element(By.NAME, 'txtUser').send_keys(login['user']) # Preenchendo a informação do usuário
        driver.find_element(By.NAME, 'txtPass').send_keys(login['password']) # Preenchendo a informação da senha
        driver.find_element(By.NAME, 'btnLogin').click() # Submetendo

        # Após a submissão, escolha da atividade na página inicial, se aparecer a opção, se não, continua       
        try:
            driver.find_element(By.ID, 'ctl17_EDU_EduNotaEtapaActionWeb_LinkControl').click()
        except: pass

        driver.get(url_contexto_educacional) # Requisição para página de contexto educacionals

        time.sleep(0.5)  # Esperando um tempo para a página carregar
        tr = driver.find_elements_by_id('rdContexto')  # Escolhendo o ano escolar

        tr[0].click()  # Seleção do ano, no meu caso, está 2019

        driver.get(url_notas_etapa) # Requisição para página das notas das etapas

        element = driver.find_element(By.ID, 'ctl24_xgvNotasFilial_DXMainTable')  # Tabela de elementos

        # Transformando o elemento em HTML
        element_html = element.get_attribute("outerHTML")

        # Parsear conteúdo HTML
        soup = BeautifulSoup(element_html, 'html.parser')

        # Para cada matéria, procura das notas de cada etapa
        for materia in soup.findAll(attrs={'class': 'dxgvDataRow_Edu'}):
            params = [] # Lista com os parâmetros de nota
            for td in materia.findAll(attrs={'class': 'dxgv'}):
                params.append(td.text) # Para cada parâmetro de nota, acrescenta-se o respectivo texto na variável
            
            # Impressão dos dados da matéria, sendo o sexto a Primeira Etapa, nono a Segunda, e décimo segundo a Terceira 
            print(
                f'Matéria: {params[3]} ; Primeira Etapa: {params[5]} ; Segunda Etapa: {params[8]} ; Terceira Etapa: {params[11]}' + '\n')
        
        # Abandonando o navegador
        driver.quit()

    except:
        reproduction_audio('erro', language) # Reproduz aúdio de erro

# Teste
if __name__ == '__main__':
    detection_portal_notas('portal notas', 'pt-br')
    time.sleep(20)

