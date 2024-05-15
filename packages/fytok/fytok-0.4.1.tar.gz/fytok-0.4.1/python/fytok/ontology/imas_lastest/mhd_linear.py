"""
  This module containes the _FyTok_ wrapper of IMAS/dd/mhd_linear
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_identifier_dynamic_aos3,_T_equilibrium_profiles_2d_grid,_T_identifier,_T_b_tor_vacuum_1
from .utilities import _E_poloidal_plane_coordinates_identifier

class _E_mhd_linear_perturbation(IntFlag):
	"""Type of the perturbation	xpath: 	"""
  
	TAE = 1
	"""Toroidal Alfven Eigenmode"""
  
	EAE = 2
	"""Ellipticity-induced Alfven Eigenmode"""
  
	NAE = 3
	"""Non-circular triangularity induced Alfven Eigenmode"""
  
	RSAE = 4
	"""Reversed Shear Alfven Eigenmode"""
  
	BAE = 5
	"""Beta induced Alfven Eigenmode"""
  
	BAAE = 6
	"""Beta induced Alfven Acoustic Eigenmode"""
  
	EPM = 7
	"""Energetic particle mode, outside any shear Alfven gap"""
  
	GAE = 8
	"""Global Alfven Eingenmode"""
  
	GAM = 9
	"""Geodesic Acoustic Mode"""
  
	EGAM = 10
	"""Energetic particle-driven Geodesic Acoustic Mode"""
  
	iKINK = 11
	"""Internal KINK mode"""
  
	eKINK = 12
	"""External KINK mode"""
  
	Tearing = 13
	"""Tearing mode"""
  
	Double_Tearing = 14
	"""Double Tearing mode"""
  

class _E_mhd_linear_model(IntFlag):
	"""Type of the MHD model used	xpath: 	"""
  
	global_ = 1
	"""Global calculation"""
  
	local = 2
	"""Local calculation"""
  
	analytical = 3
	"""Analytical estimate"""
  

class _E_mhd_linear_model(IntFlag):
	"""Type of the MHD model used	xpath: 	"""
  
	reduced = 1
	"""Reduced MHD"""
  
	reduced_kinetic = 11
	"""Reduced MHD and kinetic hybrid"""
  
	full = 2
	"""Full MHD"""
  
	full_kinetic = 21
	"""Full MHD and kinetic hybrid"""
  

class _T_complex_2d_dynamic_aos_mhd_linear_vector(SpTree):
	"""Structure (temporary) for real and imaginary part, while waiting for the
		implementation of complex numbers, dynamic within a type 3 array of structure
		(index on time))"""

	real  :array_type =  sp_property(type="dynamic",units="as_parent",coordinate1="../../../grid/dim1",coordinate2="../../../grid/dim2")
	""" Real part"""

	imaginary  :array_type =  sp_property(type="dynamic",units="as_parent",coordinate1="../../../grid/dim1",coordinate2="../../../grid/dim2")
	""" Imaginary part"""

	coefficients_real  :array_type =  sp_property(type="dynamic",coordinate1="../../../grid/dim1",coordinate2="../../../grid/dim2",coordinate3="1...N",units="as_parent")
	""" Interpolation coefficients, to be used for a high precision evaluation of the
		physical quantity (real part) with finite elements, provided on the 2D grid"""

	coefficients_imaginary  :array_type =  sp_property(type="dynamic",coordinate1="../../../grid/dim1",coordinate2="../../../grid/dim2",coordinate3="1...N",units="as_parent")
	""" Interpolation coefficients, to be used for a high precision evaluation of the
		physical quantity (imaginary part) with finite elements, provided on the 2D grid"""


class _T_complex_2d_dynamic_aos_mhd_scalar(SpTree):
	"""Structure (temporary) for real and imaginary part, while waiting for the
		implementation of complex numbers, dynamic within a type 3 array of structure
		(index on time))"""

	real  :array_type =  sp_property(type="dynamic",units="as_parent",coordinate1="../../grid/dim1",coordinate2="../../grid/dim2")
	""" Real part"""

	imaginary  :array_type =  sp_property(type="dynamic",units="as_parent",coordinate1="../../grid/dim1",coordinate2="../../grid/dim2")
	""" Imaginary part"""

	coefficients_real  :array_type =  sp_property(type="dynamic",coordinate1="../../grid/dim1",coordinate2="../../grid/dim2",coordinate3="1...N",units="as_parent")
	""" Interpolation coefficients, to be used for a high precision evaluation of the
		physical quantity (real part) with finite elements, provided on the 2D grid"""

	coefficients_imaginary  :array_type =  sp_property(type="dynamic",coordinate1="../../grid/dim1",coordinate2="../../grid/dim2",coordinate3="1...N",units="as_parent")
	""" Interpolation coefficients, to be used for a high precision evaluation of the
		physical quantity (imaginary part) with finite elements, provided on the 2D grid"""


class _T_complex_1d_mhd_alfven_spectrum(SpTree):
	"""Structure for real and imaginary part of the shear Alfven spectrum"""

	real  :array_type =  sp_property(type="dynamic",units="s^-1",coordinate1="1...N")
	""" Real part of the frequency, for a given radial position and every root found at
		this position"""

	imaginary  :array_type =  sp_property(type="dynamic",units="s^-1",coordinate1="../real")
	""" Imaginary part of the frequency, for a given radial position and every root
		found at this position"""


class _T_complex_3d_mhd_stress_tensor(SpTree):
	"""Structure for real and imaginary part of MHD stress tensors"""

	real  :array_type =  sp_property(type="dynamic",units="N.m^-2",coordinate1="../../grid/dim1",coordinate2="1...N",coordinate3="1...N")
	""" Real part of the stress tensor, for various radial positions"""

	imaginary  :array_type =  sp_property(type="dynamic",units=["s^-1","N.m^-2"],coordinate1="../../grid/dim1",coordinate2="1...N",coordinate2_same_as="../real",coordinate3="1...N",coordinate3_same_as="../real")
	""" Imaginary part of the stress tensor, for various radial positions"""


class _T_mhd_coordinate_system(SpTree):
	"""Flux surface coordinate system on a square grid of flux and poloidal angle"""

	grid_type  :_E_poloidal_plane_coordinates_identifier =  sp_property(doc_identifier="utilities/poloidal_plane_coordinates_identifier.xml")
	""" Selection of one of a set of grid types"""

	grid  :_T_equilibrium_profiles_2d_grid =  sp_property()
	""" Definition of the 2D grid"""

	r  :Field =  sp_property(type="dynamic",coordinate1="../grid/dim1",coordinate2="../grid/dim2",units="m")
	""" Values of the major radius on the grid"""

	z  :Field =  sp_property(type="dynamic",coordinate1="../grid/dim1",coordinate2="../grid/dim2",units="m")
	""" Values of the Height on the grid"""

	jacobian  :Field =  sp_property(type="dynamic",coordinate1="../grid/dim1",coordinate2="../grid/dim2",units="mixed")
	""" Absolute value of the jacobian of the coordinate system"""

	tensor_covariant  :array_type =  sp_property(type="dynamic",coordinate1="../grid/dim1",coordinate2="../grid/dim2",coordinate3="1...3",coordinate4="1...3",units="mixed")
	""" Covariant metric tensor on every point of the grid described by grid_type"""

	tensor_contravariant  :array_type =  sp_property(type="dynamic",coordinate1="../grid/dim1",coordinate2="../grid/dim2",coordinate3="1...3",coordinate4="1...3",units="mixed")
	""" Contravariant metric tensor on every point of the grid described by grid_type"""


class _T_mhd_linear_vector(SpTree):
	"""Vector structure for the MHD IDS"""

	coordinate1  :_T_complex_2d_dynamic_aos_mhd_linear_vector =  sp_property(units="as_parent")
	""" First coordinate (radial)"""

	coordinate2  :_T_complex_2d_dynamic_aos_mhd_linear_vector =  sp_property(units="as_parent")
	""" Second coordinate (poloidal)"""

	coordinate3  :_T_complex_2d_dynamic_aos_mhd_linear_vector =  sp_property(units="as_parent")
	""" Third coordinate (toroidal)"""


class _T_mhd_linear_time_slice_toroidal_mode_vacuum(SpTree):
	"""MHD modes in the vacuum"""

	grid_type  :_E_poloidal_plane_coordinates_identifier =  sp_property(doc_identifier="utilities/poloidal_plane_coordinates_identifier.xml")
	""" Selection of one of a set of grid types"""

	grid  :_T_equilibrium_profiles_2d_grid =  sp_property(cocos_alias="IDSPATH",cocos_replace="mhd_linear.time_slice{i}.toroidal_mode{j}.vacuum")
	""" Definition of the 2D grid (the content of dim1 and dim2 is defined by the
		selected grid_type)"""

	coordinate_system  :_T_mhd_coordinate_system =  sp_property(cocos_alias="IDSPATH",cocos_replace="mhd_linear.time_slice{i}.toroidal_mode{j}.vacuum.coordinate_system")
	""" Flux surface coordinate system of the equilibrium used for the MHD calculation
		on a square grid of flux and poloidal angle"""

	a_field_perturbed  :_T_mhd_linear_vector =  sp_property(units="T.m")
	""" Pertubed vector potential for given toroidal mode number"""

	b_field_perturbed  :_T_mhd_linear_vector =  sp_property(units="T")
	""" Pertubed magnetic field for given toroidal mode number"""


class _T_mhd_linear_time_slice_toroidal_mode_plasma(SpTree):
	"""MHD modes in the confined plasma"""

	grid_type  :_E_poloidal_plane_coordinates_identifier =  sp_property(doc_identifier="utilities/poloidal_plane_coordinates_identifier.xml")
	""" Selection of one of a set of grid types"""

	grid  :_T_equilibrium_profiles_2d_grid =  sp_property(cocos_alias="IDSPATH",cocos_replace="mhd_linear.time_slice{i}.toroidal_mode{j}.plasma")
	""" Definition of the 2D grid (the content of dim1 and dim2 is defined by the
		selected grid_type)"""

	coordinate_system  :_T_mhd_coordinate_system =  sp_property(cocos_alias="IDSPATH",cocos_replace="mhd_linear.time_slice{i}.toroidal_mode{j}.plasma.coordinate_system")
	""" Flux surface coordinate system of the equilibrium used for the MHD calculation
		on a square grid of flux and poloidal angle"""

	displacement_perpendicular  :_T_complex_2d_dynamic_aos_mhd_scalar =  sp_property(units="m")
	""" Perpendicular displacement of the modes"""

	displacement_parallel  :_T_complex_2d_dynamic_aos_mhd_scalar =  sp_property(units="m")
	""" Parallel displacement of the modes"""

	tau_alfven  :array_type =  sp_property(type="dynamic",coordinate1="../grid/dim1",units="s")
	""" Alven time=R/vA=R0 sqrt(mi ni(rho))/B0"""

	tau_resistive  :array_type =  sp_property(type="dynamic",coordinate1="../grid/dim1",units="s")
	""" Resistive time = mu_0 rho*rho/1.22/eta_neo"""

	a_field_perturbed  :_T_mhd_linear_vector =  sp_property(units="T.m")
	""" Pertubed vector potential for given toroidal mode number"""

	b_field_perturbed  :_T_mhd_linear_vector =  sp_property(units="T")
	""" Pertubed magnetic field for given toroidal mode number"""

	velocity_perturbed  :_T_mhd_linear_vector =  sp_property(units="m/s")
	""" Pertubed velocity for given toroidal mode number"""

	pressure_perturbed  :_T_complex_2d_dynamic_aos_mhd_scalar =  sp_property(units="Pa")
	""" Perturbed pressure for given toroidal mode number"""

	mass_density_perturbed  :_T_complex_2d_dynamic_aos_mhd_scalar =  sp_property(units="kg.m^-3")
	""" Perturbed mass density for given toroidal mode number"""

	temperature_perturbed  :_T_complex_2d_dynamic_aos_mhd_scalar =  sp_property(units="eV")
	""" Perturbed temperature for given toroidal mode number"""

	phi_potential_perturbed  :_T_complex_2d_dynamic_aos_mhd_scalar =  sp_property(units="V")
	""" Perturbed electrostatic potential for given toroidal mode number"""

	psi_potential_perturbed  :_T_complex_2d_dynamic_aos_mhd_scalar =  sp_property(units="V")
	""" Perturbed electromagnetic super-potential for given toroidal mode number, see
		ref [Antonsen/Lane Phys Fluids 23(6) 1980, formula 34], so that
		A_field_parallel=1/(i*2pi*frequency) (grad psi_potential)_parallel"""

	alfven_frequency_spectrum  :AoS[_T_complex_1d_mhd_alfven_spectrum] =  sp_property(coordinate1="../grid/dim1")
	""" Local shear Alfven spectrum as a function of radius (only in case grid/dim1 is a
		radial coordinate)"""

	stress_maxwell  :_T_complex_3d_mhd_stress_tensor =  sp_property()
	""" Maxwell stress tensor"""

	stress_reynolds  :_T_complex_3d_mhd_stress_tensor =  sp_property()
	""" Reynolds stress tensor"""

	ntv  :_T_complex_3d_mhd_stress_tensor =  sp_property()
	""" Neoclassical toroidal viscosity tensor"""


class _T_mhd_linear_time_slice_toroidal_modes(SpTree):
	"""Vector of toroidal modes"""

	perturbation_type  :_E_mhd_linear_perturbation =  sp_property(doc_identifier="mhd_linear/mhd_linear_perturbation_identifier.xml")
	""" Type of the perturbation"""

	n_tor  :int =  sp_property(type="dynamic")
	""" Toroidal mode number of the MHD mode"""

	m_pol_dominant  :float =  sp_property(type="dynamic",units="-")
	""" Dominant poloidal mode number defining the mode rational surface; for TAEs the
		lower of the two main m's has to be specified"""

	ballooning_type  :_E_mhd_linear_perturbation =  sp_property(doc_identifier="mhd_linear/mhd_linear_perturbation_identifier.xml")
	""" Ballooning type of the mode : ballooning 0; anti-ballooning:1; flute-like:2"""

	radial_mode_number  :float =  sp_property(type="dynamic",units="-")
	""" Radial mode number"""

	growthrate  :float =  sp_property(type="dynamic",units="Hz")
	""" Linear growthrate of the mode"""

	frequency  :float =  sp_property(type="dynamic",units="Hz")
	""" Frequency of the mode"""

	phase  :float =  sp_property(type="dynamic",units="rad")
	""" Additional phase offset of mode"""

	energy_perturbed  :float =  sp_property(type="dynamic",units="J")
	""" Perturbed energy associated to the mode"""

	amplitude_multiplier  :float =  sp_property(type="dynamic",units="mixed")
	""" Multiplier that is needed to convert the linear mode structures to the amplitude
		of a non-linearly saturated mode in physical units. If empty, it means that the
		structures contains no information about non-linearly saturated mode"""

	plasma  :_T_mhd_linear_time_slice_toroidal_mode_plasma =  sp_property()
	""" MHD modes in the confined plasma"""

	vacuum  :_T_mhd_linear_time_slice_toroidal_mode_vacuum =  sp_property()
	""" MHD modes in the vacuum"""


class _T_mhd_linear_time_slice(TimeSlice):
	"""Time slice description of linear MHD stability"""

	toroidal_mode  :AoS[_T_mhd_linear_time_slice_toroidal_modes] =  sp_property(coordinate1="1...N")
	""" Vector of toroidal modes. Each mode is described as exp(i(n_tor.phi -
		m_pol.theta - 2.pi.frequency.t - phase))"""


class _T_mhd_linear(IDS):
	"""Magnetohydronamic linear stability
	lifecycle_status: alpha
	lifecycle_version: 3.0.4
	lifecycle_last_change: 3.30.0"""

	dd_version="v3_38_1_dirty"
	ids_name="mhd_linear"

	model_type  :_E_mhd_linear_model =  sp_property(doc_identifier="mhd_linear/mhd_linear_model_identifier.xml")
	""" Type of model used to populate this IDS"""

	equations  :_E_mhd_linear_model =  sp_property(doc_identifier="mhd_linear/mhd_linear_equations_identifier.xml")
	""" Type of MHD equations used to populate this IDS"""

	fluids_n  :int =  sp_property(type="constant")
	""" Number of fluids considered in the model"""

	ideal_flag  :int =  sp_property(type="constant")
	""" 1 if ideal MHD is used to populate this IDS, 0 for non-ideal MHD"""

	vacuum_toroidal_field  :_T_b_tor_vacuum_1 =  sp_property(cocos_alias="IDSPATH",cocos_replace="mhd_linear.vacuum_toroidal_field")
	""" Characteristics of the vacuum toroidal field (used in rho_tor definition and in
		the normalization of current densities)"""

	time_slice  :TimeSeriesAoS[_T_mhd_linear_time_slice] =  sp_property(coordinate1="time",type="dynamic")
	""" Core plasma radial profiles for various time slices"""
