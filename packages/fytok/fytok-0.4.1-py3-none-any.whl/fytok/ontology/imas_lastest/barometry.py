"""
  This module containes the _FyTok_ wrapper of IMAS/dd/barometry
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_identifier_static,_T_rzphi0d_static,_T_signal_flt_1d

class _T_barometry_gauge(SpTree):
	"""Pressure gauge"""

	name  :str =  sp_property(type="static")
	""" Name of the gauge"""

	type  :_T_identifier_static =  sp_property()
	""" Type of the gauge (index = 1: Penning; index = 2: Baratron)"""

	position  :_T_rzphi0d_static =  sp_property()
	""" Position of the measurements"""

	pressure  :Signal =  sp_property(units="Pa")
	""" Pressure"""

	calibration_coefficient  :float =  sp_property(type="static",units="Pa")
	""" Coefficient used for converting raw signal into absolute pressure"""


class _T_barometry(IDS):
	"""Pressure measurements in the vacuum vessel. NB will need to change the type of
		the pressure node to signal_1d when moving to the new LL.
	lifecycle_status: alpha
	lifecycle_version: 3.17.2
	lifecycle_last_change: 3.33.0"""

	dd_version="v3_38_1_dirty"
	ids_name="barometry"

	gauge  :AoS[_T_barometry_gauge] =  sp_property(coordinate1="1...N")
	""" Set of gauges"""

	latency  :float =  sp_property(type="static",units="s",introduced_after_version="3.32.1")
	""" Upper bound of the delay between physical information received by the detector
		and data available on the real-time (RT) network."""
