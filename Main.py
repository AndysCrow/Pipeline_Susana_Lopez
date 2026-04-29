from dependencies import *
from trazabilidad.dataframe import LogTrazabilidad
from datetime import date

def main(data: str, log: LogTrazabilidad):

    # 1. Carga
    df_base = cargar_database(data)

    # 2. Fase 1 - Limpieza base
    df_base, log = depurar_columnas(df_base, log)
    df_base, log = exluir_folios(df_base, log)
    df_base, log = formatear_fechas(df_base, log)
    df_base, log = formatear_edad(df_base, log)

    # 3. Fase 2 - Procesamiento por grupos
    df_a, log = depurar_grupo_a(df_base, log)
    df_b, log = depurar_grupo_b(df_base, log)

    # 4. Fase 3 - Integración de grupos
    df_grupos, log = unificar_folios(df_a, df_b, log)

    # 5. Remover del base los folios ya procesados
    df_base = df_base[~df_base["CODIGO_FOLIO"].isin([
        "HC003W", "HC023W", "HC071W", "HC088W"
    ])].copy()

    # 6. Fase 4 - Unificación final
    df_final, log = depurar_df_inicial(df_base,log)
    df_final, log = unificar_dataframe(df_final, df_grupos, log)


    # 7. Exportación completa (datos + log en CSV y Excel)
    exportar_datos(df_final, log)

    return df_final, log





if __name__ == "__main__":
    main()   