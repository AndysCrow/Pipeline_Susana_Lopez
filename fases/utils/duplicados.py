import pandas as pd
from trazabilidad.dataframe import LogTrazabilidad


def eliminar_duplicados(
    df: pd.DataFrame,
    log: LogTrazabilidad,
    clave_duplicado: list[str],
    etiqueta: str,
    fase: str,
) -> tuple[pd.DataFrame, LogTrazabilidad]:

    # Mapea el dataframe por TIPO_DIAGNOSTICO a número, los NaN se les asigna el número 2
    df = df.copy()
    df["ORDEN_DIAGNOSTICO"] = df["TIPO_DIAGNOSTICO"].map(
        {"PRINCIPAL": 0, "SECUNDARIO": 1}
    ).fillna(2)

    # Ordena el dataframe por tres criterios
    df_ordenado = df.sort_values(
        by=["FECHA_FOLIO", "CODIGO_INGRESO", "ORDEN_DIAGNOSTICO"],
        ascending=[True, True, False], # Ordena ORDEN_DIAGNOSTICO de forma descendente para priorizar PRINCIPAL
        na_position="first"
    ).drop(columns=["ORDEN_DIAGNOSTICO"])

    # Marca duplicados según la clave, conservando el último (más reciente) y descartando los anteriores
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
                f"Se conserva el registro más reciente con diagnóstico Principal."
            ),
            accion = "Eliminación",
            fase   = fase,
        )

    # Devuelve solo los registros que NO son duplicados
    return df_ordenado[~filtro_duplicado], log


def eliminar_duplicados_masivo(
    df: pd.DataFrame,
    log: LogTrazabilidad,
    clave_duplicado: list[str],
    fase: str,
) -> tuple[pd.DataFrame, LogTrazabilidad]:

    df = df.copy()
    df["ORDEN_DIAGNOSTICO"] = df["TIPO_DIAGNOSTICO"].map(
        {"PRINCIPAL": 0, "SECUNDARIO": 1}
    ).fillna(2)

    df_ordenado = df.sort_values(
        by=["FECHA_FOLIO", "CODIGO_INGRESO", "ORDEN_DIAGNOSTICO"],
        ascending=[True, True, False],
        na_position="first"
    ).drop(columns=["ORDEN_DIAGNOSTICO"])

    filtro_duplicado = df_ordenado.duplicated(subset=clave_duplicado, keep="last")
    df_descartar     = df_ordenado[filtro_duplicado]
    df_depurado      = df_ordenado[~filtro_duplicado]

    log.registrar_masivo(
        df_descartados = df_descartar,
        regla_aplicada = (
            f"Eliminación de duplicados: "
            f"clave {clave_duplicado}. "
            f"Se conserva el registro más reciente con diagnóstico Principal."
        ),
        accion = "Eliminación",
        fase   = fase,
    )

    return df_depurado, log