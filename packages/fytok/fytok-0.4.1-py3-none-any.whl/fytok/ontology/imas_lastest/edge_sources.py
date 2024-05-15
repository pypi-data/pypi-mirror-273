"""
  This module containes the _FyTok_ wrapper of IMAS/dd/edge_sources
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_plasma_composition_neutral_element,_T_generic_grid_scalar_single_position,_T_identifier_dynamic_aos3,_T_generic_grid_scalar,_T_generic_grid_vector_components,_T_identifier,_T_distribution_species,_T_identifier_static,_T_generic_grid_aos3_root
from .utilities import _E_midplane_identifier

class _E_edge_source(IntFlag):
	"""Translation table for sources of particles, momentum and heat.	xpath: 	"""
  
	unspecified = 0
	"""Unspecified source type"""
  
	total = 1
	"""Combined source excluding time derivative"""
  
	total_linearized = 702
	"""Combined source (linearized) excluding time derivative"""
  
	background = 703
	"""Background source"""
  
	database = 801
	"""Source from database entry"""
  
	prescribed = 705
	"""Source prescribed from code input parameters"""
  
	time_derivative = 706
	"""Source associated with time derivative"""
  
	atomic_ionization = 707
	"""Source from atomic ionization"""
  
	molecular_ionization = 708
	"""Source from molecular ionization/dissociation"""
  
	ionization = 709
	"""Source from ionization (combined)"""
  
	recombination = 710
	"""Source from recombination"""
  
	charge_exchange = 305
	"""Source from charge exchange. Charge exchange losses are negative sources"""
  
	collisional_equipartition = 11
	"""Collisional equipartition"""
  
	ohmic = 7
	"""Source from ohmic heating"""
  
	radiation = 200
	"""Source from line + recombination assisted + bremsstrahlung"""
  
	compression = 715
	"""Internal energy source from compression"""
  
	bulk_motion = 716
	"""Internal energy source correction for bulk motion"""
  

class _T_edge_sources_source_ggd_fast_ion(SpTree):
	"""Integrated source terms related to a given ion species (fast sampled data)"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	z_ion  :float =  sp_property(type="dynamic",units="Elementary Charge Unit")
	""" Ion charge (of the dominant ionisation state; lumped ions are allowed)"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying ion (e.g. H+, D+, T+, He+2, C+, ...)"""

	neutral_index  :int =  sp_property(type="dynamic")
	""" Index of the corresponding neutral species in the ../../neutral array"""

	power  :AoS[_T_generic_grid_scalar_single_position] =  sp_property(units="W",coordinate1="1...N")
	""" Total power source or sink related to this ion species, integrated over the
		volume of the grid subset, for various grid subsets."""


class _T_edge_sources_source_ggd_neutral_state(SpTree):
	"""Source terms related to the a given state of the neutral species"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying state"""

	vibrational_level  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Vibrational level (can be bundled)"""

	vibrational_mode  :str =  sp_property(type="dynamic")
	""" Vibrational mode of this state, e.g. _A_g_. Need to define, or adopt a standard
		nomenclature."""

	electron_configuration  :str =  sp_property(type="dynamic")
	""" Configuration of atomic orbitals of this state, e.g. 1s2-2s1"""

	neutral_type  :_T_identifier_dynamic_aos3 =  sp_property()
	""" Neutral type, in terms of energy. ID =1: cold; 2: thermal; 3: fast; 4: NBI"""

	particles  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="s^-1.m^-3")
	""" Source term for the state density transport equation"""

	energy  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="W.m^-3")
	""" Source terms for the state energy transport equation"""

	momentum  :AoS[_T_generic_grid_vector_components] =  sp_property(coordinate1="1...N",units="kg.m^-1.s^-2")
	""" Source term for momentum equations, on various grid subsets"""


class _T_edge_sources_source_ggd_ion_state(SpTree):
	"""Source terms related to the a given state of the ion species"""

	z_min  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Minimum Z of the state bundle"""

	z_max  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Maximum Z of the state bundle"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying state (e.g. C+, C+2 , C+3, C+4, C+5, C+6, ...)"""

	vibrational_level  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Vibrational level (can be bundled)"""

	vibrational_mode  :str =  sp_property(type="dynamic")
	""" Vibrational mode of this state, e.g. _A_g_. Need to define, or adopt a standard
		nomenclature."""

	electron_configuration  :str =  sp_property(type="dynamic")
	""" Configuration of atomic orbitals of this state, e.g. 1s2-2s1"""

	particles  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="s^-1.m^-3")
	""" Source term for the state density transport equation"""

	energy  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="W.m^-3")
	""" Source terms for the state energy transport equation"""

	momentum  :AoS[_T_generic_grid_vector_components] =  sp_property(coordinate1="1...N",units="kg.m^-1.s^-2")
	""" Source term for momentum equations, on various grid subsets"""


class _T_edge_sources_source_ggd_electrons(SpTree):
	"""Source terms related to electrons"""

	particles  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="m^-3.s^-1")
	""" Source term for electron density equation, given on various grid subsets"""

	energy  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="W.m^-3")
	""" Source term for the electron energy equation, given on various grid subsets"""


class _T_edge_sources_source_ggd_fast(TimeSlice):
	"""Integrated source terms given on the ggd at a given time slice (fast sampled
		data)"""

	ion  :AoS[_T_edge_sources_source_ggd_fast_ion] =  sp_property(coordinate1="1...N")
	""" Source term integrals related to the various ion species"""


class _T_edge_sources_source_ggd_ion(SpTree):
	"""Source terms related to a given ion species"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	z_ion  :float =  sp_property(type="dynamic",units="Elementary Charge Unit")
	""" Ion charge (of the dominant ionisation state; lumped ions are allowed)"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying ion (e.g. H, D, T, He, C, D2, ...)"""

	neutral_index  :int =  sp_property(type="dynamic")
	""" Index of the corresponding neutral species in the ../../neutral array"""

	particles  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="s^-1.m^-3")
	""" Source term for ion density equation, on various grid subsets"""

	energy  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="W.m^-3")
	""" Source term for the ion energy transport equation, on various grid subsets"""

	momentum  :AoS[_T_generic_grid_vector_components] =  sp_property(coordinate1="1...N",units="kg.m^-1.s^-2")
	""" Source term for momentum equations (sum over states when multiple states are
		considered), on various grid subsets"""

	multiple_states_flag  :int =  sp_property(type="dynamic")
	""" Multiple states calculation flag : 0-Only the 'ion' level is considered and the
		'state' array of structure is empty; 1-Ion states are considered and are
		described in the 'state' array of structure"""

	state  :AoS[_T_edge_sources_source_ggd_ion_state] =  sp_property(coordinate1="1...N")
	""" Source terms related to the different states of the species (ionisation, energy,
		excitation, ...)"""


class _T_edge_sources_source_ggd_neutral(SpTree):
	"""Source terms related to a given neutral species"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying neutral (e.g. H, D, T, He, C, ...)"""

	ion_index  :int =  sp_property(type="dynamic")
	""" Index of the corresponding ion species in the ../../ion array"""

	particles  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="s^-1.m^-3")
	""" Source term for ion density equation, on various grid subsets"""

	energy  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="W.m^-3")
	""" Source term for the ion energy transport equation, on various grid subsets"""

	momentum  :AoS[_T_generic_grid_vector_components] =  sp_property(coordinate1="1...N",units="kg.m^-1.s^-2")
	""" Source term for momentum equations (sum over states when multiple states are
		considered), on various grid subsets"""

	multiple_states_flag  :int =  sp_property(type="dynamic")
	""" Multiple states calculation flag : 0-Only one state is considered; 1-Multiple
		states are considered and are described in the state structure"""

	state  :AoS[_T_edge_sources_source_ggd_neutral_state] =  sp_property(coordinate1="1...N")
	""" Source terms related to the different states of the species (energy, excitation,
		...)"""


class _T_edge_sources_source_ggd(TimeSlice):
	"""Source terms for a given time slice"""

	electrons  :_T_edge_sources_source_ggd_electrons =  sp_property()
	""" Sources for electrons"""

	ion  :AoS[_T_edge_sources_source_ggd_ion] =  sp_property(coordinate1="1...N")
	""" Source terms related to the different ion species, in the sense of isonuclear or
		isomolecular sequences. Ionisation states (and other types of states) must be
		differentiated at the state level below"""

	neutral  :AoS[_T_edge_sources_source_ggd_neutral] =  sp_property(coordinate1="1...N")
	""" Source terms related to the different neutral species"""

	total_ion_energy  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="W.m^-3")
	""" Source term for the total (summed over ion species) energy equation, on various
		grid subsets"""

	momentum  :AoS[_T_generic_grid_vector_components] =  sp_property(coordinate1="1...N",units="kg.m^-1.s^-2")
	""" Source term for total momentum equations, on various grid subsets"""

	current  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="A.m^-2")
	""" Current density source"""


class _T_edge_sources_source(SpTree):
	"""Source terms for a given actuator"""

	identifier  :_E_edge_source =  sp_property(doc_identifier="edge_sources/edge_source_identifier.xml")
	""" Source term identifier (process causing this source term)"""

	species  :_T_distribution_species =  sp_property()
	""" Species causing this source term (if relevant, e.g. a particular ion or neutral
		state in case of line radiation)"""

	ggd  :TimeSeriesAoS[_T_edge_sources_source_ggd] =  sp_property(coordinate1="time",type="dynamic")
	""" Source terms represented using the general grid description, for various time
		slices"""

	ggd_fast  :TimeSeriesAoS[_T_edge_sources_source_ggd_fast] =  sp_property(coordinate1="time",type="dynamic")
	""" Quantities provided at a faster sampling rate than the full ggd quantities.
		These are either integrated quantities or local quantities provided on a reduced
		set of positions. Positions and integration domains are described by a set of
		grid_subsets (of size 1 for a position)."""


class _T_edge_sources(IDS):
	"""Edge plasma sources. Energy terms correspond to the full kinetic energy equation
		(i.e. the energy flux takes into account the energy transported by the particle
		flux)
	lifecycle_status: active
	lifecycle_version: 3.22.0
	lifecycle_last_change: 3.38.1
	specific_validation_rules: yes"""

	dd_version="v3_38_1_dirty"
	ids_name="edge_sources"

	midplane  :_E_midplane_identifier =  sp_property(doc_identifier="utilities/midplane_identifier.xml",introduced_after_version="3.32.1")
	""" Choice of midplane definition (use the lowest index number if more than one
		value is relevant)"""

	grid_ggd  :TimeSeriesAoS[_T_generic_grid_aos3_root] =  sp_property(coordinate1="time",type="dynamic")
	""" Grid (using the Generic Grid Description), for various time slices. The timebase
		of this array of structure must be a subset of the ggd timebases"""

	source  :AoS[_T_edge_sources_source] =  sp_property(coordinate1="1...N")
	""" Set of source terms"""
