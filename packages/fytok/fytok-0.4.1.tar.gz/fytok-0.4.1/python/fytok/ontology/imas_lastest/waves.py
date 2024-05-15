"""
  This module containes the _FyTok_ wrapper of IMAS/dd/waves
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_plasma_composition_neutral_element,_T_core_radial_grid,_T_generic_grid_scalar,_T_generic_grid_dynamic,_T_identifier_dynamic_aos3,_T_waves_coherent_wave_identifier,_T_identifier,_T_b_tor_vacuum_1,_T_rz1d_dynamic_1

class _T_waves_CPX_1D(SpTree):
	"""Structure for 1D complex number, real and imaginary parts"""

	real  :array_type =  sp_property(type="dynamic",units="as_parent",coordinate1="../../../length")
	""" Real part"""

	imaginary  :array_type =  sp_property(type="dynamic",units="as_parent",coordinate1="../../../length")
	""" Imaginary part"""


class _T_waves_CPX_amp_phase_1D(SpTree):
	"""Structure for 1D complex number, amplitude and phase"""

	amplitude  :Expression  =  sp_property(type="dynamic",units="as_parent",coordinate1="../../../grid/rho_tor_norm")
	""" Amplitude"""

	phase  :Expression  =  sp_property(type="dynamic",units="as_parent",coordinate1="../../../grid/rho_tor_norm")
	""" Phase"""


class _T_waves_CPX_amp_phase_2D(SpTree):
	"""Structure for 2D complex number, amplitude and phase"""

	amplitude  :array_type =  sp_property(type="dynamic",units="as_parent",coordinate1="1...N",coordinate2="1...N",coordinate1_same_as="../../../grid/r",coordinate2_same_as="../../../grid/r")
	""" Amplitude"""

	phase  :array_type =  sp_property(type="dynamic",units="as_parent",coordinate1="1...N",coordinate2="1...N",coordinate1_same_as="../../../grid/r",coordinate2_same_as="../../../grid/r")
	""" Phase"""


class _T_waves_rzphipsitheta1d_dynamic_aos3(SpTree):
	"""Structure for R, Z, Phi, Psi, Theta positions (1D, dynamic within a type 3 array
		of structure)"""

	r  :array_type =  sp_property(type="dynamic",units="m",coordinate1="../../length")
	""" Major radius"""

	z  :array_type =  sp_property(type="dynamic",units="m",coordinate1="../../length")
	""" Height"""

	phi  :array_type =  sp_property(type="dynamic",units="rad",coordinate1="../../length")
	""" Toroidal angle"""

	psi  :array_type =  sp_property(type="dynamic",units="Wb",coordinate1="../../length")
	""" Poloidal flux"""

	theta  :array_type =  sp_property(type="dynamic",units="rad",coordinate1="../../length")
	""" Poloidal angle"""


class _T_waves_coherent_wave_beam_tracing_ion_state(SpTree):
	"""State related quantities for beam tracing"""

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

	power  :array_type =  sp_property(units="W",type="dynamic",coordinate1="../../../length")
	""" Power absorbed along the beam by the species"""


class _T_waves_coherent_wave_beam_tracing_electrons(SpTree):
	"""Electrons related quantities for beam tracing"""

	power  :array_type =  sp_property(units="W",type="dynamic",coordinate1="../../length")
	""" Power absorbed along the beam by the species"""


class _T_waves_coherent_wave_beam_tracing_power_flow(SpTree):
	"""Power flow for beam tracing"""

	perpendicular  :array_type =  sp_property(units="-",type="dynamic",coordinate1="../../length")
	""" Normalized power flow in the direction perpendicular to the magnetic field"""

	parallel  :array_type =  sp_property(units="-",type="dynamic",coordinate1="../../length")
	""" Normalized power flow in the direction parallel to the magnetic field"""


class _T_waves_coherent_wave_beam_tracing_beam_k(SpTree):
	"""Beam wave vector"""

	k_r  :array_type =  sp_property(units="m^-1",type="dynamic",coordinate1="../../length")
	""" Wave vector component in the major radius direction"""

	k_z  :array_type =  sp_property(units="m^-1",type="dynamic",coordinate1="../../length")
	""" Wave vector component in the vertical direction"""

	k_tor  :array_type =  sp_property(units="m^-1",type="dynamic",coordinate1="../../length")
	""" Wave vector component in the toroidal direction"""

	n_parallel  :array_type =  sp_property(units="-",type="dynamic",coordinate1="../../length")
	""" Parallel refractive index"""

	n_perpendicular  :array_type =  sp_property(units="-",type="dynamic",coordinate1="../../length")
	""" Perpendicular refractive index"""

	n_tor  :array_type =  sp_property(type="dynamic",coordinate1="../../length OR 1")
	""" Toroidal wave number, contains a single value if varying_ntor = 1 to avoid
		useless repetition constant values"""

	varying_n_tor  :int =  sp_property(type="dynamic")
	""" Flag telling whether n_tor is constant along the ray path (0) or varying (1)"""


class _T_waves_coherent_wave_global_quantities_ion_state(SpTree):
	"""Global quantities related to a given ion species state"""

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
	""" Wave power absorbed by the thermal particle population"""

	power_thermal_n_tor  :array_type =  sp_property(type="dynamic",units="W",coordinate1="../../../n_tor")
	""" Wave power absorbed by the thermal particle population per toroidal mode number"""

	power_fast  :float =  sp_property(type="dynamic",units="W")
	""" Wave power absorbed by the fast particle population"""

	power_fast_n_tor  :array_type =  sp_property(type="dynamic",units="W",coordinate1="../../../n_tor")
	""" Wave power absorbed by the fast particle population per toroidal mode number"""


class _T_waves_coherent_wave_global_quantities_electrons(SpTree):
	"""Global quantities related to electrons"""

	power_thermal  :float =  sp_property(type="dynamic",units="W")
	""" Wave power absorbed by the thermal particle population"""

	power_thermal_n_tor  :array_type =  sp_property(type="dynamic",units="W",coordinate1="../../n_tor")
	""" Wave power absorbed by the thermal particle population per toroidal mode number"""

	power_fast  :float =  sp_property(type="dynamic",units="W")
	""" Wave power absorbed by the fast particle population"""

	power_fast_n_tor  :array_type =  sp_property(type="dynamic",units="W",coordinate1="../../n_tor")
	""" Wave power absorbed by the fast particle population per toroidal mode number"""

	distribution_assumption  :int =  sp_property(type="dynamic")
	""" Assumption on the distribution function used by the wave solver to calculate the
		power deposition on this species: 0 = Maxwellian (linear absorption); 1 =
		quasi-linear (F given by a distributions IDS)."""


class _T_waves_coherent_wave_profiles_1d_ion_state(SpTree):
	"""Radial profiles (RF waves) related to a given ion species state"""

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

	power_density_thermal  :Expression  =  sp_property(units="W.m^-3",type="dynamic",coordinate1="../../../grid/rho_tor_norm")
	""" Flux surface averaged absorbed wave power density on the thermal species"""

	power_density_thermal_n_tor  :array_type =  sp_property(units="W.m^-3",type="dynamic",coordinate1="../../../grid/rho_tor_norm",coordinate2="../../../n_tor")
	""" Flux surface averaged absorbed wave power density on the thermal species, per
		toroidal mode number"""

	power_density_fast  :Expression  =  sp_property(units="W.m^-3",type="dynamic",coordinate1="../../../grid/rho_tor_norm")
	""" Flux surface averaged absorbed wave power density on the fast species"""

	power_density_fast_n_tor  :array_type =  sp_property(units="W.m^-3",type="dynamic",coordinate1="../../../grid/rho_tor_norm",coordinate2="../../../n_tor")
	""" Flux surface averaged absorbed wave power density on the fast species, per
		toroidal mode number"""

	power_inside_thermal  :Expression  =  sp_property(units="W",type="dynamic",coordinate1="../../../grid/rho_tor_norm")
	""" Absorbed wave power on thermal species inside a flux surface (cumulative volume
		integral of the absorbed power density)"""

	power_inside_thermal_n_tor  :array_type =  sp_property(units="W",type="dynamic",coordinate1="../../../grid/rho_tor_norm",coordinate2="../../../n_tor")
	""" Absorbed wave power on thermal species inside a flux surface (cumulative volume
		integral of the absorbed power density), per toroidal mode number"""

	power_inside_fast  :Expression  =  sp_property(units="W",type="dynamic",coordinate1="../../../grid/rho_tor_norm")
	""" Absorbed wave power on thermal species inside a flux surface (cumulative volume
		integral of the absorbed power density)"""

	power_inside_fast_n_tor  :array_type =  sp_property(units="W",type="dynamic",coordinate1="../../../grid/rho_tor_norm",coordinate2="../../../n_tor")
	""" Absorbed wave power on thermal species inside a flux surface (cumulative volume
		integral of the absorbed power density), per toroidal mode number"""


class _T_waves_coherent_wave_profiles_1d_electrons(SpTree):
	"""Radial profiles (RF waves) related to electrons"""

	power_density_thermal  :Expression  =  sp_property(units="W.m^-3",type="dynamic",coordinate1="../../grid/rho_tor_norm")
	""" Flux surface averaged absorbed wave power density on the thermal species"""

	power_density_thermal_n_tor  :array_type =  sp_property(units="W.m^-3",type="dynamic",coordinate1="../../grid/rho_tor_norm",coordinate2="../../n_tor")
	""" Flux surface averaged absorbed wave power density on the thermal species, per
		toroidal mode number"""

	power_density_fast  :Expression  =  sp_property(units="W.m^-3",type="dynamic",coordinate1="../../grid/rho_tor_norm")
	""" Flux surface averaged absorbed wave power density on the fast species"""

	power_density_fast_n_tor  :array_type =  sp_property(units="W.m^-3",type="dynamic",coordinate1="../../grid/rho_tor_norm",coordinate2="../../n_tor")
	""" Flux surface averaged absorbed wave power density on the fast species, per
		toroidal mode number"""

	power_inside_thermal  :Expression  =  sp_property(units="W",type="dynamic",coordinate1="../../grid/rho_tor_norm")
	""" Absorbed wave power on thermal species inside a flux surface (cumulative volume
		integral of the absorbed power density)"""

	power_inside_thermal_n_tor  :array_type =  sp_property(units="W",type="dynamic",coordinate1="../../grid/rho_tor_norm",coordinate2="../../n_tor")
	""" Absorbed wave power on thermal species inside a flux surface (cumulative volume
		integral of the absorbed power density), per toroidal mode number"""

	power_inside_fast  :Expression  =  sp_property(units="W",type="dynamic",coordinate1="../../grid/rho_tor_norm")
	""" Absorbed wave power on thermal species inside a flux surface (cumulative volume
		integral of the absorbed power density)"""

	power_inside_fast_n_tor  :array_type =  sp_property(units="W",type="dynamic",coordinate1="../../grid/rho_tor_norm",coordinate2="../../n_tor")
	""" Absorbed wave power on thermal species inside a flux surface (cumulative volume
		integral of the absorbed power density), per toroidal mode number"""


class _T_waves_coherent_wave_profiles_2d_ion_state(SpTree):
	"""Global quantities related to a given ion species state"""

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

	power_density_thermal  :array_type =  sp_property(units="W.m^-3",type="dynamic",coordinate1="1...N",coordinate2="1...N",coordinate1_same_as="../../../grid/r",coordinate2_same_as="../../../grid/r")
	""" Absorbed wave power density on the thermal species"""

	power_density_thermal_n_tor  :array_type =  sp_property(units="W.m^-3",type="dynamic",coordinate1="1...N",coordinate2="1...N",coordinate1_same_as="../../../grid/r",coordinate2_same_as="../../../grid/r",coordinate3="../../../n_tor")
	""" Absorbed wave power density on the thermal species, per toroidal mode number"""

	power_density_fast  :array_type =  sp_property(units="W.m^-3",type="dynamic",coordinate1="1...N",coordinate2="1...N",coordinate1_same_as="../../../grid/r",coordinate2_same_as="../../../grid/r")
	""" Absorbed wave power density on the fast species"""

	power_density_fast_n_tor  :array_type =  sp_property(units="W.m^-3",type="dynamic",coordinate1="1...N",coordinate2="1...N",coordinate1_same_as="../../../grid/r",coordinate2_same_as="../../../grid/r",coordinate3="../../../n_tor")
	""" Absorbed wave power density on the fast species, per toroidal mode number"""


class _T_waves_coherent_wave_profiles_2d_electrons(SpTree):
	"""Global quantities related to electrons"""

	power_density_thermal  :array_type =  sp_property(units="W.m^-3",type="dynamic",coordinate1="1...N",coordinate2="1...N",coordinate1_same_as="../../grid/r",coordinate2_same_as="../../grid/r")
	""" Absorbed wave power density on the thermal species"""

	power_density_thermal_n_tor  :array_type =  sp_property(units="W.m^-3",type="dynamic",coordinate1="1...N",coordinate2="1...N",coordinate1_same_as="../../grid/r",coordinate2_same_as="../../grid/r",coordinate3="../../n_tor")
	""" Absorbed wave power density on the thermal species, per toroidal mode number"""

	power_density_fast  :array_type =  sp_property(units="W.m^-3",type="dynamic",coordinate1="1...N",coordinate2="1...N",coordinate1_same_as="../../grid/r",coordinate2_same_as="../../grid/r")
	""" Absorbed wave power density on the fast species"""

	power_density_fast_n_tor  :array_type =  sp_property(units="W.m^-3",type="dynamic",coordinate1="1...N",coordinate2="1...N",coordinate1_same_as="../../grid/r",coordinate2_same_as="../../grid/r",coordinate3="../../n_tor")
	""" Absorbed wave power density on the fast species, per toroidal mode number"""


class _T_waves_coherent_wave_beam_tracing_ion(SpTree):
	"""Ion related quantities for beam tracing"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	z_ion  :float =  sp_property(type="dynamic",units="Elementary Charge Unit")
	""" Ion charge (of the dominant ionisation state; lumped ions are allowed)."""

	label  :str =  sp_property(type="dynamic")
	""" String identifying the species (e.g. H+, D+, T+, He+2, C+, D2, DT, CD4, ...)"""

	power  :array_type =  sp_property(units="W",type="dynamic",coordinate1="../../length")
	""" Power absorbed along the beam by the species"""

	multiple_states_flag  :int =  sp_property(type="dynamic")
	""" Multiple state calculation flag : 0-Only one state is considered; 1-Multiple
		states are considered and are described in the state structure"""

	state  :AoS[_T_waves_coherent_wave_beam_tracing_ion_state] =  sp_property(coordinate1="1...N_charge_states")
	""" Collisional exchange with the various states of the ion species (ionisation,
		energy, excitation, ...)"""


class _T_waves_coherent_wave_beam_tracing_beam_e_field(SpTree):
	"""Components of the electric field for beam tracing"""

	plus  :_T_waves_CPX_1D =  sp_property(units="V.m^-1")
	""" Left hand polarised electric field component"""

	minus  :_T_waves_CPX_1D =  sp_property(units="V.m^-1")
	""" Right hand polarised electric field component"""

	parallel  :_T_waves_CPX_1D =  sp_property(units="V.m^-1")
	""" Parallel to magnetic field polarised electric field component"""


class _T_waves_coherent_wave_global_quantities_ion(SpTree):
	"""Global quantities related to a given ion species"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	z_ion  :float =  sp_property(type="dynamic",units="Elementary Charge Unit")
	""" Ion charge (of the dominant ionisation state; lumped ions are allowed)."""

	label  :str =  sp_property(type="dynamic")
	""" String identifying the species (e.g. H+, D+, T+, He+2, C+, D2, DT, CD4, ...)"""

	power_thermal  :float =  sp_property(type="dynamic",units="W")
	""" Wave power absorbed by the thermal particle population"""

	power_thermal_n_tor  :array_type =  sp_property(type="dynamic",units="W",coordinate1="../../n_tor")
	""" Wave power absorbed by the thermal particle population per toroidal mode number"""

	power_fast  :float =  sp_property(type="dynamic",units="W")
	""" Wave power absorbed by the fast particle population"""

	power_fast_n_tor  :array_type =  sp_property(type="dynamic",units="W",coordinate1="../../n_tor")
	""" Wave power absorbed by the fast particle population per toroidal mode number"""

	multiple_states_flag  :int =  sp_property(type="dynamic")
	""" Multiple state calculation flag : 0-Only one state is considered; 1-Multiple
		states are considered and are described in the state structure"""

	distribution_assumption  :int =  sp_property(type="dynamic")
	""" Assumption on the distribution function used by the wave solver to calculate the
		power deposition on this species: 0 = Maxwellian (linear absorption); 1 =
		quasi-linear (F given by a distributions IDS)."""

	state  :AoS[_T_waves_coherent_wave_global_quantities_ion_state] =  sp_property(coordinate1="1...N_charge_states")
	""" Collisional exchange with the various states of the ion species (ionisation,
		energy, excitation, ...)"""


class _T_waves_coherent_wave_profiles_1d_ion(SpTree):
	"""Radial profiles (RF waves) related to a given ion species"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	z_ion  :float =  sp_property(type="dynamic",units="Elementary Charge Unit")
	""" Ion charge (of the dominant ionisation state; lumped ions are allowed)."""

	label  :str =  sp_property(type="dynamic")
	""" String identifying the species (e.g. H+, D+, T+, He+2, C+, D2, DT, CD4, ...)"""

	power_density_thermal  :Expression  =  sp_property(units="W.m^-3",type="dynamic",coordinate1="../../grid/rho_tor_norm")
	""" Flux surface averaged absorbed wave power density on the thermal species"""

	power_density_thermal_n_tor  :array_type =  sp_property(units="W.m^-3",type="dynamic",coordinate1="../../grid/rho_tor_norm",coordinate2="../../n_tor")
	""" Flux surface averaged absorbed wave power density on the thermal species, per
		toroidal mode number"""

	power_density_fast  :Expression  =  sp_property(units="W.m^-3",type="dynamic",coordinate1="../../grid/rho_tor_norm")
	""" Flux surface averaged absorbed wave power density on the fast species"""

	power_density_fast_n_tor  :array_type =  sp_property(units="W.m^-3",type="dynamic",coordinate1="../../grid/rho_tor_norm",coordinate2="../../n_tor")
	""" Flux surface averaged absorbed wave power density on the fast species, per
		toroidal mode number"""

	power_inside_thermal  :Expression  =  sp_property(units="W",type="dynamic",coordinate1="../../grid/rho_tor_norm")
	""" Absorbed wave power on thermal species inside a flux surface (cumulative volume
		integral of the absorbed power density)"""

	power_inside_thermal_n_tor  :array_type =  sp_property(units="W",type="dynamic",coordinate1="../../grid/rho_tor_norm",coordinate2="../../n_tor")
	""" Absorbed wave power on thermal species inside a flux surface (cumulative volume
		integral of the absorbed power density), per toroidal mode number"""

	power_inside_fast  :Expression  =  sp_property(units="W",type="dynamic",coordinate1="../../grid/rho_tor_norm")
	""" Absorbed wave power on thermal species inside a flux surface (cumulative volume
		integral of the absorbed power density)"""

	power_inside_fast_n_tor  :array_type =  sp_property(units="W",type="dynamic",coordinate1="../../grid/rho_tor_norm",coordinate2="../../n_tor")
	""" Absorbed wave power on thermal species inside a flux surface (cumulative volume
		integral of the absorbed power density), per toroidal mode number"""

	multiple_states_flag  :int =  sp_property(type="dynamic")
	""" Multiple state calculation flag : 0-Only one state is considered; 1-Multiple
		states are considered and are described in the state structure"""

	state  :AoS[_T_waves_coherent_wave_profiles_1d_ion_state] =  sp_property(coordinate1="1...N_charge_states")
	""" Collisional exchange with the various states of the ion species (ionisation,
		energy, excitation, ...)"""


class _T_waves_profiles_1d_e_field_n_tor(SpTree):
	"""Components of the surface averaged electric field"""

	plus  :_T_waves_CPX_amp_phase_1D =  sp_property(units="V.m^-1")
	""" Left hand polarised electric field component for every flux surface"""

	minus  :_T_waves_CPX_amp_phase_1D =  sp_property(units="V.m^-1")
	""" Right hand polarised electric field component for every flux surface"""

	parallel  :_T_waves_CPX_amp_phase_1D =  sp_property(units="V.m^-1")
	""" Parallel electric field component for every flux surface"""


class _T_waves_coherent_wave_full_wave_e_field(SpTree):
	"""Components of the full wave electric field"""

	plus  :AoS[_T_generic_grid_scalar] =  sp_property(units="V.m^-1",coordinate1="1...N")
	""" Left hand circularly polarised component of the perpendicular (to the static
		magnetic field) electric field, given on various grid subsets"""

	minus  :AoS[_T_generic_grid_scalar] =  sp_property(units="V.m^-1",coordinate1="1...N")
	""" Right hand circularly polarised component of the perpendicular (to the static
		magnetic field) electric field, given on various grid subsets"""

	parallel  :AoS[_T_generic_grid_scalar] =  sp_property(units="V.m^-1",coordinate1="1...N")
	""" Parallel (to the static magnetic field) component of electric field, given on
		various grid subsets"""

	normal  :AoS[_T_generic_grid_scalar] =  sp_property(units="V.m^-1",coordinate1="1...N")
	""" Magnitude of wave electric field normal to a flux surface, given on various grid
		subsets"""

	bi_normal  :AoS[_T_generic_grid_scalar] =  sp_property(units="V.m^-1",coordinate1="1...N")
	""" Magnitude of perpendicular (to the static magnetic field) wave electric field
		tangent to a flux surface, given on various grid subsets"""


class _T_waves_coherent_wave_full_wave_b_field(SpTree):
	"""Components of the full wave magnetic field"""

	parallel  :AoS[_T_generic_grid_scalar] =  sp_property(units="V.m^-1",coordinate1="1...N")
	""" Parallel (to the static magnetic field) component of the wave magnetic field,
		given on various grid subsets"""

	normal  :AoS[_T_generic_grid_scalar] =  sp_property(units="V.m^-1",coordinate1="1...N")
	""" Magnitude of wave magnetic field normal to a flux surface, given on various grid
		subsets"""

	bi_normal  :AoS[_T_generic_grid_scalar] =  sp_property(units="V.m^-1",coordinate1="1...N")
	""" Magnitude of perpendicular (to the static magnetic field) wave magnetic field
		tangent to a flux surface, given on various grid subsets"""


class _T_waves_coherent_wave_profiles_2d_grid(SpTree):
	"""2D grid for waves"""

	type  :_T_identifier_dynamic_aos3 =  sp_property(coordinate1="../rho_tor_norm",units="m^3")
	""" Grid type: index=0: Rectangular grid in the (R,Z) coordinates; index=1:
		Rectangular grid in the (radial, theta_geometric) coordinates; index=2:
		Rectangular grid in the (radial, theta_straight) coordinates. index=3:
		unstructured grid."""

	r  :array_type =  sp_property(type="dynamic",coordinate1="1...N",coordinate2="1...N",units="m")
	""" Major radius"""

	z  :array_type =  sp_property(type="dynamic",coordinate1="1...N",coordinate2="1...N",coordinate1_same_as="../r",coordinate2_same_as="../r",units="m")
	""" Height"""

	theta_straight  :array_type =  sp_property(type="dynamic",coordinate1="1...N",coordinate2="1...N",coordinate1_same_as="../r",coordinate2_same_as="../r",units="rad")
	""" Straight field line poloidal angle"""

	theta_geometric  :array_type =  sp_property(type="dynamic",coordinate1="1...N",coordinate2="1...N",coordinate1_same_as="../r",coordinate2_same_as="../r",units="rad")
	""" Geometrical poloidal angle"""

	rho_tor_norm  :array_type =  sp_property(type="dynamic",coordinate1="1...N",coordinate2="1...N",coordinate1_same_as="../r",coordinate2_same_as="../r",units="-")
	""" Normalised toroidal flux coordinate. The normalizing value for rho_tor_norm, is
		the toroidal flux coordinate at the equilibrium boundary (LCFS or 99.x % of the
		LCFS in case of a fixed boundary equilibium calculation)"""

	rho_tor  :array_type =  sp_property(type="dynamic",coordinate1="1...N",coordinate2="1...N",coordinate1_same_as="../r",coordinate2_same_as="../r",units="m")
	""" Toroidal flux coordinate. The toroidal field used in its definition is indicated
		under vacuum_toroidal_field/b0"""

	psi  :array_type =  sp_property(coordinate1="1...N",coordinate2="1...N",coordinate1_same_as="../r",coordinate2_same_as="../r",units="Wb",type="dynamic")
	""" Poloidal magnetic flux"""

	volume  :array_type =  sp_property(type="dynamic",coordinate1="1...N",coordinate2="1...N",coordinate1_same_as="../r",coordinate2_same_as="../r",units="m^3")
	""" Volume enclosed inside the magnetic surface"""

	area  :array_type =  sp_property(type="dynamic",coordinate1="1...N",coordinate2="1...N",coordinate1_same_as="../r",coordinate2_same_as="../r",units="m^2")
	""" Cross-sectional area of the flux surface"""


class _T_waves_coherent_wave_profiles_2d_ion(SpTree):
	"""Global quantities related to a given ion species"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	z_ion  :float =  sp_property(type="dynamic",units="Elementary Charge Unit")
	""" Ion charge (of the dominant ionisation state; lumped ions are allowed)."""

	label  :str =  sp_property(type="dynamic")
	""" String identifying the species (e.g. H+, D+, T+, He+2, C+, D2, DT, CD4, ...)"""

	power_density_thermal  :array_type =  sp_property(units="W.m^-3",type="dynamic",coordinate1="1...N",coordinate2="1...N",coordinate1_same_as="../../grid/r",coordinate2_same_as="../../grid/r")
	""" Absorbed wave power density on the thermal species"""

	power_density_thermal_n_tor  :array_type =  sp_property(units="W.m^-3",type="dynamic",coordinate1="1...N",coordinate2="1...N",coordinate1_same_as="../../grid/r",coordinate2_same_as="../../grid/r",coordinate3="../../n_tor")
	""" Absorbed wave power density on the thermal species, per toroidal mode number"""

	power_density_fast  :array_type =  sp_property(units="W.m^-3",type="dynamic",coordinate1="1...N",coordinate2="1...N",coordinate1_same_as="../../grid/r",coordinate2_same_as="../../grid/r")
	""" Absorbed wave power density on the fast species"""

	power_density_fast_n_tor  :array_type =  sp_property(units="W.m^-3",type="dynamic",coordinate1="1...N",coordinate2="1...N",coordinate1_same_as="../../grid/r",coordinate2_same_as="../../grid/r",coordinate3="../../n_tor")
	""" Absorbed wave power density on the fast species, per toroidal mode number"""

	multiple_states_flag  :int =  sp_property(type="dynamic")
	""" Multiple state calculation flag : 0-Only one state is considered; 1-Multiple
		states are considered and are described in the state structure"""

	state  :AoS[_T_waves_coherent_wave_profiles_2d_ion_state] =  sp_property(coordinate1="1...N_charge_states")
	""" Collisional exchange with the various states of the ion species (ionisation,
		energy, excitation, ...)"""


class _T_waves_profiles_2d_e_field_n_tor(SpTree):
	"""Components of the surface averaged electric field"""

	plus  :_T_waves_CPX_amp_phase_2D =  sp_property(units="V.m^-1")
	""" Left hand polarised electric field component"""

	minus  :_T_waves_CPX_amp_phase_2D =  sp_property(units="V.m^-1")
	""" Right hand polarised electric field component"""

	parallel  :_T_waves_CPX_amp_phase_2D =  sp_property(units="V.m^-1")
	""" Parallel electric field component"""


class _T_waves_coherent_wave_beam_tracing_beam(SpTree):
	"""Beam description"""

	power_initial  :float =  sp_property(units="W",type="dynamic")
	""" Initial power in the ray/beam"""

	length  :array_type =  sp_property(units="m",type="dynamic",coordinate1="1...N")
	""" Ray/beam curvilinear length"""

	position  :_T_waves_rzphipsitheta1d_dynamic_aos3 =  sp_property()
	""" Position of the ray/beam along its path"""

	wave_vector  :_T_waves_coherent_wave_beam_tracing_beam_k =  sp_property()
	""" Wave vector of the ray/beam along its path"""

	e_field  :_T_waves_coherent_wave_beam_tracing_beam_e_field =  sp_property()
	""" Electric field polarization of the ray/beam along its path"""

	power_flow_norm  :_T_waves_coherent_wave_beam_tracing_power_flow =  sp_property()
	""" Normalised power flow"""

	electrons  :_T_waves_coherent_wave_beam_tracing_electrons =  sp_property()
	""" Quantities related to the electrons"""

	ion  :AoS[_T_waves_coherent_wave_beam_tracing_ion] =  sp_property(coordinate1="1...N")
	""" Quantities related to the different ion species"""


class _T_waves_coherent_wave_global_quantities(TimeSlice):
	"""Global quantities (RF waves) for a given time slice"""

	frequency  :float =  sp_property(units="Hz",type="dynamic")
	""" Wave frequency"""

	n_tor  :List[int] =  sp_property(type="dynamic",coordinate1="1...N")
	""" Toroidal mode numbers"""

	power  :float =  sp_property(units="W",type="dynamic")
	""" Total absorbed wave power"""

	power_n_tor  :array_type =  sp_property(units="W",type="dynamic",coordinate1="../n_tor")
	""" Absorbed wave power per toroidal mode number"""

	current_tor  :float =  sp_property(units="A",type="dynamic")
	""" Wave driven toroidal current from a stand alone calculation (not consistent with
		other sources)"""

	current_tor_n_tor  :array_type =  sp_property(units="A",type="dynamic",coordinate1="../n_tor")
	""" Wave driven toroidal current from a stand alone calculation (not consistent with
		other sources) per toroidal mode number"""

	electrons  :_T_waves_coherent_wave_global_quantities_electrons =  sp_property()
	""" Quantities related to the electrons"""

	ion  :AoS[_T_waves_coherent_wave_global_quantities_ion] =  sp_property(coordinate1="1...N")
	""" Quantities related to the different ion species"""


class _T_waves_coherent_wave_profiles_1d(TimeSlice):
	"""Radial profiles (RF waves) for a given time slice"""

	grid  :_T_core_radial_grid =  sp_property()
	""" Radial grid"""

	n_tor  :List[int] =  sp_property(type="dynamic",coordinate1="1...N")
	""" Toroidal mode numbers"""

	power_density  :Expression  =  sp_property(units="W.m^-3",type="dynamic",coordinate1="../grid/rho_tor_norm")
	""" Flux surface averaged total absorbed wave power density (electrons + ion + fast
		populations)"""

	power_density_n_tor  :array_type =  sp_property(units="W.m^-3",type="dynamic",coordinate1="../grid/rho_tor_norm",coordinate2="../n_tor")
	""" Flux surface averaged absorbed wave power density per toroidal mode number"""

	power_inside  :Expression  =  sp_property(units="W",type="dynamic",coordinate1="../grid/rho_tor_norm")
	""" Total absorbed wave power (electrons + ion + fast populations) inside a flux
		surface (cumulative volume integral of the absorbed power density)"""

	power_inside_n_tor  :array_type =  sp_property(units="W",type="dynamic",coordinate1="../grid/rho_tor_norm",coordinate2="../n_tor")
	""" Total absorbed wave power (electrons + ion + fast populations) inside a flux
		surface (cumulative volume integral of the absorbed power density), per toroidal
		mode number"""

	current_tor_inside  :Expression  =  sp_property(units="A",type="dynamic",coordinate1="../grid/rho_tor_norm")
	""" Wave driven toroidal current, inside a flux surface"""

	current_tor_inside_n_tor  :array_type =  sp_property(units="A",type="dynamic",coordinate1="../grid/rho_tor_norm",coordinate2="../n_tor")
	""" Wave driven toroidal current, inside a flux surface, per toroidal mode number"""

	current_parallel_density  :Expression  =  sp_property(units="A.m^-2",type="dynamic",coordinate1="../grid/rho_tor_norm")
	""" Flux surface averaged wave driven parallel current density = average(j.B) / B0,
		where B0 = vacuum_toroidal_field/b0."""

	current_parallel_density_n_tor  :array_type =  sp_property(units="A.m^-2",type="dynamic",coordinate1="../grid/rho_tor_norm",coordinate2="../n_tor")
	""" Flux surface averaged wave driven parallel current density, per toroidal mode
		number"""

	e_field_n_tor  :AoS[_T_waves_profiles_1d_e_field_n_tor] =  sp_property(coordinate1="../n_tor")
	""" Components of the electric field per toroidal mode number, averaged over the
		flux surface, where the averaged is weighted with the power deposition density,
		such that e_field = ave(e_field.power_density) / ave(power_density)"""

	k_perpendicular  :array_type =  sp_property(units="V.m^-1",type="dynamic",coordinate1="../grid/rho_tor_norm",coordinate2="../n_tor")
	""" Perpendicular wave vector, averaged over the flux surface, where the averaged is
		weighted with the power deposition density, such that k_perpendicular =
		ave(k_perpendicular.power_density) / ave(power_density), for every flux surface
		and every toroidal number"""

	electrons  :_T_waves_coherent_wave_profiles_1d_electrons =  sp_property()
	""" Quantities related to the electrons"""

	ion  :AoS[_T_waves_coherent_wave_profiles_1d_ion] =  sp_property(coordinate1="1...N")
	""" Quantities related to the different ion species"""


class _T_waves_coherent_wave_full_wave(TimeSlice):
	"""Full wave solution for a given time slice"""

	grid  :_T_generic_grid_dynamic =  sp_property()
	""" Grid description"""

	e_field  :_T_waves_coherent_wave_full_wave_e_field =  sp_property()
	""" Components of the wave electric field"""

	b_field  :_T_waves_coherent_wave_full_wave_b_field =  sp_property()
	""" Components of the wave magnetic field"""

	k_perpendicular  :AoS[_T_generic_grid_scalar] =  sp_property(units="V.m^-1",coordinate1="1...N")
	""" Perpendicular wave vector, given on various grid subsets"""


class _T_waves_coherent_wave_profiles_2d(TimeSlice):
	"""2D profiles (RF waves) for a given time slice"""

	grid  :_T_waves_coherent_wave_profiles_2d_grid =  sp_property()
	""" 2D grid in a poloidal cross-section"""

	n_tor  :List[int] =  sp_property(type="dynamic",coordinate1="1...N")
	""" Toroidal mode numbers"""

	power_density  :array_type =  sp_property(units="W.m^-3",type="dynamic",coordinate1="1...N",coordinate2="1...N",coordinate1_same_as="../grid/r",coordinate2_same_as="../grid/r")
	""" Total absorbed wave power density (electrons + ion + fast populations)"""

	power_density_n_tor  :array_type =  sp_property(units="W.m^-3",type="dynamic",coordinate1="1...N",coordinate2="1...N",coordinate1_same_as="../grid/r",coordinate2_same_as="../grid/r",coordinate3="../n_tor")
	""" Absorbed wave power density per toroidal mode number"""

	e_field_n_tor  :AoS[_T_waves_profiles_2d_e_field_n_tor] =  sp_property(coordinate1="../n_tor")
	""" Components of the electric field per toroidal mode number"""

	electrons  :_T_waves_coherent_wave_profiles_2d_electrons =  sp_property()
	""" Quantities related to the electrons"""

	ion  :AoS[_T_waves_coherent_wave_profiles_2d_ion] =  sp_property(coordinate1="1...N")
	""" Quantities related to the different ion species"""


class _T_waves_coherent_wave_beam_tracing(TimeSlice):
	"""Beam tracing calculations for a given time slice"""

	beam  :AoS[_T_waves_coherent_wave_beam_tracing_beam] =  sp_property(coordinate1="1...N")
	""" Set of rays/beams describing the wave propagation"""


class _T_waves_coherent_wave(SpTree):
	"""Source terms for a given actuator"""

	identifier  :_T_waves_coherent_wave_identifier =  sp_property()
	""" Identifier of the coherent wave, in terms of the type and name of the antenna
		driving the wave and an index separating waves driven by the same antenna."""

	wave_solver_type  :_T_identifier =  sp_property()
	""" Type of wave deposition solver used for this wave. Index = 1 for beam/ray
		tracing; index = 2 for full wave"""

	global_quantities  :TimeSeriesAoS[_T_waves_coherent_wave_global_quantities] =  sp_property(coordinate1="time",type="dynamic")
	""" Global quantities for various time slices"""

	profiles_1d  :TimeSeriesAoS[_T_waves_coherent_wave_profiles_1d] =  sp_property(coordinate1="time",type="dynamic",cocos_alias="IDSPATH",cocos_replace="waves.coherent_wave{i}.profiles_1d{j}")
	""" Source radial profiles (flux surface averaged quantities) for various time
		slices"""

	profiles_2d  :TimeSeriesAoS[_T_waves_coherent_wave_profiles_2d] =  sp_property(coordinate1="time",type="dynamic")
	""" 2D profiles in poloidal cross-section, for various time slices"""

	beam_tracing  :TimeSeriesAoS[_T_waves_coherent_wave_beam_tracing] =  sp_property(coordinate1="time",type="dynamic")
	""" Beam tracing calculations, for various time slices"""

	full_wave  :TimeSeriesAoS[_T_waves_coherent_wave_full_wave] =  sp_property(coordinate1="time",type="dynamic")
	""" Solution by a full wave code, given on a generic grid description, for various
		time slices"""


class _T_waves(IDS):
	"""RF wave propagation and deposition. Note that current estimates in this IDS are
		a priori not taking into account synergies between multiple sources (a
		convergence loop with Fokker-Planck calculations is required to account for such
		synergies)
	lifecycle_status: alpha
	lifecycle_version: 3.5.0
	lifecycle_last_change: 3.37.2"""

	dd_version="v3_38_1_dirty"
	ids_name="waves"

	coherent_wave  :AoS[_T_waves_coherent_wave] =  sp_property(coordinate1="1...N",appendable_by_appender_actor="yes")
	""" Wave description for each frequency"""

	vacuum_toroidal_field  :_T_b_tor_vacuum_1 =  sp_property(cocos_alias="IDSPATH",cocos_replace="waves.vacuum_toroidal_field")
	""" Characteristics of the vacuum toroidal field (used in rho_tor definition)"""

	magnetic_axis  :_T_rz1d_dynamic_1 =  sp_property()
	""" Magnetic axis position (used to define a poloidal angle for the 2D profiles)"""
