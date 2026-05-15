import pandas as pd
import re
from trazabilidad.dataframe import LogTrazabilidad


# ──────────────────────────────────────────────
# Constantes del pipeline
# ──────────────────────────────────────────────

COLUMNAS_ESPERADAS = [
    "CODIGO_FOLIO", "NOMBRE_FOLIO", "FECHA_FOLIO",
    "GENERO", "REGIMEN", "TIPO_PACIENTE",
    "CODIGO_INGRESO", "EDAD", "MUNICIPIO", "ZONA",
    "ETNIA", "NIVEL_SOCIOECONOMICO",
    "MES", "AÑO", "CIE10", "NOMBRE_DIAGNOSTICO", 
    "TIPO_DIAGNOSTICO","OCUPACION_PACIENTE",
    'FECHA_INGRESO', 'CODIGO_AREA', 'AREA'
]

COLUMNAS_EXCLUIDAS = [
    "OID", "HCNTIPHIS", "HCCODIGO", "HCNOMBRE"
    # Agrega aquí cualquier otra columna que el pipeline elimina
    # Si tienes la lista completa en depuracion_columnas.py, puedes importarla desde allí
]

FOLIOS_EXCLUIDOS = ["HC064W"]

FOLIOS_PEDIATRICOS = ["HC003W", "HC071W"]
FOLIOS_ADULTOS     = ["HC023W", "HC088W"]

PATRON_CIE10 = re.compile(r"^[A-Z][0-9]{2}(\.[0-9]{1,4})?[A-Z]?$")


# ──────────────────────────────────────────────
# Clase principal de validación
# ──────────────────────────────────────────────

class ResultadoValidacion:
    """Acumula los resultados de todas las validaciones."""

    def __init__(self):
        self.resultados: list[dict] = []

    def _registrar(self, nombre: str, aprobado: bool, detalle: str):
        estado = "✅ APROBADO" if aprobado else "❌ FALLIDO"
        self.resultados.append({
            "validacion": nombre,
            "estado":     estado,
            "detalle":    detalle
        })
        print(f"[VALIDACIÓN] {estado} — {nombre}: {detalle}")

    def aprobado(self, nombre: str, detalle: str):
        self._registrar(nombre, True, detalle)

    def fallido(self, nombre: str, detalle: str):
        self._registrar(nombre, False, detalle)

    def resumen(self) -> pd.DataFrame:
        return pd.DataFrame(self.resultados)

    def hay_fallos(self) -> bool:
        return any("FALLIDO" in r["estado"] for r in self.resultados)


# ──────────────────────────────────────────────
# Validaciones individuales
# ──────────────────────────────────────────────

def validar_columnas_esperadas(df_final: pd.DataFrame, rv: ResultadoValidacion):
    """Verifica que las 23 columnas definidas estén presentes con sus nombres exactos."""
    faltantes = [c for c in COLUMNAS_ESPERADAS if c not in df_final.columns]
    extras    = [c for c in df_final.columns if c not in COLUMNAS_ESPERADAS]

    if not faltantes and not extras:
        rv.aprobado(
            "Columnas esperadas",
            f"Las {len(COLUMNAS_ESPERADAS)} columnas están presentes y no hay extras."
        )
    else:
        detalle = ""
        if faltantes:
            detalle += f"Faltan: {faltantes}. "
        if extras:
            detalle += f"Columnas no esperadas: {extras}."
        rv.fallido("Columnas esperadas", detalle)


def validar_columnas_excluidas_ausentes(df_final: pd.DataFrame, rv: ResultadoValidacion):
    """Verifica que ninguna columna que debía eliminarse esté en el resultado."""
    presentes = [c for c in COLUMNAS_EXCLUIDAS if c in df_final.columns]

    if not presentes:
        rv.aprobado(
            "Columnas excluidas ausentes",
            "Ninguna columna eliminada por el pipeline está en el resultado."
        )
    else:
        rv.fallido(
            "Columnas excluidas ausentes",
            f"Columnas que debían eliminarse siguen presentes: {presentes}"
        )


def validar_folio_hc064w_ausente(df_final: pd.DataFrame, rv: ResultadoValidacion):
    """Verifica que el folio HC064W no exista en el resultado."""
    n = df_final[df_final["CODIGO_FOLIO"].isin(FOLIOS_EXCLUIDOS)].shape[0]

    if n == 0:
        rv.aprobado("Folio HC064W excluido", "No hay registros de HC064W en el resultado.")
    else:
        rv.fallido("Folio HC064W excluido", f"Se encontraron {n} registros de HC064W en el resultado.")


def validar_sin_duplicados(df_final: pd.DataFrame, rv: ResultadoValidacion):
    """
    Verifica que no exista ningún par de filas con la misma combinación
    (CODIGO_INGRESO, CIE10, NOMBRE_DIAGNOSTICO), que es la clave de duplicado del pipeline.
    """
    clave = ["CODIGO_INGRESO", "CIE10", "NOMBRE_DIAGNOSTICO"]
    cols_existentes = [c for c in clave if c in df_final.columns]

    if len(cols_existentes) < len(clave):
        rv.fallido(
            "Sin duplicados",
            f"No se pudo verificar: faltan columnas clave {[c for c in clave if c not in df_final.columns]}"
        )
        return

    duplicados = df_final[df_final.duplicated(subset=cols_existentes, keep=False)]
    n = len(duplicados)

    if n == 0:
        rv.aprobado("Sin duplicados", "No se encontraron duplicados según la clave del pipeline.")
    else:
        rv.fallido("Sin duplicados", f"Se encontraron {n} filas duplicadas según (CODIGO_INGRESO, CIE10, NOMBRE_DIAGNOSTICO).")


def validar_edad_en_folios(df_final: pd.DataFrame, rv: ResultadoValidacion):
    """
    Verifica que en folios pediátricos no haya pacientes con edad >= 18
    y que en folios de adultos no haya pacientes con edad < 18 (excluyendo nulos).
    """
    if "EDAD" not in df_final.columns or "CODIGO_FOLIO" not in df_final.columns:
        rv.fallido("Edad coherente por folio", "Faltan columnas EDAD o CODIGO_FOLIO.")
        return

    df_num = df_final.copy()
    df_num["EDAD"] = pd.to_numeric(df_num["EDAD"], errors="coerce")

    # Adultos en folio pediátrico
    mask_ped = df_num["CODIGO_FOLIO"].isin(FOLIOS_PEDIATRICOS)
    adultos_en_ped = df_num[mask_ped & (df_num["EDAD"] >= 18)]
    n_adultos = len(adultos_en_ped)

    # Menores en folio de adultos
    mask_adu = df_num["CODIGO_FOLIO"].isin(FOLIOS_ADULTOS)
    menores_en_adu = df_num[mask_adu & (df_num["EDAD"] < 18)]
    n_menores = len(menores_en_adu)

    if n_adultos == 0 and n_menores == 0:
        rv.aprobado(
            "Edad coherente por folio",
            "Ningún paciente está en un folio incorrecto según su edad."
        )
    else:
        detalle = ""
        if n_adultos:
            detalle += f"{n_adultos} adultos (edad ≥ 18) en folios pediátricos. "
        if n_menores:
            detalle += f"{n_menores} menores (edad < 18) en folios de adultos."
        rv.fallido("Edad coherente por folio", detalle)


def validar_conflictos_cruzados(df_final: pd.DataFrame, rv: ResultadoValidacion):
    """
    Verifica que ningún CODIGO_INGRESO aparezca simultáneamente
    en el folio de adultos y el pediátrico del mismo grupo (A o B).
    """
    if "CODIGO_INGRESO" not in df_final.columns or "CODIGO_FOLIO" not in df_final.columns:
        rv.fallido("Sin conflictos cruzados", "Faltan columnas CODIGO_INGRESO o CODIGO_FOLIO.")
        return

    conflictos_totales = 0

    for adultos, pediatrico, grupo in [
        ("HC023W", "HC003W", "A"),
        ("HC088W", "HC071W", "B"),
    ]:
        ingresos_adu = set(df_final[df_final["CODIGO_FOLIO"] == adultos]["CODIGO_INGRESO"])
        ingresos_ped = set(df_final[df_final["CODIGO_FOLIO"] == pediatrico]["CODIGO_INGRESO"])
        conflicto = ingresos_adu & ingresos_ped
        conflictos_totales += len(conflicto)

    if conflictos_totales == 0:
        rv.aprobado(
            "Sin conflictos cruzados",
            "Ningún código de ingreso aparece en adultos y pediátrico del mismo grupo."
        )
    else:
        rv.fallido(
            "Sin conflictos cruzados",
            f"Se encontraron {conflictos_totales} códigos de ingreso con conflicto entre folios de egreso."
        )


""" def validar_conformidad_cie10(df_final: pd.DataFrame, rv: ResultadoValidacion):
  
    Verifica que los valores de CIE10 cumplan el patrón estándar.
    Reporta cuántos no cumplen, sin fallar por valores nulos.
   
    if "CIE10" not in df_final.columns:
        rv.fallido("Conformidad CIE-10", "Columna CIE10 no encontrada.")
        return

    serie = df_final["CIE10"].dropna().astype(str).str.strip()
    invalidos = serie[~serie.apply(lambda x: bool(PATRON_CIE10.match(x)))]
    n = len(invalidos)
    total = len(serie)

    if n == 0:
        rv.aprobado("Conformidad CIE-10", f"Los {total} códigos CIE-10 cumplen el patrón estándar.")
    else:
        pct = round(n / total * 100, 2)
        rv.fallido(
            "Conformidad CIE-10",
            f"{n} de {total} códigos ({pct}%) no cumplen el patrón CIE-10. "
            f"Ejemplos: {invalidos.unique()[:5].tolist()}"
        )
 """

def validar_conservacion_matematica(
    df_original: pd.DataFrame,
    df_final: pd.DataFrame,
    log: LogTrazabilidad,
    rv: ResultadoValidacion
):
    """
    Verifica que: filas_originales == filas_limpias + filas_eliminadas_en_trazabilidad.
    Esta es la validación más fuerte: cierra el ciclo matemáticamente.
    """
    total_original = len(df_original)
    total_limpio   = len(df_final)

    df_log = log.obtener()
   

    # Reconstrucción: limpio + eliminados únicos debe aproximarse al original
    # Nota: se usa nunique en eliminados porque un mismo ingreso puede tener
    # múltiples diagnósticos eliminados y cada uno genera una fila en el log.
    # La comparación exacta se hace sobre conteo de filas de eliminación en log.
    total_eliminados_filas = df_log[
        (df_log["ACCION"] == "Eliminación") &
        (df_log["CODINGRESO"].notna()) &
        (df_log["CODINGRESO"] != "N/A")
    ].shape[0]
    reconstruido = total_limpio + total_eliminados_filas

    diferencia = abs(total_original - reconstruido)

    if diferencia == 0:
        rv.aprobado(
            "Conservación matemática",
            f"Original ({total_original}) == Limpios ({total_limpio}) + Eliminados en log ({total_eliminados_filas})."
        )
    else:
        rv.fallido(
            "Conservación matemática",
            f"Diferencia de {diferencia} filas. "
            f"Original: {total_original} | Limpios: {total_limpio} | Eliminados en log: {total_eliminados_filas}. "
            f"Reconstruido: {reconstruido}. Revisar si hay acciones no registradas en trazabilidad."
        )


def validar_valores_nulos_criticos(df_final: pd.DataFrame, rv: ResultadoValidacion):
    """
    Verifica que las columnas críticas para el análisis epidemiológico
    no superen un umbral de nulos aceptable (5%).
    """
    columnas_criticas = ["CODIGO_INGRESO", "CIE10", "NOMBRE_DIAGNOSTICO", "TIPO_DIAGNOSTICO", "EDAD"]
    umbral = 0.05
    total = len(df_final)

    problemas = []
    for col in columnas_criticas:
        if col not in df_final.columns:
            continue
        n_nulos = df_final[col].isna().sum()
        pct = n_nulos / total if total > 0 else 0
        if pct > umbral:
            problemas.append(f"{col}: {n_nulos} nulos ({round(pct*100, 2)}%)")

    if not problemas:
        rv.aprobado(
            "Nulos en columnas críticas",
            f"Ninguna columna crítica supera el {int(umbral*100)}% de nulos."
        )
    else:
        rv.fallido(
            "Nulos en columnas críticas",
            "Columnas críticas con nulos excesivos: " + "; ".join(problemas)
        )


# ──────────────────────────────────────────────
# Función orquestadora — llamar desde Main.py
# ──────────────────────────────────────────────

def ejecutar_validaciones(
    df_original: pd.DataFrame,
    df_final: pd.DataFrame,
    log: LogTrazabilidad
) -> ResultadoValidacion:
    """
    Ejecuta todas las validaciones y retorna el objeto con los resultados.

    Uso en Main.py:
        from validacion.validaciones import ejecutar_validaciones
        rv = ejecutar_validaciones(df_base_original, df_final, log)
        resumen = rv.resumen()   # DataFrame con todos los resultados
    """
    rv = ResultadoValidacion()

    print("\n" + "="*60)
    print("  MÓDULO DE VALIDACIÓN — PIPELINE MORBILIDAD")
    print("="*60)

    validar_columnas_esperadas(df_final, rv)
    validar_columnas_excluidas_ausentes(df_final, rv)
    validar_folio_hc064w_ausente(df_final, rv)
    validar_sin_duplicados(df_final, rv)
    validar_edad_en_folios(df_final, rv)
    validar_conflictos_cruzados(df_final, rv)
  #  validar_conformidad_cie10(df_final, rv)
    validar_conservacion_matematica(df_original, df_final, log, rv)
    validar_valores_nulos_criticos(df_final, rv)

    print("="*60)
    aprobadas = sum(1 for r in rv.resultados if "APROBADO" in r["estado"])
    total     = len(rv.resultados)
    print(f"  RESULTADO FINAL: {aprobadas}/{total} validaciones aprobadas")
    print("="*60 + "\n")

    return rv