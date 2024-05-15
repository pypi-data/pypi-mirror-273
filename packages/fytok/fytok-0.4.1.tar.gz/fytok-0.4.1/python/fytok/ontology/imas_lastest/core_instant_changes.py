"""
  This module containes the _FyTok_ wrapper of IMAS/dd/core_instant_changes
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_core_radial_grid,_T_core_profiles_profiles_1d_electrons,_T_core_profile_ions,_T_core_profile_neutral,_T_identifier,_T_core_profiles_profiles_1d,_T_b_tor_vacuum_1

class _E_core_instant_changes_identifier(IntFlag):
	"""Translation table for types of instant changes to the plasma state.	xpath: 	"""
  
	unspecified = 0
	"""Unspecified instant changes"""
  
	total = 1
	"""Total instant changes; combines all types of events"""
  
	pellet = 2
	"""Instant changes from a pellet"""
  
	sawtooth = 3
	"""Instant changes from a sawtooth"""
  
	elm = 4
	"""Instant changes from an edge localised mode"""
  

class _T_core_instant_changes_change_profiles(TimeSlice):
	"""instant_change terms for a given time slice"""

	grid  :_T_core_radial_grid =  sp_property()
	""" Radial grid"""

	electrons  :_T_core_profiles_profiles_1d_electrons =  sp_property()
	""" Change of electrons-related quantities"""

	t_i_average  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="eV",type="dynamic")
	""" change of average ion temperature"""

	momentum_tor  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="kg.m^2.s^-1",type="dynamic")
	""" change of total toroidal momentum"""

	ion  :AoS[_T_core_profile_ions] =  sp_property(coordinate1="1...N")
	""" changes related to the different ions species"""

	neutral  :AoS[_T_core_profile_neutral] =  sp_property(coordinate1="1...N")
	""" changes related to the different neutral species"""


class _T_core_instant_changes_change(SpTree):
	"""instant_change terms for a given instant_change"""

	identifier  :_E_core_instant_changes_identifier =  sp_property(doc_identifier="core_instant_changes/core_instant_changes_identifier.xml")
	""" Instant change term identifier"""

	profiles_1d  :TimeSeriesAoS[_T_core_profiles_profiles_1d] =  sp_property(coordinate1="time",type="dynamic",cocos_alias="IDSPATH",cocos_replace="core_instant_changes.change{i}.profiles_1d{j}")
	""" Changes in 1D core profiles for various time slices. This structure mirrors
		core_profiles/profiles_1d and describes instant changes to each of these
		physical quantities (i.e. a signed difference quantity after change - quantity
		before change)"""


class _T_core_instant_changes(IDS):
	"""Instant changes of the radial core plasma profiles due to pellet, MHD, ...
	lifecycle_status: active
	lifecycle_version: 3.10.0
	lifecycle_last_change: 3.15.0"""

	dd_version="v3_38_1_dirty"
	ids_name="core_instant_changes"

	vacuum_toroidal_field  :_T_b_tor_vacuum_1 =  sp_property(cocos_alias="IDSPATH",cocos_replace="core_instant_changes.vacuum_toroidal_field")
	""" Characteristics of the vacuum toroidal field (used in Rho_Tor definition and in
		the normalization of current densities)"""

	change  :AoS[_T_core_instant_changes_change] =  sp_property(coordinate1="1...N",appendable_by_appender_actor="yes")
	""" Set of instant change terms (each being due to a different phenomenon)"""
