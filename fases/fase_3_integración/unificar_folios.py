import pandas as pd
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(root_dir)

from trazabilidad.dataframe import LogTrazabilidad

grupos_folios = {
    "Grupo A": ["HC003W", "HC023W"],
    "Grupo B": ["HC071W", "HC088W"]
}

def unificar_folios(df_a: pd.DataFrame, df_b: pd.DataFrame, log: LogTrazabilidad) -> tuple[pd.DataFrame, LogTrazabilidad]:

    # 1. Concatenar ambos grupos
    df_unificado = pd.concat([df_a, df_b], ignore_index=True)

    # Registrar cuantos registros aportó cada grupo
    for grupo, folios in grupos_folios.items():
        df_grupo = df_unificado[df_unificado["CODIGO_FOLIO"].isin(folios)]

        log.registrar(
            ingreso="N/A",
            campo="CODIGO_FOLIO",
            valor_original=", ".join(folios),
            valor_nuevo=f"{grupo}: {len(df_grupo)} registros",
            regla_aplicada="Registro de cantidad de registros aportados por cada grupo",
            accion="Registro",
            fase="Fase 3 - Unificación de folios"
        )

    print(f"[Fase 3 - Unificación folios] A: {len(df_a)} | B: {len(df_b)} | Total: {len(df_unificado)}")

    return df_unificado, log