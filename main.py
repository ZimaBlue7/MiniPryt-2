"""
Smart Horses - Juego de estrategia con caballos de ajedrez
Punto de entrada principal del juego
"""

import tkinter as tk
from gui import SmartHorsesGUI


def main():
    """Función principal que inicia el juego"""
    root = tk.Tk()
    app = SmartHorsesGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
