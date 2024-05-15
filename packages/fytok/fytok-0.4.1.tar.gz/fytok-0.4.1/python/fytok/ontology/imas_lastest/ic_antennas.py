"""
  This module containes the _FyTok_ wrapper of IMAS/dd/ic_antennas
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_identifier_static,_T_signal_flt_1d,_T_rzphi0d_static,_T_signal_flt_1d_units_level_2,_T_rzphi1d_static,_T_outline_2d_geometry_static,_T_rz0d_constant

class _T_ic_antennas_matching_element(SpTree):
	"""Matching element"""

	name  :str =  sp_property(type="static")
	""" Name"""

	type  :_T_identifier_static =  sp_property()
	""" Type of the matching element. Index = 1 : capacitor (fill capacitance); Index =
		2 : stub (fill phase)"""

	capacitance  :Signal =  sp_property(units="F")
	""" Capacitance of the macthing element"""

	phase  :Signal =  sp_property(units="rad")
	""" Phase delay induced by the stub"""


class _T_ic_antennas_measurement(SpTree):
	"""Voltage or current measurement"""

	name  :str =  sp_property(type="static")
	""" Name"""

	identifier  :str =  sp_property(type="static")
	""" Identifier"""

	position  :_T_rzphi0d_static =  sp_property()
	""" Position of the measurement"""

	amplitude  :_T_signal_flt_1d_units_level_2 =  sp_property(units="as_parent")
	""" Amplitude of the measurement"""

	phase  :Signal =  sp_property(units="rad")
	""" Phase of the measurement"""


class _T_ic_antennas_strap(SpTree):
	"""Properties of IC antenna strap"""

	outline  :_T_rzphi1d_static =  sp_property()
	""" Strap outline"""

	width_tor  :float =  sp_property(type="static",units="m")
	""" Width of strap in the toroidal direction"""

	distance_to_conductor  :float =  sp_property(type="static",units="m")
	""" Distance to conducting wall or other conductor behind the antenna strap"""

	geometry  :_T_outline_2d_geometry_static =  sp_property()
	""" Cross-sectional shape of the strap"""

	current  :Signal =  sp_property(units="A")
	""" Root mean square current flowing along the strap"""

	phase  :Signal =  sp_property(units="rad")
	""" Phase of the strap current"""


class _T_ic_antennas_surface_current(TimeSlice):
	"""Description of the IC surface current on the antenna straps and on passive
		components."""

	m_pol  :List[int] =  sp_property(type="dynamic",coordinate1="1...N")
	""" Poloidal mode numbers, used to describe the spectrum of the antenna current. The
		poloidal angle is defined from the reference point; the angle at a point (R,Z)
		is given by atan((Z-Zref)/(R-Rref)), where Rref=reference_point/r and
		Zref=reference_point/z"""

	n_tor  :List[int] =  sp_property(type="dynamic",coordinate1="1...N")
	""" Toroidal mode numbers, used to describe the spectrum of the antenna current"""

	spectrum  :array_type =  sp_property(type="dynamic",coordinate1="../m_pol",coordinate2="../n_tor",units="A")
	""" Spectrum of the total surface current on the antenna strap and passive
		components expressed in poloidal and toroidal modes"""


class _T_ic_antennas_antenna_module(SpTree):
	"""Module of an IC antenna"""

	name  :str =  sp_property(type="static")
	""" Name of the module"""

	identifier  :str =  sp_property(type="static")
	""" Identifier of the module"""

	frequency  :Signal =  sp_property(units="Hz")
	""" Frequency"""

	power_launched  :Signal =  sp_property(units="W")
	""" Power launched from this module into the vacuum vessel"""

	power_forward  :Signal =  sp_property(units="W")
	""" Forward power arriving to the back of the module"""

	power_reflected  :Signal =  sp_property(units="W")
	""" Reflected power"""

	reflection_coefficient  :Signal =  sp_property(units="-")
	""" Power reflection coefficient"""

	phase_forward  :Signal =  sp_property(units="rad")
	""" Phase of the forward power with respect to the first module"""

	phase_reflected  :Signal =  sp_property(units="rad")
	""" Phase of the reflected power with respect to the forward power of this module"""

	voltage  :AoS[_T_ic_antennas_measurement] =  sp_property(coordinate1="1...N",units="V")
	""" Set of voltage measurements"""

	current  :AoS[_T_ic_antennas_measurement] =  sp_property(coordinate1="1...N",units="A")
	""" Set of current measurements"""

	pressure  :AoS[_T_ic_antennas_measurement] =  sp_property(coordinate1="1...N",units="Pa")
	""" Set of pressure measurements"""

	matching_element  :AoS[_T_ic_antennas_matching_element] =  sp_property(coordinate1="1...N",units="A")
	""" Set of matching elements"""

	strap  :AoS[_T_ic_antennas_strap] =  sp_property(coordinate1="1...N")
	""" Set of IC antenna straps"""


class _T_ic_antennas_antenna(SpTree):
	"""Ion Cyclotron Antenna"""

	name  :str =  sp_property(type="static")
	""" Name of the antenna (unique within the set of all antennas of the experiment)"""

	identifier  :str =  sp_property(type="static")
	""" Identifier of the antenna (unique within the set of all antennas of the
		experiment)"""

	frequency  :Signal =  sp_property(units="Hz")
	""" Frequency (average over modules)"""

	power_launched  :Signal =  sp_property(units="W")
	""" Power launched from this antenna into the vacuum vessel"""

	power_forward  :Signal =  sp_property(units="W")
	""" Forward power arriving to the back of the antenna"""

	power_reflected  :Signal =  sp_property(units="W")
	""" Reflected power"""

	module  :AoS[_T_ic_antennas_antenna_module] =  sp_property(coordinate1="1...N")
	""" Set of antenna modules (each module is fed by a single transmission line)"""

	surface_current  :TimeSeriesAoS[_T_ic_antennas_surface_current] =  sp_property(coordinate1="time",type="dynamic")
	""" Description of the IC surface current on the antenna straps and on passive
		components, for every time slice"""


class _T_ic_antennas(IDS):
	"""Antenna systems for heating and current drive in the ion cyclotron (IC)
		frequencies.
	lifecycle_status: alpha
	lifecycle_version: 3.7.0
	lifecycle_last_change: 3.33.0"""

	dd_version="v3_38_1_dirty"
	ids_name="ic_antennas"

	reference_point  :_T_rz0d_constant =  sp_property()
	""" Reference point used to define the poloidal angle, e.g. the geometrical centre
		of the vacuum vessel. Used to define the poloidal mode numbers under
		antenna/surface_current"""

	antenna  :AoS[_T_ic_antennas_antenna] =  sp_property(coordinate1="1...N")
	""" Set of Ion Cyclotron antennas"""

	power_launched  :Signal =  sp_property(units="W")
	""" Power launched into the vacuum vessel by the whole ICRH system (sum over
		antennas)"""

	latency  :float =  sp_property(type="static",units="s",introduced_after_version="3.32.1")
	""" Upper bound of the delay between input command received from the RT network and
		actuator starting to react. Applies globally to the system described by this IDS
		unless specific latencies (e.g. channel-specific or antenna-specific) are
		provided at a deeper level in the IDS structure."""
