import random

class AIPlayer:
    """Jugador de IA que usa el algoritmo Minimax con poda Alpha-Beta"""

    def __init__(self, profundidad=4):
        self.profundidad = profundidad

    def calcular_heuristica(self, game_logic):
        """
        Función heurística para evaluar el estado del juego.
        La IA juega con el blanco.
        """
        # Diferencia de puntos 
        diferencia_puntos = game_logic.puntos_blanco - game_logic.puntos_negro

        # Movilidad
        mov_blanco = len(game_logic.obtener_movimientos_validos(game_logic.pos_blanco))
        mov_negro = len(game_logic.obtener_movimientos_validos(game_logic.pos_negro))
        movilidad = (mov_blanco - mov_negro) * 0.5

        return diferencia_puntos + movilidad

    def minimax(
        self,
        tablero,
        pos_blanco,
        pos_negro,
        puntos_blanco,
        puntos_negro,
        profundidad,
        es_turno_blanco,
        alpha,
        beta,
        movimientos_caballo,
        casillas_bloqueadas,
    ):
        """
        Algoritmo Minimax con poda Alpha-Beta
        La IA juega con el blanco (MAXIMIZA su puntuación)
        El humano juega con el negro (MINIMIZA la puntuación de la IA)
        puntos_blanco - puntos_negro (positivo = bueno para IA)
        """

        if profundidad == 0:
            # Evaluar desde la perspectiva de la IA
            diferencia = puntos_blanco - puntos_negro
            # Agregar factor de movilidad
            mov_blanco = self._contar_movimientos(
                pos_blanco,
                tablero,
                movimientos_caballo,
                casillas_bloqueadas,
                None,
                pos_negro,
            )
            mov_negro = self._contar_movimientos(
                pos_negro,
                tablero,
                movimientos_caballo,
                casillas_bloqueadas,
                pos_blanco,
                None,
            )
            return diferencia + (mov_blanco - mov_negro) * 0.5, None

        if es_turno_blanco:
            # Turno de la IA - MAXIMIZA la evaluación
            movimientos = self._obtener_movimientos(
                pos_blanco,
                tablero,
                movimientos_caballo,
                casillas_bloqueadas,
                None,
                pos_negro,
            )

            if not movimientos:
                # Si el blanco no puede moverse, es malo para la IA
                return puntos_blanco - puntos_negro - 100, None

            max_eval = float("-inf")
            mejor_movimiento = None

            for mov in movimientos:
                tablero_copia = [fila[:] for fila in tablero]
                puntos_ganados = tablero_copia[mov[0]][mov[1]]
                tablero_copia[mov[0]][mov[1]] = 0
                nuevos_puntos_blanco = puntos_blanco + puntos_ganados

                nuevas_bloqueadas = casillas_bloqueadas.copy()
                nuevas_bloqueadas.add(pos_blanco)
                nuevas_bloqueadas.add(mov)

                eval_score, _ = self.minimax(
                    tablero_copia,
                    mov,
                    pos_negro,
                    nuevos_puntos_blanco,
                    puntos_negro,
                    profundidad - 1,
                    False,  # Siguiente turno es del negro
                    alpha,
                    beta,
                    movimientos_caballo,
                    nuevas_bloqueadas,
                )

                if eval_score > max_eval:
                    max_eval = eval_score
                    mejor_movimiento = mov

                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Poda Beta

            return max_eval, mejor_movimiento

        else:
            # Turno del jugador negro - MINIMIZA la evaluación de la IA
            movimientos = self._obtener_movimientos(
                pos_negro,
                tablero,
                movimientos_caballo,
                casillas_bloqueadas,
                pos_blanco,
                None,
            )

            if not movimientos:
                # Si el negro no puede moverse, pierde 4 puntos 
                return puntos_blanco - (puntos_negro - 4) + 100, None

            min_eval = float("inf")
            mejor_movimiento = None

            for mov in movimientos:
                tablero_copia = [fila[:] for fila in tablero]
                puntos_ganados = tablero_copia[mov[0]][mov[1]]
                tablero_copia[mov[0]][mov[1]] = 0
                nuevos_puntos_negro = puntos_negro + puntos_ganados

                # Copiar casillas bloqueadas y agregar las nuevas
                nuevas_bloqueadas = casillas_bloqueadas.copy()
                nuevas_bloqueadas.add(pos_negro)
                nuevas_bloqueadas.add(mov)

                eval_score, _ = self.minimax(
                    tablero_copia,
                    pos_blanco,
                    mov,
                    puntos_blanco,
                    nuevos_puntos_negro,
                    profundidad - 1,
                    True,  # Siguiente turno es del blanco
                    alpha,
                    beta,
                    movimientos_caballo,
                    nuevas_bloqueadas,
                )

                if eval_score < min_eval:
                    min_eval = eval_score
                    mejor_movimiento = mov

                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Poda Alpha

            return min_eval, mejor_movimiento

    def _obtener_movimientos(
        self,
        pos,
        tablero,
        movimientos_caballo,
        casillas_bloqueadas=None,
        pos_blanco=None,
        pos_negro=None,
    ):
        """Obtiene movimientos válidos - no puede moverse a casilla ocupada por otro caballo"""
        movimientos = []
        fila, col = pos

        if casillas_bloqueadas is None:
            casillas_bloqueadas = set()

        for df, dc in movimientos_caballo:
            nueva_fila = fila + df
            nueva_col = col + dc

            # Verificar que esté en el tablero, que la casilla no esté bloqueada
            # y que no esté ocupada por el otro caballo
            
            if (
                0 <= nueva_fila < 8
                and 0 <= nueva_col < 8
                and (nueva_fila, nueva_col) not in casillas_bloqueadas
                and (pos_blanco is None or (nueva_fila, nueva_col) != pos_blanco)
                and (pos_negro is None or (nueva_fila, nueva_col) != pos_negro)
            ):
                movimientos.append((nueva_fila, nueva_col))

        return movimientos

    def _contar_movimientos(
        self,
        pos,
        tablero,
        movimientos_caballo,
        casillas_bloqueadas=None,
        pos_blanco=None,
        pos_negro=None,
    ):
        """Cuenta la cantidad de movimientos válidos"""
        return len(
            self._obtener_movimientos(
                pos,
                tablero,
                movimientos_caballo,
                casillas_bloqueadas,
                pos_blanco,
                pos_negro,
            )
        )

    def obtener_mejor_movimiento(self, game_logic):
        """Calcula y retorna el mejor movimiento para la IA """
        from config import MOVIMIENTOS_CABALLO

        _, mejor_movimiento = self.minimax(
            game_logic.tablero,
            game_logic.pos_blanco,
            game_logic.pos_negro,
            game_logic.puntos_blanco,
            game_logic.puntos_negro,
            self.profundidad,
            True,  
            float("-inf"),
            float("inf"),
            MOVIMIENTOS_CABALLO,
            game_logic.casillas_bloqueadas,
        )

        if mejor_movimiento is None:
            movimientos = game_logic.obtener_movimientos_validos(game_logic.pos_blanco)
            if movimientos:
                mejor_movimiento = random.choice(movimientos)

        return mejor_movimiento
