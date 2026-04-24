import pandas as pd
from trazabilidad.dataframe import LogTrazabilidad


def cruzar_folios(
    df_a: pd.DataFrame,
    df_b: pd.DataFrame,
    folio_a: str,
    folio_b: str,
    edad_corte: int,
    fase: str,
    log: LogTrazabilidad,
) -> tuple[pd.DataFrame, pd.DataFrame, LogTrazabilidad]:
    """
    Resuelve ingresos presentes en ambos folios simultáneamente.
    La edad del paciente decide en cuál folio debe permanecer el registro.
    Si la edad es nula, se conserva en el folio A por defecto.

    Args:
        df_a, df_b:  DataFrames de cada folio ya corregidos por edad.
        folio_a:     Código del folio A (ej: 'HC003W').
        folio_b:     Código del folio B (ej: 'HC023W').
        edad_corte:  Umbral de edad que separa ambos grupos (ej: 18).
        fase:        Nombre de la fase para el log.
        log:         Instancia activa de LogTrazabilidad.
    """
    conflictos = set(df_a["CODIGO_INGRESO"]) & set(df_b["CODIGO_INGRESO"])

    if not conflictos:
        return df_a, df_b, log

    eliminar_a = []
    eliminar_b = []

    mapa_edades = df_a.set_index("CODIGO_INGRESO")["EDAD"]

    for ingreso in conflictos:
        edad = mapa_edades.loc[ingreso]
        if isinstance(edad, pd.Series):
            edad = edad.iloc[0]

        if pd.isna(edad) or edad >= edad_corte:
            eliminar_b.append(ingreso)
            folio_descartado = folio_b
            folio_conservado = folio_a
            motivo = (
                f"Edad {edad} >= {edad_corte}: corresponde a grupo A"
                if pd.notna(edad) else
                "Edad nula: se conserva en grupo A por defecto"
            )
        else:
            eliminar_a.append(ingreso)
            folio_descartado = folio_a
            folio_conservado = folio_b
            motivo = f"Edad {edad} < {edad_corte}: corresponde a grupo B"

        log.registrar(
            ingreso        = ingreso,
            campo          = "CODIGO_FOLIO",
            valor_original = folio_descartado,
            valor_nuevo    = folio_conservado,
            regla_aplicada = (
                f"Conflicto cruzado {folio_a}/{folio_b}: ingreso ({ingreso}) "
                f"presente en ambos folios. {motivo}. "
                f"Se elimina de {folio_descartado}, se conserva en {folio_conservado}."
            ),
            accion = "Eliminación",
            fase   = fase,
        )

    df_a = df_a[~df_a["CODIGO_INGRESO"].isin(eliminar_a)]
    df_b = df_b[~df_b["CODIGO_INGRESO"].isin(eliminar_b)]

    return df_a, df_b, log