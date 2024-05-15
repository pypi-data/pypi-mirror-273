"""
  This module containes the _FyTok_ wrapper of IMAS/dd/sawteeth
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_core_radial_grid,_T_b_tor_vacuum_1

class _T_sawteeth_diagnostics(SpTree):
	"""Detailed information about the sawtooth characteristics"""

	magnetic_shear_q1  :Expression  =  sp_property(coordinate1="../../time",units="-",type="dynamic")
	""" Magnetic shear at surface q = 1, defined as rho_tor/q . dq/drho_tor"""

	rho_tor_norm_q1  :Expression  =  sp_property(coordinate1="../../time",units="-",type="dynamic")
	""" Normalised toroidal flux coordinate at surface q = 1"""

	rho_tor_norm_inversion  :Expression  =  sp_property(coordinate1="../../time",units="-",type="dynamic")
	""" Normalised toroidal flux coordinate at inversion radius"""

	rho_tor_norm_mixing  :Expression  =  sp_property(coordinate1="../../time",units="-",type="dynamic")
	""" Normalised toroidal flux coordinate at mixing radius"""

	previous_crash_trigger  :array_type =  sp_property(coordinate1="../../time",type="dynamic")
	""" Previous crash trigger. Flag indicating whether a crash condition has been
		satisfied : 0 = no crash. N(>0) = crash triggered due to condition N"""

	previous_crash_time  :Expression  =  sp_property(coordinate1="../../time",units="s",type="dynamic")
	""" Time at which the previous sawtooth crash occured"""

	previous_period  :Expression  =  sp_property(coordinate1="../../time",units="s",type="dynamic")
	""" Previous sawtooth period"""


class _T_sawteeth_profiles_1d(TimeSlice):
	"""Core profiles after sawtooth crash"""

	grid  :_T_core_radial_grid =  sp_property()
	""" Radial grid"""

	t_e  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="eV",type="dynamic")
	""" Electron temperature"""

	t_i_average  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="eV",type="dynamic")
	""" Ion temperature (averaged on charge states and ion species)"""

	n_e  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="m^-3",type="dynamic")
	""" Electron density (thermal+non-thermal)"""

	n_e_fast  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="m^-3",type="dynamic")
	""" Density of fast (non-thermal) electrons"""

	n_i_total_over_n_e  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="-",type="dynamic")
	""" Ratio of total ion density (sum over species and charge states) over electron
		density. (thermal+non-thermal)"""

	momentum_tor  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",type="dynamic",units="kg.m/s")
	""" Total plasma toroidal momentum, summed over ion species and electrons"""

	zeff  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",type="dynamic",units="-")
	""" Effective charge"""

	p_e  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Electron pressure"""

	p_e_fast_perpendicular  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Fast (non-thermal) electron perpendicular pressure"""

	p_e_fast_parallel  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Fast (non-thermal) electron parallel pressure"""

	p_i_total  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Total ion pressure (sum over the ion species)"""

	p_i_total_fast_perpendicular  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Fast (non-thermal) total ion (sum over the ion species) perpendicular pressure"""

	p_i_total_fast_parallel  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Fast (non-thermal) total ion (sum over the ion species) parallel pressure"""

	pressure_thermal  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Thermal pressure (electrons+ions)"""

	pressure_perpendicular  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Total perpendicular pressure (electrons+ions, thermal+non-thermal)"""

	pressure_parallel  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Total parallel pressure (electrons+ions, thermal+non-thermal)"""

	j_total  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="A/m^2",type="dynamic")
	""" Total parallel current density = average(jtot.B) / B0, where B0 =
		Core_Profiles/Vacuum_Toroidal_Field/ B0"""

	j_tor  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="A/m^2",type="dynamic")
	""" Total toroidal current density = average(J_Tor/R) / average(1/R)"""

	j_ohmic  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="A/m^2",type="dynamic")
	""" Ohmic parallel current density = average(J_Ohmic.B) / B0, where B0 =
		Core_Profiles/Vacuum_Toroidal_Field/ B0"""

	j_non_inductive  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="A/m^2",type="dynamic")
	""" Non-inductive (includes bootstrap) parallel current density = average(jni.B) /
		B0, where B0 = Core_Profiles/Vacuum_Toroidal_Field/ B0"""

	j_bootstrap  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="A/m^2",type="dynamic")
	""" Bootstrap current density = average(J_Bootstrap.B) / B0, where B0 =
		Core_Profiles/Vacuum_Toroidal_Field/ B0"""

	conductivity_parallel  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="ohm^-1.m^-1",type="dynamic")
	""" Parallel conductivity"""

	e_field_parallel  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="V.m^-1",type="dynamic")
	""" Parallel electric field = average(E.B) / B0, where
		Core_Profiles/Vacuum_Toroidal_Field/ B0"""

	q  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",type="dynamic",units="-")
	""" Safety factor"""

	magnetic_shear  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="-",type="dynamic")
	""" Magnetic shear, defined as rho_tor/q . dq/drho_tor"""

	phi  :Expression  =  sp_property(type="dynamic",coordinate1="../grid/rho_tor_norm",units="Wb")
	""" Toroidal flux"""

	psi_star_pre_crash  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",type="dynamic",units="Wb")
	""" Psi* = psi - phi, just before the sawtooth crash"""

	psi_star_post_crash  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",type="dynamic",units="Wb")
	""" Psi* = psi - phi, after the sawtooth crash"""


class _T_sawteeth(IDS):
	"""Description of sawtooth events. This IDS must be used in homogeneous_time = 1
		mode
	lifecycle_status: alpha
	lifecycle_version: 3.0.4
	lifecycle_last_change: 3.10.0"""

	dd_version="v3_38_1_dirty"
	ids_name="sawteeth"

	vacuum_toroidal_field  :_T_b_tor_vacuum_1 =  sp_property(cocos_alias="IDSPATH",cocos_replace="sawteeth.vacuum_toroidal_field")
	""" Characteristics of the vacuum toroidal field (used in rho_tor definition)"""

	crash_trigger  :array_type =  sp_property(coordinate1="../time",type="dynamic")
	""" Flag indicating whether a crash condition has been satisfied : 0 = no crash.
		N(>0) = crash triggered due to condition N as follows. 1: crash triggered by the
		ideal kink criterion; 2: crash triggered by the ideal kink criterion including
		kinetic effects from fast particles; 31: crash triggered by the resistive kink
		criterion (meeting necessary conditions for reconnection); 32: crash triggered
		by the resistive kink criterion (resistive kink mode is unstable). The
		distinction between 31 and 32 only indicates whether (31) or (32) was the last
		criterion to be satisfied"""

	profiles_1d  :TimeSeriesAoS[_T_sawteeth_profiles_1d] =  sp_property(coordinate1="time",type="dynamic",cocos_alias="IDSPATH",cocos_replace="sawteeth.profiles_1d{i}")
	""" Core profiles after sawtooth crash for various time slices"""

	diagnostics  :_T_sawteeth_diagnostics =  sp_property()
	""" Detailed information about the sawtooth characteristics"""
