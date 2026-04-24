import pandas as pd
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(root_dir)

from trazabilidad.dataframe import LogTrazabilidad


def unificar_dataframe(
    df_inicial: pd.DataFrame,
    df_depurado: pd.DataFrame,
    log: LogTrazabilidad
) -> tuple[pd.DataFrame, LogTrazabilidad]:

    # 1. Concatenar ambos grupos
    df_unificado = pd.concat([df_inicial, df_depurado], ignore_index=True)

    log.registrar(
        ingreso="N/A",
        campo="CODIGO_FOLIO",
        valor_original="Dataframe inicial y Dataframe depurado separados",
        valor_nuevo=f"Dataframe unificado con: {len(df_unificado)} registros",
        regla_aplicada="Unificación del Dataframe inicial (Sin los folios del Grupo A y B) y el Dataframe depurado (Folios del Grupo A y B).",
        accion="Unificación",
        fase="Fase 4 - Unificación de Dataframes"

    )
    return df_unificado, log