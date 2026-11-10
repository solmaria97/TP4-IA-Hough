import math
import random

ANCHO, ALTO = 80, 60
RADIO = 15
UMBRAL_VOTOS = 45


def crear_imagen(con_ruido=False):
    imagen = [[0] * ANCHO for _ in range(ALTO)]
    inicio = 70 if con_ruido else 0

    # Centro conocido solo para construir la imagen de prueba.
    for grados in range(inicio, 360):
        angulo = math.radians(grados)
        x = round(42 + RADIO * math.cos(angulo))
        y = round(28 + RADIO * math.sin(angulo))
        imagen[y][x] = 1

    if con_ruido:
        generador = random.Random(9)
        for _ in range(30):
            x = generador.randrange(ANCHO)
            y = generador.randrange(ALTO)
            imagen[y][x] = 1
    return imagen


def detectar_circunferencia(imagen, radio):
    alto, ancho = len(imagen), len(imagen[0])
    acumulador = [[0] * ancho for _ in range(alto)]

    # Evita votos repetidos por el redondeo de distintos angulos.
    desplazamientos = set()
    for grados in range(360):
        angulo = math.radians(grados)
        dx = round(radio * math.cos(angulo))
        dy = round(radio * math.sin(angulo))
        desplazamientos.add((dx, dy))

    for y in range(alto):
        for x in range(ancho):
            if imagen[y][x] == 1:
                for dx, dy in desplazamientos:
                    a = x - dx
                    b = y - dy
                    if 0 <= a < ancho and 0 <= b < alto:
                        acumulador[b][a] += 1

    votos, centro_x, centro_y = 0, 0, 0
    for b in range(alto):
        for a in range(ancho):
            if acumulador[b][a] > votos:
                votos = acumulador[b][a]
                centro_x, centro_y = a, b

    if votos < UMBRAL_VOTOS:
        return None
    return centro_x, centro_y, radio, votos


def mostrar_resultados(nombre, imagen):
    print('\n' + nombre)
    resultado = detectar_circunferencia(imagen, RADIO)
    if resultado is None:
        print('No se detecto una circunferencia con suficientes votos.')
    else:
        a, b, radio, votos = resultado
        print('Centro: ({}, {}) px'.format(a, b))
        print('Radio: {} px; votos: {}'.format(radio, votos))


def main():
    mostrar_resultados('CASO 1: circunferencia completa', crear_imagen())
    mostrar_resultados('CASO 2: arco incompleto y ruido', crear_imagen(True))
    vacia = [[0] * ANCHO for _ in range(ALTO)]
    mostrar_resultados('CASO 3: imagen vacia', vacia)


if __name__ == '__main__':
    main()
