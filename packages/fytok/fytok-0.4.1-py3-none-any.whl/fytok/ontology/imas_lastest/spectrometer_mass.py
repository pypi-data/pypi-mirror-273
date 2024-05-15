"""
  This module containes the _FyTok_ wrapper of IMAS/dd/spectrometer_mass
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_signal_flt_2d_validity

class _T_spectrometer_mass(IDS):
	"""Mass spectrometer diagnostic
	lifecycle_status: alpha
	lifecycle_version: 3.29.0
	lifecycle_last_change: 3.33.0"""

	dd_version="v3_38_1_dirty"
	ids_name="spectrometer_mass"

	name  :str =  sp_property(type="static")
	""" Name of the spectrometer"""

	identifier  :str =  sp_property(type="static")
	""" ID of the spectrometer"""

	a  :array_type =  sp_property(type="static",units="Atomic Mass Unit",coordinate1="1...N")
	""" Array of atomic masses for which partial pressures are recorded by the
		spectrometer"""

	pressures_partial  :_T_signal_flt_2d_validity =  sp_property(units="Pa",coordinate1="../a")
	""" Partial pressures recorded by the spectrometer"""

	latency  :float =  sp_property(type="static",units="s",introduced_after_version="3.32.1")
	""" Upper bound of the delay between physical information received by the detector
		and data available on the real-time (RT) network."""
