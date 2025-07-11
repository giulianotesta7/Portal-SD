import os
import time
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path)


def borrar_firmas(carpeta):
    for archivo in os.listdir(carpeta):
        if archivo.endswith(".png"):
            ruta = os.path.join(carpeta, archivo)
            try:
                os.remove(ruta)

            except Exception as e:
                print(f"❌ Error eliminando {archivo}: {e}")

if __name__ == "__main__":
    carpeta_firmas = os.getenv("RUTA_FIRMAS")
    borrar_firmas(carpeta_firmas)

#AGREGAR EN PROGRAMADOR DE TAREAS 
#PROGRAMA O SCRIPT: C:\Users\USUARIO\AppData\Local\Programs\Python\Python313\python.exe
#ARGUMENTOS: C:\RUTA\APP\utils\limpiar_firmas.py