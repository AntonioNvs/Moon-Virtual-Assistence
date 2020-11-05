import unicodedata, re

def detection_much_words(list_words, text):
    fator_detection: bool = False  # Criando variável de retorno, e caso nada seja achado, retorna falso
    for word in list_words:
        word = word.lower()  # Tornando a frase com todas as letras minúsculuas
        if word in text:  # Se a palavra existir no texto falado, retorna verdadeiro
            fator_detection = True

    return fator_detection


def array_to_str(array) -> str:
    string = ''
    for word in array:
        if string != '':
            string = f'{string} {word}'
        else:
            string = word
    return string


def removing_words(text, list_remove_word) -> str:
    for word_remove in list_remove_word:
        if word_remove in text:
            text = text.replace(word_remove, '')
    text = text.strip(' ')
    return text


if __name__ == '__main__':
    print(removing_words('mano em 109 no ceu', ['109 no']))


# Removendo caracteres especiais
def removing_caracters_specials(palavra):

    # Unicode normalize transforma um caracter em seu equivalente em latin.
    nfkd = unicodedata.normalize('NFKD', palavra)
    palavraSemAcento = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    # Usa expressão regular para retornar a palavra apenas com números, letras e espaço
    return re.sub('[^a-zA-Z0-9 \\\]', '', palavraSemAcento)
