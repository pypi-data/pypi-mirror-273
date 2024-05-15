"""
  This module containes the _FyTok_ wrapper of IMAS/dd/disruption
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_rz0d_dynamic_aos,_T_core_radial_grid,_T_b_tor_vacuum_1

class _T_disruption_global_quantities(SpTree):
	"""Global quantities related to the disruption"""

	current_halo_pol  :Expression  =  sp_property(coordinate1="../../time",units="A",type="dynamic")
	""" Poloidal halo current"""

	current_halo_tor  :Expression  =  sp_property(coordinate1="../../time",units="A",type="dynamic")
	""" Toroidal halo current"""

	power_ohm  :Expression  =  sp_property(coordinate1="../../time",units="W",type="dynamic")
	""" Total ohmic power"""

	power_ohm_halo  :Expression  =  sp_property(coordinate1="../../time",units="W",type="dynamic")
	""" Ohmic power in the halo region"""

	power_parallel_halo  :Expression  =  sp_property(coordinate1="../../time",units="W",type="dynamic")
	""" Power of the parallel heat flux in the halo region"""

	power_radiated_electrons_impurities  :Expression  =  sp_property(coordinate1="../../time",units="W",type="dynamic")
	""" Total power radiated by electrons on impurities"""

	power_radiated_electrons_impurities_halo  :Expression  =  sp_property(coordinate1="../../time",units="W",type="dynamic")
	""" Power radiated by electrons on impurities in the halo region"""

	energy_ohm  :Expression  =  sp_property(coordinate1="../../time",units="J",type="dynamic")
	""" Total ohmic cumulated energy (integral of the power over the disruption
		duration)"""

	energy_ohm_halo  :Expression  =  sp_property(coordinate1="../../time",units="J",type="dynamic")
	""" Ohmic cumulated energy (integral of the power over the disruption duration) in
		the halo region"""

	energy_parallel_halo  :Expression  =  sp_property(coordinate1="../../time",units="J",type="dynamic")
	""" Cumulated parallel energy (integral of the heat flux parallel power over the
		disruption duration) in the halo region"""

	energy_radiated_electrons_impurities  :Expression  =  sp_property(coordinate1="../../time",units="J",type="dynamic")
	""" Total cumulated energy (integral of the power over the disruption duration)
		radiated by electrons on impurities"""

	energy_radiated_electrons_impurities_halo  :Expression  =  sp_property(coordinate1="../../time",units="J",type="dynamic")
	""" Cumulated energy (integral of the power over the disruption duration) radiated
		by electrons on impurities in the halo region"""

	psi_halo_boundary  :Expression  =  sp_property(coordinate1="../../time",units="Wb",type="dynamic")
	""" Poloidal flux at halo region boundary"""


class _T_disruption_halo_currents_area(SpTree):
	"""Halo currents geometry and values for a given halo area"""

	start_point  :PointRZ =  sp_property()
	""" Position of the start point of this area"""

	end_point  :PointRZ =  sp_property()
	""" Position of the end point of this area"""

	current_halo_pol  :float =  sp_property(units="A",type="dynamic")
	""" Poloidal halo current crossing through this area"""


class _T_disruption_profiles_1d(TimeSlice):
	"""1D radial profiles for disruption data
	aos3Parent: yes"""

	grid  :_T_core_radial_grid =  sp_property()
	""" Radial grid"""

	j_runaways  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="A.m^-2",type="dynamic")
	""" Runaways parallel current density = average(j.B) / B0, where B0 =
		Disruption/Vacuum_Toroidal_Field/ B0"""

	power_density_conductive_losses  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="W.m^-3",type="dynamic")
	""" Power density of conductive losses to the wall (positive sign for losses)"""

	power_density_radiative_losses  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="W.m^-3",type="dynamic")
	""" Power density of radiative losses (positive sign for losses)"""


class _T_disruption_halo_currents(TimeSlice):
	"""Halo currents geometry and values for a given time slice"""

	area  :AoS[_T_disruption_halo_currents_area] =  sp_property(coordinate1="1...N")
	""" Set of wall areas through which there are halo currents"""

	active_wall_point  :PointRZ =  sp_property()
	""" R,Z position of the point of the plasma boundary in contact with the wall"""


class _T_disruption(IDS):
	"""Description of physics quantities of specific interest during a disruption, in
		particular halo currents, etc ...
	lifecycle_status: alpha
	lifecycle_version: 3.25.0
	lifecycle_last_change: 3.31.0"""

	dd_version="v3_38_1_dirty"
	ids_name="disruption"

	global_quantities  :_T_disruption_global_quantities =  sp_property()
	""" Global quantities"""

	halo_currents  :TimeSeriesAoS[_T_disruption_halo_currents] =  sp_property(coordinate1="time",type="dynamic")
	""" Halo currents geometry and values for a set of time slices"""

	profiles_1d  :TimeSeriesAoS[_T_disruption_profiles_1d] =  sp_property(coordinate1="time",type="dynamic",cocos_alias="IDSPATH",cocos_replace="disruption.profiles_1d{i}")
	""" Radial profiles for a set of time slices"""

	vacuum_toroidal_field  :_T_b_tor_vacuum_1 =  sp_property(cocos_alias="IDSPATH",cocos_replace="disruption.vacuum_toroidal_field")
	""" Characteristics of the vacuum toroidal field (used in rho_tor definition and in
		the normalization of current densities)"""
