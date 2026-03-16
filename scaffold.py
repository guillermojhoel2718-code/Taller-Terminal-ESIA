import os

base_dir = r"f:\ESIA 10MO SEMESTRE\Investigacion\Tesis-Urbana"

folders = [
    "01_Rubrica",
    "02_Datos/Municipios",
    "02_Datos/Tablas",
    "02_Datos/Mapas",
    "03_Referencias/Normatividad",
    "03_Referencias/Estadisticas",
    "03_Referencias/Analogos",
    "03_Referencias/MarcoTeorico",
    "04_Textos/Unidad_I",
    "04_Textos/Unidad_II",
    "04_Textos/Unidad_III",
    "04_Textos/Borradores",
    "05_Presentacion/Assets",
    "05_Presentacion/Versiones",
    "06_Reportes",
    "07_Outputs"
]

for folder in folders:
    os.makedirs(os.path.join(base_dir, folder), exist_ok=True)

readme_content = {
    "01_Rubrica": "Coloca aquí el PDF de Taller Terminal\n\n- Qué tipo de archivos van ahí: Documentos de evaluación y rúbricas del Taller.\n- Cómo nombrar: rúbricas oficiales (ej. Terminal_1_26-2.pdf)\n- Quién es responsable: El usuario y el agente de revisión.",
    "02_Datos": "- Qué tipo de archivos van ahí: Archivos JSON de datos, tablas tabulares y mapas.\n- Cómo nombrar: Municipios: [clave]_[municipio].json (Ej: 01_Tultitlan.json)\n- Quién es responsable: Agente recolector de datos / Usuario.",
    "03_Referencias": "- Qué tipo de archivos van ahí: Normatividad, estadísticas, documentos de investigación.\n- Cómo nombrar: [categoria]_[autor]_[año].[ext] (Ej: PDU_Tultitlan_2022.pdf)\n- Quién es responsable: Agente investigador / Usuario.",
    "04_Textos": "- Qué tipo de archivos van ahí: Archivos markdown con el protocolo y marco teórico.\n- Cómo nombrar: [unidad]_[seccion]_v[numero].md (Ej: U1_demografia_v1.md)\n- Quién es responsable: Agente redactor.",
    "05_Presentacion": "- Qué tipo de archivos van ahí: Assets para presentaciones, historial PPTX, link a Canva.\n- Cómo nombrar: Tesis_Urbana_v[numero]_[fecha].pptx (Ej: Tesis_Urbana_v1_20260315.pptx)\n- Quién es responsable: Agente diseñador PPTX / Canva.",
    "06_Reportes": "- Qué tipo de archivos van ahí: Reportes automatizados sobre referencias, rúbricas y pendientes.\n- Cómo nombrar: reporte_[tipo].md\n- Quién es responsable: Agentes auditores.",
    "07_Outputs": "- Qué tipo de archivos van ahí: Versiones finales exportadas y entregables (PDFs, PPTX revisados).\n- Cómo nombrar: [Entregable]_Final_[Fecha].ext\n- Quién es responsable: Agente de exportación / Usuario."
}

for folder, text in readme_content.items():
    with open(os.path.join(base_dir, folder, "README.md"), "w", encoding="utf-8") as f:
        f.write("# " + folder + "\n" + text)

# Helper function to create empty files
def create_empty(path):
    with open(os.path.join(base_dir, path), "w", encoding="utf-8") as f:
        f.write("")

create_empty("03_Referencias/indice_refs.md")
create_empty("05_Presentacion/canva_link.txt")
create_empty("06_Reportes/reporte_rubrica.md")
create_empty("06_Reportes/reporte_apa.md")
create_empty("06_Reportes/reporte_pendientes.md")

maestro = """# Tesis — Centro de Teletrabajo y Aprendizaje Digital
**Alumno:** Guillermo Jhoel
**Programa:** Ingeniería Arquitectónica
**Unidad actual:** Unidad I — Protocolo de Investigación

## Municipios de estudio
(90,000–120,000 hab, zona norte CDMX)
- [ ] Municipio 1: [pendiente]
- [ ] Municipio 2: [pendiente]
- [ ] Municipio 3: [pendiente]
- [ ] Municipio 4: [pendiente]
- [ ] Municipio 5: [pendiente]

## Proyecto
Tipología: Centro de Teletrabajo y Aprendizaje Digital
Usuarios: Niños y estudiantes
Estética: Industrial Organic
Alcance: Unidad I completada

## Estado de avance
| Unidad | Sección | Estado |
|--------|---------|--------|
| I | Planteamiento | ⏳ En proceso |
| I | Localización | ⏳ En proceso |
| I | Medio físico | ⏳ En proceso |
| I | Marco normativo | ⏳ En proceso |
| I | Marco social | ⏳ En proceso |
| I | Déficit | ⏳ En proceso |

## Links importantes
- Canva: [ver 05_Presentacion/canva_link.txt]
- Datos: /02_Datos/Municipios/
- Última versión: /07_Outputs/
"""
with open(os.path.join(base_dir, "MAESTRO.md"), "w", encoding="utf-8") as f:
    f.write(maestro)

contexto = """# Contexto del Proyecto
Proyecto: Centro de Teletrabajo y Aprendizaje Digital
Usuarios: Niños y estudiantes zona norte CDMX
Estética: Industrial Organic Sketch

## Paleta de colores (NUNCA usar #)
Fondo oscuro: 1A1A1A
Fondo contenido: F5F0E8
Municipio 1: C8A96E (ocre)
Municipio 2: 4A7C59 (musgo)
Municipio 3: D4441C (terracota)
Municipio 4: 6B8FA3 (acero)
Municipio 5: 8B6914 (bronce)

## Fuentes válidas
- INEGI Censo 2020
- CONEVAL 2020
- SEDUI EdoMéx
- PDU municipales oficiales
- Data México (Secretaría de Economía)

## Canva
Client ID: OC-AZzzhACvOFDv
Diseño base: DAHEDbMITxc

## Reglas globales
- Marcar datos no encontrados como [PENDIENTE]
- Nunca inventar datos numéricos
- Citas en formato APA 7 siempre
- Pausar y reportar antes de cada etapa
"""
with open(os.path.join(base_dir, "CONTEXTO_AGENTES.md"), "w", encoding="utf-8") as f:
    f.write(contexto)

print("Scaffolding complete.")
