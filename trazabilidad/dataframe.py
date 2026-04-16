import pandas as pd
from datetime import datetime
import os


class LogTrazabilidad:
    def __init__(self):
        self.columnas = [
            "timestamp",
            "ingreso",
            "campo",
            "valor_original",
            "valor_nuevo",
            "regla_aplicada",
            "accion",
            "fase"
        ]
        self.df_log = pd.DataFrame(columns=self.columnas)

    def registrar(
        self,
        ingreso,
        campo,
        valor_original,
        valor_nuevo,
        regla_aplicada,
        accion,
        fase
    ):
        nueva_fila = {
            "timestamp": datetime.now(),
            "ingreso": ingreso,
            "campo": campo,
            "valor_original": valor_original,
            "valor_nuevo": valor_nuevo,
            "regla_aplicada": regla_aplicada,
            "accion": accion,
            "fase": fase
        }

        self.df_log = pd.concat(
            [self.df_log, pd.DataFrame([nueva_fila])],
            ignore_index=True
        )

    def obtener(self):
        return self.df_log.copy()

    def resetear(self):
        self.df_log = pd.DataFrame(columns=self.columnas)

    def exportar(self, ruta_salida):
        carpeta = os.path.dirname(ruta_salida)
        if carpeta and not os.path.exists(carpeta):
            os.makedirs(carpeta)

        self.df_log.to_csv(ruta_salida, index=False, encoding="utf-8-sig")
        print(f"Log exportado en: {ruta_salida}")
        print(f"Total de registros en log: {len(self.df_log)}")