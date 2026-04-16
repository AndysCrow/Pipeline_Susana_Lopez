import pandas as pd 
import sys 
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(parent_dir)
sys.path.append(root_dir)

import trazabilidad.dataframe as dtframe


def exluir_folios (df: pd.DataFrame, log: dtframe.LogTrazabilidad) -> tuple[pd.DataFrame, dtframe.LogTrazabilidad]:

    df_excluidos = df.loc[df["CODIGO_FOLIO"] == "HC064W"]

    for _, fila in df_excluidos.iterrows():
        log.registrar(
            ingreso=fila["CODIGO_INGRESO"],
            campo="CODIGO_FOLIO",
            valor_original=fila["CODIGO_FOLIO"],
            valor_nuevo="ELIMINADO",
            regla_aplicada="Eliminación de folios con codigo HC064W",
            accion="Eliminación",
            fase="Exclusión de folios clinicos HC064W"
        )
    
    df_nuevo = df.loc[df["CODIGO_FOLIO"] != "HC064W"]

    return df_nuevo, log