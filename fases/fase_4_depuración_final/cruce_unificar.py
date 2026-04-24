#PROCEDIMIENTO DE TRABAJAR 2

import pandas as pd
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir    = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(root_dir)

from trazabilidad.dataframe import LogTrazabilidad
from fases.utils.duplicados    import eliminar_duplicados
from fases.utils.reubicar      import reubicar
from fases.utils.cruzar_folios import cruzar_folios


