import matplotlib.pyplot
import math
from sympy import *
import copy
# Calculando o valor de x em base na função polinomial com os coeficientes dados
def funcao_polinomial(coeficientes, x):
    result = 0
    n = len(coeficientes) - 1  # Descobrindo o expoente máximo da função
    for coef in coeficientes:
        result += coef * (
                x ** n)  # Pelo fato da função polinomial seguir uma lógica, o algoritmo de resolução é simples
        n -= 1

    return result


# Transformando o valor em radiano para grau
def rad_para_grau(value) -> float:
    return value * 180 / math.pi


# Transformando os coeficientes na função legível
def funcao_escrita(coefs) -> str:
    function = ''
    polaridade = ''
    n = len(coefs) - 1
    print(n)
    for coef in coefs[:-1]:
        if not (coef == coefs[0]) and not coef == coefs[len(coefs) - 1]:
            if coef >= 0:
                polaridade = '+'
            elif coef < 0:
                polaridade = ''

        coef = round(coef, 2)
        function = function + polaridade + str(coef) + 'x^' + str(n)

        n -= 1

    coef = coefs[-1]
    if coef is 0:
        return function

    if coef > 0:
        polaridade = '+'
    else:
        polaridade = ''

    return function + f'{polaridade}' + str(coef)


def definindo_tempo(x_init, x_finally, aumento_de_x, distancia_total) -> list:
    x_final = copy.deepcopy(x_finally)
    x_finally = x_init
    x_init = x_init - aumento_de_x
    dists = []
    while x_final >= x_init:
        init_printing(pretty_print=true)
        x = Symbol('x')
        result = Integral(sqrt((-2*x)**2 + 1), (x, x_init, x_finally)).doit().evalf()
        dists.append(result)
        x_init += aumento_de_x
        x_finally += aumento_de_x

    return dists


def Simulacao(velocidade, raio_roda, distancia, distancia_min, x_final, x_inicial, coeficientes, dist_entre_rodas):
    velocidade_linear = velocidade * raio_roda / 2
    aumento_de_x = (x_final - x_inicial) / (distancia / distancia_min)
    quant_x = (x_final - x_inicial) / aumento_de_x
    distancia_por_x = definindo_tempo(x_inicial, x_final, aumento_de_x, distancia)
    razao = distancia / sum(distancia_por_x)
    velocidades_B = []
    velocidades_C = []

    index = 0
    xs = []
    coef_anterior = math.atan(funcao_polinomial(coeficientes, (x_inicial - aumento_de_x)))
    while x_final >= x_inicial:
        coef_atual = math.atan(funcao_polinomial(coeficientes, x_inicial))
        variacao = coef_atual - coef_anterior
        tempo = distancia_por_x[index] * razao / velocidade_linear

        velocidade_robo = variacao / tempo
        dif_velocidade = velocidade_robo * dist_entre_rodas / raio_roda

        velocidades_B.append(velocidade_fixa + abs(dif_velocidade / 2))
        velocidades_C.append(velocidade_fixa - abs(dif_velocidade / 2))

        xs.append(x_inicial)
        coef_anterior = coef_atual
        x_inicial += aumento_de_x
        index += 1

    matplotlib.pyplot.plot(xs, velocidades_B, 'c')
    matplotlib.pyplot.plot(xs, velocidades_C, 'r')
    matplotlib.pyplot.title(
        f'Velocidades das duas rodas para andar determinada função derivativa: {funcao_escrita(coeficientes)}')
    matplotlib.pyplot.xlabel('Xs da função')
    matplotlib.pyplot.ylabel('Velocidade angular rad/s')

    matplotlib.pyplot.show()


if __name__ == '__main__':
    # Definições de variáveis
    velocidade_fixa = 8
    coeficientes = [-2, 0]
    x_inicial = -2
    x_final = 2
    distancia = 60
    distancia_minina = 5
    raio_roda = 5.6
    distancia_entre_rodas = 13
    Simulacao(velocidade_fixa, raio_roda, distancia, distancia_minina, x_final, x_inicial, coeficientes,
              distancia_entre_rodas)
