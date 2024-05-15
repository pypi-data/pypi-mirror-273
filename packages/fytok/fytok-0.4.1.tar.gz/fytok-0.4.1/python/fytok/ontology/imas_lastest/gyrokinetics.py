"""
  This module containes the _FyTok_ wrapper of IMAS/dd/gyrokinetics
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_code_partial_constant,_T_entry_tag

class _T_gyrokinetics_species(SpTree):
	"""List of species"""

	charge_norm  :float =  sp_property(type="constant",units="-")
	""" Normalised charge"""

	mass_norm  :float =  sp_property(type="constant",units="-")
	""" Normalised mass"""

	density_norm  :float =  sp_property(type="constant",units="-")
	""" Normalised density"""

	density_log_gradient_norm  :float =  sp_property(type="constant",units="-")
	""" Normalised logarithmic gradient (with respect to r_minor_norm) of the density"""

	temperature_norm  :float =  sp_property(type="constant",units="-")
	""" Normalised temperature"""

	temperature_log_gradient_norm  :float =  sp_property(type="constant",units="-")
	""" Normalised logarithmic gradient (with respect to r_minor_norm) of the
		temperature"""

	velocity_tor_gradient_norm  :float =  sp_property(type="constant",units="-")
	""" Normalised gradient (with respect to r_minor_norm) of the toroidal velocity"""


class _T_gyrokinetics_flux_surface(SpTree):
	"""Flux surface characteristics"""

	r_minor_norm  :float =  sp_property(type="constant",units="-")
	""" Normalised minor radius of the flux surface of interest = 1/2 * (max(R) -
		min(R))/L_ref"""

	elongation  :float =  sp_property(type="constant",units="-")
	""" Elongation"""

	delongation_dr_minor_norm  :float =  sp_property(type="constant",units="-",introduced_after_version="3.36.0")
	""" Derivative of the elongation with respect to r_minor_norm"""

	dgeometric_axis_r_dr_minor  :float =  sp_property(type="constant",units="-",introduced_after_version="3.36.0")
	""" Derivative of the major radius of the surface geometric axis with respect to
		r_minor"""

	dgeometric_axis_z_dr_minor  :float =  sp_property(type="constant",units="-",introduced_after_version="3.36.0")
	""" Derivative of the height of the surface geometric axis with respect to r_minor"""

	q  :float =  sp_property(type="constant",units="-")
	""" Safety factor"""

	magnetic_shear_r_minor  :float =  sp_property(type="constant",units="-")
	""" Magnetic shear, defined as r_minor_norm/q . dq/dr_minor_norm (different
		definition from the equilibrium IDS)"""

	pressure_gradient_norm  :float =  sp_property(type="constant",units="-")
	""" Normalised pressure gradient (derivative with respect to r_minor_norm)"""

	ip_sign  :float =  sp_property(type="constant",units="-")
	""" Sign of the plasma current"""

	b_field_tor_sign  :float =  sp_property(type="constant",units="-")
	""" Sign of the toroidal magnetic field"""

	shape_coefficients_c  :array_type =  sp_property(type="constant",units="-",coordinate1="1...N")
	""" 'c' coefficients in the formula defining the shape of the flux surface"""

	dc_dr_minor_norm  :array_type =  sp_property(type="constant",units="-",coordinate1="../shape_coefficients_c")
	""" Derivative of the 'c' shape coefficients with respect to r_minor_norm"""

	shape_coefficients_s  :array_type =  sp_property(type="constant",units="-",coordinate1="1...N")
	""" 's' coefficients in the formula defining the shape of the flux surface"""

	ds_dr_minor_norm  :array_type =  sp_property(type="constant",units="-",coordinate1="../shape_coefficients_s")
	""" Derivative of the 's' shape coefficients with respect to r_minor_norm"""


class _T_gyrokinetics_input_species_global(SpTree):
	"""Species global parameters"""

	beta_reference  :float =  sp_property(type="constant",units="-")
	""" Reference plasma beta (see detailed documentation at the root of the IDS)"""

	velocity_tor_norm  :float =  sp_property(type="constant",units="-")
	""" Normalised toroidal velocity of species (all species are assumed to have a
		purely toroidal velocity with a common toroidal angular frequency)"""

	zeff  :float =  sp_property(type="constant",units="-")
	""" Effective charge"""

	debye_length_reference  :float =  sp_property(type="constant",units="-")
	""" Debye length computed from the reference quantities (see detailed documentation
		at the root of the IDS)"""

	shearing_rate_norm  :float =  sp_property(type="constant",units="-")
	""" Normalised ExB shearing rate (for non-linear runs only)"""


class _T_gyrokinetics_input_normalizing(SpTree):
	"""GK normalizing quantities"""

	t_e  :float =  sp_property(type="constant",units="eV")
	""" Electron temperature at outboard equatorial midplane of the flux surface
		(poloidal_angle = 0)"""

	n_e  :float =  sp_property(type="constant",units="m^-3")
	""" Electron density at outboard equatorial midplane of the flux surface
		(poloidal_angle = 0)"""

	r  :float =  sp_property(type="constant",units="m")
	""" Major radius of the flux surface of interest, defined as (min(R)+max(R))/2"""

	b_field_tor  :float =  sp_property(type="constant",units="T")
	""" Toroidal magnetic field at major radius r"""


class _T_gyrokinetics_model(SpTree):
	"""Description of the GK model assumptions"""

	include_centrifugal_effects  :int =  sp_property(type="constant")
	""" Flag = 1 if centrifugal effects are retained, 0 otherwise"""

	include_a_field_parallel  :int =  sp_property(type="constant")
	""" Flag = 1 if fluctuations of the parallel vector potential are retained, 0
		otherwise"""

	include_b_field_parallel  :int =  sp_property(type="constant")
	""" Flag = 1 if fluctuations of the parallel magnetic field are retained, 0
		otherwise"""

	include_full_curvature_drift  :int =  sp_property(type="constant")
	""" Flag = 1 if all contributions to the curvature drift are included (including
		beta_prime), 0 otherwise. Neglecting the beta_prime contribution (Flag=0) is
		only recommended together with the neglect of parallel magnetic field
		fluctuations"""

	collisions_pitch_only  :int =  sp_property(type="constant")
	""" Flag = 1 if only pitch-angle scattering is retained, 0 otherwise"""

	collisions_momentum_conservation  :int =  sp_property(type="constant")
	""" Flag = 1 if the collision operator conserves momentum, 0 otherwise"""

	collisions_energy_conservation  :int =  sp_property(type="constant")
	""" Flag = 1 if the collision operator conserves energy, 0 otherwise"""

	collisions_finite_larmor_radius  :int =  sp_property(type="constant")
	""" Flag = 1 if finite larmor radius effects are retained in the collision operator,
		0 otherwise"""

	non_linear_run  :int =  sp_property(type="constant")
	""" Flag = 1 if this is a non-linear run, 0 for a linear run"""

	time_interval_norm  :array_type =  sp_property(type="constant",units="-",coordinate1="1...2")
	""" Normalised time interval used to average fluxes in non-linear runs"""


class _T_gyrokinetics_moments_particles(SpTree):
	"""Turbulent moments for a given eigenmode and a given species, without
		gyroaveraged quantities"""

	density  :array_type =  sp_property(type="constant",units="-",coordinate1="../../../poloidal_angle",coordinate2="../../../time_norm")
	""" Normalised density"""

	j_parallel  :array_type =  sp_property(type="constant",units="-",coordinate1="../../../poloidal_angle",coordinate2="../../../time_norm")
	""" Normalised parallel current density"""

	pressure_parallel  :array_type =  sp_property(type="constant",units="-",coordinate1="../../../poloidal_angle",coordinate2="../../../time_norm")
	""" Normalised parallel temperature"""

	pressure_perpendicular  :array_type =  sp_property(type="constant",units="-",coordinate1="../../../poloidal_angle",coordinate2="../../../time_norm")
	""" Normalised perpendicular temperature"""

	heat_flux_parallel  :array_type =  sp_property(type="constant",units="-",coordinate1="../../../poloidal_angle",coordinate2="../../../time_norm")
	""" Normalised parallel heat flux (integral of 0.5 * m * v_par * v^2)"""

	v_parallel_energy_perpendicular  :array_type =  sp_property(type="constant",units="-",coordinate1="../../../poloidal_angle",coordinate2="../../../time_norm")
	""" Normalised moment (integral over 0.5 * m * v_par * v_perp^2)"""

	v_perpendicular_square_energy  :array_type =  sp_property(type="constant",units="-",coordinate1="../../../poloidal_angle",coordinate2="../../../time_norm")
	""" Normalised moment (integral over 0.5 * m * v_perp^2 * v^2)"""


class _T_gyrokinetics_moments(SpTree):
	"""Turbulent moments for a given eigenmode and a given species, with gyroaveraged
		quantities"""

	density  :array_type =  sp_property(type="constant",units="-",coordinate1="../../../poloidal_angle",coordinate2="../../../time_norm")
	""" Normalised density"""

	density_gyroav  :array_type =  sp_property(type="constant",units="-",coordinate1="../../../poloidal_angle",coordinate2="../../../time_norm")
	""" Normalised density (gyroaveraged)"""

	j_parallel  :array_type =  sp_property(type="constant",units="-",coordinate1="../../../poloidal_angle",coordinate2="../../../time_norm")
	""" Normalised parallel current density"""

	j_parallel_gyroav  :array_type =  sp_property(type="constant",units="-",coordinate1="../../../poloidal_angle",coordinate2="../../../time_norm")
	""" Normalised parallel current density (gyroaveraged)"""

	pressure_parallel  :array_type =  sp_property(type="constant",units="-",coordinate1="../../../poloidal_angle",coordinate2="../../../time_norm")
	""" Normalised parallel temperature"""

	pressure_parallel_gyroav  :array_type =  sp_property(type="constant",units="-",coordinate1="../../../poloidal_angle",coordinate2="../../../time_norm")
	""" Normalised parallel temperature (gyroaveraged)"""

	pressure_perpendicular  :array_type =  sp_property(type="constant",units="-",coordinate1="../../../poloidal_angle",coordinate2="../../../time_norm")
	""" Normalised perpendicular temperature"""

	pressure_perpendicular_gyroav  :array_type =  sp_property(type="constant",units="-",coordinate1="../../../poloidal_angle",coordinate2="../../../time_norm")
	""" Normalised perpendicular temperature (gyroaveraged)"""

	heat_flux_parallel  :array_type =  sp_property(type="constant",units="-",coordinate1="../../../poloidal_angle",coordinate2="../../../time_norm")
	""" Normalised parallel heat flux (integral of 0.5 * m * v_par * v^2)"""

	heat_flux_parallel_gyroav  :array_type =  sp_property(type="constant",units="-",coordinate1="../../../poloidal_angle",coordinate2="../../../time_norm")
	""" Normalised parallel heat flux (integral of 0.5 * m * v_par * v^2, gyroaveraged)"""

	v_parallel_energy_perpendicular  :array_type =  sp_property(type="constant",units="-",coordinate1="../../../poloidal_angle",coordinate2="../../../time_norm")
	""" Normalised moment (integral over 0.5 * m * v_par * v_perp^2)"""

	v_parallel_energy_perpendicular_gyroav  :array_type =  sp_property(type="constant",units="-",coordinate1="../../../poloidal_angle",coordinate2="../../../time_norm")
	""" Normalised moment (integral over 0.5 * m * v_par * v_perp^2, gyroaveraged)"""

	v_perpendicular_square_energy  :array_type =  sp_property(type="constant",units="-",coordinate1="../../../poloidal_angle",coordinate2="../../../time_norm")
	""" Normalised moment (integral over 0.5 * m * v_perp^2 * v^2)"""

	v_perpendicular_square_energy_gyroav  :array_type =  sp_property(type="constant",units="-",coordinate1="../../../poloidal_angle",coordinate2="../../../time_norm")
	""" Normalised moment (integral over 0.5 * m * v_perp^2 * v^2, gyroaveraged)"""


class _T_gyrokinetics_fluxes(SpTree):
	"""Turbulent fluxes for a given eigenmode and a given species"""

	particles_phi_potential  :float =  sp_property(type="constant",units="-")
	""" Contribution of the perturbed electrostatic potential to the normalised particle
		flux"""

	particles_a_field_parallel  :float =  sp_property(type="constant",units="-")
	""" Contribution of the perturbed parallel electromagnetic potential to the
		normalised particle flux"""

	particles_b_field_parallel  :float =  sp_property(type="constant",units="-")
	""" Contribution of the perturbed parallel magnetic field to the normalised particle
		flux"""

	energy_phi_potential  :float =  sp_property(type="constant",units="-")
	""" Contribution of the perturbed electrostatic potential to the normalised energy
		flux"""

	energy_a_field_parallel  :float =  sp_property(type="constant",units="-")
	""" Contribution of the perturbed parallel electromagnetic potential to the
		normalised energy flux"""

	energy_b_field_parallel  :float =  sp_property(type="constant",units="-")
	""" Contribution of the perturbed parallel magnetic field to the normalised energy
		flux"""

	momentum_tor_parallel_phi_potential  :float =  sp_property(type="constant",units="-")
	""" Contribution of the perturbed electrostatic potential to the parallel component
		of the normalised toroidal momentum flux"""

	momentum_tor_parallel_a_field_parallel  :float =  sp_property(type="constant",units="-")
	""" Contribution of the perturbed parallel electromagnetic potential to the parallel
		component of the normalised toroidal momentum flux"""

	momentum_tor_parallel_b_field_parallel  :float =  sp_property(type="constant",units="-")
	""" Contribution of the perturbed parallel magnetic field to the parallel component
		of the normalised toroidal momentum flux"""

	momentum_tor_perpendicular_phi_potential  :float =  sp_property(type="constant",units="-")
	""" Contribution of the perturbed electrostatic potential to the perpendicular
		component of the normalised toroidal momentum flux"""

	momentum_tor_perpendicular_a_field_parallel  :float =  sp_property(type="constant",units="-")
	""" Contribution of the perturbed parallel electromagnetic potential to the
		perpendicular component of the normalised toroidal momentum flux"""

	momentum_tor_perpendicular_b_field_parallel  :float =  sp_property(type="constant",units="-")
	""" Contribution of the perturbed parallel magnetic field to the perpendicular
		component of the normalised toroidal momentum flux"""


class _T_gyrokinetics_collisions(SpTree):
	"""Collisions related quantities"""

	collisionality_norm  :array_type =  sp_property(type="constant",coordinate1="../../species",coordinate2="../../species",units="-")
	""" Normalised collisionality between two species"""


class _T_gyrokinetics_fluxes_moments(SpTree):
	"""Turbulent fluxes and moments for a given eigenmode and a given species"""

	moments_norm_gyrocenter  :_T_gyrokinetics_moments =  sp_property()
	""" Moments (normalised) of the perturbed distribution function of gyrocenters"""

	moments_norm_particle  :_T_gyrokinetics_moments_particles =  sp_property()
	""" Moments (normalised) of the perturbed distribution function of particles"""

	fluxes_norm_gyrocenter  :_T_gyrokinetics_fluxes =  sp_property()
	""" Normalised gyrocenter fluxes in the laboratory frame"""

	fluxes_norm_gyrocenter_rotating_frame  :_T_gyrokinetics_fluxes =  sp_property()
	""" Normalised gyrocenter fluxes in the rotating frame"""

	fluxes_norm_particle  :_T_gyrokinetics_fluxes =  sp_property()
	""" Normalised particle fluxes in the laboratory frame"""

	fluxes_norm_particle_rotating_frame  :_T_gyrokinetics_fluxes =  sp_property()
	""" Normalised particle fluxes in the rotating frame"""


class _T_gyrokinetics_eigenmode(Module):
	"""Output of the GK calculation for a given eigenmode"""

	poloidal_turns  :int =  sp_property(type="constant")
	""" Number of poloidal turns considered in the flux-tube simulation"""

	growth_rate_norm  :float =  sp_property(type="constant",units="-")
	""" Growth rate"""

	frequency_norm  :float =  sp_property(type="constant",units="-")
	""" Frequency"""

	growth_rate_tolerance  :float =  sp_property(type="constant",units="-")
	""" Relative tolerance on the growth rate (convergence of the simulation)"""

	phi_potential_perturbed_weight  :array_type =  sp_property(type="constant",coordinate1="../time_norm",units="-")
	""" Amplitude of the perturbed electrostatic potential normalised to the sum of
		amplitudes of all perturbed fields"""

	phi_potential_perturbed_parity  :array_type =  sp_property(type="constant",coordinate1="../time_norm",units="-")
	""" Parity of the perturbed electrostatic potential with respect to theta = 0
		(poloidal angle)"""

	a_field_parallel_perturbed_weight  :array_type =  sp_property(type="constant",coordinate1="../time_norm",units="-")
	""" Amplitude of the perturbed parallel vector potential normalised to the sum of
		amplitudes of all perturbed fields"""

	a_field_parallel_perturbed_parity  :array_type =  sp_property(type="constant",coordinate1="../time_norm",units="-")
	""" Parity of the perturbed parallel vector potential with respect to theta = 0
		(poloidal angle)"""

	b_field_parallel_perturbed_weight  :array_type =  sp_property(type="constant",coordinate1="../time_norm",units="-")
	""" Amplitude of the perturbed parallel magnetic field normalised to the sum of
		amplitudes of all perturbed fields"""

	b_field_parallel_perturbed_parity  :array_type =  sp_property(type="constant",coordinate1="../time_norm",units="-")
	""" Parity of the perturbed parallel magnetic field with respect to theta = 0
		(poloidal angle)"""

	poloidal_angle  :array_type =  sp_property(type="constant",coordinate1="1...N",units="-")
	""" Poloidal angle grid (see detailed documentation at the root of the IDS)"""

	phi_potential_perturbed_norm  :array_type =  sp_property(type="constant",coordinate1="../poloidal_angle",coordinate2="../time_norm",units="-")
	""" Normalised perturbed electrostatic potential"""

	a_field_parallel_perturbed_norm  :array_type =  sp_property(type="constant",coordinate1="../poloidal_angle",coordinate2="../time_norm",units="-")
	""" Normalised perturbed parallel vector potential"""

	b_field_parallel_perturbed_norm  :array_type =  sp_property(type="constant",coordinate1="../poloidal_angle",coordinate2="../time_norm",units="-")
	""" Normalised perturbed parallel magnetic field"""

	time_norm  :array_type =  sp_property(type="constant",coordinate1="1...N",units="-")
	""" Normalised time of the gyrokinetic simulation"""

	fluxes_moments  :AoS[_T_gyrokinetics_fluxes_moments] =  sp_property(coordinate1="../../../species")
	""" Fluxes and moments of the perturbed distribution function, for this eigenmode
		and for each species. The fluxes are time averaged for non-linear runs (using
		model/ time_interval_norm) and given at the last time step for linear runs."""

	initial_value_run  :int =  sp_property(type="constant",introduced_after_version="3.36.0")
	""" Flag = 1 if this is an initial value run, 0 for an eigenvalue run"""


class _T_gyrokinetics_wavevector(SpTree):
	"""Components of the linear mode wavevector"""

	radial_component_norm  :float =  sp_property(type="constant",units="-")
	""" Normalised radial component of the wavevector"""

	binormal_component_norm  :float =  sp_property(type="constant",units="-")
	""" Normalised binormal component of the wavevector"""

	eigenmode  :AoS[_T_gyrokinetics_eigenmode] =  sp_property(coordinate1="1...N")
	""" Set of eigenmode for this wavector"""


class _T_gyrokinetics(IDS):
	"""Description of a gyrokinetic simulation (delta-f, flux-tube). All quantities
		within this IDS are normalised (apart from time and from the normalizing
		quantities structure), thus independent of rhostar, consistently with the local
		approximation and a spectral representation is assumed in the perpendicular
		plane (i.e. homogeneous turbulence).
	lifecycle_status: alpha
	lifecycle_version: 3.22.0
	lifecycle_last_change: 3.37.0
	url: https://gitlab.com/gkdb/gkdb/raw/master/doc/general/IOGKDB.pdf"""

	dd_version="v3_38_1_dirty"
	ids_name="gyrokinetics"

	tag  :AoS[_T_entry_tag] =  sp_property(coordinate1="1...N")
	""" Set of tags to which this entry belongs"""

	normalizing_quantities  :_T_gyrokinetics_input_normalizing =  sp_property()
	""" Physical quantities used for normalization (useful to link to the original
		simulation/experience)"""

	flux_surface  :_T_gyrokinetics_flux_surface =  sp_property()
	""" Flux surface characteristics"""

	model  :_T_gyrokinetics_model =  sp_property()
	""" Assumptions of the GK calculations"""

	species_all  :_T_gyrokinetics_input_species_global =  sp_property()
	""" Physical quantities common to all species"""

	species  :AoS[_T_gyrokinetics_species] =  sp_property(coordinate1="1...N")
	""" Set of species (including electrons) used in the calculation and related
		quantities"""

	collisions  :_T_gyrokinetics_collisions =  sp_property()
	""" Collisions related quantities"""

	wavevector  :AoS[_T_gyrokinetics_wavevector] =  sp_property(coordinate1="1...N")
	""" Set of wavevectors"""

	fluxes_integrated_norm  :AoS[_T_gyrokinetics_fluxes] =  sp_property(coordinate1="../species")
	""" Normalised fluxes of particles computed in the laboratory frame per species,
		summed over all wavevectors, and averaged over the time interval specified in
		model/time_interval_norm (non-linear runs only)"""
