"""
  This module containes the _FyTok_ wrapper of IMAS/dd/interferometer
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_signal_flt_1d,_T_line_of_sight_3points,_T_signal_flt_1d_validity

class _T_interferometer_channel_wavelength_interf(SpTree):
	"""Value of the wavelength and density estimators associated to an interferometry
		wavelength"""

	value  :float =  sp_property(type="static",units="m")
	""" Wavelength value"""

	phase_corrected  :Signal =  sp_property(units="rad")
	""" Phase measured for this wavelength, corrected from fringe jumps"""

	fringe_jump_correction  :array_type =  sp_property(coordinate1="../fringe_jump_correction_times",type="constant")
	""" Signed number of 2pi phase corrections applied to remove a fringe jump, for each
		time slice on which a correction has been made"""

	fringe_jump_correction_times  :array_type =  sp_property(coordinate1="1...N",type="constant",units="s")
	""" List of time slices of the pulse on which a fringe jump correction has been made"""

	phase_to_n_e_line  :float =  sp_property(units="m^-2.rad^-1",type="static")
	""" Conversion factor to be used to convert phase into line density for this
		wavelength"""


class _T_interferometer_channel(SpTree):
	"""Charge exchange channel"""

	name  :str =  sp_property(type="static")
	""" Name of the channel"""

	identifier  :str =  sp_property(type="static")
	""" ID of the channel"""

	line_of_sight  :_T_line_of_sight_3points =  sp_property()
	""" Description of the line of sight of the channel, defined by two points when the
		beam is not reflected, a third point is added to define the reflected beam path"""

	wavelength  :AoS[_T_interferometer_channel_wavelength_interf] =  sp_property(coordinate1="1...N")
	""" Set of wavelengths used for interferometry"""

	path_length_variation  :Signal =  sp_property(units="m")
	""" Optical path length variation due to the plasma"""

	n_e_line  :Signal =  sp_property(units="m^-2")
	""" Line integrated density, possibly obtained by a combination of multiple
		interferometry wavelengths. Corresponds to the density integrated along the full
		line-of-sight (i.e. forward AND return for a reflected channel: NO dividing by 2
		correction)"""

	n_e_line_average  :Signal =  sp_property(units="m^-3")
	""" Line average density, possibly obtained by a combination of multiple
		interferometry wavelengths. Corresponds to the density integrated along the full
		line-of-sight and then divided by the length of the line-of-sight"""


class _T_interferometer(IDS):
	"""Interferometer diagnostic
	lifecycle_status: alpha
	lifecycle_version: 3.15.0
	lifecycle_last_change: 3.33.0"""

	dd_version="v3_38_1_dirty"
	ids_name="interferometer"

	channel  :AoS[_T_interferometer_channel] =  sp_property(coordinate1="1...N")
	""" Set of channels (lines-of-sight)"""

	n_e_volume_average  :Signal =  sp_property(units="m^-3")
	""" Volume average plasma density estimated from the line densities measured by the
		various channels"""

	electrons_n  :Signal =  sp_property(units="-")
	""" Total number of electrons in the plasma, estimated from the line densities
		measured by the various channels"""

	latency  :float =  sp_property(type="static",units="s",introduced_after_version="3.32.1")
	""" Upper bound of the delay between physical information received by the detector
		and data available on the real-time (RT) network."""
