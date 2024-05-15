"""
  This module containes the _FyTok_ wrapper of IMAS/dd/core_sources
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_identifier_dynamic_aos3,_T_plasma_composition_neutral_element,_T_core_radial_grid,_T_identifier,_T_distribution_species,_T_code_with_timebase,_T_b_tor_vacuum_1
from .utilities import _E_neutrals_identifier

class _E_core_source(IntFlag):
	"""Translation table for sources of particles, momentum and heat.	xpath: 	"""
  
	unspecified = 0
	"""Unspecified source type"""
  
	total = 1
	"""Total source; combines all sources"""
  
	nbi = 2
	"""Source from Neutral Beam Injection"""
  
	ec = 3
	"""Sources from electron cyclotron heating and current drive"""
  
	lh = 4
	"""Sources from lower hybrid heating and current drive"""
  
	ic = 5
	"""Sources from heating at the ion cyclotron range of frequencies"""
  
	fusion = 6
	"""Sources from fusion reactions, e.g. alpha particle heating"""
  
	ohmic = 7
	"""Source from ohmic heating"""
  
	bremsstrahlung = 8
	"""Source from bremsstrahlung; radiation losses are negative sources"""
  
	synchrotron_radiation = 9
	"""Source from synchrotron radiation; radiation losses are negative sources"""
  
	line_radiation = 10
	"""Source from line radiation; radiation losses are negative sources"""
  
	collisional_equipartition = 11
	"""Collisional equipartition"""
  
	cold_neutrals = 12
	"""Source of cold neutrals"""
  
	bootstrap_current = 13
	"""Bootstrap current"""
  
	pellet = 14
	"""Sources from injection"""
  
	auxiliary = 100
	"""Source from auxiliary systems, e.g. heating and current drive systems"""
  
	ic_nbi = 101
	"""A combination of the ic and nbi sources"""
  
	ic_fusion = 102
	"""A combination of the ic and fusion sources"""
  
	ic_nbi_fusion = 103
	"""A combination of the ic and fusion sources"""
  
	ec_lh = 104
	"""A combination of the ec and lh sources"""
  
	ec_ic = 105
	"""A combination of the ec and ic sources"""
  
	lh_ic = 106
	"""A combination of the lh and ic sources"""
  
	ec_lh_ic = 107
	"""A combination of the ec, lh and ic sources"""
  
	gas_puff = 108
	"""Gas puff"""
  
	killer_gas_puff = 109
	"""Killer gas puff"""
  
	radiation = 200
	"""Total radiation source; radiation losses are negative sources"""
  
	cyclotron_radiation = 201
	"""Source from cyclotron radiation; radiation losses are negative sources"""
  
	cyclotron_synchrotron_radiation = 202
	"""Source from combined cyclotron and synchrotron radiation; radiation losses are
		negative sources"""
  
	impurity_radiation = 203
	"""Line radiation and Bremsstrahlung source; radiation losses are negative sources."""
  
	particles_to_wall = 303
	"""Particle pumping by the wall; negative source for plasma and positive source for
		the wall"""
  
	particles_to_pump = 304
	"""Particle pumping by external pump; negative source for plasma and positive
		source for the pump"""
  
	charge_exchange = 305
	"""Source from charge exchange. Charge exchange losses are negative sources"""
  
	transport = 400
	"""Source term related to transport processes"""
  
	neoclassical = 401
	"""Source term related to neoclassical processes"""
  
	equipartition = 402
	"""Equipartition due to collisions and turbulence"""
  
	turbulent_equipartition = 403
	"""Turbulent equipartition"""
  
	runaways = 501
	"""Source from run-away processes; includes both electron and ion run-away"""
  
	ionisation = 601
	"""Source from ionisation processes (not accounting for charge exchange)"""
  
	recombination = 602
	"""Source from recombination processes (not accounting for charge exchange)"""
  
	excitation = 603
	"""Source from excitation processes"""
  
	database = 801
	"""Source from database entry"""
  
	gaussian = 802
	"""Artificial source with a gaussian profile"""
  
	custom_1 = 901
	"""Custom source terms 1; content to be decided by data provided"""
  
	custom_2 = 902
	"""Custom source terms 2; content to be decided by data provided"""
  
	custom_3 = 903
	"""Custom source terms 3; content to be decided by data provided"""
  
	custom_4 = 904
	"""Custom source terms 4; content to be decided by data provided"""
  
	custom_5 = 905
	"""Custom source terms 5; content to be decided by data provided"""
  
	custom_6 = 906
	"""Custom source terms 6; content to be decided by data provided"""
  
	custom_7 = 907
	"""Custom source terms 7; content to be decided by data provided"""
  
	custom_8 = 908
	"""Custom source terms 8; content to be decided by data provided"""
  
	custom_9 = 909
	"""Custom source terms 9; content to be decided by data provided"""
  

class _T_core_sources_source_profiles_1d_particles_decomposed_3(SpTree):
	"""Source terms decomposed for the particle transport equation, assuming
		core_radial_grid 3 levels above"""

	implicit_part  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="s^-1",type="dynamic")
	""" Implicit part of the source term, i.e. to be multiplied by the equation's
		primary quantity"""

	explicit_part  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="m^-3.s^-1",type="dynamic")
	""" Explicit part of the source term"""


class _T_core_sources_source_profiles_1d_particles_decomposed_4(SpTree):
	"""Source terms decomposed for the particle transport equation, assuming
		core_radial_grid 4 levels above"""

	implicit_part  :Expression  =  sp_property(coordinate1="../../../../grid/rho_tor_norm",units="s^-1",type="dynamic")
	""" Implicit part of the source term, i.e. to be multiplied by the equation's
		primary quantity"""

	explicit_part  :Expression  =  sp_property(coordinate1="../../../../grid/rho_tor_norm",units="m^-3.s^-1",type="dynamic")
	""" Explicit part of the source term"""


class _T_core_sources_source_profiles_1d_momentum_decomposed_4(SpTree):
	"""Source terms decomposed for the momentum transport equation, assuming
		core_radial_grid 4 levels above"""

	implicit_part  :Expression  =  sp_property(coordinate1="../../../../grid/rho_tor_norm",units="s^-1",type="dynamic")
	""" Implicit part of the source term, i.e. to be multiplied by the equation's
		primary quantity"""

	explicit_part  :Expression  =  sp_property(coordinate1="../../../../grid/rho_tor_norm",units="kg.m^2.s^-2",type="dynamic")
	""" Explicit part of the source term"""


class _T_core_sources_source_profiles_1d_energy_decomposed_4(SpTree):
	"""Source terms decomposed for the energy transport equation, assuming
		core_radial_grid 4 levels above"""

	implicit_part  :Expression  =  sp_property(coordinate1="../../../../grid/rho_tor_norm",units="s^-1",type="dynamic")
	""" Implicit part of the source term, i.e. to be multiplied by the equation's
		primary quantity"""

	explicit_part  :Expression  =  sp_property(coordinate1="../../../../grid/rho_tor_norm",units="W.m^-3",type="dynamic")
	""" Explicit part of the source term"""


class _T_core_sources_source_profiles_1d_energy_decomposed_3(SpTree):
	"""Source terms decomposed for the energy transport equation, assuming
		core_radial_grid 3 levels above"""

	implicit_part  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="s^-1",type="dynamic")
	""" Implicit part of the source term, i.e. to be multiplied by the equation's
		primary quantity"""

	explicit_part  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="W.m^-3",type="dynamic")
	""" Explicit part of the source term"""


class _T_core_sources_source_profiles_1d_energy_decomposed_2(SpTree):
	"""Source terms decomposed for the energy transport equation, assuming
		core_radial_grid 2 levels above"""

	implicit_part  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="s^-1",type="dynamic")
	""" Implicit part of the source term, i.e. to be multiplied by the equation's
		primary quantity"""

	explicit_part  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="W.m^-3",type="dynamic")
	""" Explicit part of the source term"""


class _T_core_sources_source_global_electrons(SpTree):
	"""Source terms related to electrons"""

	particles  :float =  sp_property(units="s^-1",type="dynamic")
	""" Electron particle source"""

	power  :float =  sp_property(units="W",type="dynamic")
	""" Power coupled to electrons"""


class _T_core_sources_source_profiles_1d_neutral_state(SpTree):
	"""Source terms related to the a given state of the neutral species"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying state"""

	vibrational_level  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Vibrational level (can be bundled)"""

	vibrational_mode  :str =  sp_property(type="dynamic")
	""" Vibrational mode of this state, e.g. _A_g_. Need to define, or adopt a standard
		nomenclature."""

	neutral_type  :_E_neutrals_identifier =  sp_property(doc_identifier="utilities/neutrals_identifier.xml")
	""" Neutral type (if the considered state is a neutral), in terms of energy. ID =1:
		cold; 2: thermal; 3: fast; 4: NBI"""

	electron_configuration  :str =  sp_property(type="dynamic")
	""" Configuration of atomic orbitals of this state, e.g. 1s2-2s1"""

	particles  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="s^-1.m^-3",type="dynamic")
	""" Source term for the state density transport equation"""

	energy  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="W.m^-3",type="dynamic")
	""" Source terms for the state energy transport equation"""


class _T_core_sources_source_profiles_1d_components_2(SpTree):
	"""Source terms for vector components in predefined directions, assuming
		core_radial_grid 2 levels above"""

	radial  :Expression  =  sp_property(type="dynamic",coordinate1="../../../grid/rho_tor_norm",units="kg.m^-1.s^-2")
	""" Radial component"""

	diamagnetic  :Expression  =  sp_property(type="dynamic",coordinate1="../../../grid/rho_tor_norm",units="kg.m^-1.s^-2")
	""" Diamagnetic component"""

	parallel  :Expression  =  sp_property(type="dynamic",coordinate1="../../../grid/rho_tor_norm",units="kg.m^-1.s^-2")
	""" Parallel component"""

	poloidal  :Expression  =  sp_property(type="dynamic",coordinate1="../../../grid/rho_tor_norm",units="kg.m^-1.s^-2")
	""" Poloidal component"""

	toroidal  :Expression  =  sp_property(type="dynamic",coordinate1="../../../grid/rho_tor_norm",units="kg.m^-1.s^-2")
	""" Toroidal component"""

	toroidal_decomposed  :_T_core_sources_source_profiles_1d_momentum_decomposed_4 =  sp_property()
	""" Decomposition of the source term for ion toroidal momentum equation into
		implicit and explicit parts"""


class _T_core_sources_source_profiles_1d_ions_charge_states(SpTree):
	"""Source terms related to the a given state of the ion species"""

	z_min  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Minimum Z of the charge state bundle"""

	z_max  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Maximum Z of the charge state bundle"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying charge state (e.g. C+, C+2 , C+3, C+4, C+5, C+6, ...)"""

	vibrational_level  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Vibrational level (can be bundled)"""

	vibrational_mode  :str =  sp_property(type="dynamic")
	""" Vibrational mode of this state, e.g. _A_g_. Need to define, or adopt a standard
		nomenclature."""

	electron_configuration  :str =  sp_property(type="dynamic")
	""" Configuration of atomic orbitals of this state, e.g. 1s2-2s1"""

	particles  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="s^-1.m^-3",type="dynamic")
	""" Source term for the charge state density transport equation"""

	particles_decomposed  :_T_core_sources_source_profiles_1d_particles_decomposed_4 =  sp_property()
	""" Decomposition of the source term for state density equation into implicit and
		explicit parts"""

	energy  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="W.m^-3",type="dynamic")
	""" Source terms for the charge state energy transport equation"""

	energy_decomposed  :_T_core_sources_source_profiles_1d_energy_decomposed_4 =  sp_property()
	""" Decomposition of the source term for state energy equation into implicit and
		explicit parts"""


class _T_core_sources_source_profiles_1d_electrons(SpTree):
	"""Source terms related to electrons"""

	particles  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="m^-3.s^-1",type="dynamic")
	""" Source term for electron density equation"""

	particles_decomposed  :_T_core_sources_source_profiles_1d_particles_decomposed_3 =  sp_property()
	""" Decomposition of the source term for electron density equation into implicit and
		explicit parts"""

	particles_inside  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="s^-1",type="dynamic")
	""" Electron source inside the flux surface. Cumulative volume integral of the
		source term for the electron density equation."""

	energy  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="W.m^-3",type="dynamic")
	""" Source term for the electron energy equation"""

	energy_decomposed  :_T_core_sources_source_profiles_1d_energy_decomposed_3 =  sp_property()
	""" Decomposition of the source term for electron energy equation into implicit and
		explicit parts"""

	power_inside  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="W",type="dynamic")
	""" Power coupled to electrons inside the flux surface. Cumulative volume integral
		of the source term for the electron energy equation"""


class _T_core_sources_source_global(SpTree):
	"""Source global quantities for a given time slice"""

	power  :float =  sp_property(units="W",type="dynamic")
	""" Total power coupled to the plasma"""

	total_ion_particles  :float =  sp_property(units="(ions).s^-1",type="dynamic")
	""" Total ion particle source (summed over ion species)"""

	total_ion_power  :float =  sp_property(units="W",type="dynamic")
	""" Total power coupled to ion species (summed over ion species)"""

	electrons  :_T_core_sources_source_global_electrons =  sp_property()
	""" Sources for electrons"""

	torque_tor  :float =  sp_property(units="kg.m^2.s^-2",type="dynamic")
	""" Toroidal torque"""

	current_parallel  :float =  sp_property(units="A",type="dynamic")
	""" Parallel current driven"""


class _T_core_sources_source_profiles_1d_neutral(SpTree):
	"""Source terms related to a given neutral species"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying the neutral species (e.g. H, D, T, He, C, ...)"""

	ion_index  :int =  sp_property(type="dynamic")
	""" Index of the corresponding ion species in the ../../ion array"""

	particles  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="s^-1.m^-3",type="dynamic")
	""" Source term for neutral density equation"""

	energy  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="W.m^-3",type="dynamic")
	""" Source term for the neutral energy transport equation."""

	multiple_states_flag  :int =  sp_property(type="dynamic")
	""" Multiple states calculation flag : 0-Only one state is considered; 1-Multiple
		states are considered and are described in the state structure"""

	state  :AoS[_T_core_sources_source_profiles_1d_neutral_state] =  sp_property(coordinate1="1...N")
	""" Source terms related to the different charge states of the species (energy,
		excitation, ...)"""


class _T_core_sources_source_profiles_1d_ions(SpTree):
	"""Source terms related to a given ion species"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	z_ion  :float =  sp_property(type="dynamic",units="Elementary Charge Unit")
	""" Ion charge (of the dominant ionisation state; lumped ions are allowed)"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying ion (e.g. H, D, T, He, C, D2, ...)"""

	neutral_index  :int =  sp_property(type="dynamic")
	""" Index of the corresponding neutral species in the ../../neutral array"""

	particles  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="s^-1.m^-3",type="dynamic")
	""" Source term for ion density equation"""

	particles_decomposed  :_T_core_sources_source_profiles_1d_particles_decomposed_3 =  sp_property()
	""" Decomposition of the source term for ion density equation into implicit and
		explicit parts"""

	energy  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="W.m^-3",type="dynamic")
	""" Source term for the ion energy transport equation."""

	energy_decomposed  :_T_core_sources_source_profiles_1d_energy_decomposed_3 =  sp_property()
	""" Decomposition of the source term for ion energy equation into implicit and
		explicit parts"""

	momentum  :_T_core_sources_source_profiles_1d_components_2 =  sp_property()
	""" Source term for the ion momentum transport equations along various components
		(directions)"""

	multiple_states_flag  :int =  sp_property(type="dynamic")
	""" Multiple states calculation flag : 0-Only the 'ion' level is considered and the
		'state' array of structure is empty; 1-Ion states are considered and are
		described in the 'state' array of structure"""

	state  :AoS[_T_core_sources_source_profiles_1d_ions_charge_states] =  sp_property(coordinate1="1...N")
	""" Source terms related to the different charge states of the species (ionisation,
		energy, excitation, ...)"""


class _T_core_sources_source_profiles_1d(SpTree):
	"""Source terms for a given time slice"""

	grid  :_T_core_radial_grid =  sp_property()
	""" Radial grid"""

	electrons  :_T_core_sources_source_profiles_1d_electrons =  sp_property()
	""" Sources for electrons"""

	total_ion_energy  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="W.m^-3",type="dynamic")
	""" Source term for the total (summed over ion species) energy equation"""

	total_ion_energy_decomposed  :_T_core_sources_source_profiles_1d_energy_decomposed_2 =  sp_property()
	""" Decomposition of the source term for total ion energy equation into implicit and
		explicit parts"""

	total_ion_power_inside  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="W",type="dynamic")
	""" Total power coupled to ion species (summed over ion species) inside the flux
		surface. Cumulative volume integral of the source term for the total ion energy
		equation"""

	momentum_tor  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="kg.m^-1.s^-2",type="dynamic")
	""" Source term for total toroidal momentum equation"""

	torque_tor_inside  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="kg.m^2.s^-2",type="dynamic")
	""" Toroidal torque inside the flux surface. Cumulative volume integral of the
		source term for the total toroidal momentum equation"""

	momentum_tor_j_cross_b_field  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="kg.m^-1.s^-2",type="dynamic")
	""" Contribution to the toroidal momentum source term (already included in the
		momentum_tor node) corresponding to the toroidal torques onto the thermal plasma
		due to Lorentz force associated with radial currents. These currents appear as
		return-currents (enforcing quasi-neutrality, div(J)=0) balancing radial currents
		of non-thermal particles, e.g. radial currents of fast and trapped
		neutral-beam-ions."""

	j_parallel  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="A.m^-2",type="dynamic")
	""" Parallel current density source, average(J.B) / B0, where B0 =
		core_sources/vacuum_toroidal_field/b0"""

	current_parallel_inside  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="A",type="dynamic")
	""" Parallel current driven inside the flux surface. Cumulative surface integral of
		j_parallel"""

	conductivity_parallel  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="ohm^-1.m^-1",type="dynamic")
	""" Parallel conductivity due to this source"""

	ion  :AoS[_T_core_sources_source_profiles_1d_ions] =  sp_property(coordinate1="1...N")
	""" Source terms related to the different ions species, in the sense of isonuclear
		or isomolecular sequences. Ionisation states (and other types of states) must be
		differentiated at the state level below"""

	neutral  :AoS[_T_core_sources_source_profiles_1d_neutral] =  sp_property(coordinate1="1...N")
	""" Source terms related to the different neutral species"""


class _T_core_sources_source(Module):
	"""Source terms for a given actuator"""

	identifier  :_E_core_source =  sp_property(doc_identifier="core_sources/core_source_identifier.xml")
	""" Source term identifier (process causing this source term)"""

	species  :_T_distribution_species =  sp_property()
	""" Species causing this source term (if relevant, e.g. a particular ion or neutral
		state in case of line radiation)"""

	global_quantities  :TimeSeriesAoS[_T_core_sources_source_global] =  sp_property(coordinate1="time",type="dynamic")
	""" Total source quantities integrated over the plasma volume or surface"""

	profiles_1d  :TimeSeriesAoS[_T_core_sources_source_profiles_1d] =  sp_property(coordinate1="time",type="dynamic",cocos_alias="IDSPATH",cocos_replace="core_sources.source{i}.profiles_1d{j}")
	""" Source profiles for various time slices. Source terms are positive (resp.
		negative) when there is a gain (resp. a loss) to the considered channel."""


class _T_core_sources(IDS):
	"""Core plasma thermal source terms (for the transport equations of the thermal
		species). Energy terms correspond to the full kinetic energy equation (i.e. the
		energy flux takes into account the energy transported by the particle flux)
	lifecycle_status: active
	lifecycle_version: 3.1.0
	lifecycle_last_change: 3.31.0
	specific_validation_rules: yes"""

	dd_version="v3_38_1_dirty"
	ids_name="core_sources"

	vacuum_toroidal_field  :_T_b_tor_vacuum_1 =  sp_property(cocos_alias="IDSPATH",cocos_replace="core_sources.vacuum_toroidal_field")
	""" Characteristics of the vacuum toroidal field (used in Rho_Tor definition and in
		the normalization of current densities)"""

	source  :AoS[_T_core_sources_source] =  sp_property(coordinate1="1...N",appendable_by_appender_actor="yes")
	""" Set of source terms"""
