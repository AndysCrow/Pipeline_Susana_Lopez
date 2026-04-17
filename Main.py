from dependencies import *
from trazabilidad.dataframe import LogTrazabilidad
from datetime import date

def main(data: str, log: LogTrazabilidad):
    
    df = cargar_datos.cargar_database(data)
    df,log = depuracion_columnas.depurar_columnas(df, log)
    log.exportar(f"data/output/trazabilidad_{date.today():%Y%m%d}.csv")




if __name__ == "__main__":
    main()