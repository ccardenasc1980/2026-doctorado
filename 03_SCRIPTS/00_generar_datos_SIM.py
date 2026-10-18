"""
00_generar_datos_SIM.py
Genera datos FICTICIOS para probar el flujo de la tesis.

ADVERTENCIA: estos datos NO representan organizaciones reales.
No deben citarse ni usarse como resultados. Se eliminan antes de la versión final.

Uso:
    python 03_SCRIPTS/00_generar_datos_SIM.py
Salida:
    08_DATOS_SIMULADOS/SIM_organizaciones.csv
    08_DATOS_SIMULADOS/SIM_proyectos.csv
    08_DATOS_SIMULADOS/SIM_red_actores.csv
"""
from pathlib import Path

import numpy as np
import pandas as pd

SEMILLA = 2026  # semilla fija: mismo resultado en cualquier computadora
rng = np.random.default_rng(SEMILLA)

RAIZ = Path(__file__).resolve().parents[1]
SALIDA = RAIZ / "08_DATOS_SIMULADOS"
SALIDA.mkdir(exist_ok=True)

ZONAS = ["Chulliyachi", "Matacaballo", "Las Delicias", "Constante", "Parachique",
         "Barrancos", "Vichayo", "Puerto Rico", "Nonura", "San Pedro"]
TIPOS = ["OSPA", "AMYPE", "AMYGE", "Empresa"]
MD = ["md_trazabilidad", "md_registro", "md_monitoreo", "md_interoperabilidad",
      "md_uso_datos", "md_capacidades", "md_continuidad"]
GP = ["gp_seleccion", "gp_priorizacion", "gp_gobernanza", "gp_beneficios"]


def likert(base: np.ndarray) -> np.ndarray:
    """Convierte un puntaje latente en escala 1-5."""
    return np.clip(np.round(base + rng.normal(0, 0.7, base.size)), 1, 5).astype(int)


# ---------- Organizaciones ----------
n = 160
tipo = rng.choice(TIPOS, n, p=[0.70, 0.20, 0.03, 0.07])
formal = rng.random(n) < np.where(tipo == "OSPA", 0.55, 0.90)
# Supuesto de simulación: más madurez de portafolio -> algo más de madurez digital
latente_gp = rng.normal(2.0, 0.6, n) + np.where(formal, 0.4, 0.0)
latente_md = 0.6 * latente_gp + rng.normal(0.6, 0.5, n)

org = pd.DataFrame({
    "org_id": [f"ORG-{i:03d}" for i in range(1, n + 1)],
    "zona_produccion": rng.choice(ZONAS, n),
    "provincia": "Sechura",
    "tipo_organizacion": tipo,
    "formalidad": np.where(formal, "Formal", "Informal"),
    "tiene_concesion": formal.astype(int),
    "area_ha": np.where(formal, rng.gamma(2.0, 5.0, n).round(1), 0.0),
    "n_socios": rng.integers(8, 60, n),
})
for c in GP:
    org[c] = likert(latente_gp)
for c in MD:
    org[c] = likert(latente_md)

# ---------- Proyectos ----------
m = 40
PROGRAMAS = ["PROCOMPITE", "ProInnóvate", "PNIPA", "FONDEMI", "Fospibay",
             "Cooperación", "Inversión pública"]
LINEAS = ["Semilla/hatchery", "Monitoreo", "Cultivo", "Procesamiento",
          "Comercialización", "Capacitación", "Economía circular"]
pry = pd.DataFrame({
    "pry_id": [f"PRY-{i:03d}" for i in range(1, m + 1)],
    "programa": rng.choice(PROGRAMAS, m),
    "anio": rng.integers(2018, 2027, m),
    "monto_soles": (rng.lognormal(12.5, 1.0, m)).round(-2),
    "helice_ejecutor": rng.choice(["Gobierno", "Academia", "Empresa", "Sociedad civil"],
                                  m, p=[0.45, 0.10, 0.30, 0.15]),
    "linea_tematica": rng.choice(LINEAS, m, p=[0.30, 0.15, 0.20, 0.10, 0.10, 0.10, 0.05]),
    "alineado_pna": (rng.random(m) < 0.55).astype(int),
})

# ---------- Red de actores ----------
actores = list(org["org_id"].sample(30, random_state=SEMILLA)) + [f"ACT-{i:03d}" for i in range(1, 16)]
k = 120
red = pd.DataFrame({
    "origen": rng.choice(actores, k),
    "destino": rng.choice(actores, k),
    "tipo_vinculo": rng.choice(["Financiamiento", "Información", "Técnico", "Comercial"], k),
    "intensidad": rng.integers(1, 4, k),
})
red = red[red["origen"] != red["destino"]].drop_duplicates(["origen", "destino"])

org.to_csv(SALIDA / "SIM_organizaciones.csv", index=False, encoding="utf-8")
pry.to_csv(SALIDA / "SIM_proyectos.csv", index=False, encoding="utf-8")
red.to_csv(SALIDA / "SIM_red_actores.csv", index=False, encoding="utf-8")
print(f"Datos SIMULADOS creados en {SALIDA}: {len(org)} organizaciones, "
      f"{len(pry)} proyectos, {len(red)} vínculos.")
