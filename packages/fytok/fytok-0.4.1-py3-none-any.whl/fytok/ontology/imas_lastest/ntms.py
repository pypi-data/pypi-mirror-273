"""
  This module containes the _FyTok_ wrapper of IMAS/dd/ntms
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_b_tor_vacuum_1

class _T_ntm_time_slice_mode_detailed_evolution_deltaw(SpTree):
	"""deltaw contribution to the Rutherford equation (detailed evolution)"""

	value  :array_type =  sp_property(type="dynamic",units="m^-1",coordinate1="../../time_detailed")
	""" Value of the contribution"""

	name  :str =  sp_property(type="dynamic")
	""" Name of the contribution"""


class _T_ntm_time_slice_mode_detailed_evolution_torque(SpTree):
	"""torque contribution to the Rutherford equation (detailed evolution)"""

	value  :array_type =  sp_property(type="dynamic",units="kg.m^2.s^-2",coordinate1="../../time_detailed")
	""" Value of the contribution"""

	name  :str =  sp_property(type="dynamic")
	""" Name of the contribution"""


class _T_ntm_time_slice_mode_evolution_deltaw(SpTree):
	"""deltaw contribution to the Rutherford equation"""

	value  :float =  sp_property(type="dynamic",units="m^-1")
	""" Value of the contribution"""

	name  :str =  sp_property(type="dynamic")
	""" Name of the contribution"""


class _T_ntm_time_slice_mode_evolution_torque(SpTree):
	"""torque contribution to the Rutherford equation"""

	value  :float =  sp_property(type="dynamic",units="kg.m^2.s^-2")
	""" Value of the contribution"""

	name  :str =  sp_property(type="dynamic")
	""" Name of the contribution"""


class _T_ntm_time_slice_mode_onset(SpTree):
	"""Onset characteristics of an NTM"""

	width  :float =  sp_property(type="dynamic",units="m")
	""" Seed island full width at onset time"""

	time_onset  :float =  sp_property(type="dynamic",units="s")
	""" Onset time"""

	time_offset  :float =  sp_property(type="dynamic",units="s")
	""" Offset time (when a mode disappears). If the mode reappears later in the
		simulation, use another index of the mode array of structure"""

	phase  :float =  sp_property(type="dynamic",units="rad")
	""" Phase of the mode at onset"""

	n_tor  :int =  sp_property(type="dynamic")
	""" Toroidal mode number"""

	m_pol  :int =  sp_property(type="dynamic")
	""" Poloidal mode number"""

	cause  :str =  sp_property(type="dynamic")
	""" Cause of the mode onset"""


class _T_ntm_time_slice_mode_detailed_evolution(SpTree):
	"""Detailed NTM evolution on a finer timebase than the time_slice array of
		structure"""

	time_detailed  :array_type =  sp_property(type="dynamic",units="s",coordinate1="1...N")
	""" Time array used to describe the detailed evolution of the NTM"""

	width  :array_type =  sp_property(type="dynamic",units="m",coordinate1="../time_detailed")
	""" Full width of the mode"""

	dwidth_dt  :array_type =  sp_property(type="dynamic",units="m/s",coordinate1="../time_detailed")
	""" Time derivative of the full width of the mode"""

	phase  :array_type =  sp_property(type="dynamic",units="rad",coordinate1="../time_detailed")
	""" Phase of the mode"""

	dphase_dt  :array_type =  sp_property(type="dynamic",units="rad/s",coordinate1="../time_detailed")
	""" Time derivative of the phase of the mode"""

	frequency  :array_type =  sp_property(type="dynamic",units="Hz",coordinate1="../time_detailed")
	""" Frequency of the mode"""

	dfrequency_dt  :array_type =  sp_property(type="dynamic",units="s^-2",coordinate1="../time_detailed")
	""" Time derivative of the frequency of the mode"""

	n_tor  :int =  sp_property(type="dynamic")
	""" Toroidal mode number"""

	m_pol  :int =  sp_property(type="dynamic")
	""" Poloidal mode number"""

	deltaw  :AoS[_T_ntm_time_slice_mode_detailed_evolution_deltaw] =  sp_property(coordinate1="1...N")
	""" deltaw contributions to the Rutherford equation"""

	torque  :AoS[_T_ntm_time_slice_mode_detailed_evolution_torque] =  sp_property(coordinate1="1...N")
	""" torque contributions to the Rutherford equation"""

	calculation_method  :str =  sp_property(type="dynamic")
	""" Description of how the mode evolution is calculated"""

	delta_diff  :array_type =  sp_property(type="dynamic",coordinate1="1...3",coordinate2="../time_detailed",units="m^2.s^-1")
	""" Extra diffusion coefficient for the transport equations of Te, ne, Ti"""

	rho_tor_norm  :array_type =  sp_property(coordinate1="../time_detailed",units="-",type="dynamic")
	""" Normalised flux coordinate on which the mode is centred"""

	rho_tor  :array_type =  sp_property(coordinate1="../time_detailed",units="m",type="dynamic")
	""" Flux coordinate on which the mode is centred"""


class _T_ntm_time_slice_mode(SpTree):
	"""Description of an NTM"""

	onset  :_T_ntm_time_slice_mode_onset =  sp_property()
	""" NTM onset characteristics"""

	width  :float =  sp_property(type="dynamic",units="m")
	""" Full width of the mode"""

	dwidth_dt  :float =  sp_property(type="dynamic",units="m/s")
	""" Time derivative of the full width of the mode"""

	phase  :float =  sp_property(type="dynamic",units="rad")
	""" Phase of the mode"""

	dphase_dt  :float =  sp_property(type="dynamic",units="rad/s")
	""" Time derivative of the phase of the mode"""

	frequency  :float =  sp_property(type="dynamic",units="Hz")
	""" Frequency of the mode"""

	dfrequency_dt  :float =  sp_property(type="dynamic",units="s^-2")
	""" Time derivative of the frequency of the mode"""

	n_tor  :int =  sp_property(type="dynamic")
	""" Toroidal mode number"""

	m_pol  :int =  sp_property(type="dynamic")
	""" Poloidal mode number"""

	deltaw  :AoS[_T_ntm_time_slice_mode_evolution_deltaw] =  sp_property(coordinate1="1...N")
	""" deltaw contributions to the Rutherford equation"""

	torque  :AoS[_T_ntm_time_slice_mode_evolution_torque] =  sp_property(coordinate1="1...N")
	""" torque contributions to the Rutherford equation"""

	calculation_method  :str =  sp_property(type="dynamic")
	""" Description of how the mode evolution is calculated"""

	delta_diff  :array_type =  sp_property(type="dynamic",coordinate1="1...3",units="m^2.s^-1")
	""" Extra diffusion coefficient for the transport equations of Te, ne, Ti"""

	rho_tor_norm  :float =  sp_property(units="-",type="dynamic")
	""" Normalised flux coordinate on which the mode is centred"""

	rho_tor  :float =  sp_property(units="m",type="dynamic")
	""" Flux coordinate on which the mode is centred"""

	detailed_evolution  :_T_ntm_time_slice_mode_detailed_evolution =  sp_property()
	""" Detailed NTM evolution on a finer timebase than the time_slice array of
		structure"""


class _T_ntm_time_slice(TimeSlice):
	"""Time slice description of NTMs"""

	mode  :AoS[_T_ntm_time_slice_mode] =  sp_property(coordinate1="1...N")
	""" List of the various NTM modes appearing during the simulation. If a mode appears
		several times, use several indices in this array of structure with the same m,n
		values."""


class _T_ntms(IDS):
	"""Description of neoclassical tearing modes
	lifecycle_status: alpha
	lifecycle_version: 3.0.4
	lifecycle_last_change: 3.0.4"""

	dd_version="v3_38_1_dirty"
	ids_name="ntms"

	vacuum_toroidal_field  :_T_b_tor_vacuum_1 =  sp_property(cocos_alias="IDSPATH",cocos_replace="ntms.vacuum_toroidal_field")
	""" Characteristics of the vacuum toroidal field (used in rho_tor definition)"""

	time_slice  :TimeSeriesAoS[_T_ntm_time_slice] =  sp_property(coordinate1="time",type="dynamic")
	""" Description of neoclassical tearing modes for various time slices"""
