import pandas as pd
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(root_dir)

from trazabilidad.dataframe import LogTrazabilidad
from fases.utils.duplicados import eliminar_duplicados_masivo

FASE = "Fase 4 - Depuración final"
CLAVE_DUPLICADO = ["CODIGO_INGRESO", "CIE10", "CODIGO_FOLIO","FECHA_FOLIO","NOMBRE_DIAGNOSTICO" ]


def depurar_df_inicial(
    df_completo: pd.DataFrame,
    log: LogTrazabilidad
) -> tuple[pd.DataFrame, LogTrazabilidad]:

    df_sin_duplicados, log = eliminar_duplicados_masivo(
        df_completo, log, CLAVE_DUPLICADO, "", FASE
    )

    print(
        f"[{FASE}] Entrada: {len(df_completo)} | "
        f"Eliminados: {len(df_completo) - len(df_sin_duplicados)} | "
        f"Resultado: {len(df_sin_duplicados)}"
    )
    print(f"[{FASE}] Entrada: {len(df_completo)} | Eliminados: {len(df_completo) - len(df_sin_duplicados)} | Resultado: {len(df_sin_duplicados)}")
    return df_sin_duplicados, log