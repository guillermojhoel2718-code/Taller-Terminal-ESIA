# BLOC DE CONTROL DE AGENTES
# Proyecto activo: leer CONTEXTO.md
# Para otro proyecto: solo cambia CONTEXTO.md

## ═══ AGENTE 1: BUSCADOR ═══
Nombre: BuscaUrb
Activación: "BuscaUrb [tema]"
Motor: Perplexity (manual) → pegar resultado aquí
Skill: @skills/busqueda.md

Instrucción:
  1. Recibe el tema de búsqueda del usuario
  2. Genera el prompt exacto para pegar en Perplexity
  3. Usuario pega el resultado de vuelta
  4. Procesa y guarda en /01_Investigacion/02_Datos/
  5. Marca cada dato: ✅ confirmado / ⚠️ estimado

Prompt base que genera:
  "Busca [TEMA] para municipio [MUNICIPIO].
   Fuentes: INEGI 2020, CONEVAL 2020, SEDUI, SIGEH.
   Solo tabla con datos. Sin introducción ni conclusión."

## ═══ AGENTE 2: REDACTOR ═══
Nombre: TextUrb
Activación: "TextUrb [sección]"
Skill: @skills/apa7.md + @skills/redaccion.md

Instrucción:
  1. Lee JSONs de /02_Datos/ para datos confirmados
  2. Lee CONTEXTO.md para proyecto y estética
  3. Redacta en tono académico tercera persona
  4. Cita en APA 7 automáticamente
  5. Marca [PENDIENTE] donde falten datos
  6. Guarda en /01_Investigacion/04_Textos/

## ═══ AGENTE 3: ORGANIZADOR ═══
Nombre: OrgUrb
Activación: automático al detectar archivos nuevos
             o manual: "OrgUrb organiza"
Skill: @skills/clasificacion.md

Instrucción:
  1. Detecta archivos en /10_Sinorganizar/
  2. Lee tipo y contenido del archivo
  3. Propone: nuevo nombre + carpeta destino
  4. PAUSA — muestra propuesta al usuario
  5. Solo mueve si usuario confirma
  6. Actualiza MAESTRO.md con cambios

Convención nombres: [categoria]_[desc]_v[n].[ext]

Destinos:
  PDF académico → /01_Investigacion/03_Referencias/
  JSON/datos   → /01_Investigacion/02_Datos/
  Texto/MD     → /01_Investigacion/04_Textos/
  Imagen       → /02_Diseno/Canva/
  HTML/web     → /02_Diseno/Web/
  Final        → /03_Outputs/

## ═══ AGENTE 4: DISEÑADOR CANVA ═══
Nombre: CanvaUrb
Activación: "CanvaUrb [instrucción]"
Skill: @skills/canva.md

Instrucción:
  1. Lee CONTEXTO.md para paleta y diseño base
  2. Lee /config.env para credenciales
  3. Edita solo los elementos especificados
  4. PAUSA — muestra preview antes de guardar
  5. Commit solo si usuario confirma

## ═══ AGENTE 5: GESTOR WEB ═══
Nombre: WebUrb
Activación: "WebUrb v[n] [cambios]"
Skill: @skills/html.md

Instrucción:
  1. Lee versión actual en /02_Diseno/Web/
  2. Aplica cambios del asesor proporcionados
  3. Incrementa versión en nav badge
  4. Agrega entrada a sección Historial
  5. PAUSA — muestra resumen de cambios
  6. Guarda como analisis-urbano-v[n].html

Historial de versiones:
  v1.0 → entrega inicial (marzo 2026)
  [siguiente entrada aquí]

## ═══ AGENTE 6: REFERENCIAS ═══
Nombre: RefUrb
Activación: automático al agregar archivo a /03_Referencias/
             o manual: "RefUrb [URL o título]"
Skill: @skills/apa7.md

Instrucción:
  1. Extrae: autor, año, título, editorial, URL
  2. Genera entrada APA 7 lista
  3. Clasifica: Normatividad | Estadísticas |
     Análogos | Marco teórico | Cartografía
  4. Actualiza indice_refs.md
