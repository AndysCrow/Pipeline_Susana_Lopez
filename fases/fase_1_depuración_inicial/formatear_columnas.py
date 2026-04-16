import pandas as pd
import os 
import sys 

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(parent_dir)

sys.path.append(root_dir)

import trazabilidad.dataframe as trazabilidad

def formatear_fechas(df: pd.DataFrame, logs: trazabilidad.LogTrazabilidad) -> tuple[pd.DataFrame, trazabilidad.LogTrazabilidad]:
    # Cambiar tipo de fecha principal.
    tipo_original_fecha = df["FECHA_INGRESO"].dtype

    if not pd.api.types.is_datetime64_any_dtype(df["FECHA_INGRESO"]):
        
        df["FECHA_INGRESO"] = pd.to_datetime(
            df["FECHA_INGRESO"], errors="coerce"
        )

        logs.registrar(
            ingreso="N/A",
            campo="FECHA_INGRESO",
            valor_original=f"Tipo de dato: {tipo_original_fecha}",
            valor_nuevo=f"Tipo de dato: {df['FECHA_INGRESO'].dtype}",
            regla_aplicada="Formatear la fecha al tipo correcto",
            accion="Modificación",
            fase="Formatear columna fecha"
        )
    return df, logs


def formatear_edad(df: pd.DataFrame, logs: trazabilidad.LogTrazabilidad) -> tuple[pd.DataFrame, trazabilidad.LogTrazabilidad]:

    tipo_original_edad = df["EDAD"].dtype

    if not pd.api.types.is_integer_dtype(df["EDAD"]):
        df["EDAD"] = pd.to_numeric(
            df["EDAD"], errors="coerce"
        )

        logs.registrar(
            ingreso="N/A",
            campo="EDAD",
            valor_original=f"Tipo de dato: {tipo_original_edad}",
            valor_nuevo=f"Tipo de dato: {df['EDAD'].dtype}",
            regla_aplicada="Formatear la edad al tipo correcto",
            accion="Modificación",
            fase="Formatear columna edad"
        )

    return df, logs


