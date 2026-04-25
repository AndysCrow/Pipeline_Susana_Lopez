import pandas as pd
import os
from datetime import datetime
from trazabilidad.dataframe import LogTrazabilidad


def exportar_datos(
    df_final: pd.DataFrame,
    log: LogTrazabilidad,
    ruta_salida: str = "data/output"
) -> None:

    # 1. Crear carpeta si no existe
    os.makedirs(ruta_salida, exist_ok=True)

    # 2. Timestamp para versionado
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 3. Rutas
    ruta_excel_datos = os.path.join(ruta_salida, f"datos_limpios_{timestamp}.xlsx")
    ruta_excel_log   = os.path.join(ruta_salida, f"trazabilidad_{timestamp}.xlsx")
    ruta_csv_log     = os.path.join(ruta_salida, f"trazabilidad_{timestamp}.csv")

    # 4. Exportar DataFrame limpio
    df_final.to_excel(ruta_excel_datos, index=False)

    # 5. Exportar log en CSV (usando tu método)
    log.exportar(ruta_csv_log)

    # 6. Exportar log también en Excel (desde memoria, no desde CSV)
    df_log = log.obtener()
    df_log.to_excel(ruta_excel_log, index=False)

    print(f"✔ Datos limpios: {ruta_excel_datos}")
    print(f"✔ Log CSV: {ruta_csv_log}")
    print(f"✔ Log Excel: {ruta_excel_log}")