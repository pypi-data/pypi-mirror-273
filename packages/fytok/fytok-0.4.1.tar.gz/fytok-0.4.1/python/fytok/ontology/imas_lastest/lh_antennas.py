"""
  This module containes the _FyTok_ wrapper of IMAS/dd/lh_antennas
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_rzphi1d_dynamic_aos1_common_time,_T_signal_flt_1d,_T_rzphi1d_dynamic_aos1_definition,_T_signal_flt_2d,_T_rz0d_constant

class _T_lh_antennas_antenna_row(SpTree):
	"""Horizontal row of LH waveguides"""

	name  :str =  sp_property(type="static")
	""" Name of the row"""

	position  :_T_rzphi1d_dynamic_aos1_common_time =  sp_property()
	""" Position of the middle on the row"""

	n_tor  :Expression  =  sp_property(units="-",type="dynamic",coordinate1="../time")
	""" Refraction index in the toroidal direction"""

	n_pol  :Expression  =  sp_property(units="-",type="dynamic",coordinate1="../time")
	""" Refraction index in the poloidal direction. The poloidal angle is defined from
		the reference point; the angle at a point (R,Z) is given by
		atan((Z-Zref)/(R-Rref)), where Rref=reference_point/r and Zref=reference_point/z"""

	power_density_spectrum_1d  :array_type =  sp_property(units="W",type="dynamic",coordinate1="../n_tor",coordinate2="../time")
	""" 1D power density spectrum dP/dn_tor, as a function of time"""

	power_density_spectrum_2d  :array_type =  sp_property(units="W",type="dynamic",coordinate1="../n_tor",coordinate2="../n_pol",coordinate3="../time")
	""" 2D power density spectrum d2P/(dn_tor.dn_pol), as a function of time"""

	time  :array_type =  sp_property(coordinate1="1...N",type="dynamic",units="s")
	""" Timebase for the dynamic nodes of this probe located at this level of the IDS
		structure"""


class _T_lh_antennas_antenna_module(SpTree):
	"""Module of an LH antenna"""

	name  :str =  sp_property(type="static")
	""" Name of the module"""

	identifier  :str =  sp_property(type="static")
	""" Identifier of the module"""

	power_launched  :Signal =  sp_property(units="W")
	""" Power launched from this module into the vacuum vessel"""

	power_forward  :Signal =  sp_property(units="W")
	""" Forward power arriving to the back of the module"""

	power_reflected  :Signal =  sp_property(units="W")
	""" Reflected power"""

	reflection_coefficient  :Signal =  sp_property(units="-")
	""" Power reflection coefficient"""

	phase  :Signal =  sp_property(units="rad")
	""" Phase of the forward power arriving at the back of this module"""


class _T_lh_antennas_antenna(SpTree):
	"""LH antenna"""

	name  :str =  sp_property(type="static")
	""" Name of the antenna (unique within the set of all antennas of the experiment)"""

	identifier  :str =  sp_property(type="static")
	""" Identifier of the antenna (unique within the set of all antennas of the
		experiment)"""

	model_name  :str =  sp_property(type="constant")
	""" Name of the antenna model used for antenna spectrum computation"""

	frequency  :float =  sp_property(type="static",units="Hz")
	""" Frequency"""

	power_launched  :Signal =  sp_property(units="W")
	""" Power launched from this antenna into the vacuum vessel"""

	power_forward  :Signal =  sp_property(units="W")
	""" Forward power arriving at the back of the antenna"""

	power_reflected  :Signal =  sp_property(units="W")
	""" Reflected power"""

	reflection_coefficient  :Signal =  sp_property(units="-")
	""" Power reflection coefficient, averaged over modules"""

	phase_average  :Signal =  sp_property(units="rad")
	""" Phase difference between two neighbouring modules (average over modules), at the
		mouth (front) of the antenna"""

	n_parallel_peak  :Signal =  sp_property(units="-")
	""" Peak parallel refractive index of the launched wave spectrum (simple estimate
		based on the measured phase difference)"""

	position  :_T_rzphi1d_dynamic_aos1_definition =  sp_property()
	""" Position of a reference point on the antenna (allowing also tracking the
		possible movements of the antenna)"""

	pressure_tank  :Signal =  sp_property(units="Pa")
	""" Pressure in the vacuum tank of the antenna"""

	distance_to_antenna  :array_type =  sp_property(type="constant",units="m",coordinate1="1...N")
	""" Radial distance to the antenna mouth (grid for the electron density profile). 0
		at antenna mouth, increasing towards the plasma"""

	n_e  :SignalND =  sp_property(units="m^-3",coordinate1="../distance_to_antenna")
	""" Electron density profile in front of the antenna"""

	module  :AoS[_T_lh_antennas_antenna_module] =  sp_property(coordinate1="1...N")
	""" Set of antenna modules"""

	row  :AoS[_T_lh_antennas_antenna_row] =  sp_property(coordinate1="1...N")
	""" Set of horizontal rows of waveguides (corresponding to different poloidal
		positions). A power spectrum is provided for each row."""


class _T_lh_antennas(IDS):
	"""Antenna systems for heating and current drive in the Lower Hybrid (LH)
		frequencies. In the definitions below, the front (or mouth) of the antenna
		refers to the plasma facing side of the antenna, while the back refers to the
		waveguides connected side of the antenna (towards the RF generators).
	lifecycle_status: alpha
	lifecycle_version: 3.19.1
	lifecycle_last_change: 3.33.0"""

	dd_version="v3_38_1_dirty"
	ids_name="lh_antennas"

	reference_point  :_T_rz0d_constant =  sp_property()
	""" Reference point used to define the poloidal angle, e.g. the geometrical centre
		of the vacuum vessel. Used to define the poloidal refraction index under
		antenna/row"""

	antenna  :AoS[_T_lh_antennas_antenna] =  sp_property(coordinate1="1...N")
	""" Set of Lower Hybrid antennas"""

	power_launched  :Signal =  sp_property(units="W")
	""" Power launched into the vacuum vessel by the whole LH system (sum over antennas)"""

	latency  :float =  sp_property(type="static",units="s",introduced_after_version="3.32.1")
	""" Upper bound of the delay between input command received from the RT network and
		actuator starting to react. Applies globally to the system described by this IDS
		unless specific latencies (e.g. channel-specific or antenna-specific) are
		provided at a deeper level in the IDS structure."""
