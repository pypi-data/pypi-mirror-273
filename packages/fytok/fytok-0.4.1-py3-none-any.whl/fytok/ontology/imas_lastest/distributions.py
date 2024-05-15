"""
  This module containes the _FyTok_ wrapper of IMAS/dd/distributions
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_generic_grid_scalar,_T_generic_grid_dynamic,_T_identifier_dynamic_aos3,_T_plasma_composition_neutral_element,_T_core_radial_grid,_T_waves_coherent_wave_identifier,_T_distribution_process_identifier,_T_distribution_species,_T_distribution_markers,_T_b_tor_vacuum_1,_T_rz1d_dynamic_1

class _T_distributions_d_global_quantities_thermalised(SpTree):
	"""Global quantities for thermalisation source/sinks"""

	particles  :float =  sp_property(units="s^-1",type="dynamic")
	""" Source rate of thermal particles due to the thermalisation of fast particles"""

	power  :float =  sp_property(units="W",type="dynamic")
	""" Power input to the thermal particle population due to the thermalisation of fast
		particles"""

	torque  :float =  sp_property(units="N.m",type="dynamic")
	""" Torque input to the thermal particle population due to the thermalisation of
		fast particles"""


class _T_distributions_d_global_quantities_collisions_ion_state(SpTree):
	"""Global quantities for collisions with a given ion species state"""

	z_min  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Minimum Z of the charge state bundle (z_min = z_max = 0 for a neutral)"""

	z_max  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Maximum Z of the charge state bundle (equal to z_min if no bundle)"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying charge state (e.g. C+, C+2 , C+3, C+4, C+5, C+6, ...)"""

	electron_configuration  :str =  sp_property(type="dynamic")
	""" Configuration of atomic orbitals of this state, e.g. 1s2-2s1"""

	vibrational_level  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Vibrational level (can be bundled)"""

	vibrational_mode  :str =  sp_property(type="dynamic")
	""" Vibrational mode of this state, e.g. _A_g_. Need to define, or adopt a standard
		nomenclature."""

	power_thermal  :float =  sp_property(type="dynamic",units="W")
	""" Collisional power to the thermal particle population"""

	power_fast  :float =  sp_property(type="dynamic",units="W")
	""" Collisional power to the fast particle population"""

	torque_thermal_tor  :float =  sp_property(type="dynamic",units="N.m")
	""" Collisional toroidal torque to the thermal particle population"""

	torque_fast_tor  :float =  sp_property(type="dynamic",units="N.m")
	""" Collisional toroidal torque to the fast particle population"""


class _T_distributions_d_global_quantities_collisions_electrons(SpTree):
	"""Global quantities for collisions with electrons"""

	power_thermal  :float =  sp_property(type="dynamic",units="W")
	""" Collisional power to the thermal particle population"""

	power_fast  :float =  sp_property(type="dynamic",units="W")
	""" Collisional power to the fast particle population"""

	torque_thermal_tor  :float =  sp_property(type="dynamic",units="N.m")
	""" Collisional toroidal torque to the thermal particle population"""

	torque_fast_tor  :float =  sp_property(type="dynamic",units="N.m")
	""" Collisional toroidal torque to the fast particle population"""


class _T_distributions_d_profiles_1d_thermalised(SpTree):
	"""1D profiles of thermalisation source/sinks"""

	particles  :Expression  =  sp_property(units="s^-1.m^-3",type="dynamic",coordinate1="../../grid/rho_tor_norm")
	""" Source rate of thermal particle density due to the thermalisation of fast
		particles"""

	energy  :Expression  =  sp_property(units="W.m^-3",type="dynamic",coordinate1="../../grid/rho_tor_norm")
	""" Source rate of energy density within the thermal particle population due to the
		thermalisation of fast particles"""

	momentum_tor  :Expression  =  sp_property(units="N.m^-2",type="dynamic",coordinate1="../../grid/rho_tor_norm")
	""" Source rate of toroidal angular momentum density within the thermal particle
		population due to the thermalisation of fast particles"""


class _T_distributions_d_profiles_2d_collisions_ion_state(SpTree):
	"""2D profiles for collisions with a given ion species state"""

	z_min  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Minimum Z of the charge state bundle (z_min = z_max = 0 for a neutral)"""

	z_max  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Maximum Z of the charge state bundle (equal to z_min if no bundle)"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying charge state (e.g. C+, C+2 , C+3, C+4, C+5, C+6, ...)"""

	electron_configuration  :str =  sp_property(type="dynamic")
	""" Configuration of atomic orbitals of this state, e.g. 1s2-2s1"""

	vibrational_level  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Vibrational level (can be bundled)"""

	vibrational_mode  :str =  sp_property(type="dynamic")
	""" Vibrational mode of this state, e.g. _A_g_. Need to define, or adopt a standard
		nomenclature."""

	power_thermal  :array_type =  sp_property(type="dynamic",units="W.m^-3",coordinate1="../../../../grid/r OR ../../../../grid/rho_tor_norm",coordinate2="../../../../grid/z OR ../../../../grid/theta_geometric OR ../../../../grid/theta_straight")
	""" Collisional power density to the thermal particle population"""

	power_fast  :array_type =  sp_property(type="dynamic",units="W.m^-3",coordinate1="../../../../grid/r OR ../../../../grid/rho_tor_norm",coordinate2="../../../../grid/z OR ../../../../grid/theta_geometric OR ../../../../grid/theta_straight")
	""" Collisional power density to the fast particle population"""

	torque_thermal_tor  :array_type =  sp_property(type="dynamic",units="N.m^-2",coordinate1="../../../../grid/r OR ../../../../grid/rho_tor_norm",coordinate2="../../../../grid/z OR ../../../../grid/theta_geometric OR ../../../../grid/theta_straight")
	""" Collisional toroidal torque density to the thermal particle population"""

	torque_fast_tor  :array_type =  sp_property(type="dynamic",units="N.m^-2",coordinate1="../../../../grid/r OR ../../../../grid/rho_tor_norm",coordinate2="../../../../grid/z OR ../../../../grid/theta_geometric OR ../../../../grid/theta_straight")
	""" Collisional toroidal torque density to the fast particle population"""


class _T_distributions_d_profiles_2d_partial_collisions_ion_state(SpTree):
	"""2D profiles for collisions with a given ion species state"""

	z_min  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Minimum Z of the charge state bundle (z_min = z_max = 0 for a neutral)"""

	z_max  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Maximum Z of the charge state bundle (equal to z_min if no bundle)"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying charge state (e.g. C+, C+2 , C+3, C+4, C+5, C+6, ...)"""

	electron_configuration  :str =  sp_property(type="dynamic")
	""" Configuration of atomic orbitals of this state, e.g. 1s2-2s1"""

	vibrational_level  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Vibrational level (can be bundled)"""

	vibrational_mode  :str =  sp_property(type="dynamic")
	""" Vibrational mode of this state, e.g. _A_g_. Need to define, or adopt a standard
		nomenclature."""

	power_thermal  :array_type =  sp_property(type="dynamic",units="W.m^-3",coordinate1="../../../../../grid/r OR ../../../../../grid/rho_tor_norm",coordinate2="../../../../../grid/z OR ../../../../../grid/theta_geometric OR ../../../../../grid/theta_straight")
	""" Collisional power density to the thermal particle population"""

	power_fast  :array_type =  sp_property(type="dynamic",units="W.m^-3",coordinate1="../../../../../grid/r OR ../../../../../grid/rho_tor_norm",coordinate2="../../../../../grid/z OR ../../../../../grid/theta_geometric OR ../../../../../grid/theta_straight")
	""" Collisional power density to the fast particle population"""

	torque_thermal_tor  :array_type =  sp_property(type="dynamic",units="N.m^-2",coordinate1="../../../../../grid/r OR ../../../../../grid/rho_tor_norm",coordinate2="../../../../../grid/z OR ../../../../../grid/theta_geometric OR ../../../../../grid/theta_straight")
	""" Collisional toroidal torque density to the thermal particle population"""

	torque_fast_tor  :array_type =  sp_property(type="dynamic",units="N.m^-2",coordinate1="../../../../../grid/r OR ../../../../../grid/rho_tor_norm",coordinate2="../../../../../grid/z OR ../../../../../grid/theta_geometric OR ../../../../../grid/theta_straight")
	""" Collisional toroidal torque density to the fast particle population"""


class _T_distributions_d_profiles_2d_collisions_electrons(SpTree):
	"""2D profiles for collisions with electrons"""

	power_thermal  :array_type =  sp_property(type="dynamic",units="W.m^-3",coordinate1="../../../grid/r OR ../../../grid/rho_tor_norm",coordinate2="../../../grid/z OR ../../../grid/theta_geometric OR ../../../grid/theta_straight")
	""" Collisional power density to the thermal particle population"""

	power_fast  :array_type =  sp_property(type="dynamic",units="W.m^-3",coordinate1="../../../grid/r OR ../../../grid/rho_tor_norm",coordinate2="../../../grid/z OR ../../../grid/theta_geometric OR ../../../grid/theta_straight")
	""" Collisional power density to the fast particle population"""

	torque_thermal_tor  :array_type =  sp_property(type="dynamic",units="N.m^-2",coordinate1="../../../grid/r OR ../../../grid/rho_tor_norm",coordinate2="../../../grid/z OR ../../../grid/theta_geometric OR ../../../grid/theta_straight")
	""" Collisional toroidal torque density to the thermal particle population"""

	torque_fast_tor  :array_type =  sp_property(type="dynamic",units="N.m^-2",coordinate1="../../../grid/r OR ../../../grid/rho_tor_norm",coordinate2="../../../grid/z OR ../../../grid/theta_geometric OR ../../../grid/theta_straight")
	""" Collisional toroidal torque density to the fast particle population"""


class _T_distributions_d_profiles_2d_partial_collisions_electrons(SpTree):
	"""2D profiles for collisions with electrons"""

	power_thermal  :array_type =  sp_property(type="dynamic",units="W.m^-3",coordinate1="../../../../grid/r OR ../../../../grid/rho_tor_norm",coordinate2="../../../../grid/z OR ../../../../grid/theta_geometric OR ../../../../grid/theta_straight")
	""" Collisional power density to the thermal particle population"""

	power_fast  :array_type =  sp_property(type="dynamic",units="W.m^-3",coordinate1="../../../../grid/r OR ../../../../grid/rho_tor_norm",coordinate2="../../../../grid/z OR ../../../../grid/theta_geometric OR ../../../../grid/theta_straight")
	""" Collisional power density to the fast particle population"""

	torque_thermal_tor  :array_type =  sp_property(type="dynamic",units="N.m^-2",coordinate1="../../../../grid/r OR ../../../../grid/rho_tor_norm",coordinate2="../../../../grid/z OR ../../../../grid/theta_geometric OR ../../../../grid/theta_straight")
	""" Collisional toroidal torque density to the thermal particle population"""

	torque_fast_tor  :array_type =  sp_property(type="dynamic",units="N.m^-2",coordinate1="../../../../grid/r OR ../../../../grid/rho_tor_norm",coordinate2="../../../../grid/z OR ../../../../grid/theta_geometric OR ../../../../grid/theta_straight")
	""" Collisional toroidal torque density to the fast particle population"""


class _T_distributions_d_profiles_1d_collisions_ion_state(SpTree):
	"""1D profiles for collisions with a given ion species state"""

	z_min  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Minimum Z of the charge state bundle (z_min = z_max = 0 for a neutral)"""

	z_max  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Maximum Z of the charge state bundle (equal to z_min if no bundle)"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying charge state (e.g. C+, C+2 , C+3, C+4, C+5, C+6, ...)"""

	electron_configuration  :str =  sp_property(type="dynamic")
	""" Configuration of atomic orbitals of this state, e.g. 1s2-2s1"""

	vibrational_level  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Vibrational level (can be bundled)"""

	vibrational_mode  :str =  sp_property(type="dynamic")
	""" Vibrational mode of this state, e.g. _A_g_. Need to define, or adopt a standard
		nomenclature."""

	power_thermal  :Expression  =  sp_property(type="dynamic",units="W.m^-3",coordinate1="../../../../grid/rho_tor_norm")
	""" Collisional power density to the thermal particle population"""

	power_fast  :Expression  =  sp_property(type="dynamic",units="W.m^-3",coordinate1="../../../../grid/rho_tor_norm")
	""" Collisional power density to the fast particle population"""

	torque_thermal_tor  :Expression  =  sp_property(type="dynamic",units="N.m^-2",coordinate1="../../../../grid/rho_tor_norm")
	""" Collisional toroidal torque density to the thermal particle population"""

	torque_fast_tor  :Expression  =  sp_property(type="dynamic",units="N.m^-2",coordinate1="../../../../grid/rho_tor_norm")
	""" Collisional toroidal torque density to the fast particle population"""


class _T_distributions_d_profiles_1d_partial_collisions_ion_state(SpTree):
	"""1D profiles for collisions with a given ion species state"""

	z_min  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Minimum Z of the charge state bundle (z_min = z_max = 0 for a neutral)"""

	z_max  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Maximum Z of the charge state bundle (equal to z_min if no bundle)"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying charge state (e.g. C+, C+2 , C+3, C+4, C+5, C+6, ...)"""

	electron_configuration  :str =  sp_property(type="dynamic")
	""" Configuration of atomic orbitals of this state, e.g. 1s2-2s1"""

	vibrational_level  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Vibrational level (can be bundled)"""

	vibrational_mode  :str =  sp_property(type="dynamic")
	""" Vibrational mode of this state, e.g. _A_g_. Need to define, or adopt a standard
		nomenclature."""

	power_thermal  :Expression  =  sp_property(type="dynamic",units="W.m^-3",coordinate1="../../../../../grid/rho_tor_norm")
	""" Collisional power density to the thermal particle population"""

	power_fast  :Expression  =  sp_property(type="dynamic",units="W.m^-3",coordinate1="../../../../../grid/rho_tor_norm")
	""" Collisional power density to the fast particle population"""

	torque_thermal_tor  :Expression  =  sp_property(type="dynamic",units="N.m^-2",coordinate1="../../../../../grid/rho_tor_norm")
	""" Collisional toroidal torque density to the thermal particle population"""

	torque_fast_tor  :Expression  =  sp_property(type="dynamic",units="N.m^-2",coordinate1="../../../../../grid/rho_tor_norm")
	""" Collisional toroidal torque density to the fast particle population"""


class _T_distributions_d_profiles_1d_collisions_electrons(SpTree):
	"""1D profiles for collisions with electrons"""

	power_thermal  :Expression  =  sp_property(type="dynamic",units="W.m^-3",coordinate1="../../../grid/rho_tor_norm")
	""" Collisional power density to the thermal particle population"""

	power_fast  :Expression  =  sp_property(type="dynamic",units="W.m^-3",coordinate1="../../../grid/rho_tor_norm")
	""" Collisional power density to the fast particle population"""

	torque_thermal_tor  :Expression  =  sp_property(type="dynamic",units="N.m^-2",coordinate1="../../../grid/rho_tor_norm")
	""" Collisional toroidal torque density to the thermal particle population"""

	torque_fast_tor  :Expression  =  sp_property(type="dynamic",units="N.m^-2",coordinate1="../../../grid/rho_tor_norm")
	""" Collisional toroidal torque density to the fast particle population"""


class _T_distributions_d_profiles_1d_partial_collisions_electrons(SpTree):
	"""1D profiles for collisions with electrons"""

	power_thermal  :Expression  =  sp_property(type="dynamic",units="W.m^-3",coordinate1="../../../../grid/rho_tor_norm")
	""" Collisional power density to the thermal particle population"""

	power_fast  :Expression  =  sp_property(type="dynamic",units="W.m^-3",coordinate1="../../../../grid/rho_tor_norm")
	""" Collisional power density to the fast particle population"""

	torque_thermal_tor  :Expression  =  sp_property(type="dynamic",units="N.m^-2",coordinate1="../../../../grid/rho_tor_norm")
	""" Collisional toroidal torque density to the thermal particle population"""

	torque_fast_tor  :Expression  =  sp_property(type="dynamic",units="N.m^-2",coordinate1="../../../../grid/rho_tor_norm")
	""" Collisional toroidal torque density to the fast particle population"""


class _T_distributions_d_ggd_expansion(SpTree):
	"""Expansion of the distribution function for a given time slice, using a GGD
		representation"""

	grid_subset  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="mixed")
	""" Values of the distribution function expansion, for various grid subsets"""


class _T_distributions_d_source_identifier(SpTree):
	"""Identifier of the source/sink term (wave or particle source process)"""

	type  :_T_identifier_dynamic_aos3 =  sp_property()
	""" Type of the source term. Index = 1 for a wave, index = 2 for a particle source
		process"""

	wave_index  :int =  sp_property(type="dynamic")
	""" Index into distribution/wave"""

	process_index  :int =  sp_property(type="dynamic")
	""" Index into distribution/process"""


class _T_distributions_d_global_quantities_collisions_ion(SpTree):
	"""Global quantities for collisions with a given ion species"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	z_ion  :float =  sp_property(type="dynamic",units="Elementary Charge Unit")
	""" Ion charge (of the dominant ionisation state; lumped ions are allowed)."""

	label  :str =  sp_property(type="dynamic")
	""" String identifying the species (e.g. H+, D+, T+, He+2, C+, D2, DT, CD4, ...)"""

	neutral_index  :int =  sp_property(type="dynamic")
	""" Index of the corresponding neutral species in the ../../neutral array"""

	power_thermal  :float =  sp_property(type="dynamic",units="W")
	""" Collisional power to the thermal particle population"""

	power_fast  :float =  sp_property(type="dynamic",units="W")
	""" Collisional power to the fast particle population"""

	torque_thermal_tor  :float =  sp_property(type="dynamic",units="N.m")
	""" Collisional toroidal torque to the thermal particle population"""

	torque_fast_tor  :float =  sp_property(type="dynamic",units="N.m")
	""" Collisional toroidal torque to the fast particle population"""

	multiple_states_flag  :int =  sp_property(type="dynamic")
	""" Multiple state calculation flag : 0-Only one state is considered; 1-Multiple
		states are considered and are described in the state structure"""

	state  :AoS[_T_distributions_d_global_quantities_collisions_ion_state] =  sp_property(coordinate1="1...N_charge_states")
	""" Collisional exchange with the various states of the ion species (ionisation,
		energy, excitation, ...)"""


class _T_distributions_d_profiles_2d_collisions_ion(SpTree):
	"""2D profiles for collisions with a given ion species"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	z_ion  :float =  sp_property(type="dynamic",units="Elementary Charge Unit")
	""" Ion charge (of the dominant ionisation state; lumped ions are allowed)."""

	label  :str =  sp_property(type="dynamic")
	""" String identifying the species (e.g. H+, D+, T+, He+2, C+, D2, DT, CD4, ...)"""

	neutral_index  :int =  sp_property(type="dynamic")
	""" Index of the corresponding neutral species in the ../../neutral array"""

	power_thermal  :array_type =  sp_property(type="dynamic",units="W.m^-3",coordinate1="../../../grid/r OR ../../../grid/rho_tor_norm",coordinate2="../../../grid/z OR ../../../grid/theta_geometric OR ../../../grid/theta_straight")
	""" Collisional power density to the thermal particle population"""

	power_fast  :array_type =  sp_property(type="dynamic",units="W.m^-3",coordinate1="../../../grid/r OR ../../../grid/rho_tor_norm",coordinate2="../../../grid/z OR ../../../grid/theta_geometric OR ../../../grid/theta_straight")
	""" Collisional power density to the fast particle population"""

	torque_thermal_tor  :array_type =  sp_property(type="dynamic",units="N.m^-2",coordinate1="../../../grid/r OR ../../../grid/rho_tor_norm",coordinate2="../../../grid/z OR ../../../grid/theta_geometric OR ../../../grid/theta_straight")
	""" Collisional toroidal torque density to the thermal particle population"""

	torque_fast_tor  :array_type =  sp_property(type="dynamic",units="N.m^-2",coordinate1="../../../grid/r OR ../../../grid/rho_tor_norm",coordinate2="../../../grid/z OR ../../../grid/theta_geometric OR ../../../grid/theta_straight")
	""" Collisional toroidal torque density to the fast particle population"""

	multiple_states_flag  :int =  sp_property(type="dynamic")
	""" Multiple state calculation flag : 0-Only one state is considered; 1-Multiple
		states are considered and are described in the state structure"""

	state  :AoS[_T_distributions_d_profiles_2d_collisions_ion_state] =  sp_property(coordinate1="1...N_charge_states")
	""" Collisional exchange with the various states of the ion species (ionisation,
		energy, excitation, ...)"""


class _T_distributions_d_profiles_2d_partial_collisions_ion(SpTree):
	"""2D profiles for collisions with a given ion species"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	z_ion  :float =  sp_property(type="dynamic",units="Elementary Charge Unit")
	""" Ion charge (of the dominant ionisation state; lumped ions are allowed)."""

	label  :str =  sp_property(type="dynamic")
	""" String identifying the species (e.g. H+, D+, T+, He+2, C+, D2, DT, CD4, ...)"""

	neutral_index  :int =  sp_property(type="dynamic")
	""" Index of the corresponding neutral species in the ../../neutral array"""

	power_thermal  :array_type =  sp_property(type="dynamic",units="W.m^-3",coordinate1="../../../../grid/r OR ../../../../grid/rho_tor_norm",coordinate2="../../../../grid/z OR ../../../../grid/theta_geometric OR ../../../../grid/theta_straight")
	""" Collisional power density to the thermal particle population"""

	power_fast  :array_type =  sp_property(type="dynamic",units="W.m^-3",coordinate1="../../../../grid/r OR ../../../../grid/rho_tor_norm",coordinate2="../../../../grid/z OR ../../../../grid/theta_geometric OR ../../../../grid/theta_straight")
	""" Collisional power density to the fast particle population"""

	torque_thermal_tor  :array_type =  sp_property(type="dynamic",units="N.m^-2",coordinate1="../../../../grid/r OR ../../../../grid/rho_tor_norm",coordinate2="../../../../grid/z OR ../../../../grid/theta_geometric OR ../../../../grid/theta_straight")
	""" Collisional toroidal torque density to the thermal particle population"""

	torque_fast_tor  :array_type =  sp_property(type="dynamic",units="N.m^-2",coordinate1="../../../../grid/r OR ../../../../grid/rho_tor_norm",coordinate2="../../../../grid/z OR ../../../../grid/theta_geometric OR ../../../../grid/theta_straight")
	""" Collisional toroidal torque density to the fast particle population"""

	multiple_states_flag  :int =  sp_property(type="dynamic")
	""" Multiple state calculation flag : 0-Only one state is considered; 1-Multiple
		states are considered and are described in the state structure"""

	state  :AoS[_T_distributions_d_profiles_2d_partial_collisions_ion_state] =  sp_property(coordinate1="1...N_charge_states")
	""" Collisional exchange with the various states of the ion species (ionisation,
		energy, excitation, ...)"""


class _T_distributions_d_profiles_1d_collisions_ion(SpTree):
	"""1D profiles for collisions with a given ion species"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	z_ion  :float =  sp_property(type="dynamic",units="Elementary Charge Unit")
	""" Ion charge (of the dominant ionisation state; lumped ions are allowed)."""

	label  :str =  sp_property(type="dynamic")
	""" String identifying the species (e.g. H+, D+, T+, He+2, C+, D2, DT, CD4, ...)"""

	neutral_index  :int =  sp_property(type="dynamic")
	""" Index of the corresponding neutral species in the ../../neutral array"""

	power_thermal  :Expression  =  sp_property(type="dynamic",units="W.m^-3",coordinate1="../../../grid/rho_tor_norm")
	""" Collisional power density to the thermal particle population"""

	power_fast  :Expression  =  sp_property(type="dynamic",units="W.m^-3",coordinate1="../../../grid/rho_tor_norm")
	""" Collisional power density to the fast particle population"""

	torque_thermal_tor  :Expression  =  sp_property(type="dynamic",units="N.m^-2",coordinate1="../../../grid/rho_tor_norm")
	""" Collisional toroidal torque density to the thermal particle population"""

	torque_fast_tor  :Expression  =  sp_property(type="dynamic",units="N.m^-2",coordinate1="../../../grid/rho_tor_norm")
	""" Collisional toroidal torque density to the fast particle population"""

	multiple_states_flag  :int =  sp_property(type="dynamic")
	""" Multiple state calculation flag : 0-Only one state is considered; 1-Multiple
		states are considered and are described in the state structure"""

	state  :AoS[_T_distributions_d_profiles_1d_collisions_ion_state] =  sp_property(coordinate1="1...N_charge_states")
	""" Collisional exchange with the various states of the ion species (ionisation,
		energy, excitation, ...)"""


class _T_distributions_d_profiles_1d_partial_collisions_ion(SpTree):
	"""1D profiles for collisions with a given ion species"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	z_ion  :float =  sp_property(type="dynamic",units="Elementary Charge Unit")
	""" Ion charge (of the dominant ionisation state; lumped ions are allowed)."""

	label  :str =  sp_property(type="dynamic")
	""" String identifying the species (e.g. H+, D+, T+, He+2, C+, D2, DT, CD4, ...)"""

	neutral_index  :int =  sp_property(type="dynamic")
	""" Index of the corresponding neutral species in the ../../neutral array"""

	power_thermal  :Expression  =  sp_property(type="dynamic",units="W.m^-3",coordinate1="../../../../grid/rho_tor_norm")
	""" Collisional power density to the thermal particle population"""

	power_fast  :Expression  =  sp_property(type="dynamic",units="W.m^-3",coordinate1="../../../../grid/rho_tor_norm")
	""" Collisional power density to the fast particle population"""

	torque_thermal_tor  :Expression  =  sp_property(type="dynamic",units="N.m^-2",coordinate1="../../../../grid/rho_tor_norm")
	""" Collisional toroidal torque density to the thermal particle population"""

	torque_fast_tor  :Expression  =  sp_property(type="dynamic",units="N.m^-2",coordinate1="../../../../grid/rho_tor_norm")
	""" Collisional toroidal torque density to the fast particle population"""

	multiple_states_flag  :int =  sp_property(type="dynamic")
	""" Multiple state calculation flag : 0-Only one state is considered; 1-Multiple
		states are considered and are described in the state structure"""

	state  :AoS[_T_distributions_d_profiles_1d_partial_collisions_ion_state] =  sp_property(coordinate1="1...N_charge_states")
	""" Collisional exchange with the various states of the ion species (ionisation,
		energy, excitation, ...)"""


class _T_distributions_d_fast_filter(SpTree):
	"""Description of how the fast and the thermal particle populations are separated"""

	method  :_T_identifier_dynamic_aos3 =  sp_property()
	""" Method used to separate the fast and thermal particle population (indices TBD)"""

	energy  :Expression  =  sp_property(type="dynamic",units="eV",coordinate1="../../grid/rho_tor_norm")
	""" Energy at which the fast and thermal particle populations were separated, as a
		function of radius"""


class _T_distributions_d_profiles_2d_grid(SpTree):
	"""2D grid for the distribution"""

	type  :_T_identifier_dynamic_aos3 =  sp_property(coordinate1="../rho_tor_norm",units="m^3")
	""" Grid type: index=0: Rectangular grid in the (R,Z) coordinates; index=1:
		Rectangular grid in the (radial, theta_geometric) coordinates; index=2:
		Rectangular grid in the (radial, theta_straight) coordinates."""

	r  :array_type =  sp_property(type="dynamic",coordinate1="1...N",units="m")
	""" Major radius"""

	z  :array_type =  sp_property(type="dynamic",coordinate1="1...N",units="m")
	""" Height"""

	theta_straight  :array_type =  sp_property(type="dynamic",coordinate1="1...N",units="rad")
	""" Straight field line poloidal angle"""

	theta_geometric  :array_type =  sp_property(type="dynamic",coordinate1="1...N",units="rad")
	""" Geometrical poloidal angle"""

	rho_tor_norm  :array_type =  sp_property(type="dynamic",coordinate1="1...N",units="-")
	""" Normalised toroidal flux coordinate. The normalizing value for rho_tor_norm, is
		the toroidal flux coordinate at the equilibrium boundary (LCFS or 99.x % of the
		LCFS in case of a fixed boundary equilibium calculation)"""

	rho_tor  :Expression  =  sp_property(type="dynamic",coordinate1="../rho_tor_norm",units="m")
	""" Toroidal flux coordinate. The toroidal field used in its definition is indicated
		under vacuum_toroidal_field/b0"""

	psi  :Expression  =  sp_property(coordinate1="../rho_tor_norm",units="Wb",type="dynamic")
	""" Poloidal magnetic flux"""

	volume  :Expression  =  sp_property(type="dynamic",coordinate1="../rho_tor_norm",units="m^3")
	""" Volume enclosed inside the magnetic surface"""

	area  :Expression  =  sp_property(type="dynamic",coordinate1="../rho_tor_norm",units="m^2")
	""" Cross-sectional area of the flux surface"""


class _T_distributions_d_ggd(TimeSlice):
	"""Distribution function for a given time slice, using a GGD representation"""

	grid  :_T_generic_grid_dynamic =  sp_property()
	""" Grid description"""

	temperature  :Expression  =  sp_property(coordinate1="../../profiles_1d(itime)/grid/rho_tor_norm",units="eV",type="dynamic")
	""" Reference temperature profile used to define the local thermal energy and the
		thermal velocity (for normalisation of the grid coordinates)"""

	expansion  :AoS[_T_distributions_d_ggd_expansion] =  sp_property(coordinate1="1...N",units="(m.s^-1)^-3.m^-3")
	""" Distribution function expanded into a vector of successive approximations. The
		first element in the vector (expansion(1)) is the zeroth order distribution
		function, while the K:th element in the vector (expansion(K)) is the K:th
		correction, such that the total distribution function is a sum over all elements
		in the expansion vector."""

	expansion_fd3v  :AoS[_T_distributions_d_ggd_expansion] =  sp_property(coordinate1="1...N",units="m^-3",introduced_after="3.34.0")
	""" Distribution function multiplied by the volume of the local velocity cell d3v,
		expanded into a vector of successive approximations. The first element in the
		vector (expansion(1)) is the zeroth order distribution function, while the K:th
		element in the vector (expansion(K)) is the K:th correction, such that the total
		distribution function is a sum over all elements in the expansion vector."""


class _T_distributions_d_global_quantities_source(SpTree):
	"""Global quantities for a given source/sink term"""

	identifier  :_T_distributions_d_source_identifier =  sp_property()
	""" Identifier of the wave or particle source process, defined respectively in
		distribution/wave or distribution/process"""

	particles  :float =  sp_property(units="s^-1",type="dynamic")
	""" Particle source rate"""

	power  :float =  sp_property(units="W",type="dynamic")
	""" Total power of the source"""

	torque_tor  :float =  sp_property(units="N.m",type="dynamic")
	""" Total toroidal torque of the source"""


class _T_distributions_d_global_quantities_collisions(SpTree):
	"""Global quantities for collisions"""

	electrons  :_T_distributions_d_global_quantities_collisions_electrons =  sp_property()
	""" Collisional exchange with electrons"""

	ion  :AoS[_T_distributions_d_global_quantities_collisions_ion] =  sp_property(coordinate1="1...N")
	""" Collisional exchange with the various ion species"""


class _T_distributions_d_profiles_1d_source(SpTree):
	"""1D profiles for a given source/sink term"""

	identifier  :_T_distributions_d_source_identifier =  sp_property()
	""" Identifier of the wave or particle source process, defined respectively in
		distribution/wave or distribution/process"""

	particles  :Expression  =  sp_property(units="s^-1.m^-3",type="dynamic",coordinate1="../../grid/rho_tor_norm")
	""" Source rate of thermal particle density"""

	energy  :Expression  =  sp_property(units="W.m^-3",type="dynamic",coordinate1="../../grid/rho_tor_norm")
	""" Source rate of energy density"""

	momentum_tor  :Expression  =  sp_property(units="N.m^-2",type="dynamic",coordinate1="../../grid/rho_tor_norm")
	""" Source rate of toroidal angular momentum density"""


class _T_distributions_d_profiles_1d_partial_source(SpTree):
	"""1D profiles for a given source/sink term"""

	identifier  :_T_distributions_d_source_identifier =  sp_property()
	""" Identifier of the wave or particle source process, defined respectively in
		distribution/wave or distribution/process"""

	particles  :Expression  =  sp_property(units="s^-1.m^-3",type="dynamic",coordinate1="../../../grid/rho_tor_norm")
	""" Source rate of thermal particle density"""

	energy  :Expression  =  sp_property(units="W.m^-3",type="dynamic",coordinate1="../../../grid/rho_tor_norm")
	""" Source rate of energy density"""

	momentum_tor  :Expression  =  sp_property(units="N.m^-2",type="dynamic",coordinate1="../../../grid/rho_tor_norm")
	""" Source rate of toroidal angular momentum density"""


class _T_distributions_d_profiles_2d_collisions(SpTree):
	"""2D profiles for collisions"""

	electrons  :_T_distributions_d_profiles_2d_collisions_electrons =  sp_property()
	""" Collisional exchange with electrons"""

	ion  :AoS[_T_distributions_d_profiles_2d_collisions_ion] =  sp_property(coordinate1="1...N")
	""" Collisional exchange with the various ion species"""


class _T_distributions_d_profiles_2d_partial_collisions(SpTree):
	"""2D profiles for collisions"""

	electrons  :_T_distributions_d_profiles_2d_partial_collisions_electrons =  sp_property()
	""" Collisional exchange with electrons"""

	ion  :AoS[_T_distributions_d_profiles_2d_partial_collisions_ion] =  sp_property(coordinate1="1...N")
	""" Collisional exchange with the various ion species"""


class _T_distributions_d_profiles_1d_collisions(SpTree):
	"""1D profiles for collisions"""

	electrons  :_T_distributions_d_profiles_1d_collisions_electrons =  sp_property()
	""" Collisional exchange with electrons"""

	ion  :AoS[_T_distributions_d_profiles_1d_collisions_ion] =  sp_property(coordinate1="1...N")
	""" Collisional exchange with the various ion species"""


class _T_distributions_d_profiles_1d_partial_collisions(SpTree):
	"""1D profiles for collisions"""

	electrons  :_T_distributions_d_profiles_1d_partial_collisions_electrons =  sp_property()
	""" Collisional exchange with electrons"""

	ion  :AoS[_T_distributions_d_profiles_1d_partial_collisions_ion] =  sp_property(coordinate1="1...N")
	""" Collisional exchange with the various ion species"""


class _T_distributions_d_global_quantities(TimeSlice):
	"""Global quantities from the distribution, for a given time slice"""

	particles_n  :float =  sp_property(type="dynamic",units="-")
	""" Number of particles in the distribution, i.e. the volume integral of the density
		(note: this is the number of real particles and not markers)"""

	particles_fast_n  :float =  sp_property(type="dynamic",units="-")
	""" Number of fast particles in the distribution, i.e. the volume integral of the
		density (note: this is the number of real particles and not markers)"""

	energy  :float =  sp_property(type="dynamic",units="J")
	""" Total energy in the distribution"""

	energy_fast  :float =  sp_property(type="dynamic",units="J")
	""" Total energy of the fast particles in the distribution"""

	energy_fast_parallel  :float =  sp_property(type="dynamic",units="J")
	""" Parallel energy of the fast particles in the distribution"""

	torque_tor_j_radial  :float =  sp_property(type="dynamic",units="N.m")
	""" Toroidal torque due to radial currents"""

	current_tor  :float =  sp_property(type="dynamic",units="A")
	""" Toroidal current driven by the distribution"""

	collisions  :_T_distributions_d_global_quantities_collisions =  sp_property()
	""" Power and torque exchanged between the species described by the distribution and
		the different plasma species through collisions"""

	thermalisation  :_T_distributions_d_global_quantities_thermalised =  sp_property()
	""" Volume integrated source of thermal particles, momentum and energy due to
		thermalisation. Here thermalisation refers to non-thermal particles,
		sufficiently assimilated to the thermal background to be re-categorised as
		thermal particles. Note that this source may also be negative if thermal
		particles are being accelerated such that they form a distinct non-thermal
		contribution, e.g. due run-away of RF interactions."""

	source  :AoS[_T_distributions_d_global_quantities_source] =  sp_property(coordinate1="1...N")
	""" Set of volume integrated sources and sinks of particles, momentum and energy
		included in the Fokker-Planck modelling, related to the various waves or
		particle source processes affecting the distribution"""


class _T_distributions_d_profiles_2d_partial(SpTree):
	"""2D profiles from specific particles in the distribution (trapped, co or
		counter-passing)"""

	density  :array_type =  sp_property(coordinate1="../../grid/r OR ../../grid/rho_tor_norm",coordinate2="../../grid/z OR ../../grid/theta_geometric OR ../../grid/theta_straight",units="m^-3",type="dynamic")
	""" Density (thermal+non-thermal)"""

	density_fast  :array_type =  sp_property(coordinate1="../../grid/r OR ../../grid/rho_tor_norm",coordinate2="../../grid/z OR ../../grid/theta_geometric OR ../../grid/theta_straight",units="m^-3",type="dynamic")
	""" Density of fast particles"""

	pressure  :array_type =  sp_property(coordinate1="../../grid/r OR ../../grid/rho_tor_norm",coordinate2="../../grid/z OR ../../grid/theta_geometric OR ../../grid/theta_straight",units="J.m^-3",type="dynamic")
	""" Pressure (thermal+non-thermal)"""

	pressure_fast  :array_type =  sp_property(coordinate1="../../grid/r OR ../../grid/rho_tor_norm",coordinate2="../../grid/z OR ../../grid/theta_geometric OR ../../grid/theta_straight",units="J.m^-3",type="dynamic")
	""" Pressure of fast particles"""

	pressure_fast_parallel  :array_type =  sp_property(coordinate1="../../grid/r OR ../../grid/rho_tor_norm",coordinate2="../../grid/z OR ../../grid/theta_geometric OR ../../grid/theta_straight",units="J.m^-3",type="dynamic")
	""" Pressure of fast particles in the parallel direction"""

	current_tor  :array_type =  sp_property(coordinate1="../../grid/r OR ../../grid/rho_tor_norm",coordinate2="../../grid/z OR ../../grid/theta_geometric OR ../../grid/theta_straight",units="A.m^-2",type="dynamic")
	""" Total toroidal driven current density (including electron and thermal ion
		back-current, or drag-current)"""

	current_fast_tor  :array_type =  sp_property(coordinate1="../../grid/r OR ../../grid/rho_tor_norm",coordinate2="../../grid/z OR ../../grid/theta_geometric OR ../../grid/theta_straight",units="A.m^-2",type="dynamic")
	""" Total toroidal driven current density of fast (non-thermal) particles (excluding
		electron and thermal ion back-current, or drag-current)"""

	torque_tor_j_radial  :array_type =  sp_property(type="dynamic",units="N.m^-2",coordinate1="../../grid/r OR ../../grid/rho_tor_norm",coordinate2="../../grid/z OR ../../grid/theta_geometric OR ../../grid/theta_straight")
	""" Toroidal torque due to radial currents"""

	collisions  :_T_distributions_d_profiles_2d_partial_collisions =  sp_property()
	""" Power and torque exchanged between the species described by the distribution and
		the different plasma species through collisions"""


class _T_distributions_d_profiles_1d_partial(SpTree):
	"""1D profiles from specific particles in the distribution (trapped, co or
		counter-passing)"""

	density  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="m^-3",type="dynamic")
	""" Density (thermal+non-thermal)"""

	density_fast  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="m^-3",type="dynamic")
	""" Density of fast particles"""

	pressure  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="J.m^-3",type="dynamic")
	""" Pressure (thermal+non-thermal)"""

	pressure_fast  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="J.m^-3",type="dynamic")
	""" Pressure of fast particles"""

	pressure_fast_parallel  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="J.m^-3",type="dynamic")
	""" Pressure of fast particles in the parallel direction"""

	current_tor  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="A.m^-2",type="dynamic")
	""" Total toroidal driven current density (including electron and thermal ion
		back-current, or drag-current)"""

	current_fast_tor  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="A.m^-2",type="dynamic")
	""" Total toroidal driven current density of fast (non-thermal) particles (excluding
		electron and thermal ion back-current, or drag-current)"""

	torque_tor_j_radial  :Expression  =  sp_property(type="dynamic",units="N.m^-2",coordinate1="../../grid/rho_tor_norm")
	""" Toroidal torque due to radial currents"""

	collisions  :_T_distributions_d_profiles_1d_partial_collisions =  sp_property()
	""" Power and torque exchanged between the species described by the distribution and
		the different plasma species through collisions"""

	source  :AoS[_T_distributions_d_profiles_1d_partial_source] =  sp_property(coordinate1="1...N")
	""" Set of flux averaged sources and sinks of particles, momentum and energy
		included in the Fokker-Planck modelling, related to the various waves or
		particle source processes affecting the distribution"""


class _T_distributions_d_profiles_1d(TimeSlice):
	"""1D profiles from the distribution, for a given time slice"""

	grid  :_T_core_radial_grid =  sp_property()
	""" Radial grid"""

	fast_filter  :_T_distributions_d_fast_filter =  sp_property()
	""" Description of how the fast and the thermal particle populations are separated"""

	density  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="m^-3",type="dynamic")
	""" Density (thermal+non-thermal)"""

	density_fast  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="m^-3",type="dynamic")
	""" Density of fast particles"""

	pressure  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="J.m^-3",type="dynamic")
	""" Pressure (thermal+non-thermal)"""

	pressure_fast  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="J.m^-3",type="dynamic")
	""" Pressure of fast particles"""

	pressure_fast_parallel  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="J.m^-3",type="dynamic")
	""" Pressure of fast particles in the parallel direction"""

	current_tor  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="A.m^-2",type="dynamic")
	""" Total toroidal driven current density (including electron and thermal ion
		back-current, or drag-current)"""

	current_fast_tor  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="A.m^-2",type="dynamic")
	""" Total toroidal driven current density of fast (non-thermal) particles (excluding
		electron and thermal ion back-current, or drag-current)"""

	torque_tor_j_radial  :Expression  =  sp_property(type="dynamic",units="N.m^-2",coordinate1="../grid/rho_tor_norm")
	""" Toroidal torque due to radial currents"""

	collisions  :_T_distributions_d_profiles_1d_collisions =  sp_property()
	""" Power and torque exchanged between the species described by the distribution and
		the different plasma species through collisions"""

	thermalisation  :_T_distributions_d_profiles_1d_thermalised =  sp_property()
	""" Flux surface averaged source of thermal particles, momentum and energy due to
		thermalisation. Here thermalisation refers to non-thermal particles,
		sufficiently assimilated to the thermal background to be re-categorised as
		thermal particles. Note that this source may also be negative if thermal
		particles are being accelerated such that they form a distinct non-thermal
		contribution, e.g. due run-away of RF interactions."""

	source  :AoS[_T_distributions_d_profiles_1d_source] =  sp_property(coordinate1="1...N")
	""" Set of flux averaged sources and sinks of particles, momentum and energy
		included in the Fokker-Planck modelling, related to the various waves or
		particle source processes affecting the distribution"""

	trapped  :_T_distributions_d_profiles_1d_partial =  sp_property()
	""" Flux surface averaged profile evaluated using the trapped particle part of the
		distribution."""

	co_passing  :_T_distributions_d_profiles_1d_partial =  sp_property()
	""" Flux surface averaged profile evaluated using the co-passing particle part of
		the distribution."""

	counter_passing  :_T_distributions_d_profiles_1d_partial =  sp_property()
	""" Flux surface averaged profile evaluated using the counter-passing particle part
		of the distribution."""


class _T_distributions_d_profiles_2d(TimeSlice):
	"""2D profiles from the distribution, for a given time slice"""

	grid  :_T_distributions_d_profiles_2d_grid =  sp_property()
	""" Grid. The grid has to be rectangular in a pair of coordinates, as specified in
		type"""

	density  :array_type =  sp_property(coordinate1="../grid/r OR ../grid/rho_tor_norm",coordinate2="../grid/z OR ../grid/theta_geometric OR ../grid/theta_straight",units="m^-3",type="dynamic")
	""" Density (thermal+non-thermal)"""

	density_fast  :array_type =  sp_property(coordinate1="../grid/r OR ../grid/rho_tor_norm",coordinate2="../grid/z OR ../grid/theta_geometric OR ../grid/theta_straight",units="m^-3",type="dynamic")
	""" Density of fast particles"""

	pressure  :array_type =  sp_property(coordinate1="../grid/r OR ../grid/rho_tor_norm",coordinate2="../grid/z OR ../grid/theta_geometric OR ../grid/theta_straight",units="J.m^-3",type="dynamic")
	""" Pressure (thermal+non-thermal)"""

	pressure_fast  :array_type =  sp_property(coordinate1="../grid/r OR ../grid/rho_tor_norm",coordinate2="../grid/z OR ../grid/theta_geometric OR ../grid/theta_straight",units="J.m^-3",type="dynamic")
	""" Pressure of fast particles"""

	pressure_fast_parallel  :array_type =  sp_property(coordinate1="../grid/r OR ../grid/rho_tor_norm",coordinate2="../grid/z OR ../grid/theta_geometric OR ../grid/theta_straight",units="J.m^-3",type="dynamic")
	""" Pressure of fast particles in the parallel direction"""

	current_tor  :array_type =  sp_property(coordinate1="../grid/r OR ../grid/rho_tor_norm",coordinate2="../grid/z OR ../grid/theta_geometric OR ../grid/theta_straight",units="A.m^-2",type="dynamic")
	""" Total toroidal driven current density (including electron and thermal ion
		back-current, or drag-current)"""

	current_fast_tor  :array_type =  sp_property(coordinate1="../grid/r OR ../grid/rho_tor_norm",coordinate2="../grid/z OR ../grid/theta_geometric OR ../grid/theta_straight",units="A.m^-2",type="dynamic")
	""" Total toroidal driven current density of fast (non-thermal) particles (excluding
		electron and thermal ion back-current, or drag-current)"""

	torque_tor_j_radial  :array_type =  sp_property(type="dynamic",units="N.m^-2",coordinate1="../grid/r OR ../grid/rho_tor_norm",coordinate2="../grid/z OR ../grid/theta_geometric OR ../grid/theta_straight")
	""" Toroidal torque due to radial currents"""

	collisions  :_T_distributions_d_profiles_2d_collisions =  sp_property()
	""" Power and torque exchanged between the species described by the distribution and
		the different plasma species through collisions"""

	trapped  :_T_distributions_d_profiles_2d_partial =  sp_property()
	""" Flux surface averaged profile evaluated using the trapped particle part of the
		distribution."""

	co_passing  :_T_distributions_d_profiles_2d_partial =  sp_property()
	""" Flux surface averaged profile evaluated using the co-passing particle part of
		the distribution."""

	counter_passing  :_T_distributions_d_profiles_2d_partial =  sp_property()
	""" Flux surface averaged profile evaluated using the counter-passing particle part
		of the distribution."""


class _T_distributions_d(SpTree):
	"""Description of a given distribution function"""

	wave  :AoS[_T_waves_coherent_wave_identifier] =  sp_property(coordinate1="1...N")
	""" List all waves affecting the distribution, identified as in
		waves/coherent_wave(i)/identifier in the waves IDS"""

	process  :AoS[_T_distribution_process_identifier] =  sp_property(coordinate1="1...N")
	""" List all processes (NBI units, fusion reactions, ...) affecting the
		distribution, identified as in distribution_sources/source(i)/process in the
		DISTRIBUTION_SOURCES IDS"""

	gyro_type  :int =  sp_property(type="constant")
	""" Defines how to interpret the spatial coordinates: 1 = given at the actual
		particle birth point; 2 =given at the gyro centre of the birth point"""

	species  :_T_distribution_species =  sp_property()
	""" Species described by this distribution"""

	global_quantities  :TimeSeriesAoS[_T_distributions_d_global_quantities] =  sp_property(coordinate1="time",type="dynamic")
	""" Global quantities (integrated over plasma volume for moments of the
		distribution, collisional exchange and source terms), for various time slices"""

	profiles_1d  :TimeSeriesAoS[_T_distributions_d_profiles_1d] =  sp_property(coordinate1="time",type="dynamic",cocos_alias="IDSPATH",cocos_replace="distributions.distribution{i}.profiles_1d{j}")
	""" Radial profiles (flux surface averaged quantities) for various time slices"""

	profiles_2d  :TimeSeriesAoS[_T_distributions_d_profiles_2d] =  sp_property(coordinate1="time",type="dynamic")
	""" 2D profiles in the poloidal plane for various time slices"""

	is_delta_f  :int =  sp_property(type="constant")
	""" If is_delta_f=1, then the distribution represents the deviation from a
		Maxwellian; is_delta_f=0, then the distribution represents all particles, i.e.
		the full-f solution"""

	ggd  :TimeSeriesAoS[_T_distributions_d_ggd] =  sp_property(coordinate1="time",type="dynamic")
	""" Distribution represented using the ggd, for various time slices"""

	markers  :TimeSeriesAoS[_T_distribution_markers] =  sp_property(coordinate1="time",type="dynamic")
	""" Distribution represented by a set of markers (test particles)"""


class _T_distributions(IDS):
	"""Distribution function(s) of one or many particle species. This structure is
		specifically designed to handle non-Maxwellian distribution function generated
		during heating and current drive, typically solved using a Fokker-Planck
		calculation perturbed by a heating scheme (e.g. IC, EC, LH, NBI, or alpha
		heating) and then relaxed by Coloumb collisions.
	lifecycle_status: alpha
	lifecycle_version: 3.2.1
	lifecycle_last_change: 3.38.0"""

	dd_version="v3_38_1_dirty"
	ids_name="distributions"

	distribution  :AoS[_T_distributions_d] =  sp_property(coordinate1="1...N",appendable_by_appender_actor="yes")
	""" Set of distribution functions. Every distribution function has to be associated
		with only one particle species, specified in distri_vec/species/, but there
		could be multiple distribution function for each species. In this case, the fast
		particle populations should be superposed"""

	vacuum_toroidal_field  :_T_b_tor_vacuum_1 =  sp_property(cocos_alias="IDSPATH",cocos_replace="distributions.vacuum_toroidal_field")
	""" Characteristics of the vacuum toroidal field (used in rho_tor definition and in
		the normalization of current densities)"""

	magnetic_axis  :_T_rz1d_dynamic_1 =  sp_property()
	""" Magnetic axis position (used to define a poloidal angle for the 2D profiles)"""
