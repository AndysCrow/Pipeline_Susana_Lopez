import pandas as pd
from trazabilidad.dataframe import LogTrazabilidad


def reubicar(
    df_origen: pd.DataFrame,
    df_destino: pd.DataFrame,
    condicion,
    folio_origen: str,
    folio_destino: str,
    motivo: str,
    fase: str,
    log: LogTrazabilidad,
) -> tuple[pd.DataFrame, pd.DataFrame, LogTrazabilidad]:
    """
    Mueve registros de df_origen a df_destino si cumplen la condición de edad.
    Opera SOLO sobre ingresos exclusivos (no presentes en el otro folio).

    Retorna (df_origen_sin_movidos, df_destino_aumentado, log).
    """
    df_origen = df_origen.copy()
    df_origen["EDAD"] = pd.to_numeric(df_origen["EDAD"], errors="coerce")

    # Excluir ingresos presentes en ambos — esos los maneja cruzar_folios
    ingresos_ambos   = set(df_origen["CODIGO_INGRESO"]) & set(df_destino["CODIGO_INGRESO"])
    df_origen_excl   = df_origen[~df_origen["CODIGO_INGRESO"].isin(ingresos_ambos)]
    df_origen_comun  = df_origen[df_origen["CODIGO_INGRESO"].isin(ingresos_ambos)]

    mask_mover   = df_origen_excl["EDAD"].apply(condicion)
    df_mover     = df_origen_excl[mask_mover].copy()
    df_sin_mover = df_origen_excl[~mask_mover].copy()

    if not df_mover.empty:
        for _, fila in df_mover.iterrows():
            log.registrar(
                ingreso        = fila["CODIGO_INGRESO"],
                campo          = "CODIGO_FOLIO",
                valor_original = folio_origen,
                valor_nuevo    = folio_destino,
                regla_aplicada = (
                    f"{motivo}: ingreso ({fila['CODIGO_INGRESO']}), "
                    f"edad ({fila['EDAD']}). "
                    f"Se reasigna de {folio_origen} a {folio_destino}."
                ),
                accion = "Reasignación",
                fase   = fase,
            )

        df_mover["CODIGO_FOLIO"] = folio_destino
        df_destino = pd.concat([df_destino, df_mover], ignore_index=True)

    # Reunir exclusivos corregidos + comunes intactos
    df_origen_final = pd.concat([df_sin_mover, df_origen_comun], ignore_index=True)

    return df_origen_final, df_destino, log