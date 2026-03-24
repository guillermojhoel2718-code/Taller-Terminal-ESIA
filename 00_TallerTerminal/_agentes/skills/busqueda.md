# Skill: Búsqueda con Perplexity

## Flujo
1. Recibe tema del agente
2. Genera prompt optimizado para Perplexity
3. Usuario ejecuta en Perplexity normal (sin Computer)
4. Usuario pega resultado aquí
5. Agente procesa y estructura el dato

## Plantilla de prompt para Perplexity


Actúa como analista urbano.
Fuentes: INEGI Censo 2020, CONEVAL 2020,
[FUENTE_ESPECIFICA].
Municipio: [MUNICIPIO], [ESTADO]
Busca: [DATO_ESPECIFICO]
Entrega: solo el dato + fuente + URL.
Sin introducción ni conclusión.

## Calidad del dato
✅ confirmado = fuente oficial directa
⚠️ estimado = extrapolado o indirecto
❌ no encontrado = marcar [PENDIENTE]
