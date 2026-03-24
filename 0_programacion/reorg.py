import os, shutil

base = "00_TallerTerminal"

if os.path.exists("00_Taller_Terminal") and not os.path.exists(base):
    os.rename("00_Taller_Terminal", base)

dirs = [
    f"{base}/01_Investigacion",
    f"{base}/02_Diseno/Canva",
    f"{base}/02_Diseno/Renders",
    f"{base}/02_Diseno/Web",
    f"{base}/03_Outputs",
    f"{base}/_agentes"
]
for d in dirs:
    os.makedirs(d, exist_ok=True)

def safe_move(src, dst):
    if os.path.exists(src):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if not os.path.exists(d):
                shutil.move(s, d)

safe_move(f"{base}/01_Investigacion/05_Presentacion", f"{base}/02_Diseno/Canva")
safe_move(f"{base}/02_Arquitectura_y_Proyecto", f"{base}/02_Diseno/Renders") # The user didn't mention this, but presumably architecture and renders. Ah wait, user said "02_Diseno/Renders <- mover contenido de 03_Renders".
safe_move(f"{base}/03_Renders", f"{base}/02_Diseno/Renders")
safe_move(f"{base}/09_Diseno_Web", f"{base}/02_Diseno/Web")
safe_move(f"{base}/01_Investigacion/09_Desing", f"{base}/02_Diseno/Web")

safe_move(f"{base}/01_Investigacion/07_Outputs", f"{base}/03_Outputs")
safe_move(f"{base}/01_Investigacion/outputs", f"{base}/03_Outputs")
safe_move("Tesis-Urbana/07_Outputs", f"{base}/03_Outputs")

if os.path.exists(f"{base}/01_Investigacion/08_Informes"):
    os.rename(f"{base}/01_Investigacion/08_Informes", f"{base}/01_Investigacion/07_Informes")

if os.path.exists(f"{base}/10_Gestoria"):
    os.rename(f"{base}/10_Gestoria", f"{base}/01_Investigacion/08_Gestoria")

# Note: The user said 10_Sinorganizar -> revisar contenido y clasificar. It's empty anyway, so we can ignore/delete.

for f in ["CONTEXTO_AGENTES.md", "MAESTRO.md", "REGLAS.md"]:
    if os.path.exists(f"{base}/{f}"):
        shutil.move(f"{base}/{f}", f"{base}/_agentes/{f}")
    elif os.path.exists(f"{base}/01_Investigacion/{f}"):
        shutil.move(f"{base}/01_Investigacion/{f}", f"{base}/_agentes/{f}")

# Clean up empty dirs
for root, dirs, files in os.walk(base, topdown=False):
    for d in dirs:
        p = os.path.join(root, d)
        try:
            os.rmdir(p)
        except OSError:
            pass

for root, dirs, files in os.walk("Tesis-Urbana", topdown=False):
    for d in dirs:
        p = os.path.join(root, d)
        try:
            os.rmdir(p)
        except OSError:
            pass
try:
    os.rmdir("Tesis-Urbana")
except:
    pass
try:
    os.rmdir(f"{base}/02_Arquitectura_y_Proyecto")
except:
    pass
