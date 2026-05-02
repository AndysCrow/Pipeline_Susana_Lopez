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

    # Ingresos presentes en ambos folios simultáneamente
    conflictos = set(df_a["CODIGO_INGRESO"]) & set(df_b["CODIGO_INGRESO"])

    if not conflictos: # Si no hay conflictos, no hace nada
        return df_a, df_b, log 

    eliminar_a = []
    eliminar_b = []

    mapa_edades = df_a.set_index("CODIGO_INGRESO")["EDAD"] # Maneja los ingresos por edad (Ej: Ingreso01: 25)

    for ingreso in conflictos:

        edad = mapa_edades.loc[ingreso] # Guarda la edad
        if isinstance(edad, pd.Series): # Verifica si es un valor único o una lista de valores
            edad = edad.iloc[0] # Toma el primer valor

        if pd.isna(edad) or edad >= edad_corte: # Edad nula o mayor o igual al corte
            eliminar_b.append(ingreso) # Agrega para eliminar del folio B
            folio_descartado = folio_b
            folio_conservado = folio_a
            motivo = (
                f"Edad {edad} >= {edad_corte}: corresponde a grupo A"
                if pd.notna(edad) else
                "Edad nula: se conserva en grupo A por defecto"
            )
        else:
            eliminar_a.append(ingreso) # Agrega para eliminar del folio A
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

    # Guarda solo los registros que no están en la lista de eliminados para cada folio
    df_a = df_a[~df_a["CODIGO_INGRESO"].isin(eliminar_a)]
    df_b = df_b[~df_b["CODIGO_INGRESO"].isin(eliminar_b)]

    return df_a, df_b, log