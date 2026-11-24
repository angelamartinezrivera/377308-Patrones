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

# Diccionario para corregir palabras que venían con acentos o letras repetidas
CORRECCIONES = {
    "Leán": "León",
    "Tijuaána": "Tijuana",
    "Nuevo Len": "Nuevo León",
    "Moánterrey": "Monterrey",
    "Zapopaán": "Zapopan",
    "Ciudad de Mxico": "Ciudad de México",
    "Jurez": "Juárez",
    "Quertaro": "Querétaro",
    "San Luis Potos": "San Luis Potosí",
    "Saán Luis Potos": "San Luis Potosí",
    "Aguascalieántes": "Aguascalientes",
    "Mxico": "México",
    "Tlalánepaántla de Baz": "Tlalnepantla de Baz",
    "Yucatn": "Yucatán",
    "Mrida": "Mérida",
    "Nezahualcyotl": "Nezahualcóyotl",
    "Michoacn de Ocampo": "Michoacán de Ocampo",
    "251 y ms personas": "251 y más personas",
}


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


def limpiar_datos(df):
    # Poner los nombres de las columnas en minúsculas y cambiar espacios por guión bajo
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Recorrer cada columna para quitar símbolos extraños (\ufffd) y espacios extra
    for col in df.columns:
        df[col] = (
            df[col]
            .str.replace("\ufffd", "", regex=False)
            .str.strip()
            .replace(CORRECCIONES)
        )


if __name__ == "__main__":
    # Carga todos los archivos de la lista al inicio
    tablas_crudas = cargar_todos(ARCHIVOS_CSV)