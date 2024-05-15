"""
  This module containes the _FyTok_ wrapper of IMAS/dd/wall
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_plasma_composition_neutral_element_constant,_T_rz1d_static,_T_identifier_static,_T_rz1d_dynamic_aos_time,_T_vessel_2d,_T_generic_grid_scalar,_T_identifier_dynamic_aos3,_T_plasma_composition_neutral_element,_T_generic_grid_identifier,_T_generic_grid_aos3_root,_T_temperature_reference,_T_signal_flt_1d
from .utilities import _E_materials

class _T_wall_global_quantitites_electrons(SpTree):
	"""Simple 0D description of plasma-wall interaction, related to electrons"""

	pumping_speed  :Expression  =  sp_property(type="dynamic",units="s^-1",coordinate1="../../../time")
	""" Pumped particle flux (in equivalent electrons)"""

	particle_flux_from_plasma  :Expression  =  sp_property(type="dynamic",units="s^-1",coordinate1="../../../time")
	""" Particle flux from the plasma (in equivalent electrons)"""

	particle_flux_from_wall  :array_type =  sp_property(type="dynamic",units="s^-1",coordinate1="1...3",coordinate2="../../../time")
	""" Particle flux from the wall corresponding to the conversion into various neutral
		types (first dimension: 1: cold; 2: thermal; 3: fast), in equivalent electrons"""

	gas_puff  :Expression  =  sp_property(type="dynamic",units="s^-1",coordinate1="../../../time")
	""" Gas puff rate (in equivalent electrons)"""

	power_inner_target  :Expression  =  sp_property(coordinate1="../../../time",units="W",type="dynamic")
	""" Electron power on the inner target"""

	power_outer_target  :Expression  =  sp_property(coordinate1="../../../time",units="W",type="dynamic")
	""" Electron power on the inner target"""


class _T_wall_global_quantitites_neutral_origin(SpTree):
	"""This structure allows distinguishing the species causing the sputtering"""

	element  :AoS[_T_plasma_composition_neutral_element_constant] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule of the incident species"""

	label  :str =  sp_property(type="constant")
	""" String identifying the incident species (e.g. H, D, CD4, ...)"""

	energies  :array_type =  sp_property(type="constant",units="eV",coordinate1="1...N")
	""" Array of energies of this incident species, on which the
		sputtering_physical_coefficient is tabulated"""

	sputtering_physical_coefficient  :array_type =  sp_property(type="dynamic",units="-",coordinate1="1...3",coordinate2="../energies",coordinate3="/time")
	""" Effective coefficient of physical sputtering for various neutral types (first
		dimension: 1: cold; 2: thermal; 3: fast), due to this incident species and for
		various energies (second dimension)"""

	sputtering_chemical_coefficient  :array_type =  sp_property(type="dynamic",units="-",coordinate1="1...3",coordinate2="/time")
	""" Effective coefficient of chemical sputtering for various neutral types (first
		dimension: 1: cold; 2: thermal; 3: fast), due to this incident species"""


class _T_wall_2d_limiter_unit(SpTree):
	"""2D limiter unit description"""

	name  :str =  sp_property(type="static")
	""" Name of the limiter unit"""

	closed  :int =  sp_property(type="static")
	""" Flag identifying whether the contour is closed (1) or open (0)"""

	outline  :_T_rz1d_static =  sp_property()
	""" Irregular outline of the limiting surface. Do NOT repeat the first point for
		closed contours"""

	phi_extensions  :array_type =  sp_property(type="static",units="rad",coordinate1="1...2",coordinate2="1...N")
	""" Simplified description of toroidal angle extensions of the unit, by a list of
		zones defined by their centre and full width (in toroidal angle). In each of
		these zones, the unit outline remains the same. Leave this node empty for an
		axisymmetric unit. The first dimension gives the centre and full width toroidal
		angle values for the unit. The second dimension represents the toroidal
		occurrences of the unit countour (i.e. the number of toroidal zones)."""

	resistivity  :float =  sp_property(type="static",units="ohm.m")
	""" Resistivity of the limiter unit"""


class _T_wall_2d_mobile_unit(SpTree):
	"""2D mobile parts description"""

	name  :str =  sp_property(type="static")
	""" Name of the mobile unit"""

	closed  :int =  sp_property(type="static")
	""" Flag identifying whether the contour is closed (1) or open (0)"""

	outline  :TimeSeriesAoS[_T_rz1d_dynamic_aos_time] =  sp_property(coordinate1="time",type="dynamic")
	""" Irregular outline of the mobile unit, for a set of time slices. Do NOT repeat
		the first point for closed contours"""

	phi_extensions  :array_type =  sp_property(type="static",units="rad",coordinate1="1...2",coordinate2="1...N")
	""" Simplified description of toroidal angle extensions of the unit, by a list of
		zones defined by their centre and full width (in toroidal angle). In each of
		these zones, the unit outline remains the same. Leave this node empty for an
		axisymmetric unit. The first dimension gives the centre and full width toroidal
		angle values for the unit. The second dimension represents the toroidal
		occurrences of the unit countour (i.e. the number of toroidal zones)."""

	resistivity  :float =  sp_property(type="static",units="ohm.m")
	""" Resistivity of the mobile unit"""


class _T_wall_description_ggd_energy_simple(SpTree):
	"""Incident and emitted energy fluxes related to the 3D wall description using the
		GGD"""

	incident  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="W.m^-2")
	""" Incident fluxes for various wall components (grid subsets)"""

	emitted  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="W.m^-2")
	""" Emitted fluxes for various wall components (grid subsets)"""


class _T_wall_description_ggd_energy_neutral_state(SpTree):
	"""Neutral state energy fluxes related to the 3D wall description using the GGD"""

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

	incident  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="W.m^-2")
	""" Incident fluxes for various wall components (grid subsets)"""

	emitted  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="W.m^-2")
	""" Emitted fluxes for various wall components (grid subsets)"""


class _T_wall_description_ggd_energy_ion_state(SpTree):
	"""Ion state energy fluxes related to the 3D wall description using the GGD"""

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

	incident  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="W.m^-2")
	""" Incident fluxes for various wall components (grid subsets)"""

	emitted  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="W.m^-2")
	""" Emitted fluxes for various wall components (grid subsets)"""


class _T_wall_description_ggd_particle_neutral_state(SpTree):
	"""Neutral state fluxes related to the 3D wall description using the GGD"""

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

	incident  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="m^-2.s^-1")
	""" Incident fluxes for various wall components (grid subsets)"""

	emitted  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="m^-2.s^-1")
	""" Emitted fluxes for various wall components (grid subsets)"""


class _T_wall_description_ggd_particle_ion_state(SpTree):
	"""Ion state fluxes related to the 3D wall description using the GGD"""

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

	incident  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="m^-2.s^-1")
	""" Incident fluxes for various wall components (grid subsets)"""

	emitted  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="m^-2.s^-1")
	""" Emitted fluxes for various wall components (grid subsets)"""


class _T_wall_description_ggd_particle_el(SpTree):
	"""Electron fluxes related to the 3D wall description using the GGD"""

	incident  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="m^-2.s^-1")
	""" Incident fluxes for various wall components (grid subsets)"""

	emitted  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="m^-2.s^-1")
	""" Emitted fluxes for various wall components (grid subsets)"""


class _T_wall_description_ggd_recycling_neutral_state(SpTree):
	"""Neutral state fluxes related to the 3D wall description using the GGD"""

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

	coefficient  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="-")
	""" Recycling coefficient for various wall components (grid subsets)"""


class _T_wall_description_ggd_recycling_ion_state(SpTree):
	"""Ion state fluxes related to the 3D wall description using the GGD"""

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

	coefficient  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="-")
	""" Recycling coefficient for various wall components (grid subsets)"""


class _T_wall_description_ggd_material(TimeSlice):
	"""Material forming the wall with GGD description"""

	grid_subset  :AoS[_E_materials] =  sp_property(coordinate1="1...N",doc_identifier="utilities/materials_identifier.xml")
	""" Material is described for various wall components (grid subsets), using the
		identifier convention below"""


class _T_wall_global_quantitites_neutral(SpTree):
	"""Simple 0D description of plasma-wall interaction, related to a given neutral
		species"""

	element  :AoS[_T_plasma_composition_neutral_element_constant] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	label  :str =  sp_property(type="constant")
	""" String identifying the species (e.g. H, D, CD4, ...)"""

	pumping_speed  :Expression  =  sp_property(type="dynamic",units="s^-1",coordinate1="/time")
	""" Pumped particle flux for that species"""

	particle_flux_from_plasma  :Expression  =  sp_property(type="dynamic",units="s^-1",coordinate1="/time")
	""" Particle flux from the plasma for that species"""

	particle_flux_from_wall  :array_type =  sp_property(type="dynamic",units="s^-1",coordinate1="1...3",coordinate2="/time")
	""" Particle flux from the wall corresponding to the conversion into various neutral
		types (first dimension: 1: cold; 2: thermal; 3: fast)"""

	gas_puff  :Expression  =  sp_property(type="dynamic",units="s^-1",coordinate1="/time")
	""" Gas puff rate for that species"""

	wall_inventory  :Expression  =  sp_property(type="dynamic",units="-",coordinate1="/time")
	""" Wall inventory, i.e. cumulated exchange of neutral species between plasma and
		wall from t = 0, positive if a species has gone to the wall, for that species"""

	recycling_particles_coefficient  :array_type =  sp_property(type="dynamic",units="-",coordinate1="1...3",coordinate2="/time")
	""" Particle recycling coefficient corresponding to the conversion into various
		neutral types (first dimension: 1: cold; 2: thermal; 3: fast)"""

	recycling_energy_coefficient  :array_type =  sp_property(type="dynamic",units="-",coordinate1="1...3",coordinate2="/time")
	""" Energy recycling coefficient corresponding to the conversion into various
		neutral types (first dimension: 1: cold; 2: thermal; 3: fast)"""

	incident_species  :AoS[_T_wall_global_quantitites_neutral_origin] =  sp_property(coordinate1="1...N",introduced_after_version="3.36.0")
	""" Sputtering coefficients due to a set of incident species"""


class _T_wall_2d_limiter(SpTree):
	"""2D limiter description"""

	type  :_T_identifier_static =  sp_property()
	""" Type of the limiter description. index = 0 for the official single contour
		limiter and 1 for the official disjoint PFC structure like first wall.
		Additional representations needed on a code-by-code basis follow same
		incremental pair tagging starting on index =2"""

	unit  :AoS[_T_wall_2d_limiter_unit] =  sp_property(coordinate1="1...N")
	""" Set of limiter units"""


class _T_wall_2d_mobile(SpTree):
	"""2D mobile parts description"""

	type  :_T_identifier_static =  sp_property()
	""" Type of the description"""

	unit  :AoS[_T_wall_2d_mobile_unit] =  sp_property(coordinate1="1...N")
	""" Set of mobile units"""


class _T_wall_description_ggd_energy_neutral(SpTree):
	"""Neutral energy fluxes related to the 3D wall description using the GGD"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying neutral (e.g. H, D, T, He, C, ...)"""

	ion_index  :int =  sp_property(type="dynamic")
	""" Index of the corresponding ion species in the ../../ion array"""

	incident  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="W.m^-2")
	""" Incident fluxes for various wall components (grid subsets)"""

	emitted  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="W.m^-2")
	""" Emitted fluxes for various wall components (grid subsets)"""

	multiple_states_flag  :int =  sp_property(type="dynamic")
	""" Multiple states calculation flag : 0-Only one state is considered; 1-Multiple
		states are considered and are described in the state structure"""

	state  :AoS[_T_wall_description_ggd_energy_neutral_state] =  sp_property(coordinate1="1...N")
	""" Fluxes related to the different states of the species"""


class _T_wall_description_ggd_energy_ion(SpTree):
	"""Ion energy fluxes related to the 3D wall description using the GGD"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	z_ion  :float =  sp_property(type="dynamic",units="Elementary Charge Unit")
	""" Ion charge (of the dominant ionisation state; lumped ions are allowed)"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying ion (e.g. H, D, T, He, C, D2, ...)"""

	neutral_index  :int =  sp_property(type="dynamic")
	""" Index of the corresponding neutral species in the ../../neutral array"""

	incident  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="W.m^-2")
	""" Incident fluxes for various wall components (grid subsets)"""

	emitted  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="W.m^-2")
	""" Emitted fluxes for various wall components (grid subsets)"""

	multiple_states_flag  :int =  sp_property(type="dynamic")
	""" Multiple states calculation flag : 0-Only the 'ion' level is considered and the
		'state' array of structure is empty; 1-Ion states are considered and are
		described in the 'state' array of structure"""

	state  :AoS[_T_wall_description_ggd_energy_ion_state] =  sp_property(coordinate1="1...N")
	""" Fluxes related to the different states of the species"""


class _T_wall_description_ggd_particle_neutral(SpTree):
	"""Neutral fluxes related to the 3D wall description using the GGD"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying neutral (e.g. H, D, T, He, C, ...)"""

	ion_index  :int =  sp_property(type="dynamic")
	""" Index of the corresponding ion species in the ../../ion array"""

	incident  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="m^-2.s^-1")
	""" Incident fluxes for various wall components (grid subsets)"""

	emitted  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="m^-2.s^-1")
	""" Emitted fluxes for various wall components (grid subsets)"""

	multiple_states_flag  :int =  sp_property(type="dynamic")
	""" Multiple states calculation flag : 0-Only one state is considered; 1-Multiple
		states are considered and are described in the state structure"""

	state  :AoS[_T_wall_description_ggd_particle_neutral_state] =  sp_property(coordinate1="1...N")
	""" Fluxes related to the different states of the species"""


class _T_wall_description_ggd_particle_ion(SpTree):
	"""Ion fluxes related to the 3D wall description using the GGD"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	z_ion  :float =  sp_property(type="dynamic",units="Elementary Charge Unit")
	""" Ion charge (of the dominant ionisation state; lumped ions are allowed)"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying ion (e.g. H, D, T, He, C, D2, ...)"""

	neutral_index  :int =  sp_property(type="dynamic")
	""" Index of the corresponding neutral species in the ../../neutral array"""

	incident  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="m^-2.s^-1")
	""" Incident fluxes for various wall components (grid subsets)"""

	emitted  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="m^-2.s^-1")
	""" Emitted fluxes for various wall components (grid subsets)"""

	multiple_states_flag  :int =  sp_property(type="dynamic")
	""" Multiple states calculation flag : 0-Only the 'ion' level is considered and the
		'state' array of structure is empty; 1-Ion states are considered and are
		described in the 'state' array of structure"""

	state  :AoS[_T_wall_description_ggd_particle_ion_state] =  sp_property(coordinate1="1...N")
	""" Fluxes related to the different states of the species"""


class _T_wall_description_ggd_recycling_neutral(SpTree):
	"""Neutral fluxes related to the 3D wall description using the GGD"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying neutral (e.g. H, D, T, He, C, ...)"""

	ion_index  :int =  sp_property(type="dynamic")
	""" Index of the corresponding ion species in the ../../ion array"""

	coefficient  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="-")
	""" Recycling coefficient for various wall components (grid subsets)"""

	multiple_states_flag  :int =  sp_property(type="dynamic")
	""" Multiple states calculation flag : 0-Only one state is considered; 1-Multiple
		states are considered and are described in the state structure"""

	state  :AoS[_T_wall_description_ggd_recycling_neutral_state] =  sp_property(coordinate1="1...N")
	""" Fluxes related to the different states of the species"""


class _T_wall_description_ggd_recycling_ion(SpTree):
	"""Ion fluxes related to the 3D wall description using the GGD"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	z_ion  :float =  sp_property(type="dynamic",units="Elementary Charge Unit")
	""" Ion charge (of the dominant ionisation state; lumped ions are allowed)"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying ion (e.g. H, D, T, He, C, D2, ...)"""

	neutral_index  :int =  sp_property(type="dynamic")
	""" Index of the corresponding neutral species in the ../../neutral array"""

	coefficient  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="-")
	""" Recycling coefficient for various wall components (grid subsets)"""

	multiple_states_flag  :int =  sp_property(type="dynamic")
	""" Multiple states calculation flag : 0-Only the 'ion' level is considered and the
		'state' array of structure is empty; 1-Ion states are considered and are
		described in the 'state' array of structure"""

	state  :AoS[_T_wall_description_ggd_recycling_ion_state] =  sp_property(coordinate1="1...N")
	""" Fluxes related to the different states of the species"""


class _T_wall_global_quantitites(SpTree):
	"""Simple 0D description of plasma-wall interaction"""

	electrons  :_T_wall_global_quantitites_electrons =  sp_property()
	""" Quantities related to electrons"""

	neutral  :AoS[_T_wall_global_quantitites_neutral] =  sp_property(coordinate1="1...N")
	""" Quantities related to the various neutral species"""

	temperature  :Expression  =  sp_property(type="dynamic",units="K",coordinate1="../../time")
	""" Wall temperature"""

	power_incident  :Expression  =  sp_property(type="dynamic",units="W",coordinate1="../../time",change_nbc_version="3.31.0",change_nbc_description="leaf_renamed",change_nbc_previous_name="power_from_plasma")
	""" Total power incident on the wall. This power is split in the various physical
		categories listed below"""

	power_conducted  :Expression  =  sp_property(type="dynamic",units="W",coordinate1="../../time")
	""" Power conducted by the plasma onto the wall"""

	power_convected  :Expression  =  sp_property(type="dynamic",units="W",coordinate1="../../time")
	""" Power convected by the plasma onto the wall"""

	power_radiated  :Expression  =  sp_property(type="dynamic",units="W",coordinate1="../../time")
	""" Net radiated power from plasma onto the wall (incident-reflected)"""

	power_black_body  :Expression  =  sp_property(type="dynamic",units="W",coordinate1="../../time")
	""" Black body radiated power emitted from the wall (emissivity is included)"""

	power_neutrals  :Expression  =  sp_property(type="dynamic",units="W",coordinate1="../../time")
	""" Net power from neutrals on the wall (positive means power is deposited on the
		wall)"""

	power_recombination_plasma  :Expression  =  sp_property(type="dynamic",units="W",coordinate1="../../time")
	""" Power deposited on the wall due to recombination of plasma ions"""

	power_recombination_neutrals  :Expression  =  sp_property(type="dynamic",units="W",coordinate1="../../time")
	""" Power deposited on the wall due to recombination of neutrals into a ground state
		(e.g. molecules)"""

	power_currents  :Expression  =  sp_property(type="dynamic",units="W",coordinate1="../../time")
	""" Power deposited on the wall due to electric currents (positive means power is
		deposited on the target)"""

	power_to_cooling  :Expression  =  sp_property(type="dynamic",units="W",coordinate1="../../time")
	""" Power to cooling systems"""

	power_inner_target_ion_total  :Expression  =  sp_property(coordinate1="../../time",units="W",type="dynamic")
	""" Total ion (summed over ion species) power on the inner target"""

	power_density_inner_target_max  :Expression  =  sp_property(coordinate1="../../time",units="W",type="dynamic")
	""" Maximum power density on the inner target"""

	power_density_outer_target_max  :Expression  =  sp_property(coordinate1="../../time",units="W",type="dynamic")
	""" Maximum power density on the outer target"""

	current_tor  :Expression  =  sp_property(units="A",coordinate1="../../time",type="dynamic")
	""" Toroidal current flowing in the vacuum vessel"""


class _T_wall_2d(SpTree):
	"""2D wall description"""

	type  :_T_identifier_static =  sp_property()
	""" Type of the description. index = 0 for equilibrium codes (single closed limiter
		and vessel); 1 for gas-tight walls (disjoint PFCs with inner vessel as last
		limiter_unit; no vessel structure); 2 for free boundary codes (disjoint PFCs and
		vessel)"""

	limiter  :_T_wall_2d_limiter =  sp_property()
	""" Description of the immobile limiting surface(s) or plasma facing components for
		defining the Last Closed Flux Surface."""

	mobile  :_T_wall_2d_mobile =  sp_property()
	""" In case of mobile plasma facing components, use the time-dependent description
		below this node to provide the full outline of the closest PFC surfaces to the
		plasma. Even in such a case, the 'limiter' structure is still used to provide
		the outermost limiting surface (can be used e.g. to define the boundary of the
		mesh of equilibrium reconstruction codes)"""

	vessel  :_T_vessel_2d =  sp_property()
	""" Mechanical structure of the vacuum vessel. The vessel is described as a set of
		nested layers with given physics properties; Two representations are admitted
		for each vessel unit : annular (two contours) or block elements."""


class _T_wall_description_ggd_kinetic(SpTree):
	"""Energy fluxes due to kinetic energy of particles related to the 3D wall
		description using the GGD"""

	electrons  :_T_wall_description_ggd_energy_simple =  sp_property()
	""" Electron fluxes. Fluxes are given at the wall, after the sheath."""

	ion  :AoS[_T_wall_description_ggd_energy_ion] =  sp_property(coordinate1="1...N")
	""" Fluxes related to the various ion species, in the sense of isonuclear or
		isomolecular sequences. Ionisation states (and other types of states) must be
		differentiated at the state level below. Fluxes are given at the wall, after the
		sheath."""

	neutral  :AoS[_T_wall_description_ggd_particle_neutral] =  sp_property(coordinate1="1...N")
	""" Neutral species fluxes"""


class _T_wall_description_ggd_recombination(SpTree):
	"""Energy fluxes due to recombination related to the 3D wall description using the
		GGD"""

	ion  :AoS[_T_wall_description_ggd_energy_ion] =  sp_property(coordinate1="1...N")
	""" Fluxes related to the various ion species, in the sense of isonuclear or
		isomolecular sequences. Ionisation states (and other types of states) must be
		differentiated at the state level below"""

	neutral  :AoS[_T_wall_description_ggd_particle_neutral] =  sp_property(coordinate1="1...N")
	""" Neutral species fluxes"""


class _T_wall_description_ggd_particle(SpTree):
	"""Patricle fluxes related to the 3D wall description using the GGD"""

	electrons  :_T_wall_description_ggd_particle_el =  sp_property()
	""" Electron fluxes"""

	ion  :AoS[_T_wall_description_ggd_particle_ion] =  sp_property(coordinate1="1...N")
	""" Fluxes related to the various ion species, in the sense of isonuclear or
		isomolecular sequences. Ionisation states (and other types of states) must be
		differentiated at the state level below"""

	neutral  :AoS[_T_wall_description_ggd_particle_neutral] =  sp_property(coordinate1="1...N")
	""" Neutral species fluxes"""


class _T_wall_description_ggd_recycling(SpTree):
	"""Recycling coefficients in the 3D wall description using the GGD"""

	ion  :AoS[_T_wall_description_ggd_recycling_ion] =  sp_property(coordinate1="1...N")
	""" Recycling coefficients for the various ion species, in the sense of isonuclear
		or isomolecular sequences. Ionisation states (and other types of states) must be
		differentiated at the state level below"""

	neutral  :AoS[_T_wall_description_ggd_recycling_neutral] =  sp_property(coordinate1="1...N")
	""" Recycling coefficients for the various neutral species"""


class _T_wall_description_ggd_energy(SpTree):
	"""Patricle energy fluxes related to the 3D wall description using the GGD"""

	radiation  :_T_wall_description_ggd_energy_simple =  sp_property()
	""" Total radiation, not split by process"""

	current  :_T_wall_description_ggd_energy_simple =  sp_property()
	""" Current energy fluxes"""

	recombination  :_T_wall_description_ggd_recombination =  sp_property()
	""" Wall recombination"""

	kinetic  :_T_wall_description_ggd_kinetic =  sp_property()
	""" Energy fluxes due to the kinetic energy of particles"""


class _T_wall_description_ggd_ggd(TimeSlice):
	"""Physics quantities related to the 3D wall description using the GGD"""

	power_density  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="W.m^-2")
	""" Net power density arriving on the wall surface, for various wall components
		(grid subsets)"""

	temperature  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="K")
	""" Temperature of the wall, for various wall components (grid subsets)"""

	v_biasing  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="V",introduced_after_version="3.37.2")
	""" Electric potential applied to the wall element by outside means, for various
		wall components (grid subsets). Different from the plasma electric potential or
		the sheath potential drop."""

	recycling  :_T_wall_description_ggd_recycling =  sp_property(introduced_after_version="3.37.2")
	""" Fraction of incoming particles that is reflected back to the vacuum chamber"""

	particle_fluxes  :_T_wall_description_ggd_particle =  sp_property(introduced_after_version="3.37.2")
	""" Particle fluxes. The incident and emitted components are distinguished. The net
		flux received by the wall is equal to incident - emitted"""

	energy_fluxes  :_T_wall_description_ggd_energy =  sp_property(introduced_after_version="3.37.2")
	""" Energy fluxes. The incident and emitted components are distinguished. The net
		flux received by the wall is equal to incident - emitted"""


class _T_wall_description_ggd(SpTree):
	"""3D wall description using the GGD"""

	type  :_T_identifier_static =  sp_property()
	""" Type of wall: index = 0 for gas tight and 1 for a wall with holes/open ports"""

	grid_ggd  :TimeSeriesAoS[_T_generic_grid_aos3_root] =  sp_property(coordinate1="time",type="dynamic")
	""" Wall geometry described using the Generic Grid Description, for various time
		slices (in case of mobile wall elements). The timebase of this array of
		structure must be a subset of the timebase on which physical quantities are
		described (../ggd structure). Grid_subsets are used to describe various wall
		components in a modular way."""

	material  :TimeSeriesAoS[_T_wall_description_ggd_material] =  sp_property(coordinate1="time",coordinate1_same_as="../grid_ggd",introduced_after_version="3.37.2",type="dynamic")
	""" Material of each grid_ggd object, given for each slice of the grid_ggd time base
		(the material is not supposed to change, but grid_ggd may evolve with time)"""

	ggd  :TimeSeriesAoS[_T_wall_description_ggd_ggd] =  sp_property(coordinate1="time",type="dynamic")
	""" Wall physics quantities represented using the general grid description, for
		various time slices."""


class _T_wall(IDS):
	"""Description of the torus wall and its interaction with the plasma
	lifecycle_status: alpha
	lifecycle_version: 3.1.0
	lifecycle_last_change: 3.38.0"""

	dd_version="v3_38_1_dirty"
	ids_name="wall"

	temperature_reference  :_T_temperature_reference =  sp_property(introduced_after_version="3.32.1")
	""" Reference temperature for which the machine description data is given in this
		IDS"""

	first_wall_surface_area  :float =  sp_property(units="m^2",type="static")
	""" First wall surface area"""

	first_wall_power_flux_peak  :Signal =  sp_property(units="W.m^-2")
	""" Peak power flux on the first wall"""

	first_wall_enclosed_volume  :float =  sp_property(units="m^3",type="static",introduced_after_version="3.36.0")
	""" Volume available to gas or plasma enclosed by the first wall contour"""

	global_quantities  :_T_wall_global_quantitites =  sp_property()
	""" Simple 0D description of plasma-wall interaction"""

	description_2d  :AoS[_T_wall_2d] =  sp_property(coordinate1="1...N")
	""" Set of 2D wall descriptions, for each type of possible physics or engineering
		configurations necessary (gas tight vs wall with ports and holes, coarse vs fine
		representation, single contour limiter, disjoint gapped plasma facing
		components, ...). A simplified description of the toroidal extension of the 2D
		contours is also provided by using the phi_extensions nodes."""

	description_ggd  :AoS[_T_wall_description_ggd] =  sp_property(coordinate1="1...N")
	""" Set of 3D wall descriptions, described using the GGD, for each type of possible
		physics or engineering configurations necessary (gas tight vs wall with ports
		and holes, coarse vs fine representation, ...)."""
