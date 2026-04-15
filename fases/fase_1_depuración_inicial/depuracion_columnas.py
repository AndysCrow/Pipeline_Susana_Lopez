import sys
import pandas as pd
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(parent_dir)
sys.path.append(root_dir)
import data.cargar_datos as data

columnas_clave = {
    #Datos del paciente
    "EDAD_PACIENTE": "EDAD",
    "GENERO": "GENERO",
    "ETNÍA": "ETNIA",
    "NIVEL_SOCIOECONOMICO": "NIVEL_SOCIOECONOMICO",

    # Ubicación
    "MUNICIPIO": "MUNICIPIO",
    "ZONA": "ZONA",

    # Tiempo epidemiológico
    "FECHA_INGRESO_AL_HSLV": "FECHA_INGRESO",
    "MES_VERIFICADO_X_FECHA_INGRESO_AL_HSLV": "MES",
    "AÑO_VERIFICADO_X_FECHA_INGRESO_AL_HSLV": "AÑO",

    # Información clínica (CRÍTICO)
    "DIAGNOSTICO": "CIE10",
    "TIP_DX": "TIPO_DIAGNOSTICO",
    "HCCODIGO": "CODIGO_FOLIO"
}


def depurar_columnas(df: pd.DataFrame):

    columnas_validas = [col for col in df.columns if col in columnas_clave]
    df = df[columnas_validas]
    df = df.rename(columns=columnas_clave)
    
    return df

    


