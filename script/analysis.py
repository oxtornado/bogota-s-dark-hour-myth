import json
import pandas as pd

# -------------------------------------------------------------------------
# 1. CARGA REMOTA DE DATOS
# -------------------------------------------------------------------------
print("Conectando y descargando datos remotos de Datos.gov.co...")

# Opción A: Lectura remota del archivo CSV completo directamente desde la URL
URL_CSV = "https://www.datos.gov.co/api/views/4rxi-8m8d/rows.csv?accessType=DOWNLOAD"

try:
    # Cargar en memoria (sin guardar en disco local)
    df = pd.read_csv(URL_CSV, low_memory=False)
    print(f"Datos cargados exitosamente. Total de registros nacionales: {len(df)}")
except Exception as e:
    print(f"Error al conectar con la API remota: {e}")
    exit()

# -------------------------------------------------------------------------
# 2. FILTRADO GEOGRÁFICO Y LIMPIEZA DE DATOS (ETL)
# -------------------------------------------------------------------------
print("Ejecutando limpieza y filtrado para Bogotá D.C...")

# Estandarizar nombres de columnas a mayúsculas para evitar diferencias
df.columns = [col.upper().strip() for col in df.columns]

# Identificar columnas relevantes (varían según actualización del dataset)
col_municipio = [c for c in df.columns if "MUNICIPIO" in c or "CIUDAD" in c][0]
col_hora = [c for c in df.columns if "HORA" in c][0]
col_localidad = [c for c in df.columns if "LOCALIDAD" in c or "BARRIO" in c][0]
col_armas = [c for c in df.columns if "ARMA" in c or "MODALIDAD" in c][0]

# Filtrar únicamente los eventos registrados en Bogotá D.C.
df_bogota = df[
    df[col_municipio].astype(str).str.contains("BOGOTÁ|BOGOTA", case=False, na=False)
].copy()

# Eliminar filas con localidad vacía o no especificada
df_bogota = df_bogota[
    ~df_bogota[col_localidad]
    .astype(str)
    .str.contains("SIN INFORMACION|NO REPORTA", case=False, na=False)
]

# -------------------------------------------------------------------------
# 3. TRANSFORMACIÓN Y CATEGORIZACIÓN TEMPORAL
# -------------------------------------------------------------------------
# Extraer la hora numérica del campo de texto/datetime
def extraer_hora(val):
    try:
        val_str = str(val).strip()
        if ":" in val_str:
            return int(val_str.split(":")[0])
        return int(float(val_str))
    except:
        return None

df_bogota["HORA_NUM"] = df_bogota[col_hora].apply(extraer_hora)
df_bogota = df_bogota.dropna(subset=["HORA_NUM"])

# Clasificación en las 4 franjas horarias analíticas
def clasificar_franja(hora):
    if 0 <= hora < 6:
        return "Madrugada"
    elif 6 <= hora < 12:
        return "Mañana"
    elif 12 <= hora < 18:
        return "Tarde"
    else:
        return "Noche"

df_bogota["FRANJA_HORARIA"] = df_bogota["HORA_NUM"].apply(clasificar_franja)

# -------------------------------------------------------------------------
# 4. AGREGACIÓN ESTADÍSTICA PARA LA WEB
# -------------------------------------------------------------------------
print("Calculando distribuciones de frecuencia relativas (%) ...")

# A. Distribución general por franja horaria (%)
dist_franja_general = (
    df_bogota["FRANJA_HORARIA"].value_counts(normalize=True) * 100
).round(1).to_dict()

# B. Distribución por localidad y franja horaria
dist_localidades = {}
localidades_principales = df_bogota[col_localidad].value_counts().head(10).index

for loc in localidades_principales:
    df_loc = df_bogota[df_bogota[col_localidad] == loc]
    dist_franja = (
        (df_loc["FRANJA_HORARIA"].value_counts(normalize=True) * 100)
        .round(1)
        .to_dict()
    )
    dist_localidades[loc] = dist_franja

# ESTRUCTURA DE SALIDA JSON
output_data = {
    "distribucion_general": dist_franja_general,
    "localidades": dist_localidades,
    "total_registros_analizados": len(df_bogota),
}

# Save JSON file for web app consumption
with open("data_bogota.json", "w", encoding="utf-8") as f:
    json.dump(output_data, f, ensure_ascii=False, indent=4)

print("¡Proceso finalizado! Archivo 'data_bogota.json' generado correctamente.")