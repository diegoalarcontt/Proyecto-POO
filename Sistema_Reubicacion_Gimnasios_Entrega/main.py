"""
Archivo principal para ejecutar la aplicación.
"""

import os
import sys
import tkinter as tk

# Permite importar los archivos dentro de la carpeta src.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")
sys.path.append(SRC_DIR)

from gui import AplicacionGimnasios


def main():
    root = tk.Tk()
    app = AplicacionGimnasios(root)
    root.mainloop()


if __name__ == "__main__":
    main()
