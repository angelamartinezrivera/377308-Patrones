-- ============================================================================
-- PROYECTO: Estrategia de expansión y selección de ubicación para una nueva sucursal de farmacia
-- MATERIA: Patrones de Comportamiento de Datos
-- DESCRIPCIÓN: Consultas SQL en DBeaver
-- ============================================================================

-- ============================================================================
-- BLOQUE 1: BASE DE DATOS DENUE (tabla: denue_inegi_oficial)
-- ============================================================================

-- 1. HALLAZGO 1: Top 15 municipios con mayor concentración de centros de trabajo
--    medianos y grandes (indicador de masa laboral formal y poder adquisitivo).
SELECT 
    LPAD(cve_ent::text, 2, '0') AS cve_ent,
    entidad,
    LPAD(cve_mun::text, 3, '0') AS cve_mun,
    municipio,
    COUNT(*) AS total_unidades,
    COUNT(CASE WHEN per_ocu NOT IN ('0 a 5 personas', '6 a 10 personas') THEN 1 END) AS empresas_medianas_grandes,
    ROUND(
        COUNT(CASE WHEN per_ocu NOT IN ('0 a 5 personas', '6 a 10 personas') THEN 1 END) * 100.0 / COUNT(*), 
        2
    ) AS pct_empresas_grandes
FROM denue_inegi_oficial
GROUP BY cve_ent, entidad, cve_mun, municipio
HAVING COUNT(*) >= 5000
ORDER BY empresas_medianas_grandes DESC
LIMIT 15;

-- 2. HALLAZGO 2: Concentración de fabricantes de equipo médico (339111) e higiene 
--    personal y limpieza (325610) por municipio.
SELECT 
    LPAD(cve_ent::text, 2, '0') AS cve_ent,
    entidad,
    LPAD(cve_mun::text, 3, '0') AS cve_mun,
    municipio,
    COUNT(CASE WHEN codigo_act = 339111 THEN 1 END) AS fab_equipo_medico,
    COUNT(CASE WHEN codigo_act = 325610 THEN 1 END) AS fab_higiene_personal,
    COUNT(*) AS total_proveedores_salud_higiene
FROM denue_inegi_oficial
WHERE codigo_act IN (339111, 325610)
GROUP BY cve_ent, entidad, cve_mun, municipio
ORDER BY total_proveedores_salud_higiene DESC
LIMIT 15;

-- 3. HALLAZGO 3: Distribución nacional de establecimientos por tamaño de 
--    personal ocupado (per_ocu).
SELECT 
    per_ocu AS estrato_empleados,
    COUNT(*) AS cantidad_establecimientos,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS porcentaje_nacional
FROM denue_inegi_oficial
GROUP BY per_ocu
ORDER BY cantidad_establecimientos DESC;

-- 4. HALLAZGO 5: Colonias y códigos postales con mayor concentración de 
--    centros de trabajo dentro del municipio ganador (Guadalajara, Jalisco: 14-039).
SELECT 
    nomb_asent AS colonia,
    cod_postal,
    COUNT(*) AS total_establecimientos,
    COUNT(CASE WHEN per_ocu NOT IN ('0 a 5 personas', '6 a 10 personas') THEN 1 END) AS centros_medianos_grandes
FROM denue_inegi_oficial
WHERE cve_ent = 14      -- Jalisco
  AND cve_mun = 39      -- Guadalajara
  AND nomb_asent IS NOT NULL
GROUP BY nomb_asent, cod_postal
ORDER BY centros_medianos_grandes DESC, total_establecimientos DESC
LIMIT 10;


-- ============================================================================
-- BLOQUE 2: BASE DE DATOS DE NOTICIAS (tablas: noticia_geo y noticia)
-- ============================================================================

-- 5. HALLAZGO 4: Volumen de noticias, sentimiento promedio y conteo de notas
--    negativas en los 15 municipios candidatos del Bloque 1.
SELECT 
    LPAD(TRIM(ng.cve_ent), 2, '0') AS cve_ent,
    LPAD(TRIM(ng.cve_mun), 3, '0') AS cve_mun,
    COUNT(n.id_noticia) AS total_noticias,
    ROUND(AVG(n.sentimiento)::numeric, 2) AS sentimiento_promedio,
    COUNT(CASE WHEN n.sentimiento < 0 THEN 1 END) AS noticias_negativas
FROM noticia_geo ng
JOIN noticia n ON ng.id_noticia = n.id_noticia
WHERE (LPAD(TRIM(ng.cve_ent), 2, '0'), LPAD(TRIM(ng.cve_mun), 3, '0')) IN (
    ('11', '020'), -- 1. León, Guanajuato
    ('14', '039'), -- 2. Guadalajara, Jalisco
    ('02', '004'), -- 3. Tijuana, Baja California
    ('19', '039'), -- 4. Monterrey, Nuevo León
    ('14', '120'), -- 5. Zapopan, Jalisco
    ('09', '007'), -- 6. Iztapalapa, Ciudad de México
    ('19', '006'), -- 7. Apodaca, Nuevo León
    ('08', '037'), -- 8. Juárez, Chihuahua
    ('21', '114'), -- 9. Puebla, Puebla
    ('22', '014'), -- 10. Querétaro, Querétaro
    ('24', '028'), -- 11. San Luis Potosí, San Luis Potosí
    ('19', '026'), -- 12. Guadalupe, Nuevo León
    ('01', '001'), -- 13. Aguascalientes, Aguascalientes
    ('08', '019'), -- 14. Chihuahua, Chihuahua
    ('15', '104')  -- 15. Tlalnepantla de Baz, Estado de México
)
GROUP BY LPAD(TRIM(ng.cve_ent), 2, '0'), LPAD(TRIM(ng.cve_mun), 3, '0')
ORDER BY total_noticias DESC;

-- 6. COMPLEMENTO HALLAZGO 4: Desglose de temas (tema) y sentimiento asociado
--    para el municipio seleccionado (Guadalajara, Jalisco: 14-039).
SELECT 
    COALESCE(n.tema, 'Sin clasificar') AS tema_noticia,
    COUNT(n.id_noticia) AS cantidad_noticias,
    ROUND(AVG(n.sentimiento)::numeric, 2) AS sentimiento_promedio,
    COUNT(CASE WHEN n.sentimiento < 0 THEN 1 END) AS notas_negativas
FROM noticia_geo ng
JOIN noticia n ON ng.id_noticia = n.id_noticia
WHERE LPAD(TRIM(ng.cve_ent), 2, '0') = '14' -- Guadalajara, Jalisco
  AND LPAD(TRIM(ng.cve_mun), 3, '0') = '039'
GROUP BY n.tema
ORDER BY cantidad_noticias DESC;