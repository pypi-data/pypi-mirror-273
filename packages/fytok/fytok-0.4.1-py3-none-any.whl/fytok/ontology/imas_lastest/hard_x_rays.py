"""
  This module containes the _FyTok_ wrapper of IMAS/dd/hard_x_rays
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_detector_aperture,_T_identifier_static,_T_line_of_sight_2points,_T_filter_window,_T_detector_energy_band,_T_signal_flt_2d_validity

class _T_hxr_emissivity_profile(SpTree):
	"""Hard X-rays emissivity profile"""

	lower_bound  :float =  sp_property(type="static",units="eV")
	""" Lower bound of the energy band"""

	upper_bound  :float =  sp_property(type="static",units="eV")
	""" Upper bound of the energy band"""

	rho_tor_norm  :array_type =  sp_property(type="constant",units="-",coordinate1="1...N")
	""" Normalised toroidal flux coordinate grid"""

	emissivity  :array_type =  sp_property(type="dynamic",coordinate1="../rho_tor_norm",coordinate2="../time",units="(photons).m^-3.str^-1.s^-1")
	""" Radial profile of the plasma emissivity in this energy band"""

	peak_position  :Expression  =  sp_property(type="dynamic",units="-",coordinate1="../time")
	""" Normalised toroidal flux coordinate position at which the emissivity peaks"""

	half_width_internal  :Expression  =  sp_property(type="dynamic",units="-",coordinate1="../time")
	""" Internal (towards magnetic axis) half width of the emissivity peak (in
		normalised toroidal flux)"""

	half_width_external  :Expression  =  sp_property(type="dynamic",units="-",coordinate1="../time")
	""" External (towards separatrix) half width of the emissivity peak (in normalised
		toroidal flux)"""

	validity_timed  :array_type =  sp_property(type="dynamic",coordinate1="../time")
	""" Indicator of the validity of the emissivity profile data for each time slice. 0:
		valid from automated processing, 1: valid and certified by the diagnostic RO; -
		1 means problem identified in the data processing (request verification by the
		diagnostic RO), -2: invalid data, should not be used (values lower than -2 have
		a code-specific meaning detailing the origin of their invalidity)"""

	time  :array_type =  sp_property(type="dynamic",units="s",coordinate1="1...N")
	""" Time"""


class _T_hxr_channel(SpTree):
	"""Hard X-rays channel"""

	name  :str =  sp_property(type="static")
	""" Name of the channel"""

	identifier  :str =  sp_property(type="static")
	""" ID of the channel"""

	detector  :DetectorAperture =  sp_property()
	""" Detector description"""

	aperture  :AoS[DetectorAperture] =  sp_property(coordinate1="1...N")
	""" Description of a set of collimating apertures"""

	etendue  :float =  sp_property(type="static",units="m^2.str")
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

	radiance  :_T_signal_flt_2d_validity =  sp_property(coordinate1="../energy_band",coordinate2="time",units="(photons).s^-1.m^-2.sr^-1")
	""" Photons received by the detector per unit time, per unit solid angle and per
		unit area (i.e. photon flux divided by the etendue), in multiple energy bands if
		available from the detector"""


class _T_hard_x_rays(IDS):
	"""Hard X-rays tomography diagnostic
	lifecycle_status: alpha
	lifecycle_version: 3.23.3
	lifecycle_last_change: 3.35.0"""

	dd_version="v3_38_1_dirty"
	ids_name="hard_x_rays"

	channel  :AoS[_T_hxr_channel] =  sp_property(coordinate1="1...N")
	""" Set of channels (detector or pixel of a camera)"""

	emissivity_profile_1d  :AoS[_T_hxr_emissivity_profile] =  sp_property(coordinate1="1...N")
	""" Emissivity profile per energy band (assumed common to all channels used in the
		profile reconstruction)"""

	latency  :float =  sp_property(type="static",units="s",introduced_after_version="3.32.1")
	""" Upper bound of the delay between physical information received by the detector
		and data available on the real-time (RT) network."""
