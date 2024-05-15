"""
  This module containes the _FyTok_ wrapper of IMAS/dd/equilibrium
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_identifier_dynamic_aos3,_T_rz1d_dynamic_aos,_T_rz0d_dynamic_aos,_T_rzphi0d_dynamic_aos3,_T_equilibrium_profiles_2d_grid,_T_generic_grid_dynamic,_T_generic_grid_scalar,_T_equilibrium_coordinate_system,_T_b_tor_vacuum_1
from .utilities import _E_poloidal_plane_coordinates_identifier

class _E_equilibrium_gs_deviation(IntFlag):
	"""List of boundary condition types for 1D transport solvers	xpath: equilibrium/time_slice/convergence/grad_shafranov_deviation_expression	"""
  
	absolute_gs_difference = 1
	"""Average absolute difference of the Grad-Shafranov equation, <|Del* psi -
		j_tor*R|>, averaged over the plasma poloidal cross-section"""
  
	root_mean_square_gs_difference = 2
	"""Root mean square difference of the Grad-Shafranov equation, sqrt(<(Del* psi -
		j_tor*R)^2 >), averaged over the plasma poloidal cross-section"""
  
	max_absolute_psi_residual = 3
	"""Maximum absolute difference over the plasma poloidal cross-section of the
		poloidal flux between the current and preceding iteration, on fixed grid points"""
  
	max_absolute_gs_difference_norm = 4
	"""Maximum absolute difference of the Grad-Shafranov equation, normalised,
		max(|Del* psi - j_tor*R|) / max(|Del* psi|), over the plasma poloidal
		cross-section"""
  
	max_root_mean_square_gs_difference_norm = 5
	"""Root maximum square difference of the Grad-Shafranov equation, normalised,
		sqrt(max((Del* psi - j_tor*R)^2) / max((Del* psi)^2)), over the plasma poloidal
		cross-section"""
  

class _E_equilibrium_profiles_2d_identifier(IntFlag):
	"""Various contributions to the B, j, and psi 2D maps	xpath: 	"""
  
	total = 0
	"""Total fields"""
  
	vacuum = 1
	"""Vacuum fields (without contribution from plasma)"""
  
	pf_active = 2
	"""Contribution from active coils only to the fields (pf_active IDS)"""
  
	pf_passive = 3
	"""Contribution from passive elements only to the fields (pf_passive IDS)"""
  
	plasma = 4
	"""Plasma contribution to the fields"""
  

class _T_equilibrium_gap(SpTree):
	"""Gap for describing the plasma boundary"""

	name  :str =  sp_property(type="dynamic")
	""" Name of the gap"""

	identifier  :str =  sp_property(type="dynamic")
	""" Identifier of the gap"""

	r  :float =  sp_property(units="m",type="dynamic")
	""" Major radius of the reference point"""

	z  :float =  sp_property(units="m",type="dynamic")
	""" Height of the reference point"""

	angle  :float =  sp_property(units="rad",type="dynamic")
	""" Angle measured clockwise from radial cylindrical vector (grad R) to gap vector
		(pointing away from reference point)"""

	value  :float =  sp_property(units="m",type="dynamic")
	""" Value of the gap, i.e. distance between the reference point and the separatrix
		along the gap direction"""


class _T_equilibrium_profiles_1d_rz1d_dynamic_aos(SpTree):
	"""Structure for list of R, Z positions (1D list of Npoints, dynamic within a type
		3 array of structures (index on time)), with coordinates referring to
		profiles_1d/psi"""

	r  :Expression  =  sp_property(type="dynamic",units="m",coordinate1="../../psi")
	""" Major radius"""

	z  :Expression  =  sp_property(type="dynamic",units="m",coordinate1="../../psi")
	""" Height"""


class _T_equilibrium_boundary_closest(SpTree):
	"""Position and distance to the plasma boundary of the point of the first wall
		which is the closest to plasma boundary
	aos3Parent: yes"""

	r  :float =  sp_property(type="dynamic",units="m")
	""" Major radius"""

	z  :float =  sp_property(type="dynamic",units="m")
	""" Height"""

	distance  :float =  sp_property(type="dynamic",units="m",introduced_after_version="3.32.1")
	""" Distance to the plasma boundary"""


class _T_equilibrium_global_quantities_current_centre(SpTree):
	"""R, Z, and vertical velocity of current centre, dynamic within a type 3 array of
		structure (index on time)"""

	r  :float =  sp_property(type="dynamic",units="m")
	""" Major radius of the current center, defined as integral over the poloidal cross
		section of (j_tor*r*dS) / Ip"""

	z  :float =  sp_property(type="dynamic",units="m")
	""" Height of the current center, defined as integral over the poloidal cross
		section of (j_tor*z*dS) / Ip"""

	velocity_z  :float =  sp_property(type="dynamic",units="m.s^-1")
	""" Vertical velocity of the current center"""


class _T_equilibrium_global_quantities_magnetic_axis(SpTree):
	"""R, Z, and Btor at magnetic axis, dynamic within a type 3 array of structure
		(index on time)"""

	r  :float =  sp_property(type="dynamic",units="m")
	""" Major radius of the magnetic axis"""

	z  :float =  sp_property(type="dynamic",units="m")
	""" Height of the magnetic axis"""

	b_field_tor  :float =  sp_property(type="dynamic",units="T",cocos_label_transformation="b0_like",cocos_transformation_expression=".sigma_b0_eff",cocos_leaf_name_aos_indices="equilibrium.time_slice{i}.global_quantities.magnetic_axis.b_field_tor")
	""" Total toroidal magnetic field at the magnetic axis"""


class _T_equilibrium_global_quantities_qmin(SpTree):
	"""Position and value of q_min"""

	value  :float =  sp_property(type="dynamic",units="-",cocos_label_transformation="q_like",cocos_transformation_expression=".fact_q",cocos_leaf_name_aos_indices="equilibrium.time_slice{i}.global_quantities.q_min.value")
	""" Minimum q value"""

	rho_tor_norm  :float =  sp_property(type="dynamic",units="-")
	""" Minimum q position in normalised toroidal flux coordinate"""


class _T_equilibrium_constraints_0D_b0_like(SpTree):
	"""Scalar constraint, b0_like cocos transform"""

	measured  :float =  sp_property(type="dynamic",units="as_parent",cocos_label_transformation="b0_like",cocos_transformation_expression=".sigma_b0_eff",cocos_leaf_name_aos_indices="IDSPATH.measured")
	""" Measured value"""

	source  :str =  sp_property(type="dynamic")
	""" Path to the source data for this measurement in the IMAS data dictionary"""

	time_measurement  :float =  sp_property(type="dynamic",units="s")
	""" Exact time slice used from the time array of the measurement source data. If the
		time slice does not exist in the time array of the source data, it means linear
		interpolation has been used"""

	exact  :int =  sp_property(type="dynamic")
	""" Integer flag : 1 means exact data, taken as an exact input without being fitted;
		0 means the equilibrium code does a least square fit"""

	weight  :float =  sp_property(type="dynamic",units="-")
	""" Weight given to the measurement"""

	reconstructed  :float =  sp_property(type="dynamic",units="as_parent",cocos_label_transformation="b0_like",cocos_transformation_expression=".sigma_b0_eff",cocos_leaf_name_aos_indices="IDSPATH.reconstructed")
	""" Value calculated from the reconstructed equilibrium"""

	chi_squared  :float =  sp_property(type="dynamic",units="as_parent")
	""" Squared error normalized by the standard deviation considered in the
		minimization process : chi_squared = weight^2 *(reconstructed - measured)^2 /
		sigma^2, where sigma is the standard deviation of the measurement error"""


class _T_equilibrium_constraints_0D_ip_like(SpTree):
	"""Scalar constraint, ip_like cocos transform"""

	measured  :float =  sp_property(type="dynamic",units="as_parent",cocos_label_transformation="ip_like",cocos_transformation_expression=".sigma_ip_eff",cocos_leaf_name_aos_indices="IDSPATH.measured")
	""" Measured value"""

	source  :str =  sp_property(type="dynamic")
	""" Path to the source data for this measurement in the IMAS data dictionary"""

	time_measurement  :float =  sp_property(type="dynamic",units="s")
	""" Exact time slice used from the time array of the measurement source data. If the
		time slice does not exist in the time array of the source data, it means linear
		interpolation has been used"""

	exact  :int =  sp_property(type="dynamic")
	""" Integer flag : 1 means exact data, taken as an exact input without being fitted;
		0 means the equilibrium code does a least square fit"""

	weight  :float =  sp_property(type="dynamic",units="-")
	""" Weight given to the measurement"""

	reconstructed  :float =  sp_property(type="dynamic",units="as_parent",cocos_label_transformation="ip_like",cocos_transformation_expression=".sigma_ip_eff",cocos_leaf_name_aos_indices="IDSPATH.reconstructed")
	""" Value calculated from the reconstructed equilibrium"""

	chi_squared  :float =  sp_property(type="dynamic",units="as_parent")
	""" Squared error normalized by the standard deviation considered in the
		minimization process : chi_squared = weight^2 *(reconstructed - measured)^2 /
		sigma^2, where sigma is the standard deviation of the measurement error"""


class _T_equilibrium_constraints_0D_psi_like(SpTree):
	"""Scalar constraint, psi_like cocos transform"""

	measured  :float =  sp_property(type="dynamic",units="as_parent",cocos_label_transformation="psi_like",cocos_transformation_expression=".fact_psi",cocos_leaf_name_aos_indices="IDSPATH.measured")
	""" Measured value"""

	source  :str =  sp_property(type="dynamic")
	""" Path to the source data for this measurement in the IMAS data dictionary"""

	time_measurement  :float =  sp_property(type="dynamic",units="s")
	""" Exact time slice used from the time array of the measurement source data. If the
		time slice does not exist in the time array of the source data, it means linear
		interpolation has been used"""

	exact  :int =  sp_property(type="dynamic")
	""" Integer flag : 1 means exact data, taken as an exact input without being fitted;
		0 means the equilibrium code does a least square fit"""

	weight  :float =  sp_property(type="dynamic",units="-")
	""" Weight given to the measurement"""

	reconstructed  :float =  sp_property(type="dynamic",units="as_parent",cocos_label_transformation="psi_like",cocos_transformation_expression=".fact_psi",cocos_leaf_name_aos_indices="IDSPATH.reconstructed")
	""" Value calculated from the reconstructed equilibrium"""

	chi_squared  :float =  sp_property(type="dynamic",units="as_parent")
	""" Squared error normalized by the standard deviation considered in the
		minimization process : chi_squared = weight^2 *(reconstructed - measured)^2 /
		sigma^2, where sigma is the standard deviation of the measurement error"""


class _T_equilibrium_constraints_0D_one_like(SpTree):
	"""Scalar constraint, one_like cocos transform"""

	measured  :float =  sp_property(type="dynamic",units="as_parent",cocos_label_transformation="one_like",cocos_transformation_expression="'1'",cocos_leaf_name_aos_indices="IDSPATH.measured")
	""" Measured value"""

	source  :str =  sp_property(type="dynamic")
	""" Path to the source data for this measurement in the IMAS data dictionary"""

	time_measurement  :float =  sp_property(type="dynamic",units="s")
	""" Exact time slice used from the time array of the measurement source data. If the
		time slice does not exist in the time array of the source data, it means linear
		interpolation has been used"""

	exact  :int =  sp_property(type="dynamic")
	""" Integer flag : 1 means exact data, taken as an exact input without being fitted;
		0 means the equilibrium code does a least square fit"""

	weight  :float =  sp_property(type="dynamic",units="-")
	""" Weight given to the measurement"""

	reconstructed  :float =  sp_property(type="dynamic",units="as_parent",cocos_label_transformation="one_like",cocos_transformation_expression="'1'",cocos_leaf_name_aos_indices="IDSPATH.reconstructed")
	""" Value calculated from the reconstructed equilibrium"""

	chi_squared  :float =  sp_property(type="dynamic",units="as_parent")
	""" Squared error normalized by the standard deviation considered in the
		minimization process : chi_squared = weight^2 *(reconstructed - measured)^2 /
		sigma^2, where sigma is the standard deviation of the measurement error"""


class _T_equilibrium_constraints_0D(SpTree):
	"""Scalar constraint, no cocos transform"""

	measured  :float =  sp_property(type="dynamic",units="as_parent")
	""" Measured value"""

	source  :str =  sp_property(type="dynamic")
	""" Path to the source data for this measurement in the IMAS data dictionary"""

	time_measurement  :float =  sp_property(type="dynamic",units="s")
	""" Exact time slice used from the time array of the measurement source data. If the
		time slice does not exist in the time array of the source data, it means linear
		interpolation has been used"""

	exact  :int =  sp_property(type="dynamic")
	""" Integer flag : 1 means exact data, taken as an exact input without being fitted;
		0 means the equilibrium code does a least square fit"""

	weight  :float =  sp_property(type="dynamic",units="-")
	""" Weight given to the measurement"""

	reconstructed  :float =  sp_property(type="dynamic",units="as_parent")
	""" Value calculated from the reconstructed equilibrium"""

	chi_squared  :float =  sp_property(type="dynamic",units="as_parent")
	""" Squared error normalized by the standard deviation considered in the
		minimization process : chi_squared = weight^2 *(reconstructed - measured)^2 /
		sigma^2, where sigma is the standard deviation of the measurement error"""


class _T_equilibrium_convergence(SpTree):
	"""Convergence details for the equilibrium calculation"""

	iterations_n  :int =  sp_property(type="dynamic")
	""" Number of iterations carried out in the convergence loop"""

	grad_shafranov_deviation_expression  :_E_equilibrium_gs_deviation =  sp_property(introduced_after_version="3.36.0",doc_identifier="equilibrium/equilibrium_gs_deviation.xml")
	""" Expression for calculating the residual deviation between the left and right
		hand side of the Grad Shafranov equation"""

	grad_shafranov_deviation_value  :float =  sp_property(type="dynamic",units="mixed",introduced_after_version="3.36.0")
	""" Value of the residual deviation between the left and right hand side of the Grad
		Shafranov equation, evaluated as per grad_shafranov_deviation_expression"""


class _T_equilibrium_boundary_second_separatrix(SpTree):
	"""Geometry of the plasma boundary at the secondary separatrix"""

	outline  :CurveRZ =  sp_property()
	""" RZ outline of the plasma boundary"""

	psi  :float =  sp_property(type="dynamic",units="Wb")
	""" Value of the poloidal flux at the separatrix"""

	distance_inner_outer  :float =  sp_property(type="dynamic",units="m",introduced_after_version="3.32.1")
	""" Distance between the inner and outer separatrices, in the major radius
		direction, at the plasma outboard and at the height corresponding to the maximum
		R for the inner separatrix."""

	x_point  :AoS[PointRZ] =  sp_property(coordinate1="1...N")
	""" Array of X-points, for each of them the RZ position is given"""

	strike_point  :AoS[PointRZ] =  sp_property(coordinate1="1...N",introduced_after_version="3.32.1")
	""" Array of strike points, for each of them the RZ position is given"""


class _T_equilibrium_boundary_separatrix(SpTree):
	"""Geometry of the plasma boundary at the separatrix"""

	type  :int =  sp_property(type="dynamic")
	""" 0 (limiter) or 1 (diverted)"""

	outline  :CurveRZ =  sp_property()
	""" RZ outline of the plasma boundary"""

	psi  :float =  sp_property(type="dynamic",units="Wb")
	""" Value of the poloidal flux at the separatrix"""

	geometric_axis  :PointRZ =  sp_property()
	""" RZ position of the geometric axis (defined as (Rmin+Rmax) / 2 and (Zmin+Zmax) /
		2 of the boundary)"""

	minor_radius  :float =  sp_property(type="dynamic",units="m")
	""" Minor radius of the plasma boundary (defined as (Rmax-Rmin) / 2 of the boundary)"""

	elongation  :float =  sp_property(type="dynamic",units="-",url="equilibrium/DefinitionEqBoundary.svg")
	""" Elongation of the plasma boundary"""

	elongation_upper  :float =  sp_property(type="dynamic",units="-",url="equilibrium/DefinitionEqBoundary.svg")
	""" Elongation (upper half w.r.t. geometric axis) of the plasma boundary"""

	elongation_lower  :float =  sp_property(type="dynamic",units="-",url="equilibrium/DefinitionEqBoundary.svg")
	""" Elongation (lower half w.r.t. geometric axis) of the plasma boundary"""

	triangularity  :float =  sp_property(units="-",type="dynamic",url="equilibrium/DefinitionEqBoundary.svg")
	""" Triangularity of the plasma boundary"""

	triangularity_upper  :float =  sp_property(units="-",type="dynamic",url="equilibrium/DefinitionEqBoundary.svg")
	""" Upper triangularity of the plasma boundary"""

	triangularity_lower  :float =  sp_property(units="-",type="dynamic",url="equilibrium/DefinitionEqBoundary.svg")
	""" Lower triangularity of the plasma boundary"""

	squareness_upper_inner  :float =  sp_property(type="dynamic",units="-",lifecycle_status="alpha",lifecycle_version="3.18.0")
	""" Upper inner squareness of the plasma boundary (definition from T. Luce, Plasma
		Phys. Control. Fusion 55 (2013) 095009)"""

	squareness_upper_outer  :float =  sp_property(type="dynamic",units="-",lifecycle_status="alpha",lifecycle_version="3.18.0")
	""" Upper outer squareness of the plasma boundary (definition from T. Luce, Plasma
		Phys. Control. Fusion 55 (2013) 095009)"""

	squareness_lower_inner  :float =  sp_property(type="dynamic",units="-",lifecycle_status="alpha",lifecycle_version="3.18.0")
	""" Lower inner squareness of the plasma boundary (definition from T. Luce, Plasma
		Phys. Control. Fusion 55 (2013) 095009)"""

	squareness_lower_outer  :float =  sp_property(type="dynamic",units="-",lifecycle_status="alpha",lifecycle_version="3.18.0")
	""" Lower outer squareness of the plasma boundary (definition from T. Luce, Plasma
		Phys. Control. Fusion 55 (2013) 095009)"""

	x_point  :AoS[PointRZ] =  sp_property(coordinate1="1...N")
	""" Array of X-points, for each of them the RZ position is given"""

	strike_point  :AoS[PointRZ] =  sp_property(coordinate1="1...N")
	""" Array of strike points, for each of them the RZ position is given"""

	active_limiter_point  :PointRZ =  sp_property()
	""" RZ position of the active limiter point (point of the plasma boundary in contact
		with the limiter)"""

	closest_wall_point  :_T_equilibrium_boundary_closest =  sp_property()
	""" Position and distance to the plasma boundary of the point of the first wall
		which is the closest to plasma boundary"""

	dr_dz_zero_point  :PointRZ =  sp_property(introduced_after_version="3.32.1")
	""" Outboard point on the separatrix on which dr/dz = 0 (local maximum of the major
		radius of the separatrix). In case of multiple local maxima, the closest one
		from z=z_magnetic_axis is chosen."""

	gap  :AoS[_T_equilibrium_gap] =  sp_property(coordinate1="1...N")
	""" Set of gaps, defined by a reference point and a direction."""


class _T_equilibrium_boundary(SpTree):
	"""Geometry of the plasma boundary typically taken at psi_norm = 99.x % of the
		separatrix"""

	type  :int =  sp_property(type="dynamic")
	""" 0 (limiter) or 1 (diverted)"""

	outline  :CurveRZ =  sp_property()
	""" RZ outline of the plasma boundary"""

	psi_norm  :float =  sp_property(type="dynamic",units="-")
	""" Value of the normalised poloidal flux at which the boundary is taken (typically
		99.x %), the flux being normalised to its value at the separatrix"""

	psi  :float =  sp_property(type="dynamic",units="Wb")
	""" Value of the poloidal flux at which the boundary is taken"""

	geometric_axis  :PointRZ =  sp_property()
	""" RZ position of the geometric axis (defined as (Rmin+Rmax) / 2 and (Zmin+Zmax) /
		2 of the boundary)"""

	minor_radius  :float =  sp_property(type="dynamic",units="m")
	""" Minor radius of the plasma boundary (defined as (Rmax-Rmin) / 2 of the boundary)"""

	elongation  :float =  sp_property(type="dynamic",units="-",url="equilibrium/DefinitionEqBoundary.svg")
	""" Elongation of the plasma boundary"""

	elongation_upper  :float =  sp_property(type="dynamic",units="-",url="equilibrium/DefinitionEqBoundary.svg")
	""" Elongation (upper half w.r.t. geometric axis) of the plasma boundary"""

	elongation_lower  :float =  sp_property(type="dynamic",units="-",url="equilibrium/DefinitionEqBoundary.svg")
	""" Elongation (lower half w.r.t. geometric axis) of the plasma boundary"""

	triangularity  :float =  sp_property(units="-",type="dynamic",url="equilibrium/DefinitionEqBoundary.svg")
	""" Triangularity of the plasma boundary"""

	triangularity_upper  :float =  sp_property(units="-",type="dynamic",url="equilibrium/DefinitionEqBoundary.svg")
	""" Upper triangularity of the plasma boundary"""

	triangularity_lower  :float =  sp_property(units="-",type="dynamic",url="equilibrium/DefinitionEqBoundary.svg")
	""" Lower triangularity of the plasma boundary"""

	squareness_upper_inner  :float =  sp_property(type="dynamic",units="-",lifecycle_status="alpha",lifecycle_version="3.18.0")
	""" Upper inner squareness of the plasma boundary (definition from T. Luce, Plasma
		Phys. Control. Fusion 55 (2013) 095009)"""

	squareness_upper_outer  :float =  sp_property(type="dynamic",units="-",lifecycle_status="alpha",lifecycle_version="3.18.0")
	""" Upper outer squareness of the plasma boundary (definition from T. Luce, Plasma
		Phys. Control. Fusion 55 (2013) 095009)"""

	squareness_lower_inner  :float =  sp_property(type="dynamic",units="-",lifecycle_status="alpha",lifecycle_version="3.18.0")
	""" Lower inner squareness of the plasma boundary (definition from T. Luce, Plasma
		Phys. Control. Fusion 55 (2013) 095009)"""

	squareness_lower_outer  :float =  sp_property(type="dynamic",units="-",lifecycle_status="alpha",lifecycle_version="3.18.0")
	""" Lower outer squareness of the plasma boundary (definition from T. Luce, Plasma
		Phys. Control. Fusion 55 (2013) 095009)"""

	x_point  :AoS[PointRZ] =  sp_property(coordinate1="1...N")
	""" Array of X-points, for each of them the RZ position is given"""

	strike_point  :AoS[PointRZ] =  sp_property(coordinate1="1...N")
	""" Array of strike points, for each of them the RZ position is given"""

	active_limiter_point  :PointRZ =  sp_property()
	""" RZ position of the active limiter point (point of the plasma boundary in contact
		with the limiter)"""


class _T_equilibrium_global_quantities(SpTree):
	"""0D parameters of the equilibrium"""

	beta_pol  :float =  sp_property(type="dynamic",units="-")
	""" Poloidal beta. Defined as betap = 4 int(p dV) / [R_0 * mu_0 * Ip^2]"""

	beta_tor  :float =  sp_property(type="dynamic",units="-")
	""" Toroidal beta, defined as the volume-averaged total perpendicular pressure
		divided by (B0^2/(2*mu0)), i.e. beta_toroidal = 2 mu0 int(p dV) / V / B0^2"""

	beta_normal  :float =  sp_property(type="dynamic",units="-")
	""" Normalised toroidal beta, defined as 100 * beta_tor * a[m] * B0 [T] / ip [MA]"""

	ip  :float =  sp_property(type="dynamic",units="A",cocos_label_transformation="ip_like",cocos_transformation_expression=".sigma_ip_eff",cocos_leaf_name_aos_indices="equilibrium.time_slice{i}.global_quantities.ip")
	""" Plasma current (toroidal component). Positive sign means anti-clockwise when
		viewed from above."""

	li_3  :float =  sp_property(type="dynamic",units="-")
	""" Internal inductance"""

	volume  :float =  sp_property(type="dynamic",units="m^3")
	""" Total plasma volume"""

	area  :float =  sp_property(type="dynamic",units="m^2")
	""" Area of the LCFS poloidal cross section"""

	surface  :float =  sp_property(type="dynamic",units="m^2")
	""" Surface area of the toroidal flux surface"""

	length_pol  :float =  sp_property(type="dynamic",units="m")
	""" Poloidal length of the magnetic surface"""

	psi_axis  :float =  sp_property(type="dynamic",units="Wb",cocos_label_transformation="psi_like",cocos_transformation_expression=".fact_psi",cocos_leaf_name_aos_indices="equilibrium.time_slice{i}.global_quantities.psi_axis")
	""" Poloidal flux at the magnetic axis"""

	psi_boundary  :float =  sp_property(type="dynamic",units="Wb",cocos_label_transformation="psi_like",cocos_transformation_expression=".fact_psi",cocos_leaf_name_aos_indices="equilibrium.time_slice{i}.global_quantities.psi_boundary")
	""" Poloidal flux at the selected plasma boundary"""

	magnetic_axis  :_T_equilibrium_global_quantities_magnetic_axis =  sp_property()
	""" Magnetic axis position and toroidal field"""

	current_centre  :_T_equilibrium_global_quantities_current_centre =  sp_property()
	""" Position and vertical velocity of the current centre"""

	q_axis  :float =  sp_property(type="dynamic",units="-",cocos_label_transformation="q_like",cocos_transformation_expression=".fact_q",cocos_leaf_name_aos_indices="equilibrium.time_slice{i}.global_quantities.q_axis")
	""" q at the magnetic axis"""

	q_95  :float =  sp_property(type="dynamic",units="-",cocos_label_transformation="q_like",cocos_transformation_expression=".fact_q",cocos_leaf_name_aos_indices="equilibrium.time_slice{i}.global_quantities.q_95")
	""" q at the 95% poloidal flux surface (IMAS uses COCOS=11: only positive when
		toroidal current and magnetic field are in same direction)"""

	q_min  :_T_equilibrium_global_quantities_qmin =  sp_property()
	""" Minimum q value and position"""

	energy_mhd  :float =  sp_property(type="dynamic",units="J")
	""" Plasma energy content = 3/2 * int(p,dV) with p being the total pressure (thermal
		+ fast particles) [J]. Time-dependent; Scalar"""

	psi_external_average  :float =  sp_property(type="dynamic",units="Wb",cocos_label_transformation="psi_like",cocos_transformation_expression=".fact_psi",cocos_leaf_name_aos_indices="equilibrium.time_slice{i}.global_quantities.psi_external_average")
	""" Average (over the plasma poloidal cross section) plasma poloidal magnetic flux
		produced by all external circuits (CS and PF coils, eddy currents, VS in-vessel
		coils), given by the following formula : int(psi_external.j_tor.dS) / Ip"""

	v_external  :float =  sp_property(type="dynamic",units="V",cocos_label_transformation="ip_like",cocos_transformation_expression=".sigma_ip_eff",cocos_leaf_name_aos_indices=["core_profiles.global_quantities.v_loop","equilibrium.time_slice{i}.global_quantities.v_external"],introduced_after_version="3.37.2")
	""" External voltage, i.e. time derivative of psi_external_average (with a minus
		sign : - d_psi_external_average/d_time)"""

	plasma_inductance  :float =  sp_property(type="dynamic",units="H")
	""" Plasma inductance 2 E_magnetic/Ip^2, where E_magnetic = 1/2 * int(psi.j_tor.dS)
		(integral over the plasma poloidal cross-section)"""

	plasma_resistance  :float =  sp_property(type="dynamic",units="ohm",introduced_after_version="3.37.2")
	""" Plasma resistance = int(e_field.j.dV) / Ip^2"""


class _T_equilibrium_constraints_pure_position(SpTree):
	"""R,Z position constraint"""

	position_measured  :PointRZ =  sp_property()
	""" Measured or estimated position"""

	source  :str =  sp_property(type="dynamic")
	""" Path to the source data for this measurement in the IMAS data dictionary"""

	time_measurement  :float =  sp_property(type="dynamic",units="s")
	""" Exact time slice used from the time array of the measurement source data. If the
		time slice does not exist in the time array of the source data, it means linear
		interpolation has been used"""

	exact  :int =  sp_property(type="dynamic")
	""" Integer flag : 1 means exact data, taken as an exact input without being fitted;
		0 means the equilibrium code does a least square fit"""

	weight  :float =  sp_property(type="dynamic",units="-")
	""" Weight given to the measurement"""

	position_reconstructed  :PointRZ =  sp_property()
	""" Position estimated from the reconstructed equilibrium"""

	chi_squared_r  :float =  sp_property(type="dynamic",units="m")
	""" Squared error on the major radius normalized by the standard deviation
		considered in the minimization process : chi_squared = weight^2
		*(position_reconstructed/r - position_measured/r)^2 / sigma^2, where sigma is
		the standard deviation of the measurement error"""

	chi_squared_z  :float =  sp_property(type="dynamic",units="m")
	""" Squared error on the altitude normalized by the standard deviation considered in
		the minimization process : chi_squared = weight^2 *(position_reconstructed/z -
		position_measured/z)^2 / sigma^2, where sigma is the standard deviation of the
		measurement error"""


class _T_equilibrium_constraints_0D_position(SpTree):
	"""Scalar constraint with R,Z,phi position"""

	measured  :float =  sp_property(type="dynamic",units="as_parent")
	""" Measured value"""

	position  :_T_rzphi0d_dynamic_aos3 =  sp_property()
	""" Position at which this measurement is given"""

	source  :str =  sp_property(type="dynamic")
	""" Path to the source data for this measurement in the IMAS data dictionary"""

	time_measurement  :float =  sp_property(type="dynamic",units="s")
	""" Exact time slice used from the time array of the measurement source data. If the
		time slice does not exist in the time array of the source data, it means linear
		interpolation has been used"""

	exact  :int =  sp_property(type="dynamic")
	""" Integer flag : 1 means exact data, taken as an exact input without being fitted;
		0 means the equilibrium code does a least square fit"""

	weight  :float =  sp_property(type="dynamic",units="-")
	""" Weight given to the measurement"""

	reconstructed  :float =  sp_property(type="dynamic",units="as_parent")
	""" Value calculated from the reconstructed equilibrium"""

	chi_squared  :float =  sp_property(type="dynamic",units="as_parent")
	""" Squared error normalized by the standard deviation considered in the
		minimization process : chi_squared = weight^2 *(reconstructed - measured)^2 /
		sigma^2, where sigma is the standard deviation of the measurement error"""


class _T_equilibrium_constraints_magnetisation(SpTree):
	"""Magnetisation constraints along R and Z axis"""

	magnetisation_r  :_T_equilibrium_constraints_0D =  sp_property(units="T")
	""" Magnetisation M of the iron core segment along the major radius axis, assumed to
		be constant inside a given iron segment. Reminder : H = 1/mu0 * B - mur * M;"""

	magnetisation_z  :_T_equilibrium_constraints_0D =  sp_property(units="T")
	""" Magnetisation M of the iron core segment along the vertical axis, assumed to be
		constant inside a given iron segment. Reminder : H = 1/mu0 * B - mur * M;"""


class _T_equilibrium_profiles_1d(SpTree):
	"""Equilibrium profiles (1D radial grid) as a function of the poloidal flux"""

	psi  :array_type =  sp_property(type="dynamic",coordinate1="1...N",units="Wb",cocos_label_transformation="psi_like",cocos_transformation_expression=".fact_psi",cocos_leaf_name_aos_indices="equilibrium.time_slice{i}.profiles_1d.psi")
	""" Poloidal flux"""

	phi  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="Wb",cocos_label_transformation="b0_like",cocos_transformation_expression=".sigma_b0_eff",cocos_leaf_name_aos_indices="equilibrium.time_slice{i}.profiles_1d.phi")
	""" Toroidal flux"""

	pressure  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="Pa")
	""" Pressure"""

	f  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="T.m",cocos_label_transformation="b0_like",cocos_transformation_expression=".sigma_b0_eff",cocos_leaf_name_aos_indices="equilibrium.time_slice{i}.profiles_1d.f")
	""" Diamagnetic function (F=R B_Phi)"""

	dpressure_dpsi  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="Pa.Wb^-1",cocos_label_transformation="dodpsi_like",cocos_transformation_expression=".fact_dodpsi",cocos_leaf_name_aos_indices="equilibrium.time_slice{i}.profiles_1d.dpressure_dpsi")
	""" Derivative of pressure w.r.t. psi"""

	f_df_dpsi  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="T^2.m^2/Wb",cocos_label_transformation="dodpsi_like",cocos_transformation_expression=".fact_dodpsi",cocos_leaf_name_aos_indices="equilibrium.time_slice{i}.profiles_1d.f_df_dpsi")
	""" Derivative of F w.r.t. Psi, multiplied with F"""

	j_tor  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="A.m^-2",cocos_label_transformation="ip_like",cocos_transformation_expression=".sigma_ip_eff",cocos_leaf_name_aos_indices="equilibrium.time_slice{i}.profiles_1d.j_tor")
	""" Flux surface averaged toroidal current density = average(j_tor/R) / average(1/R)"""

	j_parallel  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="A/m^2",cocos_label_transformation="ip_like",cocos_transformation_expression=".sigma_ip_eff",cocos_leaf_name_aos_indices="equilibrium.time_slice{i}.profiles_1d.j_parallel")
	""" Flux surface averaged parallel current density = average(j.B) / B0, where B0 =
		Equilibrium/Global/Toroidal_Field/B0"""

	q  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="-",cocos_label_transformation="q_like",cocos_transformation_expression=".fact_q",cocos_leaf_name_aos_indices="equilibrium.time_slice{i}.profiles_1d.q")
	""" Safety factor (IMAS uses COCOS=11: only positive when toroidal current and
		magnetic field are in same direction)"""

	magnetic_shear  :Expression  =  sp_property(coordinate1="../psi",units="-",type="dynamic")
	""" Magnetic shear, defined as rho_tor/q . dq/drho_tor"""

	r_inboard  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="m")
	""" Radial coordinate (major radius) on the inboard side of the magnetic axis"""

	r_outboard  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="m")
	""" Radial coordinate (major radius) on the outboard side of the magnetic axis"""

	rho_tor  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="m")
	""" Toroidal flux coordinate = sqrt(phi/(pi*b0)), where the toroidal flux, phi,
		corresponds to time_slice/profiles_1d/phi, the toroidal magnetic field, b0,
		corresponds to vacuum_toroidal_field/b0 and pi can be found in the IMAS
		constants"""

	rho_tor_norm  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="-")
	""" Normalised toroidal flux coordinate. The normalizing value for rho_tor_norm, is
		the toroidal flux coordinate at the equilibrium boundary (LCFS or 99.x % of the
		LCFS in case of a fixed boundary equilibium calculation)"""

	dpsi_drho_tor  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="Wb/m",cocos_label_transformation="psi_like",cocos_transformation_expression=".fact_psi",cocos_leaf_name_aos_indices="equilibrium.time_slice{i}.profiles_1d.dpsi_drho_tor")
	""" Derivative of Psi with respect to Rho_Tor"""

	geometric_axis  :_T_equilibrium_profiles_1d_rz1d_dynamic_aos =  sp_property()
	""" RZ position of the geometric axis of the magnetic surfaces (defined as
		(Rmin+Rmax) / 2 and (Zmin+Zmax) / 2 of the surface)"""

	elongation  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="-",url="equilibrium/DefinitionEqBoundary.svg")
	""" Elongation"""

	triangularity_upper  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="-",url="equilibrium/DefinitionEqBoundary.svg")
	""" Upper triangularity w.r.t. magnetic axis"""

	triangularity_lower  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="-",url="equilibrium/DefinitionEqBoundary.svg")
	""" Lower triangularity w.r.t. magnetic axis"""

	squareness_upper_inner  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="-",lifecycle_status="alpha",lifecycle_version="3.18.0")
	""" Upper inner squareness (definition from T. Luce, Plasma Phys. Control. Fusion 55
		(2013) 095009)"""

	squareness_upper_outer  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="-",lifecycle_status="alpha",lifecycle_version="3.18.0")
	""" Upper outer squareness (definition from T. Luce, Plasma Phys. Control. Fusion 55
		(2013) 095009)"""

	squareness_lower_inner  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="-",lifecycle_status="alpha",lifecycle_version="3.18.0")
	""" Lower inner squareness (definition from T. Luce, Plasma Phys. Control. Fusion 55
		(2013) 095009)"""

	squareness_lower_outer  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="-",lifecycle_status="alpha",lifecycle_version="3.18.0")
	""" Lower outer squareness (definition from T. Luce, Plasma Phys. Control. Fusion 55
		(2013) 095009)"""

	volume  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="m^3")
	""" Volume enclosed in the flux surface"""

	rho_volume_norm  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="-")
	""" Normalised square root of enclosed volume (radial coordinate). The normalizing
		value is the enclosed volume at the equilibrium boundary (LCFS or 99.x % of the
		LCFS in case of a fixed boundary equilibium calculation)"""

	dvolume_dpsi  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="m^3.Wb^-1",cocos_label_transformation="dodpsi_like",cocos_transformation_expression=".fact_dodpsi",cocos_leaf_name_aos_indices="equilibrium.time_slice{i}.profiles_1d.dvolume_dpsi")
	""" Radial derivative of the volume enclosed in the flux surface with respect to Psi"""

	dvolume_drho_tor  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="m^2")
	""" Radial derivative of the volume enclosed in the flux surface with respect to
		Rho_Tor"""

	area  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="m^2")
	""" Cross-sectional area of the flux surface"""

	darea_dpsi  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="m^2.Wb^-1",cocos_label_transformation="dodpsi_like",cocos_transformation_expression=".fact_dodpsi",cocos_leaf_name_aos_indices="equilibrium.time_slice{i}.profiles_1d.darea_dpsi")
	""" Radial derivative of the cross-sectional area of the flux surface with respect
		to psi"""

	darea_drho_tor  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="m")
	""" Radial derivative of the cross-sectional area of the flux surface with respect
		to rho_tor"""

	surface  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="m^2")
	""" Surface area of the toroidal flux surface"""

	trapped_fraction  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="-")
	""" Trapped particle fraction"""

	gm1  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="m^-2")
	""" Flux surface averaged 1/R^2"""

	gm2  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="m^-2")
	""" Flux surface averaged |grad_rho_tor|^2/R^2"""

	gm3  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="-")
	""" Flux surface averaged |grad_rho_tor|^2"""

	gm4  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="T^-2")
	""" Flux surface averaged 1/B^2"""

	gm5  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="T^2")
	""" Flux surface averaged B^2"""

	gm6  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="T^-2")
	""" Flux surface averaged |grad_rho_tor|^2/B^2"""

	gm7  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="-")
	""" Flux surface averaged |grad_rho_tor|"""

	gm8  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="m")
	""" Flux surface averaged R"""

	gm9  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="m^-1")
	""" Flux surface averaged 1/R"""

	b_field_average  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="T")
	""" Flux surface averaged modulus of B (always positive, irrespective of the sign
		convention for the B-field direction)."""

	b_field_min  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="T")
	""" Minimum(modulus(B)) on the flux surface (always positive, irrespective of the
		sign convention for the B-field direction)"""

	b_field_max  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="T")
	""" Maximum(modulus(B)) on the flux surface (always positive, irrespective of the
		sign convention for the B-field direction)"""

	beta_pol  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="-")
	""" Poloidal beta profile. Defined as betap = 4 int(p dV) / [R_0 * mu_0 * Ip^2]"""

	mass_density  :Expression  =  sp_property(type="dynamic",coordinate1="../psi",units="kg.m^-3")
	""" Mass density"""


class _T_equilibrium_profiles_2d(SpTree):
	"""Equilibrium 2D profiles in the poloidal plane"""

	type  :_E_equilibrium_profiles_2d_identifier =  sp_property(doc_identifier="equilibrium/equilibrium_profiles_2d_identifier.xml",introduced_after_version="3.37.2")
	""" Type of profiles (distinguishes contribution from plasma, vaccum fields and
		total fields)"""

	grid_type  :_E_poloidal_plane_coordinates_identifier =  sp_property(doc_identifier="utilities/poloidal_plane_coordinates_identifier.xml")
	""" Selection of one of a set of grid types"""

	grid  :_T_equilibrium_profiles_2d_grid =  sp_property(cocos_alias="IDSPATH",cocos_replace="equilibrium.time_slice{i}.profiles_2d{j}")
	""" Definition of the 2D grid (the content of dim1 and dim2 is defined by the
		selected grid_type)"""

	r  :Field =  sp_property(type="dynamic",coordinate1="../grid/dim1",coordinate2="../grid/dim2",units="m")
	""" Values of the major radius on the grid"""

	z  :Field =  sp_property(type="dynamic",coordinate1="../grid/dim1",coordinate2="../grid/dim2",units="m")
	""" Values of the Height on the grid"""

	psi  :Field =  sp_property(type="dynamic",coordinate1="../grid/dim1",coordinate2="../grid/dim2",units="Wb",cocos_label_transformation="psi_like",cocos_transformation_expression=".fact_psi",cocos_leaf_name_aos_indices="equilibrium.time_slice{i}.profiles_2d{j}.psi")
	""" Values of the poloidal flux at the grid in the poloidal plane"""

	theta  :Field =  sp_property(type="dynamic",coordinate1="../grid/dim1",coordinate2="../grid/dim2",units="rad")
	""" Values of the poloidal angle on the grid"""

	phi  :Field =  sp_property(type="dynamic",coordinate1="../grid/dim1",coordinate2="../grid/dim2",units="Wb",cocos_label_transformation="b0_like",cocos_transformation_expression=".sigma_b0_eff",cocos_leaf_name_aos_indices="equilibrium.time_slice{i}.profiles_2d{j}.phi")
	""" Toroidal flux"""

	j_tor  :Field =  sp_property(type="dynamic",coordinate1="../grid/dim1",coordinate2="../grid/dim2",units="A.m^-2",cocos_label_transformation="ip_like",cocos_transformation_expression=".sigma_ip_eff",cocos_leaf_name_aos_indices="equilibrium.time_slice{i}.profiles_2d{j}.j_tor")
	""" Toroidal plasma current density"""

	j_parallel  :Field =  sp_property(type="dynamic",coordinate1="../grid/dim1",coordinate2="../grid/dim2",units="A.m^-2",cocos_label_transformation="ip_like",cocos_transformation_expression=".sigma_ip_eff",cocos_leaf_name_aos_indices="equilibrium.time_slice{i}.profiles_2d{j}.j_parallel")
	""" Defined as (j.B)/B0 where j and B are the current density and magnetic field
		vectors and B0 is the (signed) vacuum toroidal magnetic field strength at the
		geometric reference point (R0,Z0). It is formally not the component of the
		plasma current density parallel to the magnetic field"""

	b_field_r  :Field =  sp_property(type="dynamic",coordinate1="../grid/dim1",coordinate2="../grid/dim2",units="T")
	""" R component of the poloidal magnetic field"""

	b_field_z  :Field =  sp_property(type="dynamic",coordinate1="../grid/dim1",coordinate2="../grid/dim2",units="T")
	""" Z component of the poloidal magnetic field"""

	b_field_tor  :Field =  sp_property(type="dynamic",coordinate1="../grid/dim1",coordinate2="../grid/dim2",units="T",cocos_label_transformation="b0_like",cocos_transformation_expression=".sigma_b0_eff",cocos_leaf_name_aos_indices="equilibrium.time_slice{i}.profiles_2d{j}.b_field_tor")
	""" Toroidal component of the magnetic field"""


class _T_equilibrium_ggd(SpTree):
	"""Equilibrium ggd representation"""

	r  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="m")
	""" Values of the major radius on various grid subsets"""

	z  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="m")
	""" Values of the Height on various grid subsets"""

	psi  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="Wb")
	""" Values of the poloidal flux, given on various grid subsets"""

	phi  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="Wb")
	""" Values of the toroidal flux, given on various grid subsets"""

	theta  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="rad")
	""" Values of the poloidal angle, given on various grid subsets"""

	j_tor  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="A.m^-2")
	""" Toroidal plasma current density, given on various grid subsets"""

	j_parallel  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="A.m^-2")
	""" Parallel (to magnetic field) plasma current density, given on various grid
		subsets"""

	b_field_r  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="T")
	""" R component of the poloidal magnetic field, given on various grid subsets"""

	b_field_z  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="T")
	""" Z component of the poloidal magnetic field, given on various grid subsets"""

	b_field_tor  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="T")
	""" Toroidal component of the magnetic field, given on various grid subsets"""


class _T_equilibrium_ggd_array(TimeSlice):
	"""Multiple GGDs provided at a given time slice"""

	grid  :AoS[_T_generic_grid_dynamic] =  sp_property(coordinate1="1...N")
	""" Set of GGD grids for describing the equilibrium, at a given time slice"""


class _T_equilibrium_constraints(SpTree):
	"""Measurements to constrain the equilibrium, output values and accuracy of the fit"""

	b_field_tor_vacuum_r  :_T_equilibrium_constraints_0D =  sp_property(units="T.m")
	""" Vacuum field times major radius in the toroidal field magnet. Positive sign
		means anti-clockwise when viewed from above"""

	bpol_probe  :AoS[_T_equilibrium_constraints_0D_one_like] =  sp_property(coordinate1="IDS:magnetics/bpol_probe",units="T",cocos_alias="IDSPATH",cocos_replace="equilibrium.time_slice{i}.constraints.bpol_probe{j}")
	""" Set of poloidal field probes"""

	diamagnetic_flux  :_T_equilibrium_constraints_0D_b0_like =  sp_property(units="Wb",cocos_alias="IDSPATH",cocos_replace="equilibrium.time_slice{i}.constraints.diamagnetic_flux")
	""" Diamagnetic flux"""

	faraday_angle  :AoS[_T_equilibrium_constraints_0D] =  sp_property(coordinate1="IDS:polarimeter/channel",units="rad")
	""" Set of faraday angles"""

	mse_polarisation_angle  :AoS[_T_equilibrium_constraints_0D] =  sp_property(coordinate1="IDS:mse/channel",units="rad")
	""" Set of MSE polarisation angles"""

	flux_loop  :AoS[_T_equilibrium_constraints_0D_psi_like] =  sp_property(coordinate1="IDS:magnetics/flux_loop",units="Wb",cocos_alias="IDSPATH",cocos_replace="equilibrium.time_slice{i}.constraints.flux_loop{j}")
	""" Set of flux loops"""

	ip  :_T_equilibrium_constraints_0D_ip_like =  sp_property(units="A",cocos_alias="IDSPATH",cocos_replace="equilibrium.time_slice{i}.constraints.ip")
	""" Plasma current. Positive sign means anti-clockwise when viewed from above"""

	iron_core_segment  :AoS[_T_equilibrium_constraints_magnetisation] =  sp_property(coordinate1="IDS:iron_core/segment",units="T")
	""" Magnetisation M of a set of iron core segments"""

	n_e  :AoS[_T_equilibrium_constraints_0D] =  sp_property(coordinate1="1...N",units="m^-3")
	""" Set of local density measurements"""

	n_e_line  :AoS[_T_equilibrium_constraints_0D] =  sp_property(coordinate1="IDS:interferometer/channel",units="m^-2")
	""" Set of line integrated density measurements"""

	pf_current  :AoS[_T_equilibrium_constraints_0D_ip_like] =  sp_property(coordinate1="IDS:pf_active/coil",units="A",cocos_alias="IDSPATH",cocos_replace="equilibrium.time_slice{i}.constraints.pf_current{j}")
	""" Current in a set of poloidal field coils"""

	pf_passive_current  :AoS[_T_equilibrium_constraints_0D] =  sp_property(coordinate1="IDS:pf_passive/loop",units="A")
	""" Current in a set of axisymmetric passive conductors"""

	pressure  :AoS[_T_equilibrium_constraints_0D] =  sp_property(coordinate1="1...N",units="Pa")
	""" Set of total pressure estimates"""

	q  :AoS[_T_equilibrium_constraints_0D_position] =  sp_property(coordinate1="1...N",units="-")
	""" Set of safety factor estimates at various positions"""

	x_point  :AoS[_T_equilibrium_constraints_pure_position] =  sp_property(coordinate1="1...N")
	""" Array of X-points, for each of them the RZ position is given"""

	strike_point  :AoS[_T_equilibrium_constraints_pure_position] =  sp_property(coordinate1="1...N")
	""" Array of strike points, for each of them the RZ position is given"""


class _T_equilibrium_time_slice(TimeSlice):
	"""Equilibrium at a given time slice
	type: dynamic"""

	boundary  :_T_equilibrium_boundary =  sp_property()
	""" Description of the plasma boundary used by fixed-boundary codes and typically
		chosen at psi_norm = 99.x% of the separatrix"""

	boundary_separatrix  :_T_equilibrium_boundary_separatrix =  sp_property()
	""" Description of the plasma boundary at the separatrix"""

	boundary_secondary_separatrix  :_T_equilibrium_boundary_second_separatrix =  sp_property()
	""" Geometry of the secondary separatrix, defined as the outer flux surface with an
		X-point"""

	constraints  :_T_equilibrium_constraints =  sp_property(lifecycle_status="alpha",lifecycle_version="3.17.0")
	""" In case of equilibrium reconstruction under constraints, measurements used to
		constrain the equilibrium, reconstructed values and accuracy of the fit. The
		names of the child nodes correspond to the following definition: the solver aims
		at minimizing a cost function defined as : J=1/2*sum_i [ weight_i^2
		(reconstructed_i - measured_i)^2 / sigma_i^2 ]. in which sigma_i is the standard
		deviation of the measurement error (to be found in the IDS of the measurement)"""

	global_quantities  :_T_equilibrium_global_quantities =  sp_property()
	""" 0D parameters of the equilibrium"""

	profiles_1d  :_T_equilibrium_profiles_1d =  sp_property()
	""" Equilibrium profiles (1D radial grid) as a function of the poloidal flux"""

	profiles_2d  :AoS[_T_equilibrium_profiles_2d] =  sp_property(coordinate1="1...N")
	""" Equilibrium 2D profiles in the poloidal plane. Multiple 2D representations of
		the equilibrium can be stored here."""

	ggd  :AoS[_T_equilibrium_ggd] =  sp_property(lifecycle_status="alpha",lifecycle_version="3.2.1",coordinate1="../../grids_ggd(itime)/grid")
	""" Set of equilibrium representations using the generic grid description"""

	coordinate_system  :_T_equilibrium_coordinate_system =  sp_property(cocos_alias="IDSPATH",cocos_replace="equilibrium.time_slice{i}.coordinate_system")
	""" Flux surface coordinate system on a square grid of flux and poloidal angle"""

	convergence  :_T_equilibrium_convergence =  sp_property()
	""" Convergence details"""


class _T_equilibrium(IDS):
	"""Description of a 2D, axi-symmetric, tokamak equilibrium; result of an
		equilibrium code.
	lifecycle_status: active
	lifecycle_version: 3.1.0
	lifecycle_last_change: 3.38.0"""

	dd_version="v3_38_1_dirty"
	ids_name="equilibrium"

	vacuum_toroidal_field  :_T_b_tor_vacuum_1 =  sp_property(cocos_alias="IDSPATH",cocos_replace="equilibrium.vacuum_toroidal_field")
	""" Characteristics of the vacuum toroidal field (used in rho_tor definition and in
		the normalization of current densities)"""

	grids_ggd  :TimeSeriesAoS[_T_equilibrium_ggd_array] =  sp_property(coordinate1="time",type="dynamic",lifecycle_status="alpha",lifecycle_version="3.18.0")
	""" Grids (using the Generic Grid Description), for various time slices. The
		timebase of this array of structure must be a subset of the time_slice timebase"""

	time_slice  :TimeSeriesAoS[_T_equilibrium_time_slice] =  sp_property(coordinate1="time",type="dynamic")
	""" Set of equilibria at various time slices"""
