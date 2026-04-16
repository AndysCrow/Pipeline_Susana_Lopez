import pandas as pd
import os

_df_cache = None
_ruta_cargada = None



def cargar_database(ruta_archivo: str, sheet_name: str = "Hoja1")-> pd.DataFrame:
        
    global _df_cache, _ruta_cargada

    ruta_cache = _ruta_cache(ruta_archivo)

    # Si ya se cargo la base de datos
    if _df_cache is not None and _ruta_cargada == ruta_archivo:
        print("Ya se cargo la base de datos")
        return _df_cache

    # Si ya existe una ruta para el cache
    if os.path.exists(ruta_cache):
        print("Leyendo cache...")
        _df_cache = pd.read_parquet(ruta_cache, engine="pyarrow")
        _ruta_cargada = ruta_archivo
        return _df_cache

        # Si no se encuentra el archivo de la base de datos        
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"El archivo {ruta_archivo} no existe")
    
    try:
        print(f"Leyendo archivo fuente: {ruta_archivo}")
        _df_cache = pd.read_excel(ruta_archivo,
                                  engine="pyxlsb",
                                  sheet_name=sheet_name, dtype=str)
    except Exception as e:
        raise RuntimeError(f"Error al leer el archivo Excel: {e}") from e
    
    # Normalizar las columnas
    _df_cache.columns = _df_cache.columns.str.strip().str.upper().str.replace(" ", "_")

    # Guarda el caché en el disco
    os.makedirs(os.path.dirname(ruta_cache), exist_ok=True)
    _df_cache.to_parquet(ruta_cache, engine="pyarrow")
    print(f"Caché guardado en: {ruta_cache}")

    _ruta_cargada = ruta_archivo
    return _df_cache

# Funcion que resetea el caché
def limpiar_cache():
    global _df_cache, _ruta_cargada
    _df_cache = None
    _ruta_cargada = None
    print("Caché limpio")


def _ruta_cache(ruta_archivo: str):
    carpeta = os.path.dirname(ruta_archivo) or "Data"
    nombre = os.path.splitext(os.path.basename(ruta_archivo))[0]
    return os.path.join(carpeta, "cache", f"{nombre}.parquet")

