"""
  This module containes the _FyTok_ wrapper of IMAS/dd/distribution_sources
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_generic_grid_dynamic,_T_generic_grid_scalar,_T_core_radial_grid,_T_distribution_process_identifier,_T_distribution_species,_T_distribution_markers,_T_b_tor_vacuum_1,_T_rz1d_dynamic_1

class _T_distribution_sources_source_global_shinethrough(SpTree):
	"""Global quantities related to shinethrough, for a given time slice"""

	power  :float =  sp_property(units="W",type="dynamic")
	""" Power losses due to shinethrough"""

	particles  :float =  sp_property(units="s^-1",type="dynamic")
	""" Particle losses due to shinethrough"""

	torque_tor  :float =  sp_property(units="N.m",type="dynamic")
	""" Toroidal torque losses due to shinethrough"""


class _T_distribution_sources_source_ggd(TimeSlice):
	"""Source terms for a given time slice, using a GGD representation"""

	grid  :_T_generic_grid_dynamic =  sp_property()
	""" Grid description"""

	particles  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="(m.s^-1)^-3.m^-3.s^-1")
	""" Source density of particles in phase space, for various grid subsets"""

	discrete  :List[int] =  sp_property(coordinate1="1...N",type="dynamic")
	""" List of indices of grid spaces (refers to ../grid/space) for which the source is
		discretely distributed. For example consider a source of 3.5 MeV alpha particles
		provided on a grid with two coordinates (spaces); rho_tor and energy. To specify
		that the source is given at energies exactly equal to 3.5 MeV, let discret have
		length 1 and set discrete(1)=2 since energy is dimension number 2. The source is
		then proportional to delta( 1 - energy / 3.5MeV ), where delta is the direct
		delta distribution. Discrete dimensions can only be used when the grid is
		rectangular."""


class _T_distribution_sources_source_profiles_1d(TimeSlice):
	"""Radial profile of source terms for a given time slice"""

	grid  :_T_core_radial_grid =  sp_property()
	""" Radial grid"""

	energy  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="W.m^-3",type="dynamic")
	""" Source term for the energy transport equation"""

	momentum_tor  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="N.m^-2",type="dynamic")
	""" Source term for the toroidal momentum equation"""

	particles  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="s^-1.m^-3",type="dynamic")
	""" Source term for the density transport equation"""


class _T_distribution_sources_source_global_quantities(TimeSlice):
	"""Global quantities of distribution_source for a given time slice"""

	power  :float =  sp_property(units="W",type="dynamic")
	""" Total power of the source"""

	torque_tor  :float =  sp_property(units="N.m",type="dynamic")
	""" Total toroidal torque of the source"""

	particles  :float =  sp_property(units="s^-1",type="dynamic")
	""" Particle source rate"""

	shinethrough  :_T_distribution_sources_source_global_shinethrough =  sp_property()
	""" Shinethrough losses"""


class _T_distribution_sources_source(SpTree):
	"""Source terms for a given actuator"""

	process  :AoS[_T_distribution_process_identifier] =  sp_property(coordinate1="1...N")
	""" Set of processes (NBI units, fusion reactions, ...) that provide the source."""

	gyro_type  :int =  sp_property(type="constant")
	""" Defines how to interpret the spatial coordinates: 1 = given at the actual
		particle birth point; 2 =given at the gyro centre of the birth point"""

	species  :_T_distribution_species =  sp_property()
	""" Species injected or consumed by this source/sink"""

	global_quantities  :TimeSeriesAoS[_T_distribution_sources_source_global_quantities] =  sp_property(coordinate1="time",type="dynamic")
	""" Global quantities for various time slices"""

	profiles_1d  :TimeSeriesAoS[_T_distribution_sources_source_profiles_1d] =  sp_property(coordinate1="time",type="dynamic",cocos_alias="IDSPATH",cocos_replace="distribution_sources.source{i}.profiles_1d{j}")
	""" Source radial profiles (flux surface averaged quantities) for various time
		slices"""

	ggd  :TimeSeriesAoS[_T_distribution_sources_source_ggd] =  sp_property(coordinate1="time",type="dynamic")
	""" Source terms in phase space (real space, velocity space, spin state),
		represented using the ggd, for various time slices"""

	markers  :TimeSeriesAoS[_T_distribution_markers] =  sp_property(coordinate1="time",type="dynamic")
	""" Source given as a group of markers (test particles) born per second, for various
		time slices"""


class _T_distribution_sources(IDS):
	"""Sources of particles for input to kinetic equations, e.g. Fokker-Planck
		calculation. The sources could originate from e.g. NBI or fusion reactions.
	lifecycle_status: alpha
	lifecycle_version: 3.2.1
	lifecycle_last_change: 3.32.0"""

	dd_version="v3_38_1_dirty"
	ids_name="distribution_sources"

	source  :AoS[_T_distribution_sources_source] =  sp_property(coordinate1="1...N",appendable_by_appender_actor="yes")
	""" Set of source/sink terms. A source/sink term corresponds to the particle source
		due to an NBI injection unit, a nuclear reaction or any combination of them
		(described in _identifier_)"""

	vacuum_toroidal_field  :_T_b_tor_vacuum_1 =  sp_property(cocos_alias="IDSPATH",cocos_replace="distribution_sources.vacuum_toroidal_field")
	""" Characteristics of the vacuum toroidal field (used in rho_tor definition)"""

	magnetic_axis  :_T_rz1d_dynamic_1 =  sp_property()
	""" Magnetic axis position (used to define a poloidal angle for the 2D profiles)"""
