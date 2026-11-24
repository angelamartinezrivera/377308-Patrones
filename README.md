# Estrategia de expansión y selección de ubicación para una nueva sucursal de farmacia.

Proyecto de análisis para apoyar a una cadena de farmacias en la búsqueda de posibles zonas para abrir una nueva sucursal. El análisis se enfocó en conocer la actividad empresarial, los fabricantes relacionados con el sector salud e higiene y algunas noticias económicas de distintos municipios de México.

## Objetivo del Proyecto
Identificar los municipios y zonas con mayor cantidad de empresas medianas y grandes, fabricantes de equipo médico y productos de higiene, así como revisar algunas noticias económicas para conocer mejor la actividad de cada zona y encontrar posibles oportunidades comerciales.

## Descripción General
El proyecto utiliza información del Directorio Estadístico Nacional de Unidades Económicas (DENUE) y una base de datos de noticias económicas. Para analizar esta información se realizaron las siguientes actividades:
- **Extracción de datos:** Se utilizaron consultas SQL en DBeaver para obtener información sobre empresas según su tamaño, actividad económica y ubicación, así como noticias relacionadas con distintos municipios.
- **Limpieza de datos:** Se corrigieron errores en los textos, acentos y claves geográficas, se conservaron los ceros iniciales de los códigos y se eliminaron registros repetidos.
- **Análisis de datos (EDA):** Se calcularon cantidades, porcentajes y otros datos estadísticos para comparar la actividad empresarial, los fabricantes y las noticias de cada zona.
- **Visualización:** Se realizaron gráficas para presentar los resultados y facilitar su comparación.

## Herramientas Utilizadas
* **Base de datos y consultas:** PostgreSQL / DBeaver (`consultas.sql`)
* **Procesamiento y análisis:** Python 3.14.3
* **Entorno y control de versiones:** Visual Studio Code y GitHub