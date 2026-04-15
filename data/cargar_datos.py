import pandas as pd
import os

_df_cache = None
ruta_archivo = "Data/Base_Morbilidad_Enero_2025_75_Columnas.xlsb"
ruta_cache = "Data/cache.parquet"



def cargar_database()-> pd.DataFrame:
    try:
        global _df_cache

        # Si ya se cargo la base de datos
        if _df_cache is not None:
            print("Ya se cargo la base de datos")
            return _df_cache

        # Si ya existe una ruta para el cache
        if os.path.exists(ruta_cache):
            print("Leyendo cache...")
            _df_cache = pd.read_parquet(ruta_cache, engine="pyarrow")
            return _df_cache

        # Si no se encuentra el archivo de la base de datos        
        if not os.path.exists(ruta_archivo):
            raise FileNotFoundError(f"El archivo {ruta_archivo} no existe")
        
        print("Leyendo Excel...")
        _df_cache = pd.read_excel(ruta_archivo,
                                  engine="pyxlsb",
                                  sheet_name="Hoja1")
        _df_cache.columns = _df_cache.columns.str.strip().str.upper().str.replace(" ", "_")

        _df_cache.to_parquet(ruta_cache, engine="pyarrow")

        return _df_cache


    except Exception as e:
        print(f"Error al cargar el archivo: {e}")


