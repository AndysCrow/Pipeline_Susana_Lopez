import sys
import pandas as pd
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(parent_dir)
sys.path.append(root_dir)

import data.cargar_datos as data
import trazabilidad.dataframe as dtframe


columnas_clave = {
    # Datos del paciente
    "EDAD_PACIENTE": "EDAD",
    "GENERO": "GENERO",
    "ETNÍA": "ETNIA",
    "NIVEL_SOCIOECONOMICO": "NIVEL_SOCIOECONOMICO",
    "OCUPACION_PACIENTE": "OCUPACION_PACIENTE",
    "REGIMEN": "REGIMEN",
    "TIPO_PACIENTE": "TIPO_PACIENTE",

    # Ubicación
    "MUNICIPIO": "MUNICIPIO",
    "ZONA": "ZONA",

    # Tiempo epidemiológico
    "FECHA_INGRESO_AL_HSLV": "FECHA_INGRESO",
    "FECHA_FOLIO": "FECHA_FOLIO",
    "MES_VERIFICADO_X_FECHA_INGRESO_AL_HSLV": "MES",
    "AÑO_VERIFICADO_X_FECHA_INGRESO_AL_HSLV": "AÑO",

    # Información clínica
    "DIAGNOSTICO": "CIE10",
    "DIAG_NOMBRE": "NOMBRE_DIAGNOSTICO",
    "TIP_DX": "TIPO_DIAGNOSTICO",
    "HCCODIGO": "CODIGO_FOLIO",
    "INGRESO_PAC": "CODIGO_INGRESO",
    "GASCODIGO": "CODIGO_AREA",
    "GASNOMBRE": "AREA"
}


def depurar_columnas(df: pd.DataFrame, log: dtframe.LogTrazabilidad) -> tuple[ pd.DataFrame, dtframe.LogTrazabilidad]:
    columnas_originales = list(df.columns)
    columnas_validas = [col for col in columnas_originales if col in columnas_clave]
    columnas_eliminadas = [col for col in columnas_originales if col not in columnas_clave]

    for col in columnas_eliminadas:
        log.registrar(
            ingreso="N/A",
            campo=col,
            valor_original="Columna existente",
            valor_nuevo="ELIMINADO",
            regla_aplicada="Exclusión por no aportar al análisis epidemiológico",
            accion="Eliminación",
            fase="Fase 1 -Depuración de columnas"
        )

    df = df[columnas_validas].copy()
    df = df.rename(columns=columnas_clave)

    return df, log