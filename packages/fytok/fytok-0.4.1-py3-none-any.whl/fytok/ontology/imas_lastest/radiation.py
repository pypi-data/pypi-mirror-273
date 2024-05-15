"""
  This module containes the _FyTok_ wrapper of IMAS/dd/radiation
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_identifier_dynamic_aos3,_T_generic_grid_scalar,_T_plasma_composition_neutral_element,_T_core_radial_grid,_T_identifier,_T_b_tor_vacuum_1,_T_generic_grid_aos3_root
from .utilities import _E_neutrals_identifier

class _E_radiation(IntFlag):
	"""Translation table for radiation processes	xpath: 	"""
  
	unspecified = 0
	"""Unspecified emission process"""
  
	nuclear_decay = 6
	"""Emission from nuclear decay"""
  
	bremsstrahlung = 8
	"""Emission from bremsstrahlung"""
  
	synchrotron_radiation = 9
	"""Emission from synchrotron radiation"""
  
	line_radiation = 10
	"""Emission from line radiation"""
  
	recombination = 11
	"""Emission from recombination"""
  
	runaways = 501
	"""Emission from run-away processes; includes both electron and ion run-away"""
  
	custom_1 = 901
	"""Custom emission 1; content to be decided by data provided"""
  
	custom_2 = 902
	"""Custom emission 2; content to be decided by data provided"""
  
	custom_3 = 903
	"""Custom emission 3; content to be decided by data provided"""
  
	custom_4 = 904
	"""Custom emission 4; content to be decided by data provided"""
  
	custom_5 = 905
	"""Custom emission 5; content to be decided by data provided"""
  
	custom_6 = 906
	"""Custom emission 6; content to be decided by data provided"""
  
	custom_7 = 907
	"""Custom emission 7; content to be decided by data provided"""
  
	custom_8 = 908
	"""Custom emission 8; content to be decided by data provided"""
  
	custom_9 = 909
	"""Custom emission 9; content to be decided by data provided"""
  

class _T_radiation_process_profiles_1d_ions_charge_states(SpTree):
	"""Process terms related to the a given state of the ion species"""

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

	emissivity  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="W.m^-3",type="dynamic")
	""" Emissivity from this species"""

	power_inside  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="W",type="dynamic")
	""" Radiated power from inside the flux surface (volume integral of the emissivity
		inside the flux surface)"""


class _T_radiation_process_profiles_1d_electrons(SpTree):
	"""Process terms related to electrons"""

	emissivity  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="W.m^-3",type="dynamic")
	""" Emissivity from this species"""

	power_inside  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="W",type="dynamic")
	""" Radiated power from inside the flux surface (volume integral of the emissivity
		inside the flux surface)"""


class _T_radiation_process_global_volume(SpTree):
	"""Global quantities (emissions) related to a given volume"""

	power  :float =  sp_property(units="W",type="dynamic")
	""" Total power emitted by all species"""

	power_ion_total  :float =  sp_property(units="W",type="dynamic")
	""" Total power emitted by all ion species"""

	power_neutral_total  :float =  sp_property(units="W",type="dynamic")
	""" Total power emitted by all neutral species"""

	power_electrons  :float =  sp_property(units="W",type="dynamic")
	""" Power emitted by electrons"""


class _T_radiation_process_ggd_neutral_state(SpTree):
	"""Process terms related to a given state of the neutral species"""

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

	emissivity  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="W.m^-3")
	""" Emissivity from this state, on various grid subsets"""


class _T_radiation_process_ggd_ion_charge_states(SpTree):
	"""Process terms related to a given state of the ion species"""

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

	emissivity  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="W.m^-3")
	""" Emissivity from this state, on various grid subsets"""


class _T_radiation_process_ggd_electrons(SpTree):
	"""Process terms related to electrons"""

	emissivity  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="W.m^-3")
	""" Emissivity from this species, on various grid subsets"""


class _T_radiation_process_profiles_1d_neutral_state(SpTree):
	"""Process terms related to the a given state of the neutral species"""

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

	emissivity  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="W.m^-3",type="dynamic")
	""" Emissivity from this species"""

	power_inside  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="W",type="dynamic")
	""" Radiated power from inside the flux surface (volume integral of the emissivity
		inside the flux surface)"""


class _T_radiation_process_profiles_1d_ions(SpTree):
	"""Process terms related to a given ion species"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	z_ion  :float =  sp_property(type="dynamic",units="Elementary Charge Unit")
	""" Ion charge (of the dominant ionisation state; lumped ions are allowed)"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying ion (e.g. H+, D+, T+, He+2, C+, ...)"""

	neutral_index  :int =  sp_property(type="dynamic")
	""" Index of the corresponding neutral species in the ../../neutral array"""

	emissivity  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="W.m^-3",type="dynamic")
	""" Emissivity from this species"""

	power_inside  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="W",type="dynamic")
	""" Radiated power from inside the flux surface (volume integral of the emissivity
		inside the flux surface)"""

	multiple_states_flag  :int =  sp_property(type="dynamic")
	""" Multiple states calculation flag : 0-Only one state is considered; 1-Multiple
		states are considered and are described in the state structure"""

	state  :AoS[_T_radiation_process_profiles_1d_ions_charge_states] =  sp_property(coordinate1="1...N")
	""" Process terms related to the different charge states of the species (ionisation,
		energy, excitation, ...)"""


class _T_radiation_process_global(TimeSlice):
	"""Process global quantities for a given time slice"""

	inside_lcfs  :_T_radiation_process_global_volume =  sp_property()
	""" Emissions from the core plasma, inside the last closed flux surface"""

	inside_vessel  :_T_radiation_process_global_volume =  sp_property()
	""" Total emissions inside the vacuum vessel"""


class _T_radiation_process_ggd_neutral(SpTree):
	"""Process terms related to a given neutral species"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying the neutral species (e.g. H, D, T, He, C, ...)"""

	ion_index  :int =  sp_property(type="dynamic")
	""" Index of the corresponding ion species in the ../../ion array"""

	emissivity  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="W.m^-3")
	""" Emissivity from this species, on various grid subsets"""

	multiple_states_flag  :int =  sp_property(type="dynamic")
	""" Multiple states calculation flag : 0-Only one state is considered; 1-Multiple
		states are considered and are described in the state structure"""

	state  :AoS[_T_radiation_process_ggd_neutral_state] =  sp_property(coordinate1="1...N")
	""" Process terms related to the different charge states of the species (energy,
		excitation, ...)"""


class _T_radiation_process_ggd_ion(SpTree):
	"""Process terms related to a given ion species"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	z_ion  :float =  sp_property(type="dynamic",units="Elementary Charge Unit")
	""" Ion charge (of the dominant ionisation state; lumped ions are allowed)"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying ion (e.g. H+, D+, T+, He+2, C+, ...)"""

	neutral_index  :int =  sp_property(type="dynamic")
	""" Index of the corresponding neutral species in the ../../neutral array"""

	emissivity  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="W.m^-3")
	""" Emissivity from this species, on various grid subsets"""

	multiple_states_flag  :int =  sp_property(type="dynamic")
	""" Multiple states calculation flag : 0-Only one state is considered; 1-Multiple
		states are considered and are described in the state structure"""

	state  :AoS[_T_radiation_process_ggd_ion_charge_states] =  sp_property(coordinate1="1...N")
	""" Process terms related to the different charge states of the species (ionisation,
		energy, excitation, ...)"""


class _T_radiation_process_profiles_1d_neutral(SpTree):
	"""Process terms related to a given neutral species"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying the neutral species (e.g. H, D, T, He, C, ...)"""

	ion_index  :int =  sp_property(type="dynamic")
	""" Index of the corresponding ion species in the ../../ion array"""

	emissivity  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="W.m^-3",type="dynamic")
	""" Emissivity from this species"""

	power_inside  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="W",type="dynamic")
	""" Radiated power from inside the flux surface (volume integral of the emissivity
		inside the flux surface)"""

	multiple_states_flag  :int =  sp_property(type="dynamic")
	""" Multiple states calculation flag : 0-Only one state is considered; 1-Multiple
		states are considered and are described in the state structure"""

	state  :AoS[_T_radiation_process_profiles_1d_neutral_state] =  sp_property(coordinate1="1...N")
	""" Process terms related to the different charge states of the species (energy,
		excitation, ...)"""


class _T_radiation_process_ggd(TimeSlice):
	"""Process terms for a given time slice (using the GGD)"""

	electrons  :_T_radiation_process_ggd_electrons =  sp_property()
	""" Process terms related to electrons"""

	ion  :AoS[_T_radiation_process_ggd_ion] =  sp_property(coordinate1="1...N")
	""" Process terms related to the different ion species"""

	neutral  :AoS[_T_radiation_process_ggd_neutral] =  sp_property(coordinate1="1...N")
	""" Process terms related to the different neutral species"""


class _T_radiation_process_profiles_1d(TimeSlice):
	"""Process terms for a given time slice"""

	grid  :_T_core_radial_grid =  sp_property()
	""" Radial grid"""

	electrons  :_T_radiation_process_profiles_1d_electrons =  sp_property()
	""" Processs terms related to electrons"""

	emissivity_ion_total  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="W.m^-3",type="dynamic")
	""" Emissivity (summed over ion species)"""

	power_inside_ion_total  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="W",type="dynamic")
	""" Total power from ion species (summed over ion species) inside the flux surface
		(volume integral of the emissivity inside the flux surface)"""

	emissivity_neutral_total  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="W.m^-3",type="dynamic")
	""" Emissivity (summed over neutral species)"""

	power_inside_neutral_total  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="W",type="dynamic")
	""" Total power from ion species (summed over neutral species) inside the flux
		surface (volume integral of the emissivity inside the flux surface)"""

	ion  :AoS[_T_radiation_process_profiles_1d_ions] =  sp_property(coordinate1="1...N")
	""" Process terms related to the different ion species"""

	neutral  :AoS[_T_radiation_process_profiles_1d_neutral] =  sp_property(coordinate1="1...N")
	""" Process terms related to the different neutral species"""


class _T_radiation_process(SpTree):
	"""Process terms for a given actuator"""

	identifier  :_E_radiation =  sp_property(doc_identifier="radiation/radiation_identifier.xml")
	""" Process identifier"""

	global_quantities  :TimeSeriesAoS[_T_radiation_process_global] =  sp_property(coordinate1="time",type="dynamic")
	""" Scalar volume integrated quantities"""

	profiles_1d  :TimeSeriesAoS[_T_radiation_process_profiles_1d] =  sp_property(coordinate1="time",type="dynamic",cocos_alias="IDSPATH",cocos_replace="radiation.process{i}.profiles_1d{j}")
	""" Emissivity radial profiles for various time slices"""

	ggd  :TimeSeriesAoS[_T_radiation_process_ggd] =  sp_property(coordinate1="time",type="dynamic")
	""" Emissivities represented using the general grid description, for various time
		slices"""


class _T_radiation(IDS):
	"""Radiation emitted by the plasma and neutrals
	lifecycle_status: alpha
	lifecycle_version: 3.17.1
	lifecycle_last_change: 3.25.0"""

	dd_version="v3_38_1_dirty"
	ids_name="radiation"

	vacuum_toroidal_field  :_T_b_tor_vacuum_1 =  sp_property(cocos_alias="IDSPATH",cocos_replace="radiation.vacuum_toroidal_field")
	""" Characteristics of the vacuum toroidal field (used in rho_tor definition)"""

	grid_ggd  :TimeSeriesAoS[_T_generic_grid_aos3_root] =  sp_property(coordinate1="time",type="dynamic")
	""" Grid (using the Generic Grid Description), for various time slices. The timebase
		of this array of structure must be a subset of the process/ggd timebases"""

	process  :AoS[_T_radiation_process] =  sp_property(coordinate1="1...N")
	""" Set of emission processes. The radiation characteristics are described at the
		level of the originating entity. For instance describe line radiation from
		neutrals under profiles_1d/neutral. Line and recombination radiation under
		profiles_1d/ion. Bremsstrahlung radiation under profiles_1d/neutral and ion ..."""
