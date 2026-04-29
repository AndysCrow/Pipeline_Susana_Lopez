from data.cargar_datos import cargar_database
from data.exportar_datos import exportar_datos

from fases.fase_1_depuración_inicial.depuracion_columnas import depurar_columnas
from fases.fase_1_depuración_inicial.excluir_folios import exluir_folios
from fases.fase_1_depuración_inicial.formatear_columnas import (
    formatear_fechas,
    formatear_edad
)

from fases.fase_2_separación_de_grupos.grupo_a import depurar_grupo_a
from fases.fase_2_separación_de_grupos.grupo_b import depurar_grupo_b

from fases.fase_3_integración.unificar_folios import unificar_folios

from fases.fase_4_depuración_final.eliminar_duplicados import depurar_df_inicial
from fases.fase_4_depuración_final.cruce_unificar import unificar_dataframe


__all__ = [
    # Data
    "cargar_database",
    "exportar_datos",

    # Fase 1
    "depurar_columnas",
    "exluir_folios",
    "formatear_fechas",
    "formatear_edad",

    # Fase 2
    "depurar_grupo_a",
    "depurar_grupo_b",

    # Fase 3
    "unificar_folios",

    # Fase 4
    "depurar_df_inicial",
    "unificar_dataframe"
]