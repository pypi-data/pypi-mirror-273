"""
  This module containes the _FyTok_ wrapper of IMAS/dd/bremsstrahlung_visible
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_line_of_sight_2points,_T_filter_wavelength,_T_signal_flt_1d,_T_signal_flt_1d_validity

class _T_bremsstrahlung_channel(SpTree):
	"""Bremsstrahlung channel"""

	name  :str =  sp_property(type="static")
	""" Name of the channel"""

	line_of_sight  :_T_line_of_sight_2points =  sp_property()
	""" Description of the line of sight of the channel, given by 2 points"""

	filter  :_T_filter_wavelength =  sp_property()
	""" Filter wavelength range and detection efficiency"""

	intensity  :Signal =  sp_property(units="(counts) s^-1")
	""" Intensity, i.e. number of photoelectrons detected by unit time, taking into
		account electronic gain compensation and channels relative calibration"""

	radiance_spectral  :Signal =  sp_property(units="(photons).m^-2.s^-1.sr^-1.m^-1")
	""" Calibrated spectral radiance (radiance per unit wavelength)"""

	zeff_line_average  :Signal =  sp_property(units="-")
	""" Average effective charge along the line of sight"""


class _T_bremsstrahlung_visible(IDS):
	"""Diagnostic for measuring the bremsstrahlung from thermal particules in the
		visible light range, in view of determining the effective charge of the plasma.
	lifecycle_status: alpha
	lifecycle_version: 3.22.0
	lifecycle_last_change: 3.33.0"""

	dd_version="v3_38_1_dirty"
	ids_name="bremsstrahlung_visible"

	channel  :AoS[_T_bremsstrahlung_channel] =  sp_property(coordinate1="1...N")
	""" Set of channels (detector or pixel of a camera)"""

	latency  :float =  sp_property(type="static",units="s",introduced_after_version="3.32.1")
	""" Upper bound of the delay between physical information received by the detector
		and data available on the real-time (RT) network."""
