"""
  This module containes the _FyTok_ wrapper of IMAS/dd/thomson_scattering
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_rzphi0d_static,_T_rzphi1d_dynamic_aos1_common_time,_T_signal_flt_1d,_T_ids_identification,_T_identifier_static
from .utilities import _E_midplane_identifier

class _T_thomson_scattering_channel(SpTree):
	"""Thomson scattering channel"""

	name  :str =  sp_property(type="static")
	""" Name of the channel"""

	identifier  :str =  sp_property(type="static")
	""" ID of the channel"""

	position  :_T_rzphi0d_static =  sp_property()
	""" Average position of the measurements (intersection between laser beam and line
		of sight)"""

	delta_position  :_T_rzphi1d_dynamic_aos1_common_time =  sp_property()
	""" Incremental variation of the position of the measurements, due to e.g. different
		lasers not intersecting the line of sight at the same position. The actual
		position is then the static position + delta_position"""

	distance_separatrix_midplane  :Signal =  sp_property(units="m",introduced_after_version="3.32.1")
	""" Distance between the measurement position and the separatrix, mapped along flux
		surfaces to the outboard midplane, in the major radius direction. Positive value
		means the measurement is outside of the separatrix."""

	t_e  :Signal =  sp_property(units="eV")
	""" Electron temperature"""

	n_e  :Signal =  sp_property(units="m^-3")
	""" Electron density"""


class _T_thomson_scattering(IDS):
	"""Thomson scattering diagnostic
	lifecycle_status: alpha
	lifecycle_version: 3.0.4
	lifecycle_last_change: 3.33.0"""

	dd_version="v3_38_1_dirty"
	ids_name="thomson_scattering"

	equilibrium_id  :_T_ids_identification =  sp_property(introduced_after_version="3.32.1")
	""" ID of the IDS equilibrium used to map measurements - we may decide that this is
		superseeded when the systematic documentation of input provenance is adopted"""

	midplane  :_E_midplane_identifier =  sp_property(doc_identifier="utilities/midplane_identifier.xml",introduced_after_version="3.32.1")
	""" Choice of midplane definition for the mapping of measurements on an equilibrium"""

	channel  :AoS[_T_thomson_scattering_channel] =  sp_property(coordinate1="1...N")
	""" Set of channels (lines-of-sight)"""

	latency  :float =  sp_property(type="static",units="s",introduced_after_version="3.32.1")
	""" Upper bound of the delay between physical information received by the detector
		and data available on the real-time (RT) network."""
