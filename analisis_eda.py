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


def complementar_datos(h1, h2, h3, h4, h4_comp, h5):
    # Cruzar claves de estado y municipio de h1 y h2 para ponerle nombre a h4
    catalogo_mun = pd.concat([
        h1[["cve_ent", "entidad", "cve_mun", "municipio"]],
        h2[["cve_ent", "entidad", "cve_mun", "municipio"]],
    ]).drop_duplicates()
    h4 = h4.merge(catalogo_mun, on=["cve_ent", "cve_mun"], how="left")

    # Calcular porcentajes clave para comparar proporciones
    h4["pct_negativas"] = (h4["noticias_negativas"] / h4["total_noticias"] * 100).round(2)
    h4_comp["pct_negativas"] = (h4_comp["notas_negativas"] / h4_comp["cantidad_noticias"] * 100).round(2)
    h5["pct_medianos_grandes"] = (h5["centros_medianos_grandes"] / h5["total_establecimientos"] * 100).round(2)
    h3["pct_acumulado"] = h3["porcentaje_nacional"].cumsum().round(2)

    return h1, h2, h3, h4, h4_comp, h5


def generar_estadisticas_anexo(tablas, carpeta_anexos):
    # Resumen estadístico (conteo, media, desv. estándar, min, cuartiles, max) para Anexo 11.3
    ruta_txt = os.path.join(carpeta_anexos, "estadistica_descriptiva_11_3.txt")
    with open(ruta_txt, "w", encoding="utf-8") as archivo:
        for nombre, df in tablas.items():
            archivo.write(f"=== ESTADISTICA DESCRIPTIVA: {nombre} ===\n")
            resumen = df.describe().round(2)
            archivo.write(resumen.to_string())
            archivo.write("\n\n")

        # Correlaciones importantes entre variables numéricas
        h1, _, _, h4, _, h5 = tablas.values()
        archivo.write("=== CORRELACIONES DE PEARSON ===\n")
        archivo.write(f"H1 (Total unidades vs % empresas grandes): {h1['total_unidades'].corr(h1['pct_empresas_grandes']):.3f}\n")
        archivo.write(f"H4 (Total noticias vs Sentimiento promedio): {h4['total_noticias'].corr(h4['sentimiento_promedio']):.3f}\n")
        archivo.write(f"H5 (Total establecimientos vs Centros grandes): {h5['total_establecimientos'].corr(h5['centros_medianos_grandes']):.3f}\n")

    print(f"Estadísticas guardadas en: {ruta_txt}")
