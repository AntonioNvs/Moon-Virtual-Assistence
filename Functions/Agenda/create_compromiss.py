import os.path, os, sys, time, pickle
from datetime import datetime, timedelta

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import speech_recognition as sr

# Pegando o path atual e adicionando nos arquivos de importação
path = os.path.dirname(os.path.realpath(__file__))
path = path[:path.index('Moon')+4]

sys.path.append(path)

from Manipulation.manipulation_audio import reproduction_audio
from Manipulation.manipulation_text import detection_much_words

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def detection_create_compromiss(text, language):
    if detection_much_words(['criar compromisso', 'criar evento', 'cria evento', 'cria compromisso'], text):
        event = create_event(language)
        Main(event, language)


def create_event(language):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # Título
        reproduction_audio('titulo_agenda', language)
        audio = r.listen(source)
        titulo = r.recognize_google(audio, language=language)

        # Data
        reproduction_audio('data_agenda', language)
        audio = r.listen(source)
        data = r.recognize_google(audio, language=language)

    title = input('Título do evento: ')
    date_and_hour = input('Data e hora (AAAA-MM-DDTHH:MM:SS): ')
    date_and_hour_end = input('Data e hora (AAAA-MM-DDTHH:MM:SS): ')

    date_and_hour_init = date_and_hour + '-03:00'
    date_and_hour_end = date_and_hour_end + '-03:00'
    print(date_and_hour_end)
    event = {
        'summary': title,
        'start': {
            'dateTime': date_and_hour_init,
        },
        'end': {
            'dateTime': date_and_hour_end,
        }
    }

    return event


def Main(evento, language):
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('calendar', 'v3', credentials=creds)

    e = service.events().insert(calendarId='primary',
                                body=evento,
                                sendNotifications=True).execute()
    print(f'Event created: {e.get("htmlLink")}')


if __name__ == '__main__':
    # detection_create_compromiss('criar compromisso', 'pt-br')
    event = create_event('pt-br')
    Main(event, 'pt-br')