import pandas as pd
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(root_dir)

from trazabilidad.dataframe import LogTrazabilidad

FOLIOS_GRUPO_A = ["HC003W", "HC023W"]
EDAD_PEDIATRICO = 18
FASE = "Fase 2 - Grupo A"

# Clave de duplicado: mismo ingreso + mismo diagnóstico + mismo proceso (folio)
CLAVE_DUPLICADO = ["CODIGO_INGRESO", "CIE10", "CODIGO_FOLIO"]


def depurar_grupo_a(
    df: pd.DataFrame,
    log: LogTrazabilidad
) -> tuple[pd.DataFrame, LogTrazabilidad]:

    # 1. Filtrar folios del grupo A
    filtro_folio = df["CODIGO_FOLIO"].isin(FOLIOS_GRUPO_A)
    df_grupo = df[filtro_folio].copy()

    # 2. Separar adultos y pediátricos
    filtro_pediatrico = df_grupo["EDAD"] < EDAD_PEDIATRICO
    df_adultos    = df_grupo[~filtro_pediatrico].copy()
    df_pediatrico = df_grupo[filtro_pediatrico].copy()

    # 3. Eliminar duplicados de cada subgrupo
    df_adultos_dep,    log = eliminar_duplicados(
        df_adultos,    log, etiqueta="adulto"
    )
    df_pediatrico_dep, log = eliminar_duplicados(
        df_pediatrico, log, etiqueta="pediátrico"
    )

    # 4. Reunificar
    df_resultado = pd.concat(
        [df_adultos_dep, df_pediatrico_dep], ignore_index=True
    )

    print(
        f"[{FASE}] Registros entrada: {len(df_grupo)} | "
        f"Eliminados: {len(df_grupo) - len(df_resultado)} | "
        f"Resultado: {len(df_resultado)}"
    )

    return df_resultado, log



def eliminar_duplicados(
    df: pd.DataFrame,
    log: LogTrazabilidad,
    etiqueta: str
) -> tuple[pd.DataFrame, LogTrazabilidad]:
    """
    Elimina registros donde el mismo ingreso presenta el mismo diagnóstico
    en el mismo proceso (folio) más de una vez. Conserva el último por
    FECHA_INGRESO dentro de cada grupo duplicado.
    """
    df_ordenado = df.sort_values(
        by=["CODIGO_INGRESO", "FECHA_INGRESO"],
        ascending=[True, True],
        na_position="first"
    )

    # Duplicado = misma combinación ingreso + diagnóstico + folio
    filtro_duplicado = df_ordenado.duplicated(
        subset=CLAVE_DUPLICADO, keep="last"
    )
    df_descartar = df_ordenado[filtro_duplicado]

    # Registrar cada descarte en el log
    for _, fila in df_descartar.iterrows():
        log.registrar(
            ingreso        = fila["CODIGO_INGRESO"],
            campo          = "CODIGO_FOLIO",
            valor_original = fila["CODIGO_FOLIO"],
            valor_nuevo    = None,
            regla_aplicada = (
                f"Duplicado en Grupo A ({etiqueta}): mismo ingreso "
                f"({fila['CODIGO_INGRESO']}), mismo diagnóstico "
                f"({fila['CIE10']}), mismo proceso ({fila['CODIGO_FOLIO']}). "
                f"Se conserva el último registro."
            ),
            accion         = "Eliminación",
            fase           = FASE,
        )

    df_depurado = df_ordenado[~filtro_duplicado]
    return df_depurado, log