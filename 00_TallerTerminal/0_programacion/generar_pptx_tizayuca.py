# Tizayuca — Generador de PPTX desde JSON
# Ejecutar en Google Colab

# ─── 1. INSTALAR DEPENDENCIAS ────────────────────────────────
!pip install python-pptx requests -q

# ─── 2. CLONAR O DESCARGAR EL JSON DESDE GITHUB ──────────────
import requests, json

GITHUB_RAW = (
    "https://raw.githubusercontent.com/"
    "guillermojhoel2718-code/Taller-Terminal-ESIA/main/"
    "00_TallerTerminal/01_Investigacion/Datos/Municipios/02_Tizayuca.json"
)

response = requests.get(GITHUB_RAW)
data = response.json()
print("✅ JSON cargado:", data["municipio"], data["estado"])

# ─── 3. CONFIGURACIÓN DE SLIDES ──────────────────────────────
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# Paleta del proyecto (Industrial Organic)
COLOR_FONDO   = RGBColor(0x1A, 0x1A, 0x1A)   # fondo oscuro
COLOR_MUSGO   = RGBColor(0x4A, 0x7C, 0x59)   # Tizayuca
COLOR_ARENA   = RGBColor(0xF5, 0xF0, 0xE8)   # texto claro
COLOR_BLANCO  = RGBColor(0xFF, 0xFF, 0xFF)

W = Inches(13.33)   # widescreen 16:9
H = Inches(7.5)

prs = Presentation()
prs.slide_width  = W
prs.slide_height = H

BLANK = prs.slide_layouts[6]  # layout completamente en blanco

# ─── HELPER: fondo oscuro ────────────────────────────────────
def fondo_oscuro(slide):
    from pptx.util import Pt
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_FONDO

# ─── HELPER: agregar caja de texto ───────────────────────────
def add_text(slide, text, left, top, width, height,
             size=20, bold=False, color=COLOR_ARENA,
             align=PP_ALIGN.LEFT, italic=False):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txBox

# ─── HELPER: barra de acento lateral ─────────────────────────
def barra_musgo(slide, top=Inches(1.8), height=Inches(4.5)):
    rect = slide.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.RECTANGLE
        Inches(0.3), top, Inches(0.08), height
    )
    rect.fill.solid()
    rect.fill.fore_color.rgb = COLOR_MUSGO
    rect.line.fill.background()

# ════════════════════════════════════════════════════════════
# SLIDE 1 — PORTADA
# ════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
fondo_oscuro(slide)

# Acento superior verde
rect = slide.shapes.add_shape(1, 0, 0, W, Inches(0.08))
rect.fill.solid(); rect.fill.fore_color.rgb = COLOR_MUSGO
rect.line.fill.background()

add_text(slide, "TIZAYUCA, HIDALGO",
         Inches(1), Inches(1.5), Inches(11), Inches(1.2),
         size=44, bold=True, color=COLOR_MUSGO, align=PP_ALIGN.CENTER)

add_text(slide, "Centro de Teletrabajo y Aprendizaje Digital",
         Inches(1), Inches(2.9), Inches(11), Inches(0.8),
         size=24, color=COLOR_ARENA, align=PP_ALIGN.CENTER)

add_text(slide, "Protocolo de Investigación — Unidad I",
         Inches(1), Inches(3.7), Inches(11), Inches(0.6),
         size=16, color=COLOR_ARENA, align=PP_ALIGN.CENTER, italic=True)

add_text(slide, f"Población: {data['poblacion']:,} hab  ·  "
                f"Superficie: {data['superficie_km2']} km²  ·  "
                f"Densidad: {data['densidad_hab_km2']:,} hab/km²",
         Inches(1), Inches(5.0), Inches(11), Inches(0.6),
         size=14, color=RGBColor(0xAA, 0xAA, 0xAA), align=PP_ALIGN.CENTER)

add_text(slide, "Ingeniería Arquitectónica — ESIA Tecamachalco · IPN",
         Inches(1), Inches(6.2), Inches(11), Inches(0.5),
         size=12, color=RGBColor(0x88, 0x88, 0x88), align=PP_ALIGN.CENTER)

# ════════════════════════════════════════════════════════════
# SLIDE 2 — LOCALIZACIÓN GEOGRÁFICA
# ════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
fondo_oscuro(slide)
barra_musgo(slide)

add_text(slide, "Localización Geográfica",
         Inches(0.6), Inches(0.3), Inches(12), Inches(0.7),
         size=28, bold=True, color=COLOR_MUSGO)

reg = data.get("region_geografica", {})
coord = data.get("coordenadas", {})
col = data.get("colindancias", {})

items_loc = [
    f"📍  República → Eje Neovolcánico → Hidalgo → Región 6 Tizayuca → ZMVM (nodo norte)",
    f"🗺️  Centroide: {coord.get('centroide_lat','')} / {coord.get('centroide_lon','')}",
    f"📏  Superficie: {data['superficie_km2']} km²  ·  Altitud: {coord.get('altitud_oficial_msnm','')} msnm",
    f"↔️  Distancia CDMX: {data['distancia_azcapo_km']} km (MEX-85D)",
    f"🔵  Único municipio hidalguense integrado formalmente a la ZMVM",
    f"N: {col.get('norte','')}",
    f"S: {col.get('sur','')}",
    f"E: {col.get('este','')}  ·  O: {col.get('oeste','')}",
]

for i, item in enumerate(items_loc):
    add_text(slide, item,
             Inches(0.6), Inches(1.3 + i*0.72), Inches(12), Inches(0.65),
             size=15, color=COLOR_ARENA)

# ════════════════════════════════════════════════════════════
# SLIDE 3 — MEDIO FÍSICO
# ════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
fondo_oscuro(slide)
barra_musgo(slide)

add_text(slide, "Medio Físico",
         Inches(0.6), Inches(0.3), Inches(12), Inches(0.7),
         size=28, bold=True, color=COLOR_MUSGO)

geo = data.get("geologia", {})
eda = data.get("edafologia", {})
cli = data.get("clima", {})
veg = data.get("vegetacion_fauna", {})

items_fis = [
    f"🏔  Topografía: {data.get('topografia','')}",
    f"🪨  Geología: {geo.get('roca_dominante','')} · Período: {geo.get('periodo_principal','')}",
    f"🌱  Edafología: {eda.get('suelo_dominante','')}",
    f"   Aptitud constructiva: {eda.get('aptitud_constructiva','')[:80]}…",
    f"🌡  Clima: {cli.get('clasificacion_koppen','')}",
    f"   Temp. media {cli.get('temp_media_anual_c','')}°C · Precip. {cli.get('precipitacion_media_mm','')}",
    f"🌿  Vegetación original: {veg.get('vegetacion_original','')}",
    f"   Estado actual: sin vegetación nativa conservada (100% uso no forestal)",
]

for i, item in enumerate(items_fis):
    add_text(slide, item,
             Inches(0.6), Inches(1.2 + i*0.68), Inches(12), Inches(0.62),
             size=14, color=COLOR_ARENA)

# ════════════════════════════════════════════════════════════
# SLIDE 4 — DATOS SOCIODEMOGRÁFICOS
# ════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
fondo_oscuro(slide)
barra_musgo(slide)

add_text(slide, "Datos Sociodemográficos",
         Inches(0.6), Inches(0.3), Inches(12), Inches(0.7),
         size=28, bold=True, color=COLOR_MUSGO)

items_soc = [
    (f"Población total 2020",     f"{data['poblacion']:,} hab"),
    (f"Crecimiento intercensal",  "+72.7% (2010–2020)"),
    (f"Densidad",                 f"{data['densidad_hab_km2']:,} hab/km²"),
    (f"Viviendas habitadas",      f"{data['viviendas_habitadas']:,}"),
    (f"Ocupantes / vivienda",     f"{data['ocupantes_vivienda']}"),
    (f"Pobreza total",            f"{data['pobreza_pct']}%"),
    (f"Pobreza extrema",          f"{data['pobreza_extrema_pct']}%"),
    (f"Rezago educativo",         f"{data['rezago_educativo_pct']}%"),
    (f"GINI",                     "0.30"),
]

for i, (label, val) in enumerate(items_soc):
    col_l = Inches(0.6) if i < 5 else Inches(6.8)
    top   = Inches(1.2 + (i % 5) * 1.0)
    add_text(slide, label, col_l, top, Inches(3.2), Inches(0.4),
             size=13, color=RGBColor(0xAA, 0xAA, 0xAA))
    add_text(slide, val, col_l, top + Inches(0.38), Inches(3.2), Inches(0.5),
             size=22, bold=True, color=COLOR_MUSGO)

# ════════════════════════════════════════════════════════════
# SLIDE 5 — SERVICIOS BÁSICOS
# ════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
fondo_oscuro(slide)
barra_musgo(slide)

add_text(slide, "Servicios Básicos",
         Inches(0.6), Inches(0.3), Inches(12), Inches(0.7),
         size=28, bold=True, color=COLOR_MUSGO)

servicios = [
    ("💧 Agua potable",      f"{data['agua_pct']}%"),
    ("🚿 Drenaje",           f"{data['drenaje_pct']}%"),
    ("⚡ Electricidad",      f"{data['electricidad_pct']}%"),
    ("🌐 Internet",          f"{data['internet_pct']}%"),
    ("💻 Computadora",       f"{data['computadora_pct']}%"),
]

for i, (label, val) in enumerate(servicios):
    left = Inches(0.6 + (i % 3) * 4.1)
    top  = Inches(1.6 + (i // 3) * 2.5)
    add_text(slide, val,   left, top,            Inches(3.8), Inches(1.2),
             size=42, bold=True, color=COLOR_MUSGO, align=PP_ALIGN.CENTER)
    add_text(slide, label, left, top+Inches(1.1), Inches(3.8), Inches(0.5),
             size=14, color=COLOR_ARENA, align=PP_ALIGN.CENTER)

# ════════════════════════════════════════════════════════════
# SLIDE 6 — HIDROGRAFÍA Y RIESGOS
# ════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
fondo_oscuro(slide)
barra_musgo(slide)

add_text(slide, "Hidrografía y Riesgos Naturales",
         Inches(0.6), Inches(0.3), Inches(12), Inches(0.7),
         size=28, bold=True, color=COLOR_MUSGO)

rie = data.get("riesgos_naturales", {})

items_hid = [
    f"💧  {data.get('hidrografia','')}",
    "",
    f"⚠️  Riesgos:",
    f"   • Subsidencia: {rie.get('subsidencia','')}",
    f"   • Sismicidad: {rie.get('sismicidad','')}",
    "",
    f"📋  Fuente: {rie.get('fuente_riesgos','')}",
]

for i, item in enumerate(items_hid):
    add_text(slide, item,
             Inches(0.6), Inches(1.3 + i*0.78), Inches(12), Inches(0.72),
             size=15, color=COLOR_ARENA)

# ════════════════════════════════════════════════════════════
# SLIDE 7 — DÉFICIT Y JUSTIFICACIÓN
# ════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
fondo_oscuro(slide)
barra_musgo(slide)

add_text(slide, "Déficit Identificado",
         Inches(0.6), Inches(0.3), Inches(12), Inches(0.7),
         size=28, bold=True, color=COLOR_MUSGO)

add_text(slide, data.get("deficit_principal", ""),
         Inches(0.6), Inches(1.3), Inches(12), Inches(1.0),
         size=18, color=COLOR_ARENA)

add_text(slide, "Datos [PENDIENTE] — continuar recolección:",
         Inches(0.6), Inches(2.5), Inches(12), Inches(0.5),
         size=14, color=RGBColor(0xFF, 0xCC, 0x00), bold=True)

pendientes = [k for k,v in data.items() if v == "[PENDIENTE]"]
add_text(slide, "  ·  ".join(pendientes),
         Inches(0.6), Inches(3.1), Inches(12), Inches(2.0),
         size=12, color=RGBColor(0x88, 0x88, 0x88))

# ─── EXPORTAR ────────────────────────────────────────────────
OUTPUT = "/content/Tizayuca_Unidad1.pptx"
prs.save(OUTPUT)
print(f"\n✅  Presentación generada: {OUTPUT}")

# Descargar automáticamente en Colab
from google.colab import files
files.download(OUTPUT)
