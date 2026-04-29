""" import pandas as pd

from trazabilidad.dataframe import LogTrazabilidad

def separar_folios(
        df: pd.DataFrame,
        folios_interes: list[str],
        log: LogTrazabilidad
) -> tuple[pd.DataFrame, list[str], LogTrazabilidad]:
    
    # 1. Dataframe solo con los folios de interés
    df_folios = df[df["CODIGO_FOLIO"].isin(folios_interes)].copy()

    # 2. Dataframe con los folios restantes
    df_restante = df[~df["CODIGO_FOLIO"].isin(folios_interes)].copy() 

    # Registrar en el log
    log.registrar(
        ingreso="N/A",
        campo="CODIGO_FOLIO",
        valor_original="DataFrame completo",
        valor_nuevo=(
            f"DataFrame con: {', '.join(folios_interes)} | "
            f"DataFrame restante"
        ),
        regla_aplicada="Separación de DataFrame por folios de interés",
        accion="Clasificación",
        fase="Fase 2 - Separación de folios"
    )

    return df_folios, df_restante, log """