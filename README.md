**Nombre:** Angela Guadalupe Martínez Rivera

# Estrategia de expansión y selección de ubicación para una nueva sucursal de farmacia

## Objetivo del proyecto

Proyecto de análisis para apoyar a una cadena de farmacias en la búsqueda de posibles zonas para abrir una nueva sucursal. El análisis se enfocó en conocer la actividad empresarial, los fabricantes relacionados con el sector salud e higiene y algunas noticias económicas de distintos municipios de México.

## Descripción general
El proyecto utiliza información del Directorio Estadístico Nacional de Unidades Económicas (DENUE) y una base de datos de noticias económicas. Para analizar esta información se realizaron las siguientes actividades:
- **Extracción de datos:** Se utilizaron consultas SQL en DBeaver para obtener información sobre empresas según su tamaño, actividad económica y ubicación, así como noticias relacionadas con distintos municipios.
- **Limpieza de datos:** Se corrigieron errores en los textos, acentos y claves geográficas, se conservaron los ceros iniciales de los códigos y se eliminaron registros repetidos.
- **Análisis de datos (EDA):** Se calcularon cantidades, porcentajes y otros datos estadísticos para comparar la actividad empresarial, los fabricantes y las noticias de cada zona.
- **Visualización:** Se realizaron gráficas para presentar los resultados y facilitar su comparación.

## Herramientas y librerías utilizadas
* **Base de datos y consultas:** PostgreSQL / DBeaver (`consultas.sql`).
* **Procesamiento y análisis:** Python 3.14.3
    - `pandas`: Limpieza, manipulación de tablas CSV y estadística descriptiva.
    - `matplotlib`: Generación de gráficas.
* **Entorno y control de versiones:** Visual Studio Code y GitHub.

## Guía de ejecución

### 1. Clonar el repositorio

Abre **CMD**, ubícate en la carpeta donde guardas tus proyectos (por ejemplo, `Documents`) y clona el repositorio:

```bash
cd Documents
git clone https://github.com/angelamartinezrivera/377308-Patrones.git
```

### 2. Crear y activar el entorno virtual (`venv`)

Para ejecutar los scripts del proyecto, sigue estos pasos desde la terminal de **Visual Studio Code**:

Dentro de la carpeta `377308-Patrones`, crea el entorno virtual:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar las librerías necesarias
Con el entorno virtual activo, instala `pandas` y `matplotlib`:

```bash
pip install pandas matplotlib
```

### 4. Verificar los archivos de datos (`.csv`)
Revisar que en la carpeta (`377308-Patrones`) se encuentren los 6 archivos CSV exportados desde DBeaver con `consultas.sql` (`hallazgo_1.csv`, `hallazgo_2.csv`, `hallazgo_3.csv`, `hallazgo_4.csv`, `hallazgo_5.csv` y `complemento_hallazgo_4.csv`).

### 5. Ejecutar el script de limpieza (`limpieza.py`)
Ejecuta el primer script para corregir acentos, conservar los ceros iniciales en claves geográficas (`cve_ent`, `cve_mun`, `cod_postal`), eliminar duplicados y generar los archivos limpios:

```bash
python limpieza.py
```

### 6. Ejecutar el script de análisis y visualizaciones (`analisis_eda.py`)
Una vez generados los CSV limpios, ejecuta el segundo script para generar el resumen de estadística descriptiva y crear las gráficas del informe:

```bash
python analisis_eda.py
```