# Gestión de portafolios de proyectos de innovación con enfoque de cuádruple hélice para la transformación digital de la maricultura en Piura

Repositorio de datos, código y documentación de la tesis doctoral de **Carlos Alberto Cárdenas Cruz**
Doctorado en Administración con mención en Tecnología — Escuela de Posgrado, Universidad Nacional de Ingeniería (UNI)

> **Estado:** plantilla inicial (octubre 2026). Los únicos datos incluidos son **SIMULADOS** (carpeta `08_DATOS_SIMULADOS`, prefijo `SIM_`). No representan a ninguna organización real y no deben citarse como resultados.

---

## Estructura

| Carpeta | Contenido | ¿En GitHub? |
|---|---|---|
| `00_ADMIN/` | Autorizaciones (Anexo XIV, Guía N.° 2 UNI), consentimientos | No (protegida) |
| `01_DATOS_CRUDOS/` | Catastro acuícola, padrón DIREPRO, expedientes, encuestas, entrevistas | No (protegida) |
| `02_DATOS_PROCESADOS/` | Bases limpias y **anonimizadas** (ORG-001, PRY-001…) | Sí, excepto la tabla de llaves |
| `03_SCRIPTS/` | Código, numerado en el orden de ejecución | Sí |
| `04_RESULTADOS/` | Tablas y figuras que van a la tesis | Sí |
| `05_DOCUMENTACION/` | Diccionario de datos, bitácora de decisiones, instrumentos | Sí |
| `06_TESIS/` | Plan de tesis, tesis, artículo | Sí |
| `07_BIBLIOGRAFIA/` | `referencias.bib`, PDFs de acceso abierto, registro de licencias | Sí, excepto `pdf_restringidos/` |
| `08_DATOS_SIMULADOS/` | Datos ficticios para probar el flujo | Sí (se eliminan antes de la versión final) |

## Flujo de datos

```
01_DATOS_CRUDOS ──► 03_SCRIPTS/01_limpieza ──► 02_DATOS_PROCESADOS ──► 03_SCRIPTS/0X_análisis ──► 04_RESULTADOS ──► 06_TESIS
```

Regla: **ningún dato se corrige a mano.** Todo cambio entre la capa cruda y los resultados queda en un script.

## Cómo reproducir (con datos simulados)

Requisitos: Python 3.10 o superior.

```bash
pip install -r requirements.txt
python 03_SCRIPTS/00_generar_datos_SIM.py     # crea 08_DATOS_SIMULADOS/SIM_*.csv
python 03_SCRIPTS/05_indices_madurez.py --sim # calcula índices y exporta tablas
```

Las salidas se guardan en `04_RESULTADOS/tablas/` con prefijo `SIM_`.

## Protección de datos

- Los datos que identifican a personas u organizaciones (RUC, nombres, ubicación exacta, condición de informalidad) **no se publican**.
- Solo se publican cifras agregadas, con un mínimo de **5 casos por celda**.
- La correspondencia código ↔ identidad (`tabla_llaves.csv`) se guarda solo en un disco cifrado del autor.

## Cita

Cárdenas Cruz, C. A. (2026). *Datos y código de la tesis doctoral "Gestión de portafolios de proyectos de innovación con enfoque de cuádruple hélice para la transformación digital de la maricultura en Piura"* [Repositorio]. GitHub. https://github.com/ccardenasc1980/2026-doctorado

(Se reemplazará por el DOI de Zenodo al publicar la primera versión.)

## Licencia

Pendiente de definir al hacer público el repositorio. Propuesta: MIT para el código y CC BY 4.0 para los datos agregados y la documentación.
