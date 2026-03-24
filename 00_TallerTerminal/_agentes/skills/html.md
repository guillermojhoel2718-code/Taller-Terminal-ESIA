---
name: sitio-web-interactivo
description: Crear y actualizar el sitio web HTML del análisis urbano. Usar cuando se necesite generar una nueva versión del sitio, aplicar correcciones del asesor, agregar secciones o modificar contenido visual. No cambiar estructura sin autorización explícita del usuario.
---

# Sitio Web Interactivo

Gestiona las versiones del sitio HTML de análisis urbano del proyecto.

## Convención de versiones

| Versión | Significado |
|---------|-------------|
| v1.0 | Entrega inicial |
| v1.x | Correcciones del asesor (sin cambio estructural) |
| v2.0 | Cambios estructurales aprobados |

## Flujo al actualizar

1. Leer la versión actual desde `analisis-urbano-v[n].html`
2. Aplicar los cambios solicitados
3. Incrementar el badge de versión en el nav
4. Agregar entrada al historial interno:
   ```
   ### v[n] — [fecha]
   - [cambio 1]
   - [cambio 2]
   ```
5. Guardar como nueva versión en la ruta correcta
6. PAUSA — confirmar con el usuario antes de reemplazar la versión anterior

## Ruta de archivos

```
/02_Diseno/Web/analisis-urbano-v[n].html
```

## Reglas

- NO cambiar estructura de secciones sin autorización explícita
- PAUSA obligatoria antes de sobrescribir cualquier versión
- Siempre documentar el cambio en el historial interno del HTML
