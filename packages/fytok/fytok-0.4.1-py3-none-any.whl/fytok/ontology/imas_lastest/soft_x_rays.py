"""
  This module containes the _FyTok_ wrapper of IMAS/dd/soft_x_rays
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_detector_aperture,_T_identifier_static,_T_line_of_sight_2points,_T_filter_window,_T_detector_energy_band,_T_signal_flt_2d,_T_signal_int_1d

class _T_sxr_channel(SpTree):
	"""Soft X-rays channel"""

	name  :str =  sp_property(type="static")
	""" Name of the channel"""

	identifier  :str =  sp_property(type="static")
	""" ID of the channel"""

	detector  :DetectorAperture =  sp_property()
	""" Detector description"""

	aperture  :AoS[DetectorAperture] =  sp_property(coordinate1="1...N")
	""" Description of a set of collimating apertures"""

	etendue  :float =  sp_property(type="static",units="m^2.sr")
	""" Etendue (geometric extent) of the channel's optical system"""

	etendue_method  :_T_identifier_static =  sp_property()
	""" Method used to calculate the etendue. Index = 0 : exact calculation with a 4D
		integral; 1 : approximation with first order formula (detector surface times
		solid angle subtended by the apertures); 2 : other methods"""

	line_of_sight  :_T_line_of_sight_2points =  sp_property()
	""" Description of the line of sight of the channel, given by 2 points"""

	filter_window  :AoS[_T_filter_window] =  sp_property(coordinate1="1...N",introduced_after_version="3.34.0")
	""" Set of filter windows"""

	energy_band  :AoS[_T_detector_energy_band] =  sp_property(coordinate1="1...N")
	""" Set of energy bands in which photons are counted by the detector"""

	brightness  :SignalND =  sp_property(coordinate1="../energy_band",coordinate2="time",units="W.m^-2.sr^-1")
	""" Power flux received by the detector, per unit solid angle and per unit area
		(i.e. power divided by the etendue), in multiple energy bands if available from
		the detector"""

	power  :SignalND =  sp_property(coordinate1="../energy_band",coordinate2="time",units="W")
	""" Power received on the detector, in multiple energy bands if available from the
		detector"""

	validity_timed  :Signal =  sp_property()
	""" Indicator of the validity of the channel as a function of time (0 means valid,
		negative values mean non-valid)"""

	validity  :int =  sp_property(type="static")
	""" Indicator of the validity of the channel for the whole acquisition period (0
		means valid, negative values mean non-valid)"""


class _T_soft_x_rays(IDS):
	"""Soft X-rays tomography diagnostic
	lifecycle_status: alpha
	lifecycle_version: 3.10.2
	lifecycle_last_change: 3.35.0"""

	dd_version="v3_38_1_dirty"
	ids_name="soft_x_rays"

	channel  :AoS[_T_sxr_channel] =  sp_property(coordinate1="1...N")
	""" Set of channels (detector or pixel of a camera)"""

	latency  :float =  sp_property(type="static",units="s",introduced_after_version="3.32.1")
	""" Upper bound of the delay between physical information received by the detector
		and data available on the real-time (RT) network."""
