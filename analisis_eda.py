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

    print(f"Estadísticas guardadas en resultados_eda.")


def graficas_principales(h1, h2, h3, h4, h5, carpeta_prin):
    # Gráfica 6.1: Top municipios por empresas medianas y grandes
    top_h1 = h1.sort_values("empresas_medianas_grandes", ascending=True).tail(10)
    plt.figure(figsize=(9, 5))
    plt.barh(top_h1["municipio"], top_h1["empresas_medianas_grandes"], color="#1f77b4")
    plt.title("Top 10 Municipios con Mayor Cantidad de Empresas Medianas y Grandes")
    plt.xlabel("Cantidad de empresas medianas y grandes")
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_prin, "fig_6_1_empresas_grandes_municipio.png"))
    plt.close()

    # Gráfica 6.2: Proveedores de salud vs higiene personal (barras apiladas)
    top_h2 = h2.head(10).iloc[::-1]
    plt.figure(figsize=(9, 5))
    plt.barh(top_h2["municipio"], top_h2["fab_equipo_medico"], label="Equipo Médico", color="#2ca02c")
    plt.barh(top_h2["municipio"], top_h2["fab_higiene_personal"], left=top_h2["fab_equipo_medico"], label="Higiene Personal", color="#98df8a")
    plt.title("Top 10 Municipios Proveedores de Salud e Higiene Personal")
    plt.xlabel("Total de proveedores")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_prin, "fig_6_2_proveedores_salud_higiene.png"))
    plt.close()

    # Gráfica 6.3: Distribución nacional por estrato de empleados
    plt.figure(figsize=(9, 5))
    plt.bar(h3["estrato_empleados"], h3["porcentaje_nacional"], color="#ff7f0e")
    plt.title("Distribución Porcentual Nacional de Establecimientos por Tamaño")
    plt.ylabel("Porcentaje nacional (%)")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_prin, "fig_6_3_distribucion_estratos.png"))
    plt.close()

    # Gráfica 6.4: Sentimiento promedio por municipio monitoreado
    h4_ord = h4.sort_values("sentimiento_promedio")
    colores_sent = ["#d62728" if x < 0 else "#2ca02c" for x in h4_ord["sentimiento_promedio"]]
    plt.figure(figsize=(9, 5))
    plt.barh(h4_ord["municipio"], h4_ord["sentimiento_promedio"], color=colores_sent)
    plt.axvline(0, color="black", linewidth=0.8)
    plt.title("Sentimiento Promedio de Noticias Económicas por Municipio")
    plt.xlabel("Índice de sentimiento promedio")
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_prin, "fig_6_4_sentimiento_municipios.png"))
    plt.close()

    # Gráfica 6.5: Concentración de centros medianos y grandes por colonia (Guadalajara)
    h5_ord = h5.sort_values("centros_medianos_grandes", ascending=True)
    plt.figure(figsize=(9, 5))
    plt.barh(h5_ord["colonia"], h5_ord["centros_medianos_grandes"], color="#9467bd")
    plt.title("Top 10 Colonias en Guadalajara por Centros Medianos y Grandes")
    plt.xlabel("Centros medianos y grandes")
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_prin, "fig_6_5_colonias_gdl.png"))
    plt.close()


def graficas_anexos(h1, h4_comp, h5, carpeta_anexos):
    # Anexo 11.4 A: Relación entre tamaño total del municipio y % de empresas grandes
    plt.figure(figsize=(8, 5))
    plt.scatter(h1["total_unidades"], h1["pct_empresas_grandes"], color="#1f77b4", s=70)
    for _, fila in h1.iterrows():
        plt.annotate(fila["municipio"], (fila["total_unidades"], fila["pct_empresas_grandes"]), fontsize=8)
    plt.title("Relación entre Total de Unidades Económicas y % de Empresas Grandes")
    plt.xlabel("Total de unidades económicas")
    plt.ylabel("Porcentaje de empresas grandes (%)")
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_anexos, "anexo_11_4_dispersion_h1.png"))
    plt.close()

    # Anexo 11.4 B: Sentimiento promedio por tema de noticia
    h4c_ord = h4_comp.sort_values("sentimiento_promedio")
    colores_tema = ["#d62728" if x < 0 else "#1f77b4" for x in h4c_ord["sentimiento_promedio"]]
    plt.figure(figsize=(8, 5))
    plt.barh(h4c_ord["tema_noticia"], h4c_ord["sentimiento_promedio"], color=colores_tema)
    plt.axvline(0, color="black", linewidth=0.8)
    plt.title("Sentimiento Promedio por Tema de Noticia (Complemento Hallazgo 4)")
    plt.xlabel("Sentimiento promedio")
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_anexos, "anexo_11_4_sentimiento_temas.png"))
    plt.close()

    # Anexo 11.4 C: Porcentaje de especialización industrial por colonia en Guadalajara
    h5_pct = h5.sort_values("pct_medianos_grandes", ascending=True)
    plt.figure(figsize=(8, 5))
    plt.barh(h5_pct["colonia"], h5_pct["pct_medianos_grandes"], color="#8c564b")
    plt.title("Densidad Relativa (%) de Centros Medianos/Grandes por Colonia")
    plt.xlabel("Porcentaje respecto al total de establecimientos (%)")
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_anexos, "anexo_11_4_densidad_colonias.png"))
    plt.close()


if __name__ == "__main__":
    # Crear carpetas de salida para organizar resultados
    carpeta_prin = os.path.join("resultados_eda", "graficas_principales")
    carpeta_anexos = os.path.join("resultados_eda", "anexos")
    os.makedirs(carpeta_prin, exist_ok=True)
    os.makedirs(carpeta_anexos, exist_ok=True)

    # Carga, complementa y analiza
    h1, h2, h3, h4, h4_comp, h5 = cargar_tablas_limpias()
    h1, h2, h3, h4, h4_comp, h5 = complementar_datos(h1, h2, h3, h4, h4_comp, h5)

    # Agrupar las 6 tablas ya complementadas en un diccionario
    tablas = {
        "Hallazgo 1 (Municipios)": h1,
        "Hallazgo 2 (Salud/Higiene)": h2,
        "Hallazgo 3 (Estratos)": h3,
        "Hallazgo 4 (Noticias Mun.)": h4,
        "Complemento H4 (Temas)": h4_comp,
        "Hallazgo 5 (Colonias GDL)": h5,
    }

    # Genera el resumen estadístico y todas las gráficas (principales y de anexos) para el informe
    generar_estadisticas_anexo(tablas, carpeta_anexos)
    graficas_principales(h1, h2, h3, h4, h5, carpeta_prin)
    graficas_anexos(h1, h4_comp, h5, carpeta_anexos)
    print("Análisis exploratorio y gráficas generados en resultados_eda.")