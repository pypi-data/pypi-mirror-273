__path__ = __import__("pkgutil").extend_path(__path__, __name__)

import os



from spdm.utils.envs import SP_MPI

from .ontology import GLOBAL_ONTOLOGY

from .utils.logger import logger
from .utils.envs import *


__version__ = FY_VERSION

############################################################


try:
    from importlib import resources as impresources
    from . import _mapping
    from spdm.core.Entry import EntryProxy

    EntryProxy._mapping_path.extend([p.resolve() for p in impresources.files(_mapping)._paths])

except Exception as error:
    raise FileNotFoundError(f"Can not find mappings!") from error

############################################################


if not FY_QUIET and (SP_MPI is  None or SP_MPI.COMM_WORLD.Get_rank() == 0):  # 粗略猜测是否在交互环境下运行
    logger.info(FY_LOGO)
