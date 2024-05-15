"""
  This module containes the _FyTok_ wrapper of IMAS/dd/core_profiles
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_core_profiles_profiles_1d,_T_b_tor_vacuum_1

class _T_core_profiles_global_quantities_ion(SpTree):
	"""Various ion global quantities"""

	t_i_volume_average  :float =  sp_property(units="eV",type="dynamic")
	""" Volume averaged temperature of this ion species (averaged over the plasma volume
		up to the LCFS)"""

	n_i_volume_average  :float =  sp_property(units="m^-3",type="dynamic")
	""" Volume averaged density of this ion species (averaged over the plasma volume up
		to the LCFS)"""


class _T_core_profiles_global_quantities(SpTree):
	"""Various global quantities calculated from the fields solved in the transport
		equations and from the Derived Profiles"""

	ip  :float =  sp_property(units="A",type="dynamic",cocos_label_transformation="ip_like",cocos_transformation_expression=".sigma_ip_eff",cocos_leaf_name_aos_indices="core_profiles.global_quantities.ip")
	""" Total plasma current (toroidal component). Positive sign means anti-clockwise
		when viewed from above."""

	current_non_inductive  :float =  sp_property(units="A",type="dynamic",cocos_label_transformation="ip_like",cocos_transformation_expression=".sigma_ip_eff",cocos_leaf_name_aos_indices="core_profiles.global_quantities.current_non_inductive")
	""" Total non-inductive current (toroidal component). Positive sign means
		anti-clockwise when viewed from above."""

	current_bootstrap  :float =  sp_property(units="A",type="dynamic",cocos_label_transformation="ip_like",cocos_transformation_expression=".sigma_ip_eff",cocos_leaf_name_aos_indices="core_profiles.global_quantities.current_bootstrap")
	""" Bootstrap current (toroidal component). Positive sign means anti-clockwise when
		viewed from above."""

	v_loop  :float =  sp_property(units="V",type="dynamic",cocos_label_transformation="ip_like",cocos_transformation_expression=".sigma_ip_eff",cocos_leaf_name_aos_indices="core_profiles.global_quantities.v_loop")
	""" LCFS loop voltage (positive value drives positive ohmic current that flows
		anti-clockwise when viewed from above)"""

	li_3  :float =  sp_property(type="dynamic",units="-")
	""" Internal inductance. The li_3 definition is used, i.e. li_3 = 2/R0/mu0^2/Ip^2 *
		int(Bp^2 dV)."""

	beta_tor  :float =  sp_property(type="dynamic",units="-")
	""" Toroidal beta, defined as the volume-averaged total perpendicular pressure
		divided by (B0^2/(2*mu0)), i.e. beta_toroidal = 2 mu0 int(p dV) / V / B0^2"""

	beta_tor_norm  :float =  sp_property(type="dynamic",units="-")
	""" Normalised toroidal beta, defined as 100 * beta_tor * a[m] * B0 [T] / ip [MA]"""

	beta_pol  :float =  sp_property(type="dynamic",units="-")
	""" Poloidal beta. Defined as betap = 4 int(p dV) / [R_0 * mu_0 * Ip^2]"""

	energy_diamagnetic  :float =  sp_property(units="J",type="dynamic")
	""" Plasma energy content = 3/2 * integral over the plasma volume of the total
		perpendicular pressure"""

	z_eff_resistive  :float =  sp_property(units="-",type="dynamic")
	""" Volume average plasma effective charge, estimated from the flux consumption in
		the ohmic phase"""

	t_e_peaking  :float =  sp_property(units="-",type="dynamic")
	""" Electron temperature peaking factor, defined as the Te value at the magnetic
		axis divided by the volume averaged Te (average over the plasma volume up to the
		LCFS)"""

	t_i_average_peaking  :float =  sp_property(units="-",type="dynamic")
	""" Ion temperature (averaged over ion species and states) peaking factor, defined
		as the Ti value at the magnetic axis divided by the volume averaged Ti (average
		over the plasma volume up to the LCFS)"""

	resistive_psi_losses  :float =  sp_property(type="dynamic",units="Wb")
	""" Resistive part of the poloidal flux losses, defined as the volume-averaged
		scalar product of the electric field and the ohmic current density, normalized
		by the plasma current and integrated in time from the beginning of the plasma
		discharge: int ( (int(E_field_tor.j_ohm_tor) dV) / Ip ) dt)"""

	ejima  :float =  sp_property(type="dynamic",units="-")
	""" Ejima coefficient : resistive psi losses divided by (mu0*R*Ip). See S. Ejima et
		al, Nuclear Fusion, Vol.22, No.10 (1982), 1313"""

	t_e_volume_average  :float =  sp_property(units="eV",type="dynamic",introduced_after_version="3.33.0")
	""" Volume averaged electron temperature (average over the plasma volume up to the
		LCFS)"""

	n_e_volume_average  :float =  sp_property(units="m^-3",type="dynamic",introduced_after_version="3.33.0")
	""" Volume averaged electron density (average over the plasma volume up to the LCFS)"""

	ion  :AoS[_T_core_profiles_global_quantities_ion] =  sp_property(coordinate1="../../profiles_1d/ion",introduced_after_version="3.33.0")
	""" Quantities related to the different ion species, in the sense of isonuclear or
		isomolecular sequences. The set of ion species of this array must be the same as
		the one defined in profiles_1d/ion, at the time slice indicated in
		ion_time_slice"""

	ion_time_slice  :float =  sp_property(units="s",type="constant",introduced_after_version="3.33.0")
	""" Time slice of the profiles_1d array used to define the ion composition of the
		global_quantities/ion array."""


class _T_core_profiles(IDS):
	"""Core plasma radial profiles
	lifecycle_status: active
	lifecycle_version: 3.1.0
	lifecycle_last_change: 3.34.0
	specific_validation_rules: yes"""

	dd_version="v3_38_1_dirty"
	ids_name="core_profiles"

	profiles_1d  :TimeSeriesAoS[_T_core_profiles_profiles_1d] =  sp_property(coordinate1="time",type="dynamic",cocos_alias="IDSPATH",cocos_replace="core_profiles.profiles_1d{i}")
	""" Core plasma radial profiles for various time slices"""

	global_quantities  :TimeSeriesAoS[_T_core_profiles_global_quantities] =  sp_property(coordinate1="time",type="dynamic",cocos_alias="IDSPATH",cocos_replace="core_profiles.global_quantities{i}")
	""" Various global quantities derived from the profiles"""

	vacuum_toroidal_field  :_T_b_tor_vacuum_1 =  sp_property(cocos_alias="IDSPATH",cocos_replace="core_profiles.vacuum_toroidal_field")
	""" Characteristics of the vacuum toroidal field (used in rho_tor definition and in
		the normalization of current densities)"""
