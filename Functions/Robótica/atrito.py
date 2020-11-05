import matplotlib.pyplot
import math


def graphics(text):
    raio_roda = 2.8
    dist_entre_rodas = 13

    raio_roda = raio_roda ** 2
    text = text.split(' ')
    distancia = None
    velocidade_B = None
    velocidade_C = None
    massa = None

    for word in text:
        if word == 'distância':
            index = text.index(word)
            distancia = int(text[index + 1])
        if word == 'B':
            index = text.index(word)
            velocidade_B = int(text[index + 1])
        if word == 'C':
            index = text.index(word)
            velocidade_C = int(text[index + 1])
        if word == 'massa':
            index = text.index(word)
            massa = int(text[index + 1])

    if velocidade_B is None or velocidade_C is None or distancia is None or massa is None:
        raise Exception('Está faltando dados')

    angulo = []
    forca_atrito = []
    velocidades = (velocidade_B + velocidade_C) ** 2

    for degree in range(90):
        angulo.append(degree)
        atrito = (raio_roda * degree * math.pi * velocidades) / (720 * distancia)
        forca_atrito.append(atrito * massa)

    print(forca_atrito)
    matplotlib.pyplot.plot(angulo, forca_atrito)
    matplotlib.pyplot.title('Força de atrito em um movimento curvilíneo')
    matplotlib.pyplot.xlabel('Angulo da curva')
    matplotlib.pyplot.ylabel('Força de atrito')

    matplotlib.pyplot.show()


if __name__ == '__main__':
    graphics('distância 50 massa 1 velocidade B 16 velocidade C 16')
