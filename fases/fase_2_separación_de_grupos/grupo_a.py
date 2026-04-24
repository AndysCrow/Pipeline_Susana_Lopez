import pandas as pd
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir    = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(root_dir)

from trazabilidad.dataframe import LogTrazabilidad
from fases.utils.duplicados    import eliminar_duplicados
from fases.utils.reubicar      import reubicar
from fases.utils.cruzar_folios import cruzar_folios

FOLIO_ADULTOS    = "HC023W"
FOLIO_PEDIATRICO = "HC003W"
FOLIOS_GRUPO_A   = [FOLIO_ADULTOS, FOLIO_PEDIATRICO]
EDAD_PEDIATRICO  = 18
FASE             = "Fase 2 - Grupo A"
CLAVE_DUPLICADO  = ["CODIGO_INGRESO", "CIE10", "CODIGO_FOLIO"]


def depurar_grupo_a(
    df: pd.DataFrame,
    log: LogTrazabilidad
) -> tuple[pd.DataFrame, LogTrazabilidad]:

    # 1. Filtrar folios del grupo A
    df_grupo = df[df["CODIGO_FOLIO"].isin(FOLIOS_GRUPO_A)].copy()

    # 2. Separar por folio
    df_adultos    = df_grupo[df_grupo["CODIGO_FOLIO"] == FOLIO_ADULTOS].copy()
    df_pediatrico = df_grupo[df_grupo["CODIGO_FOLIO"] == FOLIO_PEDIATRICO].copy()

    # 3. Eliminar duplicados dentro de cada folio
    df_adultos,    log = eliminar_duplicados(df_adultos,    log, CLAVE_DUPLICADO, "adulto",     FASE)
    df_pediatrico, log = eliminar_duplicados(df_pediatrico, log, CLAVE_DUPLICADO, "pediátrico", FASE)

    # 4. Reubicar exclusivos mal ubicados por edad
    df_adultos, df_pediatrico, log = reubicar(
        df_origen     = df_adultos,
        df_destino    = df_pediatrico,
        condicion     = lambda edad: pd.notna(edad) and edad < EDAD_PEDIATRICO,
        folio_origen  = FOLIO_ADULTOS,
        folio_destino = FOLIO_PEDIATRICO,
        motivo        = "Paciente pediátrico ubicado en folio de adultos",
        fase          = FASE,
        log           = log,
    )
    df_pediatrico, df_adultos, log = reubicar(
        df_origen     = df_pediatrico,
        df_destino    = df_adultos,
        condicion     = lambda edad: pd.notna(edad) and edad >= EDAD_PEDIATRICO,
        folio_origen  = FOLIO_PEDIATRICO,
        folio_destino = FOLIO_ADULTOS,
        motivo        = "Paciente adulto ubicado en folio pediátrico",
        fase          = FASE,
        log           = log,
    )

    # 5. Resolver conflictos cruzados
    df_adultos, df_pediatrico, log = cruzar_folios(
        df_a       = df_adultos,
        df_b       = df_pediatrico,
        folio_a    = FOLIO_ADULTOS,
        folio_b    = FOLIO_PEDIATRICO,
        edad_corte = EDAD_PEDIATRICO,
        fase       = FASE,
        log        = log,
    )

    # 6. Unificar
    df_resultado = pd.concat([df_adultos, df_pediatrico], ignore_index=True)

    print(
        f"[{FASE}] Entrada: {len(df_grupo)} | "
        f"Eliminados: {len(df_grupo) - len(df_resultado)} | "
        f"Resultado: {len(df_resultado)}"
    )

    return df_resultado, log