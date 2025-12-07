import sqlite3
import os

# Ruta absoluta al archivo nuam.db dentro de la carpeta config
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "nuam.db")

def conectar():
    try:
        conexion = sqlite3.connect(DB_PATH)
        print(f" Conectado a la base de datos: {DB_PATH}")
        return conexion
    except sqlite3.Error as e:
        print(f" Error de conexión: {e}")
