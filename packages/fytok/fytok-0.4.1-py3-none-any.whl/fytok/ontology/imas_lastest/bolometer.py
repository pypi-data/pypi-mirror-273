"""
  This module containes the _FyTok_ wrapper of IMAS/dd/bolometer
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_detector_aperture,_T_identifier_static,_T_line_of_sight_3points,_T_signal_flt_1d,_T_signal_int_1d

class _T_bolometer_channel(SpTree):
	"""Bolometer channel"""

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

	line_of_sight  :_T_line_of_sight_3points =  sp_property()
	""" Description of the reference line of sight of the channel, defined by two points
		when the beam is not reflected, a third point is added to define the reflected
		beam path"""

	power  :Signal =  sp_property(units="W")
	""" Power received on the detector"""

	validity_timed  :Signal =  sp_property()
	""" Indicator of the validity of the channel as a function of time (0 means valid,
		negative values mean non-valid)"""

	validity  :int =  sp_property(type="static")
	""" Indicator of the validity of the channel for the whole acquisition period (0
		means valid, negative values mean non-valid)"""


class _T_bolometer(IDS):
	"""Bolometer diagnostic
	lifecycle_status: alpha
	lifecycle_version: 3.7.4
	lifecycle_last_change: 3.33.0"""

	dd_version="v3_38_1_dirty"
	ids_name="bolometer"

	channel  :AoS[_T_bolometer_channel] =  sp_property(coordinate1="1...N")
	""" Set of channels (detector or pixel of a camera)"""

	power_radiated_total  :Expression  =  sp_property(coordinate1="../time",type="dynamic",units="W")
	""" Total radiated power reconstructed from bolometry data"""

	power_radiated_inside_lcfs  :Expression  =  sp_property(coordinate1="../time",type="dynamic",units="W")
	""" Radiated power from the plasma inside the Last Closed Flux Surface,
		reconstructed from bolometry data"""

	power_radiated_validity  :array_type =  sp_property(coordinate1="../time",type="dynamic")
	""" Validity flag related to the radiated power reconstructions"""

	latency  :float =  sp_property(type="static",units="s",introduced_after_version="3.32.1")
	""" Upper bound of the delay between physical information received by the detector
		and data available on the real-time (RT) network."""
