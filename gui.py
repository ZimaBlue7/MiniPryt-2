"""
Interfaz gráfica para Smart Horses usando Tkinter
"""

import tkinter as tk
from tkinter import messagebox, ttk
from config import *
from game_logic import GameLogic
from ai_player import AIPlayer


class SmartHorsesGUI:
    """Interfaz gráfica del juego Smart Horses"""

    def __init__(self, root):
        self.root = root
        self.root.title("🐴 Smart Horses")
        self.root.configure(bg=COLOR_FONDO)
        self.root.resizable(False, False)

        self.game_logic = None
        self.ai_player = None
        self.casillas_canvas = {}
        self.movimientos_resaltados = []
        self.esperando_ia = False

        self.mostrar_menu_inicio()

    def mostrar_menu_inicio(self):
        """Muestra el menú de inicio para seleccionar dificultad"""
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()

        # Resetear tamaño de ventana
        self.root.geometry("")  # Resetear geometría

        # Frame principal con scrollbar por si acaso
        main_container = tk.Frame(self.root, bg=COLOR_FONDO)
        main_container.pack(expand=True, fill="both")

        frame = tk.Frame(main_container, bg=COLOR_FONDO, padx=40, pady=40)
        frame.pack(expand=True, fill="both")

        # Título
        titulo = tk.Label(
            frame,
            text=" SMART HORSES ",
            font=("Arial", 32, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO,
        )
        titulo.pack(pady=20)

        # Subtítulo
        subtitulo = tk.Label(
            frame,
            text="Juego de estrategia con caballos de ajedrez",
            font=("Arial", 14),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO,
        )
        subtitulo.pack(pady=10)

        # Reglas
        reglas = tk.Label(
            frame,
            text="📖 REGLAS:\n\n"
            "• La IA juega con el caballo blanco (♘) y empieza\n"
            "• Tú juegas con el caballo negro (♞)\n"
            "• Posiciones iniciales aleatorias (no coinciden)\n"
            "• Los caballos se mueven en L (como en ajedrez)\n"
            "• Haz clic en tu caballo negro para ver movimientos\n"
            "• Haz clic en una casilla verde para mover\n"
            "• Valores: -10, -5, -4, -3, -1, +1, +3, +4, +5, +10\n"
            "• Si no tienes movimientos, pierdes 4 puntos\n"
            "• ¡Gana quien tenga más puntos al final!",
            font=("Arial", 10),
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
            justify="left",
            padx=20,
            pady=15,
        )
        reglas.pack(pady=20, ipadx=10, ipady=10)

        # Selector de dificultad
        diff_label = tk.Label(
            frame,
            text="Selecciona la dificultad:",
            font=("Arial", 14, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO,
        )
        diff_label.pack(pady=10)

        self.nivel_var = tk.StringVar(value="Amateur")

        for nivel in NIVELES.keys():
            btn = tk.Radiobutton(
                frame,
                text=f"{nivel} (Profundidad {NIVELES[nivel]})",
                variable=self.nivel_var,
                value=nivel,
                font=("Arial", 12),
                bg=COLOR_FONDO,
                fg=COLOR_TEXTO,
                selectcolor=COLOR_PANEL,
                activebackground=COLOR_FONDO,
                activeforeground=COLOR_TEXTO,
            )
            btn.pack(pady=5)

        # Botón iniciar
        btn_iniciar = tk.Button(
            frame,
            text="🎮 INICIAR JUEGO",
            font=("Arial", 16, "bold"),
            bg="#27AE60",
            fg="white",
            activebackground="#229954",
            activeforeground="white",
            padx=30,
            pady=15,
            cursor="hand2",
            command=self.iniciar_juego,
        )
        btn_iniciar.pack(pady=30)

        # Forzar actualización y centrar ventana
        self.root.update_idletasks()

        # Ajustar tamaño de ventana al contenido
        width = max(600, self.root.winfo_reqwidth())
        height = max(700, self.root.winfo_reqheight())
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def iniciar_juego(self):
        """Inicia el juego con la dificultad seleccionada"""
        from config import generar_tablero_aleatorio

        nivel = self.nivel_var.get()
        profundidad = NIVELES[nivel]

        # Generar tablero aleatorio con posiciones aleatorias
        # Blanco = IA (empieza primero), Negro = Jugador humano
        tablero, pos_blanco, pos_negro = generar_tablero_aleatorio()

        self.game_logic = GameLogic(tablero, pos_blanco, pos_negro)
        self.ai_player = AIPlayer(profundidad)

        self.crear_interfaz_juego()

        # La IA (blanco) siempre empieza, así que hace el primer movimiento
        # Importante: llamar después de crear la interfaz
        self.root.after(1000, self.primer_movimiento_ia)

    def primer_movimiento_ia(self):
        """Ejecuta el primer movimiento de la IA al iniciar el juego"""
        if self.game_logic and self.ai_player:
            self.turno_ia()

    def crear_interfaz_juego(self):
        """Crea la interfaz principal del juego"""
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()

        # Frame principal
        main_frame = tk.Frame(self.root, bg=COLOR_FONDO)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Panel izquierdo (tablero)
        tablero_frame = tk.Frame(main_frame, bg=COLOR_FONDO)
        tablero_frame.pack(side="left", padx=10)

        # Título del tablero
        titulo = tk.Label(
            tablero_frame,
            text=" SMART HORSES ",
            font=("Arial", 20, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO,
        )
        titulo.pack(pady=10)

        # Canvas del tablero
        self.canvas = tk.Canvas(
            tablero_frame,
            width=TAMANO_CELDA * TAMANO_TABLERO,
            height=TAMANO_CELDA * TAMANO_TABLERO,
            bg=COLOR_FONDO,
            highlightthickness=2,
            highlightbackground=COLOR_TEXTO,
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.click_tablero)

        # Panel derecho (información)
        info_frame = tk.Frame(main_frame, bg=COLOR_PANEL, width=280)
        info_frame.pack(side="right", fill="y", padx=10)
        info_frame.pack_propagate(False)

        # Turno actual
        tk.Label(
            info_frame,
            text="TURNO ACTUAL",
            font=("Arial", 12, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
        ).pack(pady=(20, 5))

        self.label_turno = tk.Label(
            info_frame,
            text="⚪ Blanco",
            font=("Arial", 14, "bold"),
            bg=COLOR_PANEL,
            fg="white",
        )
        self.label_turno.pack(pady=5)

        # Separador
        tk.Frame(info_frame, height=2, bg=COLOR_TEXTO).pack(fill="x", padx=20, pady=15)

        # Puntuación
        tk.Label(
            info_frame,
            text="PUNTUACIÓN",
            font=("Arial", 12, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
        ).pack(pady=(10, 5))

        # Puntos Blanco (IA)
        frame_blanco = tk.Frame(info_frame, bg=COLOR_PANEL)
        frame_blanco.pack(pady=10, fill="x", padx=20)

        tk.Label(
            frame_blanco,
            text=" Blanco (IA):",
            font=("Arial", 11),
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
        ).pack(side="left")

        self.label_puntos_blanco = tk.Label(
            frame_blanco,
            text="0",
            font=("Arial", 11, "bold"),
            bg=COLOR_PANEL,
            fg="white",
        )
        self.label_puntos_blanco.pack(side="right")

        # Puntos Negro (Jugador)
        frame_negro = tk.Frame(info_frame, bg=COLOR_PANEL)
        frame_negro.pack(pady=10, fill="x", padx=20)

        tk.Label(
            frame_negro,
            text=" Negro (Tú):",
            font=("Arial", 11),
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
        ).pack(side="left")

        self.label_puntos_negro = tk.Label(
            frame_negro,
            text="0",
            font=("Arial", 11, "bold"),
            bg=COLOR_PANEL,
            fg="white",
        )
        self.label_puntos_negro.pack(side="right")

        # Separador
        tk.Frame(info_frame, height=2, bg=COLOR_TEXTO).pack(fill="x", padx=20, pady=15)

        # Instrucciones
        tk.Label(
            info_frame,
            text="INSTRUCCIONES",
            font=("Arial", 12, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
        ).pack(pady=(10, 5))

        instrucciones = tk.Label(
            info_frame,
            text="1. La IA (blanco)\n"
            "   mueve primero\n\n"
            "2. Haz clic en tu\n"
            "   caballo negro\n\n"
            "3. Se mostrarán los\n"
            "   movimientos válidos\n\n"
            "4. Haz clic en una\n"
            "   casilla verde\n\n"
            " Las casillas rojas\n"
            "   con X ya no se\n"
            "   pueden usar\n\n"
            " Si no puedes\n"
            "   moverte, pierdes\n"
            "   4 puntos por turno",
            font=("Arial", 9),
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
            justify="left",
        )
        instrucciones.pack(pady=10, padx=15)

        # Botones
        btn_frame = tk.Frame(info_frame, bg=COLOR_PANEL)
        btn_frame.pack(side="bottom", pady=20)

        tk.Button(
            btn_frame,
            text="🔄 Nuevo Juego",
            font=("Arial", 10),
            bg="#3498DB",
            fg="white",
            activebackground="#2980B9",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.mostrar_menu_inicio,
        ).pack(pady=5)

        # Dibujar tablero inicial
        self.dibujar_tablero()

        # Centrar ventana
        self.root.update_idletasks()
        width = ANCHO_VENTANA
        height = ALTO_VENTANA
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def dibujar_tablero(self):
        """Dibuja el tablero con las casillas y caballos"""
        self.canvas.delete("all")
        self.casillas_canvas = {}

        for fila in range(TAMANO_TABLERO):
            for col in range(TAMANO_TABLERO):
                x1 = col * TAMANO_CELDA
                y1 = fila * TAMANO_CELDA
                x2 = x1 + TAMANO_CELDA
                y2 = y1 + TAMANO_CELDA

                # Color de la casilla
                if (fila, col) in self.game_logic.casillas_bloqueadas:
                    # Casillas bloqueadas en rojo oscuro
                    color = COLOR_BLOQUEADO
                elif (fila, col) in self.movimientos_resaltados:
                    color = COLOR_MOVIMIENTO_VALIDO
                elif (fila + col) % 2 == 0:
                    color = COLOR_CELDA_CLARA
                else:
                    color = COLOR_CELDA_OSCURA

                # Dibujar casilla
                rect = self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=color, outline="#8B4513", width=1
                )
                self.casillas_canvas[(fila, col)] = rect

                # Dibujar puntos de la casilla (solo si no está bloqueada)
                puntos = self.game_logic.tablero[fila][col]
                if (
                    puntos != 0
                    and (fila, col) not in self.game_logic.casillas_bloqueadas
                ):
                    color_texto = "#C0392B" if puntos < 0 else "#27AE60"
                    self.canvas.create_text(
                        x1 + TAMANO_CELDA // 2,
                        y1 + 15,
                        text=f"{puntos:+d}",
                        font=("Arial", 10, "bold"),
                        fill=color_texto,
                    )

                # Marcar casillas bloqueadas con una X
                if (fila, col) in self.game_logic.casillas_bloqueadas:
                    # Dibujar X grande
                    self.canvas.create_line(
                        x1 + 10, y1 + 10, x2 - 10, y2 - 10, fill="#FFFFFF", width=3
                    )
                    self.canvas.create_line(
                        x1 + 10, y2 - 10, x2 - 10, y1 + 10, fill="#FFFFFF", width=3
                    )

                # Dibujar caballos
                if (fila, col) == self.game_logic.pos_blanco:
                    self.canvas.create_text(
                        x1 + TAMANO_CELDA // 2,
                        y1 + TAMANO_CELDA // 2 + 5,
                        text="♘",
                        font=("Arial", 40),
                        fill="white",
                        tags="caballo_blanco",
                    )
                elif (fila, col) == self.game_logic.pos_negro:
                    self.canvas.create_text(
                        x1 + TAMANO_CELDA // 2,
                        y1 + TAMANO_CELDA // 2 + 5,
                        text="♞",
                        font=("Arial", 40),
                        fill="black",
                        tags="caballo_negro",
                    )

        # Actualizar información
        self.actualizar_info()

    def actualizar_info(self):
        """Actualiza la información del panel derecho"""
        if self.game_logic.turno_blanco:
            if self.game_logic.blanco_sin_movimientos:
                self.label_turno.config(
                    text="⚪ Blanco/IA (Sin movimientos)", fg="orange"
                )
            else:
                self.label_turno.config(text="⚪ Blanco (IA)", fg="white")
        else:
            if self.game_logic.negro_sin_movimientos:
                self.label_turno.config(
                    text="⚫ Negro/Tú (Sin movimientos)", fg="orange"
                )
            else:
                self.label_turno.config(text="⚫ Negro (Tu turno)", fg="lightgreen")

        self.label_puntos_blanco.config(text=str(self.game_logic.puntos_blanco))
        self.label_puntos_negro.config(text=str(self.game_logic.puntos_negro))

        # Validación automática: si es turno del negro pero no tiene movimientos,
        # cambiar automáticamente al turno de la IA
        if (
            not self.game_logic.turno_blanco
            and self.game_logic.negro_sin_movimientos
            and not self.game_logic.juego_terminado
            and not self.esperando_ia
        ):
            # Cambiar turno al blanco (IA) automáticamente
            self.game_logic.turno_blanco = True
            self.root.after(1000, self.turno_ia)

    def click_tablero(self, event):
        """Maneja los clicks en el tablero"""
        if self.esperando_ia or self.game_logic.juego_terminado:
            return

        col = event.x // TAMANO_CELDA
        fila = event.y // TAMANO_CELDA

        if not (0 <= fila < 8 and 0 <= col < 8):
            return

        # Si es turno del negro (jugador humano)
        if not self.game_logic.turno_blanco:
            # Si el negro no tiene movimientos, pasar al turno de la IA
            if self.game_logic.negro_sin_movimientos:
                self.game_logic.turno_blanco = True
                self.root.after(500, self.turno_ia)
                return

            # Si hace click en su caballo negro, mostrar movimientos
            if (fila, col) == self.game_logic.pos_negro:
                self.movimientos_resaltados = (
                    self.game_logic.obtener_movimientos_validos(
                        self.game_logic.pos_negro
                    )
                )
                self.dibujar_tablero()

            # Si hace click en un movimiento válido, mover
            elif (fila, col) in self.movimientos_resaltados:
                self.movimientos_resaltados = []
                if self.game_logic.mover_caballo((fila, col)):
                    self.dibujar_tablero()

                    # Verificar fin del juego
                    if self.game_logic.verificar_fin_juego():
                        self.mostrar_fin_juego()
                        return

                    # Turno de la IA (blanco)
                    if self.game_logic.turno_blanco:
                        self.root.after(500, self.turno_ia)

    def turno_ia(self):
        """Ejecuta el turno de la IA"""
        if self.game_logic.juego_terminado:
            return

        self.esperando_ia = True
        self.label_turno.config(text="⚪ IA pensando...")
        self.root.update()

        # Si la IA (blanco) no tiene movimientos, cambiar turno
        if self.game_logic.blanco_sin_movimientos:
            self.esperando_ia = False
            self.game_logic.turno_blanco = False
            self.dibujar_tablero()

            # Verificar fin del juego
            if self.game_logic.verificar_fin_juego():
                self.root.after(500, self.mostrar_fin_juego)
            return

        mejor_movimiento = self.ai_player.obtener_mejor_movimiento(self.game_logic)

        if mejor_movimiento:
            self.game_logic.mover_caballo(mejor_movimiento)

        self.esperando_ia = False
        self.dibujar_tablero()

        # Verificar fin del juego
        if self.game_logic.verificar_fin_juego():
            self.root.after(500, self.mostrar_fin_juego)
            return

        # Continuar automáticamente si el jugador contrario no tiene movimientos
        # Caso 1: Si es turno del negro pero no tiene movimientos, la IA continúa
        if not self.game_logic.turno_blanco and self.game_logic.negro_sin_movimientos:
            self.game_logic.turno_blanco = True
            self.root.after(1000, self.turno_ia)
        # Caso 2: Si es turno del blanco pero no tiene movimientos, la IA intenta de nuevo
        elif (
            self.game_logic.turno_blanco
            and self.game_logic.blanco_sin_movimientos
            and not self.game_logic.negro_sin_movimientos
        ):
            self.game_logic.turno_blanco = False
            # El turno pasa al negro, pero si tampoco tiene movimientos,
            # la validación automática en dibujar_tablero() lo manejará

    def mostrar_fin_juego(self):
        """Muestra el mensaje de fin del juego"""
        ganador = self.game_logic.obtener_ganador()

        mensaje = f"🏁 JUEGO TERMINADO 🏁\n\n"
        mensaje += f"⚪ Blanco (IA): {self.game_logic.puntos_blanco} puntos\n"
        mensaje += f"⚫ Negro (Tú): {self.game_logic.puntos_negro} puntos\n\n"

        if ganador == "Negro":
            mensaje += "🎉 ¡GANASTE! ¡Felicidades! 🎉"
            titulo = "¡Victoria!"
        elif ganador == "Blanco":
            mensaje += "😔 La IA ganó. ¡Intenta de nuevo!"
            titulo = "Derrota"
        else:
            mensaje += "🤝 ¡Es un empate!"
            titulo = "Empate"

        respuesta = messagebox.askyesno(
            titulo, mensaje + "\n\n¿Quieres jugar de nuevo?", icon="info"
        )

        if respuesta:
            self.mostrar_menu_inicio()
        else:
            self.root.quit()
