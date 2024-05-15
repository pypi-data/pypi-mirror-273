"""
  This module containes the _FyTok_ wrapper of IMAS/dd/core_transport
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_identifier_dynamic_aos3,_T_plasma_composition_neutral_element,_T_core_radial_grid,_T_identifier,_T_code_with_timebase,_T_b_tor_vacuum_1

class _E_core_transport_identifier(IntFlag):
	"""Translation table for different types of transport coefficients.	xpath: 	"""
  
	unspecified = 0
	"""Unspecified transport type"""
  
	combined = 1
	"""Combination of data from available transport models. Representation of the total
		transport in the system"""
  
	transport_solver = 2
	"""Output from a transport solver"""
  
	background = 3
	"""Background transport level, ad-hoc transport model not directly related to a
		physics model"""
  
	database = 4
	"""Transport specified by a database entry external to the dynamic evolution of the
		plasma"""
  
	neoclassical = 5
	"""Neoclassical"""
  
	anomalous = 6
	"""Representation of turbulent transport"""
  
	mhd = 19
	"""Transport arising from MHD frequency modes"""
  
	ntm = 20
	"""Transport arising from the presence of NTMs"""
  
	sawteeth = 21
	"""Transport arising from the presence of sawteeth"""
  
	elm_continuous = 22
	"""Continuous ELM model --- gives the ELM averaged profile"""
  
	elm_resolved = 23
	"""Time resolved ELM model"""
  
	pedestal = 24
	"""Transport level to give edge pedestal"""
  
	not_provided = 25
	"""No data provided"""
  

class _T_core_transport_model_1_density(SpTree):
	"""Transport coefficients for density equations. Coordinates one level above."""

	d  :Expression  =  sp_property(coordinate1="../../grid_d/rho_tor_norm",units="m^2.s^-1",type="dynamic")
	""" Effective diffusivity"""

	v  :Expression  =  sp_property(coordinate1="../../grid_v/rho_tor_norm",units="m.s^-1",type="dynamic")
	""" Effective convection"""

	flux  :Expression  =  sp_property(coordinate1="../../grid_flux/rho_tor_norm",units="m^-2.s^-1",type="dynamic")
	""" Flux"""


class _T_core_transport_model_1_energy(SpTree):
	"""Transport coefficients for energy equations. Coordinates one level above."""

	d  :Expression  =  sp_property(coordinate1="../../grid_d/rho_tor_norm",units="m^2.s^-1",type="dynamic")
	""" Effective diffusivity"""

	v  :Expression  =  sp_property(coordinate1="../../grid_v/rho_tor_norm",units="m.s^-1",type="dynamic")
	""" Effective convection"""

	flux  :Expression  =  sp_property(coordinate1="../../grid_flux/rho_tor_norm",units="W.m^-2",type="dynamic")
	""" Flux"""


class _T_core_transport_model_1_momentum(SpTree):
	"""Transport coefficients for momentum equations. Coordinates one level above."""

	d  :Expression  =  sp_property(coordinate1="../../grid_d/rho_tor_norm",units="m^2.s^-1",type="dynamic")
	""" Effective diffusivity"""

	v  :Expression  =  sp_property(coordinate1="../../grid_v/rho_tor_norm",units="m.s^-1",type="dynamic")
	""" Effective convection"""

	flux  :Expression  =  sp_property(coordinate1="../../grid_flux/rho_tor_norm",units="kg.m^-1.s^-2",type="dynamic")
	""" Flux"""


class _T_core_transport_model_2_density(SpTree):
	"""Transport coefficients for density equations. Coordinates two levels above."""

	d  :Expression  =  sp_property(coordinate1="../../../grid_d/rho_tor_norm",units="m^2.s^-1",type="dynamic")
	""" Effective diffusivity"""

	v  :Expression  =  sp_property(coordinate1="../../../grid_v/rho_tor_norm",units="m.s^-1",type="dynamic")
	""" Effective convection"""

	flux  :Expression  =  sp_property(coordinate1="../../../grid_flux/rho_tor_norm",units="m^-2.s^-1",type="dynamic")
	""" Flux"""


class _T_core_transport_model_2_energy(SpTree):
	"""Transport coefficients for energy equations. Coordinates two levels above."""

	d  :Expression  =  sp_property(coordinate1="../../../grid_d/rho_tor_norm",units="m^2.s^-1",type="dynamic")
	""" Effective diffusivity"""

	v  :Expression  =  sp_property(coordinate1="../../../grid_v/rho_tor_norm",units="m.s^-1",type="dynamic")
	""" Effective convection"""

	flux  :Expression  =  sp_property(coordinate1="../../../grid_flux/rho_tor_norm",units="W.m^-2",type="dynamic")
	""" Flux"""


class _T_core_transport_model_3_density(SpTree):
	"""Transport coefficients for density equations. Coordinates three levels above."""

	d  :Expression  =  sp_property(coordinate1="../../../../grid_d/rho_tor_norm",units="m^2.s^-1",type="dynamic")
	""" Effective diffusivity"""

	v  :Expression  =  sp_property(coordinate1="../../../../grid_v/rho_tor_norm",units="m.s^-1",type="dynamic")
	""" Effective convection"""

	flux  :Expression  =  sp_property(coordinate1="../../../../grid_flux/rho_tor_norm",units="m^-2.s^-1",type="dynamic")
	""" Flux"""


class _T_core_transport_model_3_energy(SpTree):
	"""Transport coefficients for energy equations. Coordinates three levels above."""

	d  :Expression  =  sp_property(coordinate1="../../../../grid_d/rho_tor_norm",units="m^2.s^-1",type="dynamic")
	""" Effective diffusivity"""

	v  :Expression  =  sp_property(coordinate1="../../../../grid_v/rho_tor_norm",units="m.s^-1",type="dynamic")
	""" Effective convection"""

	flux  :Expression  =  sp_property(coordinate1="../../../../grid_flux/rho_tor_norm",units="W.m^-2",type="dynamic")
	""" Flux"""


class _T_core_transport_model_3_momentum(SpTree):
	"""Transport coefficients for momentum equation in a given direction. Coordinates
		three levels above."""

	d  :Expression  =  sp_property(coordinate1="../../../../grid_d/rho_tor_norm",units="m^2.s^-1",type="dynamic")
	""" Effective diffusivity"""

	v  :Expression  =  sp_property(coordinate1="../../../../grid_v/rho_tor_norm",units="m.s^-1",type="dynamic")
	""" Effective convection"""

	flux  :Expression  =  sp_property(coordinate1="../../../../grid_flux/rho_tor_norm",units="kg.m^-1.s^-2",type="dynamic")
	""" Flux"""

	flow_damping_rate  :Expression  =  sp_property(coordinate1="../../../../grid_flux/rho_tor_norm",units="s^-1",type="dynamic")
	""" Damping rate for this flow component (e.g. due to collisions, calculated from a
		neoclassical model)"""


class _T_core_transport_model_4_momentum(SpTree):
	"""Transport coefficients for momentum equation in a given direction. Coordinates
		four levels above."""

	d  :Expression  =  sp_property(coordinate1="../../../../../grid_d/rho_tor_norm",units="m^2.s^-1",type="dynamic")
	""" Effective diffusivity"""

	v  :Expression  =  sp_property(coordinate1="../../../../../grid_v/rho_tor_norm",units="m.s^-1",type="dynamic")
	""" Effective convection"""

	flux  :Expression  =  sp_property(coordinate1="../../../../../grid_flux/rho_tor_norm",units="kg.m^-1.s^-2",type="dynamic")
	""" Flux"""

	flow_damping_rate  :Expression  =  sp_property(coordinate1="../../../../../grid_flux/rho_tor_norm",units="s^-1",type="dynamic")
	""" Damping rate for this flow component (e.g. due to collisions, calculated from a
		neoclassical model)"""


class _T_core_transport_model_components_3_momentum(SpTree):
	"""Transport coefficients for momentum equations on various components. Coordinates
		three levels above the leaves"""

	radial  :_T_core_transport_model_3_momentum =  sp_property()
	""" Radial component"""

	diamagnetic  :_T_core_transport_model_3_momentum =  sp_property()
	""" Diamagnetic component"""

	parallel  :_T_core_transport_model_3_momentum =  sp_property()
	""" Parallel component"""

	poloidal  :_T_core_transport_model_3_momentum =  sp_property()
	""" Poloidal component"""

	toroidal  :_T_core_transport_model_3_momentum =  sp_property()
	""" Toroidal component"""


class _T_core_transport_model_components_4_momentum(SpTree):
	"""Transport coefficients for momentum equations on various components. Coordinates
		four levels above the leaves"""

	radial  :_T_core_transport_model_4_momentum =  sp_property()
	""" Radial component"""

	diamagnetic  :_T_core_transport_model_4_momentum =  sp_property()
	""" Diamagnetic component"""

	parallel  :_T_core_transport_model_4_momentum =  sp_property()
	""" Parallel component"""

	poloidal  :_T_core_transport_model_4_momentum =  sp_property()
	""" Poloidal component"""

	toroidal  :_T_core_transport_model_4_momentum =  sp_property()
	""" Toroidal component"""


class _T_core_transport_model_neutral_state(SpTree):
	"""Transport coefficients related to the a given state of the neutral species"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying state"""

	vibrational_level  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Vibrational level (can be bundled)"""

	vibrational_mode  :str =  sp_property(type="dynamic")
	""" Vibrational mode of this state, e.g. _A_g_. Need to define, or adopt a standard
		nomenclature."""

	electron_configuration  :str =  sp_property(type="dynamic")
	""" Configuration of atomic orbitals of this state, e.g. 1s2-2s1"""

	particles  :_T_core_transport_model_3_density =  sp_property()
	""" Transport quantities related to density equation of the charge state considered
		(thermal+non-thermal)"""

	energy  :_T_core_transport_model_3_energy =  sp_property()
	""" Transport quantities related to the energy equation of the charge state
		considered"""


class _T_core_transport_model_electrons(SpTree):
	"""Transport coefficients related to electrons"""

	particles  :_T_core_transport_model_2_density =  sp_property()
	""" Transport quantities for the electron density equation"""

	energy  :_T_core_transport_model_2_energy =  sp_property()
	""" Transport quantities for the electron energy equation"""
	

class _T_core_transport_model_ions_charge_states(SpTree):
	"""Transport coefficients related to the a given state of the ion species"""

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

	particles  :_T_core_transport_model_3_density =  sp_property()
	""" Transport quantities related to density equation of the charge state considered
		(thermal+non-thermal)"""

	energy  :_T_core_transport_model_3_energy =  sp_property()
	""" Transport quantities related to the energy equation of the charge state
		considered"""

	momentum  :_T_core_transport_model_components_4_momentum =  sp_property()
	""" Transport coefficients related to the state momentum equations for various
		components (directions)"""


class _T_core_transport_model_neutral(SpTree):
	"""Transport coefficients related to a given neutral species"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying ion (e.g. H+, D+, T+, He+2, C+, ...)"""

	ion_index  :int =  sp_property(type="dynamic")
	""" Index of the corresponding ion species in the ../../ion array"""

	particles  :_T_core_transport_model_2_density =  sp_property()
	""" Transport related to the neutral density equation"""

	energy  :_T_core_transport_model_2_energy =  sp_property()
	""" Transport coefficients related to the neutral energy equation"""

	multiple_states_flag  :int =  sp_property(type="dynamic")
	""" Multiple states calculation flag : 0-Only one state is considered; 1-Multiple
		states are considered and are described in the state structure"""

	state  :AoS[_T_core_transport_model_neutral_state] =  sp_property(coordinate1="1...N")
	""" Transport coefficients related to the different states of the species"""


class _T_core_transport_model_ions(SpTree):
	"""Transport coefficients related to a given ion species"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	z_ion  :float =  sp_property(type="dynamic",units="Elementary Charge Unit")
	""" Ion charge (of the dominant ionisation state; lumped ions are allowed)"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying ion (e.g. H, D, T, He, C, D2, ...)"""

	neutral_index  :int =  sp_property(type="dynamic")
	""" Index of the corresponding neutral species in the ../../neutral array"""

	particles  :_T_core_transport_model_2_density =  sp_property()
	""" Transport related to the ion density equation"""

	energy  :_T_core_transport_model_2_energy =  sp_property()
	""" Transport coefficients related to the ion energy equation"""

	momentum  :_T_core_transport_model_components_3_momentum =  sp_property()
	""" Transport coefficients related to the ion momentum equations for various
		components (directions)"""

	multiple_states_flag  :int =  sp_property(type="dynamic")
	""" Multiple states calculation flag : 0-Only the 'ion' level is considered and the
		'state' array of structure is empty; 1-Ion states are considered and are
		described in the 'state' array of structure"""

	state  :AoS[_T_core_transport_model_ions_charge_states] =  sp_property(coordinate1="1...N")
	""" Transport coefficients related to the different states of the species"""


class _T_core_transport_model_profiles_1d(TimeSlice):
	"""Transport coefficient profiles at a given time slice"""

	grid_d  :_T_core_radial_grid =  sp_property()
	""" Grid for effective diffusivities and parallel conductivity"""

	grid_v  :_T_core_radial_grid =  sp_property()
	""" Grid for effective convections"""

	grid_flux  :_T_core_radial_grid =  sp_property()
	""" Grid for fluxes"""

	conductivity_parallel  :Expression  =  sp_property(coordinate1="../grid_d/rho_tor_norm",units="ohm^-1.m^-1",type="dynamic")
	""" Parallel conductivity"""

	electrons  :_T_core_transport_model_electrons =  sp_property()
	""" Transport quantities related to the electrons"""

	total_ion_energy  :_T_core_transport_model_1_energy =  sp_property()
	""" Transport coefficients for the total (summed over ion species) energy equation"""

	momentum_tor  :_T_core_transport_model_1_momentum =  sp_property()
	""" Transport coefficients for total toroidal momentum equation"""

	e_field_radial  :Expression  =  sp_property(coordinate1="../grid_flux/rho_tor_norm",units="V.m^-1",type="dynamic")
	""" Radial component of the electric field (calculated e.g. by a neoclassical model)"""

	ion  :AoS[_T_core_transport_model_ions] =  sp_property(coordinate1="1...N")
	""" Transport coefficients related to the various ion species, in the sense of
		isonuclear or isomolecular sequences. Ionisation states (and other types of
		states) must be differentiated at the state level below"""

	neutral  :AoS[_T_core_transport_model_neutral] =  sp_property(coordinate1="1...N")
	""" Transport coefficients related to the various neutral species"""


class _T_core_transport_model(Module):
	"""Transport coefficients for a given model"""

	comment  :str =  sp_property(type="constant")
	""" Any comment describing the model"""

	identifier  :_E_core_transport_identifier =  sp_property(doc_identifier="core_transport/core_transport_identifier.xml")
	""" Transport model identifier"""

	flux_multiplier  :float =  sp_property(type="constant",units="-")
	""" Multiplier applied to the particule flux when adding its contribution in the
		expression of the heat flux : can be 0, 3/2 or 5/2"""

	profiles_1d  :TimeSeriesAoS[_T_core_transport_model_profiles_1d] =  sp_property(coordinate1="time",type="dynamic",cocos_alias="IDSPATH",cocos_replace="core_transport.model{i}.profiles_1d{j}")
	""" Transport coefficient profiles for various time slices. Fluxes and convection
		are positive (resp. negative) when outwards i.e. towards the LCFS (resp. inwards
		i.e. towards the magnetic axes)."""


class _T_core_transport(IDS):
	"""Core plasma transport of particles, energy, momentum and poloidal flux. The
		transport of particles, energy and momentum is described by diffusion
		coefficients, D, and convection velocities, v. These are defined by the total
		fluxes of particles, energy and momentum, across a flux surface given by : V'
		[-D Y' <|grad(rho_tor_norm)|^2gt; + v Y <|grad(rho_tor_norm)|>], where Y
		represents the particles, energy and momentum density, respectively, while V is
		the volume inside a flux surface, the primes denote derivatives with respect to
		rho_tor_norm and < X > is the flux surface average of a quantity X. This
		formulation remains valid when changing simultaneously rho_tor_norm into rho_tor
		in the gradient terms and in the derivatives denoted by the prime. The average
		flux stored in the IDS as sibling of D and v is the total flux described above
		divided by the flux surface area V' <|grad(rho_tor_norm)|>. Note that the energy
		flux includes the energy transported by the particle flux.
	lifecycle_status: active
	lifecycle_version: 3.1.0
	lifecycle_last_change: 3.29.0
	specific_validation_rules: yes"""

	dd_version="v3_38_1_dirty"
	ids_name="core_transport"

	vacuum_toroidal_field  :_T_b_tor_vacuum_1 =  sp_property(cocos_alias="IDSPATH",cocos_replace="core_transport.vacuum_toroidal_field")
	""" Characteristics of the vacuum toroidal field (used in Rho_Tor definition and in
		the normalization of current densities)"""

	model  :AoS[_T_core_transport_model] =  sp_property(coordinate1="1...N",appendable_by_appender_actor="yes")
	""" Transport is described by a combination of various transport models"""
