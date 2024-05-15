"""
  This module containes the _FyTok_ wrapper of IMAS/dd/polarimeter
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_signal_flt_1d,_T_line_of_sight_3points,_T_signal_flt_1d_validity

class _T_polarimeter_channel_wavelength_interf(SpTree):
	"""Value of the wavelength and density estimators associated to an interferometry
		wavelength"""

	value  :float =  sp_property(type="static",units="m")
	""" Wavelength value"""

	phase_corrected  :Signal =  sp_property(units="rad")
	""" Phase measured for this wavelength, corrected from fringe jumps"""

	fring_jump_correction  :array_type =  sp_property(coordinate1="../fring_jump_correction_times",type="constant")
	""" Signed number of 2pi phase corrections applied to remove a fringe jump, for each
		time slice on which a correction has been made"""

	fring_jump_correction_times  :array_type =  sp_property(coordinate1="1...N",type="constant",units="s")
	""" List of time slices of the pulse on which a fringe jump correction has been made"""

	phase_to_n_e_line  :float =  sp_property(units="m^-2.rad^-1",type="static")
	""" Conversion factor to be used to convert phase into line density for this
		wavelength"""


class _T_polarimeter_channel(SpTree):
	"""Charge exchange channel"""

	name  :str =  sp_property(type="static")
	""" Name of the channel"""

	identifier  :str =  sp_property(type="static")
	""" ID of the channel"""

	line_of_sight  :_T_line_of_sight_3points =  sp_property()
	""" Description of the line of sight of the channel, defined by two points when the
		beam is not reflected, a third point is added to define the reflected beam path"""

	wavelength  :float =  sp_property(type="static",units="m")
	""" Wavelength used for polarimetry"""

	polarisation_initial  :float =  sp_property(type="static",units="m")
	""" Initial polarisation vector before entering the plasma"""

	ellipticity_initial  :float =  sp_property(type="static",units="m")
	""" Initial ellipticity before entering the plasma"""

	faraday_angle  :Signal =  sp_property(units="rad")
	""" Faraday angle (variation of the Faraday angle induced by crossing the plasma)"""

	ellipticity  :Signal =  sp_property(units="-")
	""" Ellipticity"""


class _T_polarimeter(IDS):
	"""Polarimeter diagnostic
	lifecycle_status: alpha
	lifecycle_version: 3.15.0
	lifecycle_last_change: 3.33.0"""

	dd_version="v3_38_1_dirty"
	ids_name="polarimeter"

	channel  :AoS[_T_polarimeter_channel] =  sp_property(coordinate1="1...N")
	""" Set of channels (lines-of-sight)"""

	latency  :float =  sp_property(type="static",units="s",introduced_after_version="3.32.1")
	""" Upper bound of the delay between physical information received by the detector
		and data available on the real-time (RT) network."""
