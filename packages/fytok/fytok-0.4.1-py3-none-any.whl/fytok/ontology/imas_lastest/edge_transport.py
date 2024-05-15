"""
  This module containes the _FyTok_ wrapper of IMAS/dd/edge_transport
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_generic_grid_scalar,_T_generic_grid_vector_components,_T_identifier_dynamic_aos3,_T_plasma_composition_neutral_element,_T_generic_grid_scalar_single_position,_T_identifier,_T_code_with_timebase,_T_identifier_static,_T_generic_grid_aos3_root
from .utilities import _E_midplane_identifier

class _E_edge_transport(IntFlag):
	"""Translation table for different types of transport coefficients.	xpath: 	"""
  
	unspecified = 0
	"""Unspecified transport type"""
  
	combined = 1
	"""Combination of data from all available transport models"""
  
	combined_radial = 100
	"""Combination of data from all available radial transport models"""
  
	background_radial = 101
	"""Background radial transport level"""
  
	database_radial = 102
	"""Radial transport specified by a database entry"""
  
	prescribed_radial = 103
	"""Radial transport model prescribed from code input parameters"""
  
	combined_parallel = 200
	"""Combination of data from all available radial transport models"""
  
	background_parallel = 201
	"""Background radial transport level"""
  
	database_parallel = 202
	"""Radial transport specified by a database entry"""
  
	prescribed_parallel = 203
	"""Radial transport model prescribed from code input parameters"""
  
	twenty_one_moment_parallel = 204
	"""21 moment fluid closure model"""
  
	braginskii_parallel = 205
	"""Braginskii fluid transport model"""
  

class _T_edge_transport_model_energy(SpTree):
	"""Transport coefficients for energy equations."""

	d  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="m^2.s^-1")
	""" Effective diffusivity, on various grid subsets"""

	v  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="m.s^-1")
	""" Effective convection, on various grid subsets"""

	flux  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="W.m^-2")
	""" Flux, on various grid subsets"""

	flux_limiter  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="-")
	""" Flux limiter coefficient, on various grid subsets"""


class _T_edge_transport_model_momentum(SpTree):
	"""Transport coefficients for momentum equations."""

	d  :AoS[_T_generic_grid_vector_components] =  sp_property(coordinate1="1...N",units="m^2.s^-1")
	""" Effective diffusivity, on various grid subsets"""

	v  :AoS[_T_generic_grid_vector_components] =  sp_property(coordinate1="1...N",units="m.s^-1")
	""" Effective convection, on various grid subsets"""

	flux  :AoS[_T_generic_grid_vector_components] =  sp_property(coordinate1="1...N",units="kg.m^-1.s^-2")
	""" Flux, on various grid subsets"""

	flux_limiter  :AoS[_T_generic_grid_vector_components] =  sp_property(coordinate1="1...N",units="-")
	""" Flux limiter coefficient, on various grid subsets"""


class _T_edge_transport_model_density(SpTree):
	"""Transport coefficients for energy equations."""

	d  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="m^2.s^-1")
	""" Effective diffusivity, on various grid subsets"""

	v  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="m.s^-1")
	""" Effective convection, on various grid subsets"""

	flux  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="m^-2.s^-1")
	""" Flux, on various grid subsets"""

	flux_limiter  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="-")
	""" Flux limiter coefficient, on various grid subsets"""


class _T_edge_transport_model_ggd_fast_neutral(SpTree):
	"""Transport coefficients related to a given neutral species (fast sampled data)"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying neutral (e.g. H, D, T, He, C, ...)"""

	ion_index  :int =  sp_property(type="dynamic")
	""" Index of the corresponding ion species in the ../../ion array"""

	particle_flux_integrated  :AoS[_T_generic_grid_scalar_single_position] =  sp_property(coordinate1="1...N",units="s^-1")
	""" Total number of particles of this species crossing a surface per unit time, for
		various surfaces (grid subsets)"""


class _T_edge_transport_model_ggd_fast_ion(SpTree):
	"""Transport coefficients related to a given ion species (fast sampled data)"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	z_ion  :float =  sp_property(type="dynamic",units="Elementary Charge Unit")
	""" Ion charge (of the dominant ionisation state; lumped ions are allowed)"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying ion (e.g. H, D, T, He, C, D2, ...)"""

	neutral_index  :int =  sp_property(type="dynamic")
	""" Index of the corresponding neutral species in the ../../neutral array"""

	particle_flux_integrated  :AoS[_T_generic_grid_scalar_single_position] =  sp_property(coordinate1="1...N",units="s^-1")
	""" Total number of particles of this species crossing a surface per unit time, for
		various surfaces (grid subsets)"""


class _T_edge_transport_model_ggd_fast_electrons(SpTree):
	"""Transport coefficients related to electrons (fast sampled data)"""

	particle_flux_integrated  :AoS[_T_generic_grid_scalar_single_position] =  sp_property(coordinate1="1...N",units="s^-1")
	""" Total number of particles of this species crossing a surface per unit time, for
		various surfaces (grid subsets)"""

	power  :AoS[_T_generic_grid_scalar_single_position] =  sp_property(coordinate1="1...N",units="W")
	""" Power carried by this species crossing a surface, for various surfaces (grid
		subsets)"""


class _T_edge_transport_model_neutral_state(SpTree):
	"""Transport coefficients related to a given state of the neutral species"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying state"""

	vibrational_level  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Vibrational level (can be bundled)"""

	vibrational_mode  :str =  sp_property(type="dynamic")
	""" Vibrational mode of this state, e.g. _A_g_. Need to define, or adopt a standard
		nomenclature."""

	neutral_type  :_T_identifier_dynamic_aos3 =  sp_property()
	""" Neutral type, in terms of energy. ID =1: cold; 2: thermal; 3: fast; 4: NBI"""

	electron_configuration  :str =  sp_property(type="dynamic")
	""" Configuration of atomic orbitals of this state, e.g. 1s2-2s1"""

	particles  :_T_edge_transport_model_density =  sp_property()
	""" Transport quantities related to density equation of the state considered
		(thermal+non-thermal)"""

	energy  :_T_edge_transport_model_energy =  sp_property()
	""" Transport quantities related to the energy equation of the state considered"""

	momentum  :_T_edge_transport_model_momentum =  sp_property()
	""" Transport coefficients related to the momentum equations of the state
		considered. The various components two levels below this node refer to the
		momentum vector components, while their flux is given in the direction
		perpendicular to the edges or faces of the grid."""


class _T_edge_transport_model_ion_state(SpTree):
	"""Transport coefficients related to a given state of the ion species"""

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

	particles  :_T_edge_transport_model_density =  sp_property()
	""" Transport quantities related to density equation of the state considered
		(thermal+non-thermal)"""

	energy  :_T_edge_transport_model_energy =  sp_property()
	""" Transport quantities related to the energy equation of the state considered"""

	momentum  :_T_edge_transport_model_momentum =  sp_property()
	""" Transport coefficients related to the momentum equations of the state
		considered. The various components two levels below this node refer to the
		momentum vector components, while their flux is given in the direction
		perpendicular to the edges or faces of the grid."""


class _T_edge_transport_model_electrons(SpTree):
	"""Transport coefficients related to electrons"""

	particles  :_T_edge_transport_model_density =  sp_property()
	""" Transport quantities for the electron density equation"""

	energy  :_T_edge_transport_model_energy =  sp_property()
	""" Transport quantities for the electron energy equation"""


class _T_edge_transport_model_ggd_fast(TimeSlice):
	"""Transport coefficient given on the ggd at a given time slice (fast sampled data)"""

	electrons  :_T_edge_transport_model_ggd_fast_electrons =  sp_property()
	""" Transport quantities and flux integrals related to the electrons"""

	ion  :AoS[_T_edge_transport_model_ggd_fast_ion] =  sp_property(coordinate1="1...N")
	""" Transport coefficients and flux integrals related to the various ion species, in
		the sense of isonuclear or isomolecular sequences. Ionisation states (and other
		types of states) must be differentiated at the state level below"""

	neutral  :AoS[_T_edge_transport_model_ggd_fast_neutral] =  sp_property(coordinate1="1...N")
	""" Transport coefficients and flux integrals related to the various ion and neutral
		species"""

	power_ion_total  :AoS[_T_generic_grid_scalar_single_position] =  sp_property(coordinate1="1...N",units="W")
	""" Power carried by all ions (sum over ions species) crossing a surface, for
		various surfaces (grid subsets)"""

	energy_flux_max  :AoS[_T_generic_grid_scalar_single_position] =  sp_property(coordinate1="1...N",units="W.m^-2")
	""" Maximum power density over a surface, for various surfaces (grid subsets)"""

	power  :AoS[_T_generic_grid_scalar_single_position] =  sp_property(coordinate1="1...N",units="W")
	""" Power (sum over all species) crossing a surface, for various surfaces (grid
		subsets)"""


class _T_edge_transport_model_neutral(SpTree):
	"""Transport coefficients related to a given neutral species"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying neutral (e.g. H, D, T, He, C, ...)"""

	ion_index  :int =  sp_property(type="dynamic")
	""" Index of the corresponding ion species in the ../../ion array"""

	particles  :_T_edge_transport_model_density =  sp_property()
	""" Transport related to the ion density equation"""

	energy  :_T_edge_transport_model_energy =  sp_property()
	""" Transport coefficients related to the ion energy equation"""

	momentum  :_T_edge_transport_model_momentum =  sp_property()
	""" Transport coefficients for the neutral momentum equations. The various
		components two levels below this node refer to the momentum vector components,
		while their flux is given in the direction perpendicular to the edges or faces
		of the grid."""

	multiple_states_flag  :int =  sp_property(type="dynamic")
	""" Multiple states calculation flag : 0-Only one state is considered; 1-Multiple
		states are considered and are described in the state structure"""

	state  :AoS[_T_edge_transport_model_neutral_state] =  sp_property(coordinate1="1...N")
	""" Transport coefficients related to the different states of the species"""


class _T_edge_transport_model_ion(SpTree):
	"""Transport coefficients related to a given ion species"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	z_ion  :float =  sp_property(type="dynamic",units="Elementary Charge Unit")
	""" Ion charge (of the dominant ionisation state; lumped ions are allowed)"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying ion (e.g. H, D, T, He, C, D2, ...)"""

	neutral_index  :int =  sp_property(type="dynamic")
	""" Index of the corresponding neutral species in the ../../neutral array"""

	particles  :_T_edge_transport_model_density =  sp_property()
	""" Transport related to the ion density equation"""

	energy  :_T_edge_transport_model_energy =  sp_property()
	""" Transport coefficients related to the ion energy equation"""

	momentum  :_T_edge_transport_model_momentum =  sp_property()
	""" Transport coefficients for the ion momentum equations. The various components
		two levels below this node refer to the momentum vector components, while their
		flux is given in the direction perpendicular to the edges or faces of the grid."""

	multiple_states_flag  :int =  sp_property(type="dynamic")
	""" Multiple states calculation flag : 0-Only the 'ion' level is considered and the
		'state' array of structure is empty; 1-Ion states are considered and are
		described in the 'state' array of structure"""

	state  :AoS[_T_edge_transport_model_ion_state] =  sp_property(coordinate1="1...N")
	""" Transport coefficients related to the different states of the species"""


class _T_edge_transport_model_ggd(TimeSlice):
	"""Transport coefficient given on the ggd at a given time slice"""

	conductivity  :AoS[_T_generic_grid_vector_components] =  sp_property(coordinate1="1...N",units="ohm^-1.m^-1")
	""" Conductivity, on various grid subsets"""

	electrons  :_T_edge_transport_model_electrons =  sp_property()
	""" Transport quantities related to the electrons"""

	total_ion_energy  :_T_edge_transport_model_energy =  sp_property()
	""" Transport coefficients for the total (summed over ion species) energy equation"""

	momentum  :_T_edge_transport_model_momentum =  sp_property()
	""" Transport coefficients for total momentum equation. The various components two
		levels below this node refer to the momentum vector components, while their flux
		is given in the direction perpendicular to the edges or faces of the grid."""

	ion  :AoS[_T_edge_transport_model_ion] =  sp_property(coordinate1="1...N")
	""" Transport coefficients related to the various ion species, in the sense of
		isonuclear or isomolecular sequences. Ionisation states (and other types of
		states) must be differentiated at the state level below"""

	neutral  :AoS[_T_edge_transport_model_neutral] =  sp_property(coordinate1="1...N")
	""" Transport coefficients related to the various neutral species"""


class _T_edge_transport_model(Module):
	"""Transport coefficients for a given model"""

	identifier  :_E_edge_transport =  sp_property(doc_identifier="edge_transport/edge_transport_identifier.xml")
	""" Transport model identifier"""

	flux_multiplier  :float =  sp_property(type="constant",units="-")
	""" Multiplier applied to the particule flux when adding its contribution in the
		expression of the heat flux : can be 0, 3/2 or 5/2"""

	ggd  :TimeSeriesAoS[_T_edge_transport_model_ggd] =  sp_property(coordinate1="time",type="dynamic")
	""" Transport coefficients represented using the general grid description, for
		various time slices. Fluxes are given in the direction perpendicular to the
		edges or faces of the grid (flow crossing that surface divided by its actual
		area). Radial fluxes are positive when they are directed away from the magnetic
		axis. Poloidal fluxes are positive when they are directed in such a way that
		they travel clockwise around the magnetic axis (poloidal plane viewed such that
		the centerline of the tokamak is on the left). Parallel fluxes are positive when
		they are co-directed with the magnetic field. Toroidal fluxes are positive if
		travelling counter-clockwise when looking at the plasma from above"""

	ggd_fast  :TimeSeriesAoS[_T_edge_transport_model_ggd_fast] =  sp_property(coordinate1="time",type="dynamic")
	""" Quantities provided at a faster sampling rate than the full ggd quantities.
		These are either integrated quantities or local quantities provided on a reduced
		set of positions. Positions and integration domains are described by a set of
		grid_subsets (of size 1 for a position)."""


class _T_edge_transport(IDS):
	"""Edge plasma transport. Energy terms correspond to the full kinetic energy
		equation (i.e. the energy flux takes into account the energy transported by the
		particle flux)
	lifecycle_status: active
	lifecycle_version: 3.22.0
	lifecycle_last_change: 3.38.1
	specific_validation_rules: yes"""

	dd_version="v3_38_1_dirty"
	ids_name="edge_transport"

	midplane  :_E_midplane_identifier =  sp_property(doc_identifier="utilities/midplane_identifier.xml",introduced_after_version="3.32.1")
	""" Choice of midplane definition (use the lowest index number if more than one
		value is relevant)"""

	grid_ggd  :TimeSeriesAoS[_T_generic_grid_aos3_root] =  sp_property(coordinate1="time",type="dynamic")
	""" Grid (using the Generic Grid Description), for various time slices. The timebase
		of this array of structure must be a subset of the ggd timebases"""

	model  :AoS[_T_edge_transport_model] =  sp_property(coordinate1="1...N_Models")
	""" Transport is described by a combination of various transport models"""
