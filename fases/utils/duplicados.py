import pandas as pd
from trazabilidad.dataframe import LogTrazabilidad


def eliminar_duplicados(
    df: pd.DataFrame,
    log: LogTrazabilidad,
    clave_duplicado: list[str],
    etiqueta: str,
    fase: str,
) -> tuple[pd.DataFrame, LogTrazabilidad]:
    """
    Dentro de un mismo folio, elimina registros donde la clave_duplicado
    se repite más de una vez. Conserva el último por FECHA_FOLIO.

    Args:
        df:              DataFrame del folio a deduplicar.
        log:             Instancia activa de LogTrazabilidad.
        clave_duplicado: Columnas que definen un duplicado.
        etiqueta:        Etiqueta descriptiva para el log (ej: 'adulto').
        fase:            Nombre de la fase para el log.
    """
    df_ordenado = df.sort_values(
        by=["FECHA_FOLIO", "CODIGO_INGRESO"],
        ascending=[True, True],
        na_position="first"
    )

    filtro_duplicado = df_ordenado.duplicated(subset=clave_duplicado, keep="last")
    df_descartar     = df_ordenado[filtro_duplicado]

    for _, fila in df_descartar.iterrows():
        log.registrar(
            ingreso        = fila["CODIGO_INGRESO"],
            campo          = "CODIGO_FOLIO",
            valor_original = fila["CODIGO_FOLIO"],
            valor_nuevo    = "ELIMINADO",
            regla_aplicada = (
                f"Duplicado ({etiqueta}): mismo ingreso "
                f"({fila['CODIGO_INGRESO']}), mismo diagnóstico "
                f"({fila['CIE10']}), mismo proceso ({fila['CODIGO_FOLIO']}). "
                f"Se conserva el último registro."
            ),
            accion = "Eliminación",
            fase   = fase,
        )

    return df_ordenado[~filtro_duplicado], log


def eliminar_duplicados_masivo(
    df: pd.DataFrame,
    log: LogTrazabilidad,
    clave_duplicado: list[str],
    etiqueta: str,
    fase: str,
) -> tuple[pd.DataFrame, LogTrazabilidad]:
    """
    Versión optimizada para DataFrames grandes (+50k filas).
    Registra todos los descartados en una sola operación vectorizada.
    """
    df_ordenado = df.sort_values(
        by=["FECHA_FOLIO", "CODIGO_INGRESO"],
        ascending=[True, True],
        na_position="first"
    )

    filtro_duplicado = df_ordenado.duplicated(subset=clave_duplicado, keep="last")
    df_descartar     = df_ordenado[filtro_duplicado]
    df_depurado      = df_ordenado[~filtro_duplicado]

    log.registrar_masivo(
        df_descartados = df_descartar,
        regla_aplicada = (
            f"Eliminación de duplicados ({etiqueta}): "
            f"clave {clave_duplicado}. Se conserva el último registro."
        ),
        accion = "Eliminación",
        fase   = fase,
    )

    return df_depurado, log