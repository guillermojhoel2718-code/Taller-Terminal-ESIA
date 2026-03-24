---
name: busqueda-urbana
description: Generar prompts optimizados para buscar datos urbanos, estadísticos y normativos en Perplexity. Usar cuando se necesite información de municipios, indicadores INEGI/CONEVAL, topografía, hidrografía, normativa urbana o cualquier dato que requiera fuente oficial externa. KUKLES activa esta skill y entrega el prompt al usuario para que lo ejecute manualmente en Perplexity.
---

# Búsqueda con Perplexity

Esta skill genera prompts listos para copiar y pegar en Perplexity. El agente **no ejecuta la búsqueda** — la ejecuta el usuario.

## Flujo

1. Recibe: tema + municipio/estado + tipo de dato
2. Genera prompt optimizado (ver plantilla)
3. Muestra prompt en bloque copiable
4. Espera a que el usuario pegue el resultado
5. Procesa y estructura el dato recibido

## Plantilla de prompt para Perplexity

```
Actúa como analista urbano.
Fuentes: INEGI Censo 2020, CONEVAL 2020, [FUENTE_ESPECIFICA].
Municipio: [MUNICIPIO], [ESTADO]
Busca: [DATO_ESPECIFICO]
Entrega: solo el dato + fuente + URL.
Sin introducción ni conclusión.
```

## Calidad del dato

| Símbolo | Significado |
|---------|-------------|
| ✅ confirmado | fuente oficial directa |
| ⚠️ estimado | extrapolado o indirecto |
| ❌ no encontrado | marcar [PENDIENTE] |

## Reglas

- Siempre indicar la fuente y año del dato
- Si el dato no se encuentra → marcar `[PENDIENTE]` en MAESTRO.md
- No inventar ni estimar sin advertir al usuario
