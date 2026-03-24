---
name: canva-connect
description: Editar la presentación de Canva del proyecto usando la Canva Connect API. Usar cuando se solicite actualizar slides, cambiar texto en la presentación, aplicar cambios del asesor a diapositivas, o sincronizar datos nuevos en el diseño. Solo edita texto — no modifica layouts ni estructura visual.
---

# Canva Connect API

Edita la presentación activa del proyecto usando la API de Canva.

## Credenciales

Leer de `/config.env`:
```
CANVA_CLIENT_ID
CANVA_ACCESS_TOKEN
```

## Diseño activo

Leer de `CONTEXTO.md`: campo `"Diseño activo"`

## Paleta de colores

Leer de `CONTEXTO.md`: sección `"Paleta"`

> ⚠️ NUNCA usar `#` en los valores hex al pasar colores a la API.
> Ejemplo correcto: `FF5733` — incorrecto: `#FF5733`

## Flujo de edición

1. Leer diseño activo desde `CONTEXTO.md`
2. Verificar credenciales en `/config.env`
3. Identificar el slide y campo a modificar
4. Mostrar al usuario: slide + campo + valor nuevo
5. PAUSA — esperar confirmación
6. Ejecutar máximo 20 operaciones por transacción
7. Reportar resultado al terminar

## Reglas

- Solo editar texto — no cambiar layouts ni estructura
- PAUSA obligatoria antes de cualquier escritura
- Máximo 20 operaciones por transacción
- Si falla la autenticación → reportar error sin reintentar
