"""
  This module containes the _FyTok_ wrapper of IMAS/dd/cryostat
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_vessel_2d

class _T_cryostat_2d(SpTree):
	"""2D cryostat description"""

	cryostat  :_T_vessel_2d =  sp_property()
	""" Mechanical structure of the cryostat. It is described as a set of nested layers
		with given physics properties; Two representations are admitted for each vessel
		unit : annular (two contours) or block elements."""

	thermal_shield  :_T_vessel_2d =  sp_property()
	""" Mechanical structure of the cryostat thermal shield. It is described as a set of
		nested layers with given physics properties; Two representations are admitted
		for each vessel unit : annular (two contours) or block elements."""


class _T_cryostat(IDS):
	"""Description of the cryostat surrounding the machine (if any)
	lifecycle_status: alpha
	lifecycle_version: 3.28.0
	lifecycle_last_change: 3.28.0"""

	dd_version="v3_38_1_dirty"
	ids_name="cryostat"

	description_2d  :AoS[_T_cryostat_2d] =  sp_property(coordinate1="1...N")
	""" Set of 2D cryostat descriptions, for each type of possible physics or
		engineering configurations necessary"""
