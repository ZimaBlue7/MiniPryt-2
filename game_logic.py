"""
Lógica del juego Smart Horses
"""

from config import MOVIMIENTOS_CABALLO


class GameLogic:
    """Clase que maneja toda la lógica del juego"""

    def __init__(self, tablero_inicial, pos_blanco, pos_negro):
        self.tablero = [fila[:] for fila in tablero_inicial]
        self.pos_blanco = pos_blanco
        self.pos_negro = pos_negro
        self.puntos_blanco = 0
        self.puntos_negro = 0
        self.turno_blanco = True  # El juego siempre inicia con el blanco
        self.juego_terminado = False
        self.casillas_bloqueadas = (
            set()
        )  # Conjunto de casillas que ya no se pueden usar
        self.blanco_sin_movimientos = False  # Si el blanco no puede moverse
        self.negro_sin_movimientos = False  # Si el negro no puede moverse
        # NO bloquear posiciones iniciales - solo se bloquean al moverse
        # (según las reglas, las casillas se bloquean cuando el caballo se mueve)

    def obtener_movimientos_validos(self, pos):
        """Retorna lista de movimientos válidos desde una posición"""
        movimientos = []
        fila, col = pos

        for df, dc in MOVIMIENTOS_CABALLO:
            nueva_fila = fila + df
            nueva_col = col + dc

            # Verificar que esté en el tablero, que la casilla no esté bloqueada
            # y que no esté ocupada por el otro caballo
            if (
                0 <= nueva_fila < 8
                and 0 <= nueva_col < 8
                and (nueva_fila, nueva_col) not in self.casillas_bloqueadas
                and (nueva_fila, nueva_col) != self.pos_blanco
                and (nueva_fila, nueva_col) != self.pos_negro
            ):
                movimientos.append((nueva_fila, nueva_col))

        return movimientos

    def mover_caballo(self, nueva_pos):
        """Mueve el caballo actual a la nueva posición"""
        if self.juego_terminado:
            return False

        if self.turno_blanco:
            # Turno de la IA (blanco)
            movimientos_validos = self.obtener_movimientos_validos(self.pos_blanco)
            if nueva_pos not in movimientos_validos:
                return False

            # Si el negro (jugador) no puede moverse, restar 4 puntos por cada movimiento del blanco
            if self.negro_sin_movimientos:
                self.puntos_negro -= 4

            # Bloquear la casilla anterior
            self.casillas_bloqueadas.add(self.pos_blanco)

            self.pos_blanco = nueva_pos
            puntos_ganados = self.tablero[nueva_pos[0]][nueva_pos[1]]
            self.tablero[nueva_pos[0]][nueva_pos[1]] = 0
            self.puntos_blanco += puntos_ganados

            # Bloquear la nueva casilla
            self.casillas_bloqueadas.add(nueva_pos)
        else:
            # Turno del jugador humano (negro)
            movimientos_validos = self.obtener_movimientos_validos(self.pos_negro)
            if nueva_pos not in movimientos_validos:
                return False

            # Si el blanco (IA) no puede moverse, restar 4 puntos por cada movimiento del negro
            if self.blanco_sin_movimientos:
                self.puntos_blanco -= 4

            # Bloquear la casilla anterior
            self.casillas_bloqueadas.add(self.pos_negro)

            self.pos_negro = nueva_pos
            puntos_ganados = self.tablero[nueva_pos[0]][nueva_pos[1]]
            self.tablero[nueva_pos[0]][nueva_pos[1]] = 0
            self.puntos_negro += puntos_ganados

            # Bloquear la nueva casilla
            self.casillas_bloqueadas.add(nueva_pos)

        # Cambiar turno
        self.turno_blanco = not self.turno_blanco

        # Verificar estado de movimientos
        self.verificar_sin_movimientos()

        return True

    def verificar_sin_movimientos(self):
        """Verifica si algún jugador no tiene movimientos disponibles"""
        movimientos_blanco = self.obtener_movimientos_validos(self.pos_blanco)
        movimientos_negro = self.obtener_movimientos_validos(self.pos_negro)

        self.blanco_sin_movimientos = len(movimientos_blanco) == 0
        self.negro_sin_movimientos = len(movimientos_negro) == 0

        # El juego termina solo cuando ambos no pueden moverse
        if self.blanco_sin_movimientos and self.negro_sin_movimientos:
            self.juego_terminado = True

    def verificar_fin_juego(self):
        """Verifica si el juego ha terminado"""
        mov_blanco = self.obtener_movimientos_validos(self.pos_blanco)
        mov_negro = self.obtener_movimientos_validos(self.pos_negro)

        if not mov_blanco and not mov_negro:
            self.juego_terminado = True
            return True

        return False

    def obtener_ganador(self):
        """Retorna el ganador del juego"""
        if self.puntos_blanco > self.puntos_negro:
            return "Blanco"
        elif self.puntos_negro > self.puntos_blanco:
            return "Negro"
        else:
            return "Empate"
