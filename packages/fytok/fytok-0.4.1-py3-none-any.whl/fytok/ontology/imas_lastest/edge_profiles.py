"""
  This module containes the _FyTok_ wrapper of IMAS/dd/edge_profiles
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_identifier_dynamic_aos3,_T_plasma_composition_neutral_element,_T_generic_grid_scalar,_T_generic_grid_vector_components,_T_generic_grid_scalar_single_position,_T_b_tor_vacuum_1,_T_identifier_static,_T_generic_grid_aos3_root
from .utilities import _E_neutrals_identifier
from .utilities import _E_midplane_identifier

class _T_edge_profiles_vector_components_1(SpTree):
	"""Vector components in predefined directions for 1D profiles, assuming
		edge_radial_grid one level above
	aos3Parent: yes"""

	radial  :array_type =  sp_property(type="dynamic",coordinate1="../../grid/rho_pol_norm",units="as_parent")
	""" Radial component"""

	diamagnetic  :array_type =  sp_property(type="dynamic",coordinate1="../../grid/rho_pol_norm",units="as_parent")
	""" Diamagnetic component"""

	parallel  :array_type =  sp_property(type="dynamic",coordinate1="../../grid/rho_pol_norm",units="as_parent")
	""" Parallel component"""

	poloidal  :array_type =  sp_property(type="dynamic",coordinate1="../../grid/rho_pol_norm",units="as_parent")
	""" Poloidal component"""

	toroidal  :array_type =  sp_property(type="dynamic",coordinate1="../../grid/rho_pol_norm",units="as_parent")
	""" Toroidal component"""


class _T_edge_profiles_vector_components_2(SpTree):
	"""Vector components in predefined directions for 1D profiles, assuming
		edge_radial_grid two levels above
	aos3Parent: yes"""

	radial  :array_type =  sp_property(type="dynamic",coordinate1="../../../grid/rho_pol_norm",units="as_parent")
	""" Radial component"""

	diamagnetic  :array_type =  sp_property(type="dynamic",coordinate1="../../../grid/rho_pol_norm",units="as_parent")
	""" Diamagnetic component"""

	parallel  :array_type =  sp_property(type="dynamic",coordinate1="../../../grid/rho_pol_norm",units="as_parent")
	""" Parallel component"""

	poloidal  :array_type =  sp_property(type="dynamic",coordinate1="../../../grid/rho_pol_norm",units="as_parent")
	""" Poloidal component"""

	toroidal  :array_type =  sp_property(type="dynamic",coordinate1="../../../grid/rho_pol_norm",units="as_parent")
	""" Toroidal component"""


class _T_edge_profiles_vector_components_3(SpTree):
	"""Vector components in predefined directions for 1D profiles, assuming
		edge_radial_grid 3 levels above
	aos3Parent: yes"""

	radial  :array_type =  sp_property(type="dynamic",coordinate1="../../../../grid/rho_pol_norm",units="as_parent")
	""" Radial component"""

	diamagnetic  :array_type =  sp_property(type="dynamic",coordinate1="../../../../grid/rho_pol_norm",units="as_parent")
	""" Diamagnetic component"""

	parallel  :array_type =  sp_property(type="dynamic",coordinate1="../../../../grid/rho_pol_norm",units="as_parent")
	""" Parallel component"""

	poloidal  :array_type =  sp_property(type="dynamic",coordinate1="../../../../grid/rho_pol_norm",units="as_parent")
	""" Poloidal component"""

	toroidal  :array_type =  sp_property(type="dynamic",coordinate1="../../../../grid/rho_pol_norm",units="as_parent")
	""" Toroidal component"""


class _T_edge_radial_grid(SpTree):
	"""1D radial grid for edge_profiles IDSs
	aos3Parent: yes"""

	rho_pol_norm  :array_type =  sp_property(type="dynamic",coordinate1="1...N",units="-")
	""" Normalised poloidal flux coordinate = sqrt((psi(rho)-psi(magnetic_axis) /
		(psi(LCFS)-psi(magnetic_axis)))"""

	psi  :array_type =  sp_property(coordinate1="../rho_pol_norm",units="Wb",type="dynamic")
	""" Poloidal magnetic flux"""

	rho_tor_norm  :array_type =  sp_property(type="dynamic",coordinate1="../rho_pol_norm",units="-")
	""" Normalised toroidal flux coordinate. The normalizing value for rho_tor_norm, is
		the toroidal flux coordinate at the equilibrium boundary (LCFS or 99.x % of the
		LCFS in case of a fixed boundary equilibium calculation, see
		time_slice/boundary/b_flux_pol_norm in the equilibrium IDS)"""

	rho_tor  :array_type =  sp_property(type="dynamic",coordinate1="../rho_pol_norm",units="m")
	""" Toroidal flux coordinate. rho_tor = sqrt(b_flux_tor/(pi*b0)) ~
		sqrt(pi*r^2*b0/(pi*b0)) ~ r [m]. The toroidal field used in its definition is
		indicated under vacuum_toroidal_field/b0"""

	volume  :array_type =  sp_property(type="dynamic",coordinate1="../rho_pol_norm",units="m^3")
	""" Volume enclosed inside the magnetic surface"""

	area  :array_type =  sp_property(type="dynamic",coordinate1="../rho_pol_norm",units="m^2")
	""" Cross-sectional area of the flux surface"""

	psi_magnetic_axis  :float =  sp_property(type="dynamic",units="Wb")
	""" Value of the poloidal magnetic flux at the magnetic axis (useful to normalize
		the psi array values when the radial grid doesn't go from the magnetic axis to
		the plasma boundary)"""

	psi_boundary  :float =  sp_property(type="dynamic",units="Wb")
	""" Value of the poloidal magnetic flux at the plasma boundary (useful to normalize
		the psi array values when the radial grid doesn't go from the magnetic axis to
		the plasma boundary)"""


class _T_edge_profiles_1d_fit(SpTree):
	"""Edge profile fit information"""

	measured  :array_type =  sp_property(type="dynamic",units="as_parent for a local measurement, as_parent.m for a line integrated measurement",coordinate1="1...N")
	""" Measured values"""

	source  :List[str] =  sp_property(type="dynamic",coordinate1="../measured")
	""" Path to the source data for each measurement in the IMAS data dictionary, e.g.
		ece/channel(i)/t_e for the electron temperature on the i-th channel in the ECE
		IDS"""

	time_measurement  :array_type =  sp_property(type="dynamic",units="s",coordinate1="../measured")
	""" Exact time slices used from the time array of the measurement source data. If
		the time slice does not exist in the time array of the source data, it means
		linear interpolation has been used"""

	time_measurement_slice_method  :_T_identifier_dynamic_aos3 =  sp_property()
	""" Method used to slice the data : index = 0 means using exact time slice of the
		measurement, 1 means linear interpolation, ..."""

	time_measurement_width  :array_type =  sp_property(type="dynamic",units="s",coordinate1="../measured")
	""" In case the measurements are averaged over a time interval, this node is the
		full width of this time interval (empty otherwise). In case the
		slicing/averaging method doesn't use a hard time interval cutoff, this width is
		the characteristic time span of the slicing/averaging method. By convention, the
		time interval starts at time_measurement-time_width and ends at
		time_measurement."""

	local  :array_type =  sp_property(type="dynamic",coordinate1="../measured")
	""" Integer flag : 1 means local measurement, 0 means line-integrated measurement"""

	rho_tor_norm  :array_type =  sp_property(type="dynamic",units="-",coordinate1="../measured")
	""" Normalised toroidal flux coordinate of each measurement (local value for a local
		measurement, minimum value reached by the line of sight for a line measurement)"""

	rho_pol_norm  :array_type =  sp_property(type="dynamic",units="-",coordinate1="../measured")
	""" Normalised poloidal flux coordinate of each measurement (local value for a local
		measurement, minimum value reached by the line of sight for a line measurement)"""

	weight  :array_type =  sp_property(type="dynamic",units="-",coordinate1="../measured")
	""" Weight given to each measured value"""

	reconstructed  :array_type =  sp_property(type="dynamic",units="as_parent for a local measurement, as_parent.m for a line integrated measurement",coordinate1="../measured")
	""" Value reconstructed from the fit"""

	chi_squared  :array_type =  sp_property(type="dynamic",units="-",coordinate1="../measured")
	""" Squared error normalized by the weighted standard deviation considered in the
		minimization process : chi_squared = weight^2 *(reconstructed - measured)^2 /
		sigma^2, where sigma is the standard deviation of the measurement error"""

	parameters  :str =  sp_property(type="dynamic")
	""" List of the fit specific parameters in XML format"""


class _T_edge_profiles_neutral_state(SpTree):
	"""Quantities related to the a given state of the neutral species
	aos3Parent: yes"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying state"""

	electron_configuration  :str =  sp_property(type="dynamic")
	""" Configuration of atomic orbitals of this state, e.g. 1s2-2s1"""

	vibrational_level  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Vibrational level (can be bundled)"""

	vibrational_mode  :str =  sp_property(type="dynamic")
	""" Vibrational mode of this state, e.g. _A_g_. Need to define, or adopt a standard
		nomenclature."""

	neutral_type  :_E_neutrals_identifier =  sp_property(doc_identifier="utilities/neutrals_identifier.xml")
	""" Neutral type (if the considered state is a neutral), in terms of energy. ID =1:
		cold; 2: thermal; 3: fast; 4: NBI"""

	temperature  :array_type =  sp_property(coordinate1="../../../grid/rho_pol_norm",units="eV",type="dynamic")
	""" Temperature"""

	density  :array_type =  sp_property(coordinate1="../../../grid/rho_pol_norm",units="m^-3",type="dynamic")
	""" Density (thermal+non-thermal)"""

	density_thermal  :array_type =  sp_property(coordinate1="../../../grid/rho_pol_norm",units="m^-3",type="dynamic")
	""" Density of thermal particles"""

	density_fast  :array_type =  sp_property(coordinate1="../../../grid/rho_pol_norm",units="m^-3",type="dynamic")
	""" Density of fast (non-thermal) particles"""

	pressure  :array_type =  sp_property(coordinate1="../../../grid/rho_pol_norm",units="Pa",type="dynamic")
	""" Pressure (thermal+non-thermal)"""

	pressure_thermal  :array_type =  sp_property(coordinate1="../../../grid/rho_pol_norm",units="Pa",type="dynamic")
	""" Pressure (thermal) associated with random motion ~average((v-average(v))^2)"""

	pressure_fast_perpendicular  :array_type =  sp_property(coordinate1="../../../grid/rho_pol_norm",units="Pa",type="dynamic")
	""" Fast (non-thermal) perpendicular pressure"""

	pressure_fast_parallel  :array_type =  sp_property(coordinate1="../../../grid/rho_pol_norm",units="Pa",type="dynamic")
	""" Fast (non-thermal) parallel pressure"""


class _T_edge_profiles_time_slice_neutral_state(SpTree):
	"""Quantities related to a given state of the neutral species"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying state"""

	electron_configuration  :str =  sp_property(type="dynamic")
	""" Configuration of atomic orbitals of this state, e.g. 1s2-2s1"""

	vibrational_level  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Vibrational level (can be bundled)"""

	vibrational_mode  :str =  sp_property(type="dynamic")
	""" Vibrational mode of this state, e.g. _A_g_. Need to define, or adopt a standard
		nomenclature."""

	neutral_type  :_T_identifier_dynamic_aos3 =  sp_property()
	""" Neutral type, in terms of energy. ID =1: cold; 2: thermal; 3: fast; 4: NBI"""

	temperature  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="eV")
	""" Temperature, given on various grid subsets"""

	density  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="m^-3")
	""" Density (thermal+non-thermal), given on various grid subsets"""

	density_fast  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="m^-3")
	""" Density of fast (non-thermal) particles, given on various grid subsets"""

	pressure  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="Pa")
	""" Pressure, given on various grid subsets"""

	pressure_fast_perpendicular  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="Pa")
	""" Fast (non-thermal) perpendicular pressure, given on various grid subsets"""

	pressure_fast_parallel  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="Pa")
	""" Fast (non-thermal) parallel pressure, given on various grid subsets"""

	velocity  :AoS[_T_generic_grid_vector_components] =  sp_property(units="m.s^-1",coordinate1="1...N")
	""" Velocity, given on various grid subsets"""

	velocity_diamagnetic  :AoS[_T_generic_grid_vector_components] =  sp_property(coordinate1="1...N",units="m.s^-1")
	""" Velocity due to the diamagnetic drift, given on various grid subsets"""

	velocity_exb  :AoS[_T_generic_grid_vector_components] =  sp_property(coordinate1="1...N",units="m.s^-1")
	""" Velocity due to the ExB drift, given on various grid subsets"""

	energy_density_kinetic  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="J.m^-3")
	""" Kinetic energy density, given on various grid subsets"""

	distribution_function  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="mixed")
	""" Distribution function, given on various grid subsets"""


class _T_edge_profiles_time_slice_ion_charge_state(SpTree):
	"""Quantities related to a given charge state of the ion species"""

	z_min  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Minimum Z of the state bundle (z_min = z_max = 0 for a neutral)"""

	z_max  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Maximum Z of the state bundle (equal to z_min if no bundle)"""

	z_average  :AoS[_T_generic_grid_scalar] =  sp_property(units="Elementary Charge Unit",coordinate1="1...N")
	""" Average Z of the state bundle (equal to z_min if no bundle), = sum (Z*x_z) where
		x_z is the relative concentration of a given charge state in the bundle, i.e.
		sum(x_z) = 1 over the bundle, given on various grid subsets"""

	z_square_average  :AoS[_T_generic_grid_scalar] =  sp_property(units="Elementary Charge Unit",coordinate1="1...N")
	""" Average Z square of the state bundle (equal to z_min if no bundle), = sum
		(Z^2*x_z) where x_z is the relative concentration of a given charge state in the
		bundle, i.e. sum(x_z) = 1 over the bundle, given on various grid subsets"""

	ionisation_potential  :AoS[_T_generic_grid_scalar] =  sp_property(units="Elementary Charge Unit",coordinate1="1...N")
	""" Cumulative and average ionisation potential to reach a given bundle. Defined as
		sum (x_z* (sum of Epot from z'=0 to z-1)), where Epot is the ionisation
		potential of ion Xz_+, and x_z is the relative concentration of a given charge
		state in the bundle, i.e. sum(x_z) = 1 over the bundle, given on various grid
		subsets"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying state (e.g. C+, C+2 , C+3, C+4, C+5, C+6, ...)"""

	electron_configuration  :str =  sp_property(type="dynamic")
	""" Configuration of atomic orbitals of this state, e.g. 1s2-2s1"""

	vibrational_level  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Vibrational level (can be bundled)"""

	vibrational_mode  :str =  sp_property(type="dynamic")
	""" Vibrational mode of this state, e.g. _A_g_. Need to define, or adopt a standard
		nomenclature."""

	temperature  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="eV")
	""" Temperature, given on various grid subsets"""

	density  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="m^-3")
	""" Density (thermal+non-thermal), given on various grid subsets"""

	density_fast  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="m^-3")
	""" Density of fast (non-thermal) particles, given on various grid subsets"""

	pressure  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="Pa")
	""" Pressure, given on various grid subsets"""

	pressure_fast_perpendicular  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="Pa")
	""" Fast (non-thermal) perpendicular pressure, given on various grid subsets"""

	pressure_fast_parallel  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="Pa")
	""" Fast (non-thermal) parallel pressure, given on various grid subsets"""

	velocity  :AoS[_T_generic_grid_vector_components] =  sp_property(units="m.s^-1",coordinate1="1...N")
	""" Velocity, given on various grid subsets"""

	velocity_diamagnetic  :AoS[_T_generic_grid_vector_components] =  sp_property(coordinate1="1...N",units="m.s^-1")
	""" Velocity due to the diamagnetic drift, given on various grid subsets"""

	velocity_exb  :AoS[_T_generic_grid_vector_components] =  sp_property(coordinate1="1...N",units="m.s^-1")
	""" Velocity due to the ExB drift, given on various grid subsets"""

	energy_density_kinetic  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="J.m^-3")
	""" Kinetic energy density, given on various grid subsets"""

	distribution_function  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="mixed")
	""" Distribution function, given on various grid subsets"""


class _T_edge_profiles_ggd_fast_ion(SpTree):
	"""Fast sampled quantities related to a given ion species"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	z_ion  :float =  sp_property(type="dynamic",units="Elementary Charge Unit")
	""" Ion charge (of the dominant ionisation state; lumped ions are allowed)."""

	label  :str =  sp_property(type="dynamic")
	""" String identifying the species (e.g. H+, D+, T+, He+2, C+, D2, DT, CD4, ...)"""

	neutral_index  :int =  sp_property(type="dynamic")
	""" Index of the corresponding neutral species in the ../../neutral array"""

	content  :AoS[_T_generic_grid_scalar_single_position] =  sp_property(units="-",coordinate1="1...N")
	""" Particle content = total number of particles for this ion species in the volume
		of the grid subset, for various grid subsets"""

	temperature  :AoS[_T_generic_grid_scalar_single_position] =  sp_property(coordinate1="1...N",units="eV")
	""" Temperature (average over states when multiple states are considered), given at
		various positions (grid subset of size 1)"""

	density  :AoS[_T_generic_grid_scalar_single_position] =  sp_property(coordinate1="1...N",units="m^-3")
	""" Density (thermal+non-thermal) (sum over states when multiple states are
		considered), given at various positions (grid subset of size 1)"""


class _T_edge_profiles_time_slice_electrons(SpTree):
	"""Quantities related to electrons"""

	temperature  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="eV")
	""" Temperature, given on various grid subsets"""

	density  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="m^-3")
	""" Density (thermal+non-thermal), given on various grid subsets"""

	density_fast  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="m^-3")
	""" Density of fast (non-thermal) particles, given on various grid subsets"""

	pressure  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="Pa")
	""" Pressure, given on various grid subsets"""

	pressure_fast_perpendicular  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="Pa")
	""" Fast (non-thermal) perpendicular pressure, given on various grid subsets"""

	pressure_fast_parallel  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="Pa")
	""" Fast (non-thermal) parallel pressure, given on various grid subsets"""

	velocity  :AoS[_T_generic_grid_vector_components] =  sp_property(units="m.s^-1",coordinate1="1...N")
	""" Velocity, given on various grid subsets"""

	distribution_function  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="mixed")
	""" Distribution function, given on various grid subsets"""


class _T_edge_profiles_ggd_fast_electrons(SpTree):
	"""Fast sampled quantities related to electrons"""

	temperature  :AoS[_T_generic_grid_scalar_single_position] =  sp_property(coordinate1="1...N",units="eV")
	""" Temperature, given at various positions (grid subset of size 1)"""

	density  :AoS[_T_generic_grid_scalar_single_position] =  sp_property(coordinate1="1...N",units="m^-3")
	""" Density (thermal+non-thermal), given at various positions (grid subset of size
		1)"""


class _T_edge_profiles_ions_charge_states2(SpTree):
	"""Quantities related to the a given state of the ion species
	aos3Parent: yes"""

	z_min  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Minimum Z of the charge state bundle"""

	z_max  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Maximum Z of the charge state bundle (equal to z_min if no bundle)"""

	z_average  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Average Z of the charge state bundle, volume averaged over the plasma radius
		(equal to z_min if no bundle), = sum (Z*x_z) where x_z is the relative
		concentration of a given charge state in the bundle, i.e. sum(x_z) = 1 over the
		bundle."""

	z_square_average  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Average Z square of the charge state bundle, volume averaged over the plasma
		radius (equal to z_min squared if no bundle), = sum (Z^2*x_z) where x_z is the
		relative concentration of a given charge state in the bundle, i.e. sum(x_z) = 1
		over the bundle."""

	z_average_1d  :array_type =  sp_property(coordinate1="../../../grid/rho_pol_norm",units="-",type="dynamic")
	""" Average charge profile of the charge state bundle (equal to z_min if no bundle),
		= sum (Z*x_z) where x_z is the relative concentration of a given charge state in
		the bundle, i.e. sum(x_z) = 1 over the bundle."""

	z_average_square_1d  :array_type =  sp_property(coordinate1="../../../grid/rho_pol_norm",units="-",type="dynamic")
	""" Average square charge profile of the charge state bundle (equal to z_min squared
		if no bundle), = sum (Z^2*x_z) where x_z is the relative concentration of a
		given charge state in the bundle, i.e. sum(x_z) = 1 over the bundle."""

	ionisation_potential  :float =  sp_property(units="eV",type="dynamic")
	""" Cumulative and average ionisation potential to reach a given bundle. Defined as
		sum (x_z* (sum of Epot from z'=0 to z-1)), where Epot is the ionisation
		potential of ion Xz_+, and x_z is the relative concentration of a given charge
		state in the bundle, i.e. sum(x_z) = 1 over the bundle."""

	label  :str =  sp_property(type="dynamic")
	""" String identifying state (e.g. C+, C+2 , C+3, C+4, C+5, C+6, ...)"""

	electron_configuration  :str =  sp_property(type="dynamic")
	""" Configuration of atomic orbitals of this state, e.g. 1s2-2s1"""

	vibrational_level  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Vibrational level (can be bundled)"""

	vibrational_mode  :str =  sp_property(type="dynamic")
	""" Vibrational mode of this state, e.g. _A_g_. Need to define, or adopt a standard
		nomenclature."""

	rotation_frequency_tor  :array_type =  sp_property(coordinate1="../../../grid/rho_pol_norm",units="rad.s^-1",type="dynamic")
	""" Toroidal rotation frequency (i.e. toroidal velocity divided by the major radius
		at which the toroidal velocity is taken)"""

	temperature  :array_type =  sp_property(coordinate1="../../../grid/rho_pol_norm",units="eV",type="dynamic")
	""" Temperature"""

	density  :array_type =  sp_property(coordinate1="../../../grid/rho_pol_norm",units="m^-3",type="dynamic")
	""" Density (thermal+non-thermal)"""

	density_fit  :_T_edge_profiles_1d_fit =  sp_property(units="m^-3")
	""" Information on the fit used to obtain the density profile"""

	density_thermal  :array_type =  sp_property(coordinate1="../../../grid/rho_pol_norm",units="m^-3",type="dynamic")
	""" Density of thermal particles"""

	density_fast  :array_type =  sp_property(coordinate1="../../../grid/rho_pol_norm",units="m^-3",type="dynamic")
	""" Density of fast (non-thermal) particles"""

	pressure  :array_type =  sp_property(coordinate1="../../../grid/rho_pol_norm",units="Pa",type="dynamic")
	""" Pressure (thermal+non-thermal)"""

	pressure_thermal  :array_type =  sp_property(coordinate1="../../../grid/rho_pol_norm",units="Pa",type="dynamic")
	""" Pressure (thermal) associated with random motion ~average((v-average(v))^2)"""

	pressure_fast_perpendicular  :array_type =  sp_property(coordinate1="../../../grid/rho_pol_norm",units="Pa",type="dynamic")
	""" Fast (non-thermal) perpendicular pressure"""

	pressure_fast_parallel  :array_type =  sp_property(coordinate1="../../../grid/rho_pol_norm",units="Pa",type="dynamic")
	""" Fast (non-thermal) parallel pressure"""


class _T_edge_profile_neutral(SpTree):
	"""Quantities related to a given neutral species
	aos3Parent: yes"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying the species (e.g. H, D, T, He, C, D2, DT, CD4, ...)"""

	ion_index  :int =  sp_property(type="dynamic")
	""" Index of the corresponding ion species in the ../../ion array"""

	temperature  :array_type =  sp_property(coordinate1="../../grid/rho_pol_norm",units="eV",type="dynamic")
	""" Temperature (average over charge states when multiple charge states are
		considered)"""

	density  :array_type =  sp_property(coordinate1="../../grid/rho_pol_norm",units="m^-3",type="dynamic")
	""" Density (thermal+non-thermal) (sum over charge states when multiple charge
		states are considered)"""

	density_thermal  :array_type =  sp_property(coordinate1="../../grid/rho_pol_norm",units="m^-3",type="dynamic")
	""" Density (thermal) (sum over charge states when multiple charge states are
		considered)"""

	density_fast  :array_type =  sp_property(coordinate1="../../grid/rho_pol_norm",units="m^-3",type="dynamic")
	""" Density of fast (non-thermal) particles (sum over charge states when multiple
		charge states are considered)"""

	pressure  :array_type =  sp_property(coordinate1="../../grid/rho_pol_norm",units="Pa",type="dynamic")
	""" Pressure (thermal+non-thermal) (sum over charge states when multiple charge
		states are considered)"""

	pressure_thermal  :array_type =  sp_property(coordinate1="../../grid/rho_pol_norm",units="Pa",type="dynamic")
	""" Pressure (thermal) associated with random motion ~average((v-average(v))^2) (sum
		over charge states when multiple charge states are considered)"""

	pressure_fast_perpendicular  :array_type =  sp_property(coordinate1="../../grid/rho_pol_norm",units="Pa",type="dynamic")
	""" Fast (non-thermal) perpendicular pressure (sum over charge states when multiple
		charge states are considered)"""

	pressure_fast_parallel  :array_type =  sp_property(coordinate1="../../grid/rho_pol_norm",units="Pa",type="dynamic")
	""" Fast (non-thermal) parallel pressure (sum over charge states when multiple
		charge states are considered)"""

	multiple_states_flag  :int =  sp_property(type="dynamic")
	""" Multiple states calculation flag : 0-Only one state is considered; 1-Multiple
		states are considered and are described in the state structure"""

	state  :AoS[_T_edge_profiles_neutral_state] =  sp_property(coordinate1="1...N")
	""" Quantities related to the different states of the species (energy, excitation,
		...)"""


class _T_edge_profiles_profiles_1d_electrons(SpTree):
	"""Quantities related to electrons
	aos3Parent: yes"""

	temperature  :array_type =  sp_property(coordinate1="../../grid/rho_pol_norm",units="eV",type="dynamic")
	""" Temperature"""

	temperature_validity  :int =  sp_property(type="dynamic")
	""" Indicator of the validity of the temperature profile. 0: valid from automated
		processing, 1: valid and certified by the RO; - 1 means problem identified in
		the data processing (request verification by the RO), -2: invalid data, should
		not be used"""

	temperature_fit  :_T_edge_profiles_1d_fit =  sp_property(units="eV")
	""" Information on the fit used to obtain the temperature profile"""

	density  :array_type =  sp_property(coordinate1="../../grid/rho_pol_norm",units="m^-3",type="dynamic")
	""" Density (thermal+non-thermal)"""

	density_validity  :int =  sp_property(type="dynamic")
	""" Indicator of the validity of the density profile. 0: valid from automated
		processing, 1: valid and certified by the RO; - 1 means problem identified in
		the data processing (request verification by the RO), -2: invalid data, should
		not be used"""

	density_fit  :_T_edge_profiles_1d_fit =  sp_property(units="m^-3")
	""" Information on the fit used to obtain the density profile"""

	density_thermal  :array_type =  sp_property(coordinate1="../../grid/rho_pol_norm",units="m^-3",type="dynamic")
	""" Density of thermal particles"""

	density_fast  :array_type =  sp_property(coordinate1="../../grid/rho_pol_norm",units="m^-3",type="dynamic")
	""" Density of fast (non-thermal) particles"""

	pressure  :array_type =  sp_property(coordinate1="../../grid/rho_pol_norm",units="Pa",type="dynamic")
	""" Pressure (thermal+non-thermal)"""

	pressure_thermal  :array_type =  sp_property(coordinate1="../../grid/rho_pol_norm",units="Pa",type="dynamic")
	""" Pressure (thermal) associated with random motion ~average((v-average(v))^2)"""

	pressure_fast_perpendicular  :array_type =  sp_property(coordinate1="../../grid/rho_pol_norm",units="Pa",type="dynamic")
	""" Fast (non-thermal) perpendicular pressure"""

	pressure_fast_parallel  :array_type =  sp_property(coordinate1="../../grid/rho_pol_norm",units="Pa",type="dynamic")
	""" Fast (non-thermal) parallel pressure"""

	collisionality_norm  :array_type =  sp_property(coordinate1="../../grid/rho_pol_norm",units="-",type="dynamic")
	""" Collisionality normalised to the bounce frequency"""


class _T_edge_profiles_time_slice_neutral(SpTree):
	"""Quantities related to a given neutral species"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying the species (e.g. H, D, T, He, C, D2, DT, CD4, ...)"""

	ion_index  :int =  sp_property(type="dynamic")
	""" Index of the corresponding ion species in the ../../ion array"""

	temperature  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="eV")
	""" Temperature (average over states when multiple states are considered), given on
		various grid subsets"""

	density  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="m^-3")
	""" Density (thermal+non-thermal) (sum over states when multiple states are
		considered), given on various grid subsets"""

	density_fast  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="m^-3")
	""" Density of fast (non-thermal) particles (sum over states when multiple states
		are considered), given on various grid subsets"""

	pressure  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="Pa")
	""" Pressure (average over states when multiple states are considered), given on
		various grid subsets"""

	pressure_fast_perpendicular  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="Pa")
	""" Fast (non-thermal) perpendicular pressure (average over states when multiple
		states are considered), given on various grid subsets"""

	pressure_fast_parallel  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="Pa")
	""" Fast (non-thermal) parallel pressure (average over states when multiple states
		are considered), given on various grid subsets"""

	velocity  :AoS[_T_generic_grid_vector_components] =  sp_property(units="m.s^-1",coordinate1="1...N")
	""" Velocity (average over states when multiple states are considered), given on
		various grid subsets"""

	energy_density_kinetic  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="J.m^-3")
	""" Kinetic energy density (sum over states when multiple states are considered),
		given on various grid subsets"""

	multiple_states_flag  :int =  sp_property(type="dynamic")
	""" Multiple state calculation flag : 0-Only one state is considered; 1-Multiple
		states are considered and are described in the state structure"""

	state  :AoS[_T_edge_profiles_time_slice_neutral_state] =  sp_property(coordinate1="1...N_charge_states")
	""" Quantities related to the different states of the species (energy, excitation,
		...)"""


class _T_edge_profiles_time_slice_ion(SpTree):
	"""Quantities related to a given ion species"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	z_ion  :float =  sp_property(type="dynamic",units="Elementary Charge Unit")
	""" Ion charge (of the dominant ionisation state; lumped ions are allowed)."""

	label  :str =  sp_property(type="dynamic")
	""" String identifying the species (e.g. H+, D+, T+, He+2, C+, D2, DT, CD4, ...)"""

	neutral_index  :int =  sp_property(type="dynamic")
	""" Index of the corresponding neutral species in the ../../neutral array"""

	temperature  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="eV")
	""" Temperature (average over states when multiple states are considered), given on
		various grid subsets"""

	density  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="m^-3")
	""" Density (thermal+non-thermal) (sum over states when multiple states are
		considered), given on various grid subsets"""

	density_fast  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="m^-3")
	""" Density of fast (non-thermal) particles (sum over states when multiple states
		are considered), given on various grid subsets"""

	pressure  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="Pa")
	""" Pressure (average over states when multiple states are considered), given on
		various grid subsets"""

	pressure_fast_perpendicular  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="Pa")
	""" Fast (non-thermal) perpendicular pressure (average over states when multiple
		states are considered), given on various grid subsets"""

	pressure_fast_parallel  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="Pa")
	""" Fast (non-thermal) parallel pressure (average over states when multiple states
		are considered), given on various grid subsets"""

	velocity  :AoS[_T_generic_grid_vector_components] =  sp_property(units="m.s^-1",coordinate1="1...N")
	""" Velocity (average over states when multiple states are considered), given on
		various grid subsets"""

	energy_density_kinetic  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="J.m^-3")
	""" Kinetic energy density (sum over states when multiple states are considered),
		given on various grid subsets"""

	multiple_states_flag  :int =  sp_property(type="dynamic")
	""" Multiple state calculation flag : 0-Only one state is considered; 1-Multiple
		states are considered and are described in the state structure"""

	state  :AoS[_T_edge_profiles_time_slice_ion_charge_state] =  sp_property(coordinate1="1...N_charge_states")
	""" Quantities related to the different states of the species (ionisation, energy,
		excitation, ...)"""


class _T_edge_profiles_ggd_fast(TimeSlice):
	"""Quantities provided at a faster sampling rate than the full ggd quantities, on a
		reduced set of positions. Positions are described by a set of grid_subsets of
		size 1"""

	electrons  :_T_edge_profiles_ggd_fast_electrons =  sp_property()
	""" Quantities related to the electrons"""

	ion  :AoS[_T_edge_profiles_ggd_fast_ion] =  sp_property(coordinate1="1...N")
	""" Quantities related to the different ion species"""

	energy_thermal  :AoS[_T_generic_grid_scalar_single_position] =  sp_property(units="J",coordinate1="1...N")
	""" Plasma energy content = 3/2 * integral over the volume of the grid subset of the
		thermal pressure (summed over all species), for various grid subsets"""


class _T_edge_profile_ions(SpTree):
	"""Quantities related to a given ion species
	aos3Parent: yes"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	z_ion  :float =  sp_property(type="dynamic",units="Elementary Charge Unit")
	""" Ion charge (of the dominant ionisation state; lumped ions are allowed), volume
		averaged over plasma radius"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying ion (e.g. H, D, T, He, C, D2, ...)"""

	neutral_index  :int =  sp_property(type="dynamic")
	""" Index of the corresponding neutral species in the ../../neutral array"""

	z_ion_1d  :array_type =  sp_property(coordinate1="../../grid/rho_pol_norm",units="-",type="dynamic")
	""" Average charge of the ion species (sum of states charge weighted by state
		density and divided by ion density)"""

	z_ion_square_1d  :array_type =  sp_property(coordinate1="../../grid/rho_pol_norm",units="-",type="dynamic")
	""" Average square charge of the ion species (sum of states square charge weighted
		by state density and divided by ion density)"""

	temperature  :array_type =  sp_property(coordinate1="../../grid/rho_pol_norm",units="eV",type="dynamic")
	""" Temperature (average over charge states when multiple charge states are
		considered)"""

	temperature_validity  :int =  sp_property(type="dynamic")
	""" Indicator of the validity of the temperature profile. 0: valid from automated
		processing, 1: valid and certified by the RO; - 1 means problem identified in
		the data processing (request verification by the RO), -2: invalid data, should
		not be used"""

	temperature_fit  :_T_edge_profiles_1d_fit =  sp_property(units="eV")
	""" Information on the fit used to obtain the temperature profile"""

	density  :array_type =  sp_property(coordinate1="../../grid/rho_pol_norm",units="m^-3",type="dynamic")
	""" Density (thermal+non-thermal) (sum over charge states when multiple charge
		states are considered)"""

	density_validity  :int =  sp_property(type="dynamic")
	""" Indicator of the validity of the density profile. 0: valid from automated
		processing, 1: valid and certified by the RO; - 1 means problem identified in
		the data processing (request verification by the RO), -2: invalid data, should
		not be used"""

	density_fit  :_T_edge_profiles_1d_fit =  sp_property(units="m^-3")
	""" Information on the fit used to obtain the density profile"""

	density_thermal  :array_type =  sp_property(coordinate1="../../grid/rho_pol_norm",units="m^-3",type="dynamic")
	""" Density (thermal) (sum over charge states when multiple charge states are
		considered)"""

	density_fast  :array_type =  sp_property(coordinate1="../../grid/rho_pol_norm",units="m^-3",type="dynamic")
	""" Density of fast (non-thermal) particles (sum over charge states when multiple
		charge states are considered)"""

	pressure  :array_type =  sp_property(coordinate1="../../grid/rho_pol_norm",units="Pa",type="dynamic")
	""" Pressure (thermal+non-thermal) (sum over charge states when multiple charge
		states are considered)"""

	pressure_thermal  :array_type =  sp_property(coordinate1="../../grid/rho_pol_norm",units="Pa",type="dynamic")
	""" Pressure (thermal) associated with random motion ~average((v-average(v))^2) (sum
		over charge states when multiple charge states are considered)"""

	pressure_fast_perpendicular  :array_type =  sp_property(coordinate1="../../grid/rho_pol_norm",units="Pa",type="dynamic")
	""" Fast (non-thermal) perpendicular pressure (sum over charge states when multiple
		charge states are considered)"""

	pressure_fast_parallel  :array_type =  sp_property(coordinate1="../../grid/rho_pol_norm",units="Pa",type="dynamic")
	""" Fast (non-thermal) parallel pressure (sum over charge states when multiple
		charge states are considered)"""

	rotation_frequency_tor  :array_type =  sp_property(coordinate1="../../grid/rho_pol_norm",units="rad.s^-1",type="dynamic")
	""" Toroidal rotation frequency (i.e. toroidal velocity divided by the major radius
		at which the toroidal velocity is taken) (average over charge states when
		multiple charge states are considered)"""

	velocity  :_T_edge_profiles_vector_components_2 =  sp_property(units="m.s^-1")
	""" Velocity (average over charge states when multiple charge states are considered)
		at the position of maximum major radius on every flux surface"""

	multiple_states_flag  :int =  sp_property(type="dynamic")
	""" Multiple states calculation flag : 0-Only the 'ion' level is considered and the
		'state' array of structure is empty; 1-Ion states are considered and are
		described in the 'state' array of structure"""

	state  :AoS[_T_edge_profiles_ions_charge_states2] =  sp_property(coordinate1="1...N")
	""" Quantities related to the different states of the species (ionisation, energy,
		excitation, ...)"""


class _T_edge_profiles_time_slice(TimeSlice):
	"""edge plasma description for a given time slice"""

	electrons  :_T_edge_profiles_time_slice_electrons =  sp_property()
	""" Quantities related to the electrons"""

	ion  :AoS[_T_edge_profiles_time_slice_ion] =  sp_property(coordinate1="1...N")
	""" Quantities related to the different ion species"""

	neutral  :AoS[_T_edge_profiles_time_slice_neutral] =  sp_property(coordinate1="1...N")
	""" Quantities related to the different neutral species"""

	t_i_average  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="eV")
	""" Ion temperature (averaged on ion species), given on various grid subsets"""

	n_i_total_over_n_e  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="-")
	""" Ratio of total ion density (sum over ion species) over electron density.
		(thermal+non-thermal), given on various grid subsets"""

	zeff  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="-")
	""" Effective charge, given on various grid subsets"""

	pressure_thermal  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="Pa")
	""" Thermal pressure (electrons+ions), given on various grid subsets"""

	pressure_perpendicular  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="Pa")
	""" Total perpendicular pressure (electrons+ions, thermal+non-thermal), given on
		various grid subsets"""

	pressure_parallel  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="Pa")
	""" Total parallel pressure (electrons+ions, thermal+non-thermal), given on various
		grid subsets"""

	j_total  :AoS[_T_generic_grid_vector_components] =  sp_property(units="A.m^-2",coordinate1="1...N",introduced_after_version="3.32.1")
	""" Total current density, given on various grid subsets"""

	j_parallel  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="A.m^-2",introduced_after_version="3.32.1")
	""" Current due to parallel electric and thermo-electric conductivity and potential
		and electron temperature gradients along the field line, differences away from
		ambipolar flow in the parallel direction between ions and electrons (this is not
		the parallel component of j_total)"""

	j_anomalous  :AoS[_T_generic_grid_vector_components] =  sp_property(units="A.m^-2",coordinate1="1...N")
	""" Anomalous current density, given on various grid subsets"""

	j_inertial  :AoS[_T_generic_grid_vector_components] =  sp_property(units="A.m^-2",coordinate1="1...N")
	""" Inertial current density, given on various grid subsets"""

	j_ion_neutral_friction  :AoS[_T_generic_grid_vector_components] =  sp_property(units="A.m^-2",coordinate1="1...N")
	""" Current density due to ion neutral friction, given on various grid subsets"""

	j_parallel_viscosity  :AoS[_T_generic_grid_vector_components] =  sp_property(units="A.m^-2",coordinate1="1...N")
	""" Current density due to the parallel viscosity, given on various grid subsets"""

	j_perpendicular_viscosity  :AoS[_T_generic_grid_vector_components] =  sp_property(units="A.m^-2",coordinate1="1...N")
	""" Current density due to the perpendicular viscosity, given on various grid
		subsets"""

	j_heat_viscosity  :AoS[_T_generic_grid_vector_components] =  sp_property(units="A.m^-2",coordinate1="1...N")
	""" Current density due to the heat viscosity, given on various grid subsets"""

	j_pfirsch_schlueter  :AoS[_T_generic_grid_vector_components] =  sp_property(units="A.m^-2",coordinate1="1...N")
	""" Current density due to Pfirsch-Schlüter effects, given on various grid subsets"""

	j_diamagnetic  :AoS[_T_generic_grid_vector_components] =  sp_property(units="A.m^-2",coordinate1="1...N")
	""" Current density due to the diamgnetic drift, given on various grid subsets"""

	e_field  :AoS[_T_generic_grid_vector_components] =  sp_property(coordinate1="1...N",units="V.m^-1")
	""" Electric field, given on various grid subsets"""

	phi_potential  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="V")
	""" Electric potential, given on various grid subsets"""


class _T_edge_profiles_profiles_1d(TimeSlice):
	"""1D radial profiles for edge
	aos3Parent: yes"""

	grid  :_T_edge_radial_grid =  sp_property()
	""" Radial grid"""

	electrons  :_T_edge_profiles_profiles_1d_electrons =  sp_property()
	""" Quantities related to the electrons"""

	ion  :AoS[_T_edge_profile_ions] =  sp_property(coordinate1="1...N")
	""" Quantities related to the different ion species, in the sense of isonuclear or
		isomolecular sequences. Ionisation states (and other types of states) must be
		differentiated at the state level below"""

	neutral  :AoS[_T_edge_profile_neutral] =  sp_property(coordinate1="1...N")
	""" Quantities related to the different neutral species"""

	t_i_average  :array_type =  sp_property(coordinate1="../grid/rho_pol_norm",units="eV",type="dynamic")
	""" Ion temperature (averaged on charge states and ion species)"""

	t_i_average_fit  :_T_edge_profiles_1d_fit =  sp_property(units="eV")
	""" Information on the fit used to obtain the t_i_average profile"""

	n_i_total_over_n_e  :array_type =  sp_property(coordinate1="../grid/rho_pol_norm",units="-",type="dynamic")
	""" Ratio of total ion density (sum over species and charge states) over electron
		density. (thermal+non-thermal)"""

	n_i_thermal_total  :array_type =  sp_property(coordinate1="../grid/rho_pol_norm",units="m^-3",type="dynamic")
	""" Total ion thermal density (sum over species and charge states)"""

	momentum_tor  :array_type =  sp_property(coordinate1="../grid/rho_pol_norm",type="dynamic",units="kg.m^-1.s^-1")
	""" Total plasma toroidal momentum, summed over ion species and electrons weighted
		by their density and major radius, i.e. sum_over_species(n*R*m*Vphi)"""

	zeff  :array_type =  sp_property(coordinate1="../grid/rho_pol_norm",type="dynamic",units="-")
	""" Effective charge"""

	zeff_fit  :_T_edge_profiles_1d_fit =  sp_property(units="-")
	""" Information on the fit used to obtain the zeff profile"""

	pressure_ion_total  :array_type =  sp_property(coordinate1="../grid/rho_pol_norm",units="Pa",type="dynamic")
	""" Total (sum over ion species) thermal ion pressure"""

	pressure_thermal  :array_type =  sp_property(coordinate1="../grid/rho_pol_norm",units="Pa",type="dynamic")
	""" Thermal pressure (electrons+ions)"""

	pressure_perpendicular  :array_type =  sp_property(coordinate1="../grid/rho_pol_norm",units="Pa",type="dynamic")
	""" Total perpendicular pressure (electrons+ions, thermal+non-thermal)"""

	pressure_parallel  :array_type =  sp_property(coordinate1="../grid/rho_pol_norm",units="Pa",type="dynamic")
	""" Total parallel pressure (electrons+ions, thermal+non-thermal)"""

	j_total  :array_type =  sp_property(coordinate1="../grid/rho_pol_norm",units="A/m^2",type="dynamic")
	""" Total parallel current density = average(jtot.B) / B0, where B0 =
		edge_profiles/Vacuum_Toroidal_Field/ B0"""

	current_parallel_inside  :array_type =  sp_property(coordinate1="../grid/rho_pol_norm",units="A",type="dynamic")
	""" Parallel current driven inside the flux surface. Cumulative surface integral of
		j_total"""

	j_tor  :array_type =  sp_property(coordinate1="../grid/rho_pol_norm",units="A/m^2",type="dynamic")
	""" Total toroidal current density = average(J_Tor/R) / average(1/R)"""

	j_ohmic  :array_type =  sp_property(coordinate1="../grid/rho_pol_norm",units="A/m^2",type="dynamic")
	""" Ohmic parallel current density = average(J_Ohmic.B) / B0, where B0 =
		edge_profiles/Vacuum_Toroidal_Field/ B0"""

	j_non_inductive  :array_type =  sp_property(coordinate1="../grid/rho_pol_norm",units="A/m^2",type="dynamic")
	""" Non-inductive (includes bootstrap) parallel current density = average(jni.B) /
		B0, where B0 = edge_profiles/Vacuum_Toroidal_Field/ B0"""

	j_bootstrap  :array_type =  sp_property(coordinate1="../grid/rho_pol_norm",units="A/m^2",type="dynamic")
	""" Bootstrap current density = average(J_Bootstrap.B) / B0, where B0 =
		edge_profiles/Vacuum_Toroidal_Field/ B0"""

	conductivity_parallel  :array_type =  sp_property(coordinate1="../grid/rho_pol_norm",units="ohm^-1.m^-1",type="dynamic")
	""" Parallel conductivity"""

	e_field  :_T_edge_profiles_vector_components_1 =  sp_property(units="V.m^-1")
	""" Electric field, averaged on the magnetic surface. E.g for the parallel
		component, average(E.B) / B0, using edge_profiles/vacuum_toroidal_field/b0"""

	phi_potential  :array_type =  sp_property(coordinate1="../grid/rho_pol_norm",type="dynamic",units="V")
	""" Electrostatic potential, averaged on the magnetic flux surface"""

	rotation_frequency_tor_sonic  :array_type =  sp_property(coordinate1="../grid/rho_pol_norm",units="s^-1",type="dynamic",url="https://doi.org/10.1063/1.865350")
	""" Derivative of the flux surface averaged electrostatic potential with respect to
		the poloidal flux, multiplied by -1. This quantity is the toroidal angular
		rotation frequency due to the ExB drift, introduced in formula (43) of Hinton
		and Wong, Physics of Fluids 3082 (1985), also referred to as sonic flow in
		regimes in which the toroidal velocity is dominant over the poloidal velocity"""

	q  :array_type =  sp_property(coordinate1="../grid/rho_pol_norm",type="dynamic",units="-",cocos_label_transformation="q_like",cocos_transformation_expression=".fact_q",cocos_leaf_name_aos_indices="edge_profiles.profiles_1d{i}.q")
	""" Safety factor"""

	magnetic_shear  :array_type =  sp_property(coordinate1="../grid/rho_pol_norm",units="-",type="dynamic")
	""" Magnetic shear, defined as rho_tor/q . dq/drho_tor"""


class _T_edge_profiles(IDS):
	"""Edge plasma profiles (includes the scrape-off layer and possibly part of the
		confined plasma)
	lifecycle_status: active
	lifecycle_version: 3.22.0
	lifecycle_last_change: 3.38.1
	specific_validation_rules: yes"""

	dd_version="v3_38_1_dirty"
	ids_name="edge_profiles"

	vacuum_toroidal_field  :_T_b_tor_vacuum_1 =  sp_property(cocos_alias="IDSPATH",cocos_replace="edge_profiles.vacuum_toroidal_field")
	""" Characteristics of the vacuum toroidal field (used in rho_tor definition and in
		the normalization of current densities)"""

	midplane  :_E_midplane_identifier =  sp_property(doc_identifier="utilities/midplane_identifier.xml",introduced_after_version="3.32.1")
	""" Choice of midplane definition (use the lowest index number if more than one
		value is relevant)"""

	profiles_1d  :TimeSeriesAoS[_T_edge_profiles_profiles_1d] =  sp_property(coordinate1="time",type="dynamic")
	""" SOL radial profiles for various time slices, taken on outboard equatorial
		mid-plane"""

	grid_ggd  :TimeSeriesAoS[_T_generic_grid_aos3_root] =  sp_property(coordinate1="time",type="dynamic")
	""" Grid (using the Generic Grid Description), for various time slices. The timebase
		of this array of structure must be a subset of the ggd timebase"""

	ggd  :TimeSeriesAoS[_T_edge_profiles_time_slice] =  sp_property(coordinate1="time",type="dynamic")
	""" Edge plasma quantities represented using the general grid description, for
		various time slices. The timebase of this array of structure must be a subset of
		the ggd_fast timebase (only if the ggd_fast array of structure is used)"""

	ggd_fast  :TimeSeriesAoS[_T_edge_profiles_ggd_fast] =  sp_property(coordinate1="time",type="dynamic")
	""" Quantities provided at a faster sampling rate than the full ggd quantities.
		These are either integrated quantities or local quantities provided on a reduced
		set of positions. Positions and integration domains are described by a set of
		grid_subsets (of size 1 for a position)."""
