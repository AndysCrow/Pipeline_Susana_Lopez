import pandas as pd
import os

_df_cache = None
ruta_archivo = "Data/Base_Morbilidad_Enero_2025_75_Columnas.xlsb"



def cargar_database():
    try:

        if not os.path.exists(ruta_archivo):
            raise FileNotFoundError(f"El archivo '{ruta_archivo}' no se encuentra.")
        else:
            global _df_cache
            if _df_cache is None:
                print("Leyendo Excel...")
                _df_cache = pd.read_excel(ruta_archivo, engine="pyxlsb", sheet_name="Hoja1", dtype=str)
            
            else:
                print("Ya se cargo la base de datos.")
            
            _df_cache.columns = (_df_cache.columns.str.strip().str.upper().str.replace(" ", "_"))
            return _df_cache

    except Exception as e:
        print(f"Error al cargar el archivo: {e}")


