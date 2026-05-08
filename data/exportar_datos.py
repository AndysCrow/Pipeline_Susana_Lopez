import pandas as pd
import io
from datetime import datetime
from trazabilidad.dataframe import LogTrazabilidad


def exportar_datos(
    df_final: pd.DataFrame,
    log: LogTrazabilidad,
) -> dict[str, bytes]:
    """
    Serializa los resultados en memoria como CSV y los retorna como bytes.
    No escribe nada a disco; la descarga la maneja la UI.
    """

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # CSV datos limpios
    buf_datos = io.StringIO()
    df_final.to_csv(buf_datos, index=False)
    bytes_datos = buf_datos.getvalue().encode("utf-8")

    # CSV trazabilidad
    buf_log = io.StringIO()
    log.obtener().to_csv(buf_log, index=False)
    bytes_log = buf_log.getvalue().encode("utf-8")

    print(f"✔ Datos limpios listos en memoria ({len(df_final)} registros)")
    print(f"✔ Trazabilidad lista en memoria ({len(log.obtener())} registros)")

    return {
        f"datos_limpios_{timestamp}.csv": bytes_datos,
        f"trazabilidad_{timestamp}.csv": bytes_log,
    }