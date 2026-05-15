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

        edad = mapa_edades.loc[ingreso]

        if isinstance(edad, pd.Series):
            edad = edad.iloc[0]

        if pd.isna(edad) or edad >= edad_corte:

            filas_eliminar = df_b[df_b["CODIGO_INGRESO"] == ingreso]

            eliminar_b.append(ingreso)

            folio_descartado = folio_b
            folio_conservado = folio_a

            motivo = (
                f"Edad {edad} >= {edad_corte}: corresponde a grupo A"
                if pd.notna(edad) else
                "Edad nula: se conserva en grupo A por defecto"
            )

        else:

            filas_eliminar = df_a[df_a["CODIGO_INGRESO"] == ingreso]

            eliminar_a.append(ingreso)

            folio_descartado = folio_a
            folio_conservado = folio_b

            motivo = f"Edad {edad} < {edad_corte}: corresponde a grupo B"

        for _, fila in filas_eliminar.iterrows():

            log.registrar(
                ingreso        = fila["CODIGO_INGRESO"],
                campo          = "CODIGO_FOLIO",
                valor_original = fila["CODIGO_FOLIO"],
                valor_nuevo    = folio_conservado,
                regla_aplicada = (
                    f"Conflicto cruzado {folio_a}/{folio_b}: "
                    f"ingreso ({fila['CODIGO_INGRESO']}), "
                    f"diagnóstico ({fila['CIE10']}). "
                    f"{motivo}. "
                    f"Se elimina de {folio_descartado}, "
                    f"se conserva en {folio_conservado}."
                ),
                accion = "Eliminación",
                fase   = fase,
            )

    # Guarda solo los registros que no están en la lista de eliminados para cada folio
    df_a = df_a[~df_a["CODIGO_INGRESO"].isin(eliminar_a)]
    df_b = df_b[~df_b["CODIGO_INGRESO"].isin(eliminar_b)]

    return df_a, df_b, log