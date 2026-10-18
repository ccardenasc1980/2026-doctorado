"""
05_indices_madurez.py
Calcula los índices de madurez de gestión de portafolios (IGP) y de madurez digital (IMD)
por organización, y genera las tablas para el Capítulo III (OE3 / HE3).

Uso:
    python 03_SCRIPTS/05_indices_madurez.py --sim   # con datos simulados
    python 03_SCRIPTS/05_indices_madurez.py         # con datos reales (02_DATOS_PROCESADOS)
Salida (04_RESULTADOS/tablas/):
    [SIM_]tabla_indices_por_formalidad.csv
    [SIM_]tabla_indices_por_zona.csv      (zonas con < 5 organizaciones se agrupan en "Otras")
    [SIM_]correlacion_IGP_IMD.txt
"""
import sys
from pathlib import Path

import pandas as pd

MIN_CELDA = 5  # regla de protección: no publicar celdas con menos de 5 organizaciones

RAIZ = Path(__file__).resolve().parents[1]
SIM = "--sim" in sys.argv
prefijo = "SIM_" if SIM else ""
entrada = (RAIZ / "08_DATOS_SIMULADOS" / "SIM_organizaciones.csv" if SIM
           else RAIZ / "02_DATOS_PROCESADOS" / "organizaciones.csv")
salida = RAIZ / "04_RESULTADOS" / "tablas"
salida.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(entrada)
GP = [c for c in df.columns if c.startswith("gp_")]
MD = [c for c in df.columns if c.startswith("md_")]

# Índices en escala 0-100: (promedio Likert - 1) / 4 * 100
df["IGP"] = ((df[GP].mean(axis=1) - 1) / 4 * 100).round(1)
df["IMD"] = ((df[MD].mean(axis=1) - 1) / 4 * 100).round(1)


def resumen(grupo: str) -> pd.DataFrame:
    t = (df.groupby(grupo)
           .agg(n=("org_id", "count"), IGP_media=("IGP", "mean"), IMD_media=("IMD", "mean"))
           .round(1)
           .reset_index())
    pequenas = t["n"] < MIN_CELDA
    if pequenas.any():
        # Agrupar celdas pequeñas para evitar reidentificación
        otras = df[df[grupo].isin(t.loc[pequenas, grupo])]
        fila = pd.DataFrame({grupo: ["Otras (agrupadas)"], "n": [len(otras)],
                             "IGP_media": [round(otras["IGP"].mean(), 1)],
                             "IMD_media": [round(otras["IMD"].mean(), 1)]})
        t = pd.concat([t[~pequenas], fila], ignore_index=True)
    return t


resumen("formalidad").to_csv(salida / f"{prefijo}tabla_indices_por_formalidad.csv", index=False)
resumen("zona_produccion").to_csv(salida / f"{prefijo}tabla_indices_por_zona.csv", index=False)

rho = df["IGP"].corr(df["IMD"], method="spearman")
texto = (f"{'DATOS SIMULADOS - NO CITAR' if SIM else 'Datos reales'}\n"
         f"n = {len(df)}\n"
         f"Correlación de Spearman IGP-IMD: rho = {rho:.3f}\n")
(salida / f"{prefijo}correlacion_IGP_IMD.txt").write_text(texto, encoding="utf-8")
print(texto)
print(f"Tablas guardadas en {salida}")
