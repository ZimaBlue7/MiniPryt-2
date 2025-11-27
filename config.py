"""
Configuración del juego Smart Horses
"""
import random

# Valores fijos de las casillas con puntos 
VALORES_CASILLAS = [-10, -5, -4, -3, -1, 1, 3, 4, 5, 10]

def generar_tablero_aleatorio():
    """
    Genera un tablero aleatorio con:
    - 10 casillas con puntos 
    - 2 posiciones iniciales para los caballos
    - Ninguna posición puede coincidir
    """
    # Crear tablero vacío
    tablero = [[0 for _ in range(8)] for _ in range(8)]

    # Generar todas las posiciones posibles
    todas_posiciones = [(i, j) for i in range(8) for j in range(8)]

    # Seleccionar 12 posiciones aleatorias sin repetir (10 casillas + 2 caballos)
    posiciones_seleccionadas = random.sample(todas_posiciones, 12)

    # Asignar las primeras 10 posiciones a las casillas con puntos
    for i, pos in enumerate(posiciones_seleccionadas[:10]):
        fila, col = pos
        tablero[fila][col] = VALORES_CASILLAS[i]

    # Las últimas 2 posiciones son para los caballos
    pos_blanco = posiciones_seleccionadas[10]
    pos_negro = posiciones_seleccionadas[11]

    return tablero, pos_blanco, pos_negro


TABLERO_INICIAL = None
POS_INICIAL_BLANCO = None
POS_INICIAL_NEGRO = None

# Movimientos del caballo - L de ajedrez
MOVIMIENTOS_CABALLO = [
    (-2, -1),
    (-2, 1),
    (-1, -2),
    (-1, 2),
    (1, -2),
    (1, 2),
    (2, -1),
    (2, 1),
]

# Configuración de niveles
NIVELES = {"Principiante": 2, "Amateur": 4, "Experto": 6}

# Configuración visual
TAMANO_CELDA = 70
TAMANO_TABLERO = 8
ANCHO_VENTANA = TAMANO_CELDA * TAMANO_TABLERO + 300
ALTO_VENTANA = TAMANO_CELDA * TAMANO_TABLERO + 100

# Colores
COLOR_CELDA_CLARA = "#F0D9B5"
COLOR_CELDA_OSCURA = "#B58863"
COLOR_MOVIMIENTO_VALIDO = "#90EE90"
COLOR_SELECCIONADO = "#FFD700"
COLOR_BLOQUEADO = "#8B0000"  
COLOR_FONDO = "#2C3E50"
COLOR_TEXTO = "#ECF0F1"
COLOR_PANEL = "#34495E"
