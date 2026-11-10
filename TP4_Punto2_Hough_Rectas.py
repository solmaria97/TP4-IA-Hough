import math
import random

ANCHO, ALTO = 80, 60
UMBRAL_VOTOS = 25


def crear_imagen(con_ruido=False):
    imagen = [[0] * ANCHO for _ in range(ALTO)]

    # Borde vertical: x = 20.
    for y in range(8, 53):
        imagen[y][20] = 1

    # Borde horizontal: y = 40.
    for x in range(10, 71):
        imagen[40][x] = 1

    if con_ruido:
        # Elimina partes de ambos bordes.
        for y in range(22, 29):
            imagen[y][20] = 0

        for x in range(43, 51):
            imagen[40][x] = 0

        # Agrega ruido reproducible.
        generador = random.Random(7)

        for _ in range(30):
            x = generador.randrange(ANCHO)
            y = generador.randrange(ALTO)
            imagen[y][x] = 1

    return imagen


def detectar_rectas(imagen):
    alto, ancho = len(imagen), len(imagen[0])

    d = math.ceil(math.hypot(ancho - 1, alto - 1))

    # Filas: valores de rho entre -d y d.
    # Columnas: angulos entre 0 y 179 grados.
    acumulador = [[0] * 180 for _ in range(2 * d + 1)]

    cosenos = [
        math.cos(math.radians(t)) for t in range(180)
    ]
    senos = [
        math.sin(math.radians(t)) for t in range(180)
    ]

    # Votacion de los pixeles de borde.
    for y in range(alto):
        for x in range(ancho):
            if imagen[y][x] == 1:
                for theta in range(180):
                    rho = round(
                        x * cosenos[theta] + y * senos[theta]
                    )
                    acumulador[rho + d][theta] += 1

    rectas = []

    # En este ejemplo se buscan hasta dos rectas.
    for _ in range(2):
        votos = 0
        mejor_rho = 0
        mejor_theta = 0

        for fila in range(len(acumulador)):
            for theta in range(180):
                if acumulador[fila][theta] > votos:
                    votos = acumulador[fila][theta]
                    mejor_rho = fila - d
                    mejor_theta = theta

        if votos < UMBRAL_VOTOS:
            break

        rectas.append((mejor_rho, mejor_theta, votos))

        # Suprime maximos cercanos para evitar duplicados.
        for dt in range(-5, 6):
            theta = mejor_theta + dt
            rho_central = mejor_rho

            # Al cruzar el limite angular cambia el signo de rho.
            if theta < 0 or theta >= 180:
                theta %= 180
                rho_central = -mejor_rho

            for dr in range(-4, 5):
                fila = rho_central + dr + d

                if 0 <= fila < len(acumulador):
                    acumulador[fila][theta] = 0

    return rectas


def mostrar_resultados(nombre, imagen):
    print("\n" + nombre)

    rectas = detectar_rectas(imagen)

    if not rectas:
        print("No se detectaron rectas con suficientes votos.")

    for numero, (rho, theta, votos) in enumerate(rectas, 1):
        print(
            "Recta {}: rho = {} px, theta = {} grados, votos = {}"
            .format(numero, rho, theta, votos)
        )


mostrar_resultados(
    "CASO 1: bordes completos",
    crear_imagen()
)

mostrar_resultados(
    "CASO 2: bordes interrumpidos y ruido",
    crear_imagen(True)
)

mostrar_resultados(
    "CASO 3: imagen vacia",
    [[0] * ANCHO for _ in range(ALTO)]
)