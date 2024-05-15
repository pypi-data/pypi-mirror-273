"""
  This module containes the _FyTok_ wrapper of IMAS/dd/refractometer
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_identifier,_T_signal_flt_1d,_T_signal_flt_2d,_T_line_of_sight_2points

class _E_refractometer_formula(IntFlag):
	"""Translation table for analytical formulas used by refractometer post-processing	xpath: 	"""
  
	flat = 1
	"""ne [m^-3] = 1e20 * alpha1"""
  
	rho_tor_norm_1 = 2
	"""ne [m^-3] = 1e20 * alpha1 * (exp(-(rho_tor_norm / alpha2)^2) * (1 + tanh(100 *
		((1-rho_tor_norm) / alpha3))) / 2)"""
  

class _T_refractometer_shape_approximation(SpTree):
	"""Shape approximation for the electron density profile"""

	formula  :_E_refractometer_formula =  sp_property(doc_identifier="refractometer/refractometer_formula_identifier.xml")
	""" Analytical formula representing the electron density profile as a function of a
		radial coordinate and adjustable parameters f(rho_tor_norm, alpha1, ... alphaN)"""

	parameters  :array_type =  sp_property(type="dynamic",coordinate1="1...N",coordinate2="../../n_e_line/time",units="mixed")
	""" Values of the formula's parameters alpha1, ..., alphaN"""


class _T_refractometer_channel_bandwidth(SpTree):
	"""refractometer channel bandwidth"""

	frequency_main  :float =  sp_property(type="static",units="Hz")
	""" Main frequency used to probe the plasma (before upshifting and modulating)"""

	phase  :Expression  =  sp_property(type="dynamic",coordinate1="../time",units="rad",introduced_after_version="3.32.1")
	""" Phase of the envelope of the probing signal, relative to the phase at launch"""

	i_component  :array_type =  sp_property(type="dynamic",coordinate1="1...N",coordinate1_same_as="../time_detector",coordinate2="../time",units="V",introduced_after_version="3.32.1")
	""" I component of the IQ detector used to retrieve the phase of signal's envelope,
		sampled on a high resolution time_detector grid just before each measurement
		time slice represented by the ../time vector"""

	q_component  :array_type =  sp_property(type="dynamic",coordinate1="1...N",coordinate1_same_as="../time_detector",coordinate2="../time",units="V",introduced_after_version="3.32.1")
	""" Q component of the IQ detector used to retrieve the phase of signal's envelope,
		sampled on a high resolution time_detector grid just before each measurement
		time slice represented by the ../time vector"""

	n_e_line  :Signal =  sp_property(coordinate1="time",units="m^-2")
	""" Integral of the electron density along the line of sight, deduced from the
		envelope phase measurements"""

	phase_quadrature  :SignalND =  sp_property(coordinate1="1...2",coordinate2="time",units="V")
	""" In-phase and Quadrature components of the analysed signal. They are returned by
		an IQ-detector, that takes carrying and reference signals as the input and
		yields I and Q components. These are respectively stored as the first and the
		second index of the first dimension of the data child."""

	time_detector  :array_type =  sp_property(coordinate1="1...N",coordinate2="../time",type="dynamic",units="s",introduced_after_version="3.32.1")
	""" High sampling timebase of the IQ-detector signal measurements"""

	time  :array_type =  sp_property(coordinate1="1...N",type="dynamic",units="s",introduced_after_version="3.32.1")
	""" Timebase for this bandwidth"""


class _T_refractometer_channel(SpTree):
	"""refractometer channel"""

	name  :str =  sp_property(type="static")
	""" Name of the channel"""

	identifier  :str =  sp_property(type="static")
	""" ID of the channel"""

	mode  :str =  sp_property(type="static")
	""" Detection mode _X_ or _O_"""

	line_of_sight  :_T_line_of_sight_2points =  sp_property()
	""" Description of the line of sight. The first point corresponds to the probing
		wave emission point. The second point corresponds to the probing wave detection
		point"""

	bandwidth  :AoS[_T_refractometer_channel_bandwidth] =  sp_property(coordinate1="1...N")
	""" Set of frequency bandwidths"""

	n_e_line  :Signal =  sp_property(coordinate1="time",units="m^-2")
	""" Integral of the electron density along the line of sight, deduced from the
		envelope phase measurements"""

	n_e_profile_approximation  :_T_refractometer_shape_approximation =  sp_property()
	""" Approximation of the radial electron density profile with an array of parameters
		and an approximation formula, used by post-processing programs for the
		identification of the electron density profile."""


class _T_refractometer(IDS):
	"""Density profile refractometer diagnostic
	lifecycle_status: alpha
	lifecycle_version: 3.31.0
	lifecycle_last_change: 3.33.0"""

	dd_version="v3_38_1_dirty"
	ids_name="refractometer"

	type  :str =  sp_property(type="static")
	""" Type of refractometer (differential, impulse, ...)"""

	channel  :AoS[_T_refractometer_channel] =  sp_property(coordinate1="1...N")
	""" Set of channels, e.g. different reception antennas of the refractometer"""

	latency  :float =  sp_property(type="static",units="s",introduced_after_version="3.32.1")
	""" Upper bound of the delay between physical information received by the detector
		and data available on the real-time (RT) network."""
