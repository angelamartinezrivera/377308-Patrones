import os  # Librería para revisar si existen archivos y crear carpetas
import pandas as pd  # Librería para análisis y manipulación de tablas
import matplotlib.pyplot as plt  # Generación de gráficas

# Configuración visual general de las gráficas
plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams["figure.dpi"] = 150
plt.rcParams["font.size"] = 10


def cargar_tablas_limpias():
    # Lee los 6 archivos limpios
    h1 = pd.read_csv(os.path.join("limpios", "limpio_hallazgo_1.csv"), dtype={"cve_ent": str, "cve_mun": str})
    h2 = pd.read_csv(os.path.join("limpios", "limpio_hallazgo_2.csv"), dtype={"cve_ent": str, "cve_mun": str})
    h3 = pd.read_csv(os.path.join("limpios", "limpio_hallazgo_3.csv"))
    h4 = pd.read_csv(os.path.join("limpios", "limpio_hallazgo_4.csv"), dtype={"cve_ent": str, "cve_mun": str})
    h4_comp = pd.read_csv(os.path.join("limpios", "limpio_complemento_hallazgo_4.csv"))
    h5 = pd.read_csv(os.path.join("limpios", "limpio_hallazgo_5.csv"), dtype={"cod_postal": str})
    return h1, h2, h3, h4, h4_comp, h5