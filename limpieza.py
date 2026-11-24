import os # Librería para revisar si existen archivos y crear carpetas
import pandas as pd # Librería para trabajar con tablas de datos

# Lista con los nombres de los archivos CSV
ARCHIVOS_CSV = [
    "complemento_hallazgo_4.csv",
    "hallazgo_1.csv",
    "hallazgo_2.csv",
    "hallazgo_3.csv",
    "hallazgo_4.csv",
    "hallazgo_5.csv"
]


def cargar_todos(lista_archivos):
    # Diccionario vacío donde se guarda cada tabla leída
    tablas = {}

    for nombre in lista_archivos:
        # Verificar que el archivo exista en la carpeta antes de intentar abrirlo
        if os.path.exists(nombre):
            # Lee todo como texto para que no se borren los ceros a la izquierda
            tablas[nombre] = pd.read_csv(
                nombre, dtype=str, encoding="utf-8", encoding_errors="replace"
            )
            print(f"Cargado: {nombre}")
        else:
            print(f"No encontrado: {nombre}")

    return tablas


if __name__ == "__main__":
    # Paso 1: Carga todos los archivos de la lista al inicio
    tablas_crudas = cargar_todos(ARCHIVOS_CSV)