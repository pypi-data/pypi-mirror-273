""" 
    This module containes the _FyTok_ wrapper of IMAS/dd/utilities 

  
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 

"""
    
from enum import IntFlag
import numpy as np
from spdm.core.HTree         import List
from spdm.core.AoS           import AoS
from spdm.core.TimeSeries    import TimeSeriesAoS,TimeSlice
from spdm.core.Signal        import Signal,SignalND
from spdm.core.Function      import Function 
from spdm.core.Expression    import Expression 
from spdm.core.Field         import Field
from spdm.core.sp_property   import sp_property,SpTree
from spdm.utils.typing import array_type

    

class _E_neutrals_identifier(IntFlag):
	"""Translation table for identifying different types of neutral. The neutrals are
		characterised by their energy and source of the neutrals.	xpath: 	"""
  
	cold = 1
	"""Cold neutrals"""
  
	thermal = 2
	"""Thermal neutrals"""
  
	fast = 3
	"""Fast neutrals"""
  
	nbi = 4
	"""NBI neutrals"""
  

class _E_neutrals_identifier(IntFlag):
	"""Translation table for identifying different types of neutral. The neutrals are
		characterised by their energy and source of the neutrals.	xpath: 	"""
  
	cold = 1
	"""Cold neutrals"""
  
	thermal = 2
	"""Thermal neutrals"""
  
	fast = 3
	"""Fast neutrals"""
  
	nbi = 4
	"""NBI neutrals"""
  

class _E_coordinate(IntFlag):
	"""Translation table for coordinate_identifier_definitions.	xpath: 	"""
  
	unspecified = 0
	"""unspecified"""
  
	x = 1
	"""First cartesian coordinate in the horizontal plane"""
  
	y = 2
	"""Second cartesian coordinate in the horizontal plane (grad(x) x grad(y) =
		grad(z))"""
  
	z = 3
	"""Vertical coordinate z"""
  
	r = 4
	"""Major radius"""
  
	phi = 5
	"""Toroidal angle"""
  
	psi = 10
	"""Poloidal magnetic flux"""
  
	rho_tor = 11
	"""The square root of the toroidal flux, sqrt((Phi-Phi_axis)/pi/B0), where Phi is
		the toroidal flux and B0 is the vaccum magnetic field"""
  
	rho_tor_norm = 12
	"""The square root of the normalised toroidal flux,
		sqrt((Phi-Phi_axis)/(Phi_lcf-Phi_axis)), where Phi is the toroidal flux"""
  
	rho_pol = 13
	"""The square root of the poloidal flux, sqrt(psi-psi_axis), where psi is the
		poloidal flux"""
  
	rho_pol_norm = 14
	"""The square root of the normalised poloidal flux,
		sqrt((psi-psi_axis)/(psi_lcf-psi_axis)), where psi is the poloidal flux"""
  
	theta = 20
	"""Geometrical poloidal angle around the magnetic axis"""
  
	theta_straight = 21
	"""Straight field line poloidal angle"""
  
	theta_equal_arc = 22
	"""Equal-arc poloidal angle; a differential of the angle is proportional to the
		length of the corresponding arc in the poloidal plane."""
  
	velocity = 100
	"""Total velocity; modulus of the velocity vector"""
  
	velocity_x = 101
	"""Velocity component in the x-direction"""
  
	velocity_y = 102
	"""Velocity component in the y-direction"""
  
	velocity_z = 103
	"""Velocity component in the z-direction"""
  
	velocity_phi = 104
	"""Velocity component in the toroidal direction"""
  
	velocity_parallel = 105
	"""Velocity component parallel to the magnetic field"""
  
	velocity_perpendicular = 106
	"""Velocity perpendicular to the magnetic field"""
  
	velocity_thermal = 107
	"""Velocity normalised to the local thermal velocity of the thermal ions (of the
		relevant species)"""
  
	velocity_radial = 108
	"""Velocity component in the radial direction"""
  
	momentum = 200
	"""Modulus of the relativistic momentum vector"""
  
	momentum_parallel = 201
	"""Component of the relativistic momentum vector parallel to the magnetic field"""
  
	momentum_perpendicular = 202
	"""Component of the relativistic momentum vector perpendicular to the magnetic
		field"""
  
	canonical_momentum_phi = 203
	"""Canonical toroidal angular momentum"""
  
	energy_hamiltonian = 300
	"""Hamiltonian energy, including both kinetic and potential energy"""
  
	energy_kinetic = 301
	"""Kinetic energy"""
  
	magnetic_moment = 302
	"""magnetic moment"""
  
	lambda_ = 400
	"""Ratio, magnetic moment over hamiltonian energy"""
  
	pitch_angle = 402
	"""Angle between the magnetic field and the velocity vector"""
  
	pitch = 403
	"""Ratio, parallel velocity over total velocity"""
  
	pitch_at_min_b = 404
	"""Pitch, ratio between the parallel over the perpendicular velocity, at the
		minimum value of the magnetic field strength along the guiding centre orbit"""
  

class _E_species_identifier(IntFlag):
	"""Translation table for species_reference_identifier_definition.	xpath: 	"""
  
	unspecified = 0
	"""unspecified"""
  
	electron = 1
	"""Electron"""
  
	ion = 2
	"""Ion species in a single/average state; refer to ion-structure"""
  
	ion_state = 3
	"""Ion species in a particular state; refer to ion/state-structure"""
  
	neutral = 4
	"""Neutral species in a single/average state; refer to neutral-structure"""
  
	neutral_state = 5
	"""Neutral species in a particular state; refer to neutral/state-structure"""
  
	neutron = 6
	"""Neutron"""
  
	photon = 7
	"""Photon"""
  

class _E_distribution_source_identifier(IntFlag):
	"""Translation table for Heating and Current Drive (HCD) distsource types, i.e.
		types particles source in Fokker-Planck equation (from NBI and nuclear
		reactions).	xpath: 	"""
  
	unspecified = 0
	"""unspecified"""
  
	NBI = 1
	"""Source from neutral beam injection"""
  
	nuclear = 100
	"""Source from nuclear reaction (reaction type unspecified)"""
  
	H_H_to_D_positron_nu = 101
	"""Source from nuclear reaction: H+H->D+positron+neutrino"""
  
	H_D_to_He3_gamma = 102
	"""Source from nuclear reaction: H+D->He3+gamma"""
  
	H_T_to_He3_n = 103
	"""Source from nuclear reaction: H+T->He3+neutron"""
  
	H_He3_to_He4_positron_nu = 104
	"""Source from nuclear reaction: H+He3->He4+positron+neutrino"""
  
	D_D_to_T_H = 105
	"""Source from nuclear reaction: D+D->T+H"""
  
	D_D_to_He3_n = 106
	"""Source from nuclear reaction: D+D->He3+neutron"""
  
	D_T_to_He4_n = 107
	"""Source from nuclear reaction: T+D->He4+neutron"""
  
	D_He3_to_He4_H = 108
	"""Source from nuclear reaction: He3+D->He4+H"""
  
	T_T_to_He4_n_n = 109
	"""Source from nuclear reaction: T+T->He4+neutron+neutron"""
  
	T_He3_to_He4_H_n = 110
	"""Source from nuclear reaction: He3+T->He4+H+neutron"""
  
	He3_He3_to_He4_H_H = 111
	"""Source from nuclear reaction: He3+He3->He4+neutron+neutron"""
  
	He3_He4_to_Be7_gamma = 112
	"""Source from nuclear reaction: He3+He4->Be7+gamma"""
  
	Li6_n_to_He4_T = 113
	"""Source from nuclear reaction: Li6+n->He4+T"""
  
	Li7_n_to_He4_T_n = 114
	"""Source from nuclear reaction: Li7+n->He4+T+n"""
  
	runaway = 1000
	"""Source from runaway processes"""
  

class _E_ggd_space_identifier(IntFlag):
	"""Translation table for ggd_space_identifier_definitions.	xpath: 	"""
  
	unspecified = 0
	"""unspecified"""
  
	node_coordinates = 1
	"""For nodes : node coordinates"""
  
	node_coordinates_connection = 11
	"""For nodes : node coordinates, then connection length, and distance in the
		poloidal plane to the nearest solid surface outside the separatrix"""
  
	edge_areas = 21
	"""For edges : contains 3 surface areas after uniform extension in the third
		dimension of the edges. Geometry(1) and geometry(2) are the projections of that
		area along the local poloidal and radial coordinate respectively. Geometry(3) is
		the full surface area of the extended edge"""
  
	face_indices_volume = 31
	"""For faces : coordinates indices (ix, iy) of the face within the structured grid
		of the code. The third element contains the volume after uniform extension in
		the third dimension of the faces"""
  
	face_indices_volume_connection = 32
	"""For faces : coordinates indices (ix, iy) of the face within the structured grid
		of the code. The third element contains the volume after uniform extension in
		the third dimension of the faces. The fourth element is the connection length.
		The fifth element is the distance in the poloidal plane to the nearest solid
		surface outside the separatrix"""
  

class _E_ggd_space_identifier(IntFlag):
	"""Translation table for ggd_space_identifier_definitions.	xpath: 	"""
  
	unspecified = 0
	"""unspecified"""
  
	primary_standard = 1
	"""Primary space defining the standard grid"""
  
	primary_staggered = 2
	"""Primary space defining a grid staggered with respect to the primary standard
		space"""
  
	secondary_structured = 3
	"""Secondary space defining additional dimensions that extend the primary standard
		space in a structured way"""
  

class _E_coordinate(IntFlag):
	"""Translation table for coordinate_identifier_definitions.	xpath: 	"""
  
	unspecified = 0
	"""unspecified"""
  
	x = 1
	"""First cartesian coordinate in the horizontal plane"""
  
	y = 2
	"""Second cartesian coordinate in the horizontal plane (grad(x) x grad(y) =
		grad(z))"""
  
	z = 3
	"""Vertical coordinate z"""
  
	r = 4
	"""Major radius"""
  
	phi = 5
	"""Toroidal angle"""
  
	psi = 10
	"""Poloidal magnetic flux"""
  
	rho_tor = 11
	"""The square root of the toroidal flux, sqrt((Phi-Phi_axis)/pi/B0), where Phi is
		the toroidal flux and B0 is the vaccum magnetic field"""
  
	rho_tor_norm = 12
	"""The square root of the normalised toroidal flux,
		sqrt((Phi-Phi_axis)/(Phi_lcf-Phi_axis)), where Phi is the toroidal flux"""
  
	rho_pol = 13
	"""The square root of the poloidal flux, sqrt(psi-psi_axis), where psi is the
		poloidal flux"""
  
	rho_pol_norm = 14
	"""The square root of the normalised poloidal flux,
		sqrt((psi-psi_axis)/(psi_lcf-psi_axis)), where psi is the poloidal flux"""
  
	theta = 20
	"""Geometrical poloidal angle around the magnetic axis"""
  
	theta_straight = 21
	"""Straight field line poloidal angle"""
  
	theta_equal_arc = 22
	"""Equal-arc poloidal angle; a differential of the angle is proportional to the
		length of the corresponding arc in the poloidal plane."""
  
	velocity = 100
	"""Total velocity; modulus of the velocity vector"""
  
	velocity_x = 101
	"""Velocity component in the x-direction"""
  
	velocity_y = 102
	"""Velocity component in the y-direction"""
  
	velocity_z = 103
	"""Velocity component in the z-direction"""
  
	velocity_phi = 104
	"""Velocity component in the toroidal direction"""
  
	velocity_parallel = 105
	"""Velocity component parallel to the magnetic field"""
  
	velocity_perpendicular = 106
	"""Velocity perpendicular to the magnetic field"""
  
	velocity_thermal = 107
	"""Velocity normalised to the local thermal velocity of the thermal ions (of the
		relevant species)"""
  
	velocity_radial = 108
	"""Velocity component in the radial direction"""
  
	momentum = 200
	"""Modulus of the relativistic momentum vector"""
  
	momentum_parallel = 201
	"""Component of the relativistic momentum vector parallel to the magnetic field"""
  
	momentum_perpendicular = 202
	"""Component of the relativistic momentum vector perpendicular to the magnetic
		field"""
  
	canonical_momentum_phi = 203
	"""Canonical toroidal angular momentum"""
  
	energy_hamiltonian = 300
	"""Hamiltonian energy, including both kinetic and potential energy"""
  
	energy_kinetic = 301
	"""Kinetic energy"""
  
	magnetic_moment = 302
	"""magnetic moment"""
  
	lambda_ = 400
	"""Ratio, magnetic moment over hamiltonian energy"""
  
	pitch_angle = 402
	"""Angle between the magnetic field and the velocity vector"""
  
	pitch = 403
	"""Ratio, parallel velocity over total velocity"""
  
	pitch_at_min_b = 404
	"""Pitch, ratio between the parallel over the perpendicular velocity, at the
		minimum value of the magnetic field strength along the guiding centre orbit"""
  

class _E_ggd_subset_identifier(IntFlag):
	"""Translation table for ggd_subset_identifier_definitions.	xpath: 	"""
  
	unspecified = 0
	"""unspecified"""
  
	nodes = 1
	"""All nodes (0D) belonging to the associated spaces, implicit declaration (no need
		to replicate the grid elements in the grid_subset structure). In case of a
		structured grid represented with multiple 1D spaces, the order of the implicit
		elements in the grid_subset follows Fortran ordering, i.e. iterate always on
		nodes of the first space first, then move to the second node of the second
		space, ... : [((s1_1 to s1_end), s2_1, s3_1 ... sN_1), (((s1_1 to s1_end), s2_2,
		s3_1, ... sN_1)), ... ((s1_1 to s1_end), s2_end, s3_end ... sN_end)]"""
  
	nodes_combining_spaces = 200
	"""All nodes (0D) belonging to the first space, implicitly extended in other
		dimensions represented by the other spaces in a structured way. The number of
		subset elements is thus equal to the number of nodes in the first space.
		Implicit declaration (no need to replicate the grid elements in the grid_subset
		structure)."""
  
	edges = 2
	"""All edges (1D) belonging to the associated spaces, implicit declaration (no need
		to replicate the grid elements in the grid_subset structure)"""
  
	x_aligned_edges = 3
	"""All x-aligned (poloidally) aligned edges belonging to the associated spaces"""
  
	y_aligned_edges = 4
	"""All y-aligned (radially) aligned edges belonging to the associated spaces"""
  
	cells = 5
	"""All cells (2D) belonging to the associated spaces, implicit declaration (no need
		to replicate the grid elements in the grid_subset structure)"""
  
	x_points = 6
	"""Nodes defining x-points"""
  
	core_cut = 7
	"""y-aligned edges inside the separatrix connecting to the active x-point"""
  
	PFR_cut = 8
	"""y-aligned edges in the private flux region connecting to the active x-point"""
  
	outer_throat = 9
	"""y-aligned edges in the outer SOL connecting to the active x-point"""
  
	inner_throat = 10
	"""y-aligned edges in the inner SOL connecting to the active x-point"""
  
	outer_midplane = 11
	"""y-aligned edges connecting to the node closest to outer midplane on the
		separatrix"""
  
	inner_midplane = 12
	"""y-aligned edges connecting to the node closest to inner midplane on the
		separatrix"""
  
	outer_target = 13
	"""y-aligned edges defining the outer target"""
  
	inner_target = 14
	"""y-aligned edges defining the inner target"""
  
	core_boundary = 15
	"""Innermost x-aligned edges"""
  
	separatrix = 16
	"""x-aligned edges defining the active separatrix"""
  
	main_chamber_wall = 17
	"""x-aligned edges defining main chamber wall outside of the divertor regions"""
  
	outer_baffle = 18
	"""x-aligned edges defining the chamber wall of the outer active divertor region"""
  
	inner_baffle = 19
	"""x-aligned edges defining the chamber wall of the inner active divertor region"""
  
	outer_PFR_wall = 20
	"""x-aligned edges defining the private flux region wall of the outer active
		divertor region"""
  
	inner_PFR_wall = 21
	"""x-aligned edges defining the private flux region wall of the inner active
		divertor region"""
  
	core = 22
	"""Cells inside the active separatrix"""
  
	sol = 23
	"""Cells defining the main SOL outside of the divertor regions"""
  
	outer_divertor = 24
	"""Cells defining the outer divertor region"""
  
	inner_divertor = 25
	"""Cells defining the inner divertor region"""
  
	core_sol = 26
	"""x-aligned edges defining part of active separatrix separating core and sol"""
  
	full_main_chamber_wall = 27
	"""main_chamber_wall + outer_baffle(s) + inner_baffle(s)"""
  
	full_PFR_wall = 28
	"""outer_PFR__wall(s) + inner_PFR_wall(s)"""
  
	core_cut_X2 = 29
	"""y-aligned edges inside the separatrix connecting to the non-active x-point"""
  
	PFR_cut_X2 = 30
	"""y-aligned edges in the private flux region connecting to the non-active x-point"""
  
	outer_throat_X2 = 31
	"""y-aligned edges in the outer SOL connecting to the non-active x-point"""
  
	inner_throat_X2 = 32
	"""y-aligned edges in the inner SOL connecting to the non-active x-point"""
  
	separatrix_2 = 33
	"""x-aligned edges defining the non-active separatrix"""
  
	outer_baffle_2 = 34
	"""x-aligned edges defining the chamber wall of the outer non-active divertor
		region"""
  
	inner_baffle_2 = 35
	"""x-aligned edges defining the chamber wall of the inner non-active divertor
		region"""
  
	outer_PFR_wall_2 = 36
	"""x-aligned edges defining the private flux region wall of the outer non-active
		divertor region"""
  
	inner_PFR_wall_2 = 37
	"""x-aligned edges defining the private flux region wall of the inner non-active
		divertor region"""
  
	intra_sep = 38
	"""Cells between the two separatrices"""
  
	outer_divertor_2 = 39
	"""Cells defining the outer inactive divertor region"""
  
	inner_divertor_2 = 40
	"""Cells defining the inner inactive divertor region"""
  
	outer_target_2 = 41
	"""y-aligned edges defining the outer inactive target"""
  
	inner_target_2 = 42
	"""y-aligned edges defining the inner inactive target"""
  
	volumes = 43
	"""All volumes (3D) belonging to the associated spaces, implicit declaration (no
		need to replicate the grid elements in the grid_subset structure)"""
  
	full_wall = 44
	"""All edges defining walls, baffles, and targets"""
  
	outer_sf_leg_entrance_1 = 45
	"""y-aligned edges defining the SOL entrance of the first snowflake outer leg"""
  
	outer_sf_leg_entrance_2 = 46
	"""y-aligned edges defining the SOL entrance of the third snowflake outer leg"""
  
	outer_sf_pfr_connection_1 = 47
	"""y-aligned edges defining the connection between the outer snowflake entrance and
		third leg"""
  
	outer_sf_pfr_connection_2 = 48
	"""y-aligned edges defining the connection between the outer snowflake first and
		second leg"""
  
	magnetic_axis = 100
	"""Point corresponding to the magnetic axis"""
  
	outer_mid_plane_separatrix = 101
	"""Point on active separatrix at outer mid-plane"""
  
	inner_mid_plane_separatrix = 102
	"""Point on active separatrix at inner mid-plane"""
  
	outer_target_separatrix = 103
	"""Point on active separatrix at outer active target"""
  
	inner_target_separatrix = 104
	"""Point on active separatrix at inner active target"""
  
	outer_target_separatrix_2 = 105
	"""Point on non-active separatrix at outer non-active target"""
  
	inner_target_separatrix_2 = 106
	"""Point on non-active separatrix at inner non-active target"""
  

class _E_ggd_identifier(IntFlag):
	"""Translation table for ggd_identifier_definitions.	xpath: 	"""
  
	unspecified = 0
	"""unspecified"""
  
	linear = 1
	"""Linear"""
  
	cylinder = 2
	"""Cylindrical geometry (straight in axial direction)"""
  
	limiter = 3
	"""Limiter"""
  
	SN = 4
	"""Single null"""
  
	CDN = 5
	"""Connected double null"""
  
	DDN_bottom = 6
	"""Disconnected double null with inner X-point below the midplane"""
  
	DDN_top = 7
	"""Disconnected double null with inner X-point above the midplane"""
  
	annulus = 8
	"""Annular geometry (not necessarily with straight axis)"""
  
	stellarator_island = 9
	"""Stellarator island geometry"""
  
	structured_spaces = 10
	"""Structured grid represented with multiple spaces of dimension 1"""
  
	LFS_snowflake_minus = 11
	"""Snowflake grid with secondary x point on the low field side, and the secondary
		separatrix on top of the primary"""
  
	LFS_snowflake_plus = 12
	"""Snowflake grid with secondary x point to the right of the primary, and the
		secondary separatrix below the primary"""
  
	reference = 100
	"""Refers to a GGD described in another IDS indicated by grid_path. In such a case,
		do not fill the grid_ggd node of this IDS"""
  

class _E_ggd_identifier(IntFlag):
	"""Translation table for ggd_identifier_definitions.	xpath: 	"""
  
	unspecified = 0
	"""unspecified"""
  
	linear = 1
	"""Linear"""
  
	cylinder = 2
	"""Cylindrical geometry (straight in axial direction)"""
  
	limiter = 3
	"""Limiter"""
  
	SN = 4
	"""Single null"""
  
	CDN = 5
	"""Connected double null"""
  
	DDN_bottom = 6
	"""Disconnected double null with inner X-point below the midplane"""
  
	DDN_top = 7
	"""Disconnected double null with inner X-point above the midplane"""
  
	annulus = 8
	"""Annular geometry (not necessarily with straight axis)"""
  
	stellarator_island = 9
	"""Stellarator island geometry"""
  
	structured_spaces = 10
	"""Structured grid represented with multiple spaces of dimension 1"""
  
	LFS_snowflake_minus = 11
	"""Snowflake grid with secondary x point on the low field side, and the secondary
		separatrix on top of the primary"""
  
	LFS_snowflake_plus = 12
	"""Snowflake grid with secondary x point to the right of the primary, and the
		secondary separatrix below the primary"""
  
	reference = 100
	"""Refers to a GGD described in another IDS indicated by grid_path. In such a case,
		do not fill the grid_ggd node of this IDS"""
  

class _E_spectrometer_visible_emissivity_grid_identifier(IntFlag):
	"""List of coordinate systems for describing the poloidal plane	xpath: 	"""
  
	r_z_phi = 1
	"""Cylindrical r,z,phi grid : r=dim1, z=dim2, phi=dim3"""
  

class _E_spectrometer_x_reflector_geometry(IntFlag):
	"""Geometry of the contour of a planar or curved object	xpath: 	"""
  
	polygonal = 1
	"""Contour described by a polygonal outline in the (X1, X2) plane"""
  
	circular = 2
	"""Circle in the (X1, X2) plane, defined by its centre and radius"""
  
	rectangle = 3
	"""Rectangle in the (X1, X2) plane, defined by its centre and widths in the X1 and
		X2 directions"""
  

class _E_spectrometer_x_reflector_geometry(IntFlag):
	"""Curvature of a curved object	xpath: 	"""
  
	planar = 1
	"""Planar object, no curvature"""
  
	cylindrical_x1 = 2
	"""Cylindrical in the X1 direction, use x1_curvature"""
  
	cylindrical_x2 = 3
	"""Cylindrical in the X2 direction, use x2_curvature"""
  
	spherical = 4
	"""Spherical : same curvature radius in X1 and X2 directions, indicated in
		x1_curvature"""
  
	toroidal = 5
	"""Toroidal : x1_curvature in X1 direction and x2_curvature in X2 direction"""
  

class _E_materials(IntFlag):
	"""Materials used in the device mechanical structures	xpath: 	"""
  
	unspecified = 0
	"""unspecified"""
  
	C = 1
	"""Carbon"""
  
	W = 2
	"""Tungsten"""
  
	C_W_coating = 3
	"""Carbon with tungsten coating"""
  
	SS = 4
	"""Stainless steel"""
  
	SS_C_coating = 5
	"""Stainless steel with carbon coating"""
  
	IN = 6
	"""Inconel"""
  
	IN_C_coating = 7
	"""Inconel with carbon coating"""
  
	B_C = 8
	"""Boron carbide"""
  
	Ti_C_coating = 9
	"""Titanium with carbon coating"""
  
	Be = 10
	"""Beryllium"""
  
	Mo = 11
	"""Molybdenum"""
  
	Quartz = 12
	"""Quartz"""
  
	Ge = 13
	"""Germanium"""
  
	Si = 14
	"""Silicon"""
  
	LiF = 15
	"""Lithium fluoride"""
  
	InSb = 16
	"""Indium antimonide"""
  

class _E_spectrometer_x_reflector_geometry(IntFlag):
	"""Geometry of the contour of a planar or curved object	xpath: 	"""
  
	polygonal = 1
	"""Contour described by a polygonal outline in the (X1, X2) plane"""
  
	circular = 2
	"""Circle in the (X1, X2) plane, defined by its centre and radius"""
  
	rectangle = 3
	"""Rectangle in the (X1, X2) plane, defined by its centre and widths in the X1 and
		X2 directions"""
  

class _E_spectrometer_x_reflector_geometry(IntFlag):
	"""Curvature of a curved object	xpath: 	"""
  
	planar = 1
	"""Planar object, no curvature"""
  
	cylindrical_x1 = 2
	"""Cylindrical in the X1 direction, use x1_curvature"""
  
	cylindrical_x2 = 3
	"""Cylindrical in the X2 direction, use x2_curvature"""
  
	spherical = 4
	"""Spherical : same curvature radius in X1 and X2 directions, indicated in
		x1_curvature"""
  
	toroidal = 5
	"""Toroidal : x1_curvature in X1 direction and x2_curvature in X2 direction"""
  

class _E_materials(IntFlag):
	"""Materials used in the device mechanical structures	xpath: 	"""
  
	unspecified = 0
	"""unspecified"""
  
	C = 1
	"""Carbon"""
  
	W = 2
	"""Tungsten"""
  
	C_W_coating = 3
	"""Carbon with tungsten coating"""
  
	SS = 4
	"""Stainless steel"""
  
	SS_C_coating = 5
	"""Stainless steel with carbon coating"""
  
	IN = 6
	"""Inconel"""
  
	IN_C_coating = 7
	"""Inconel with carbon coating"""
  
	B_C = 8
	"""Boron carbide"""
  
	Ti_C_coating = 9
	"""Titanium with carbon coating"""
  
	Be = 10
	"""Beryllium"""
  
	Mo = 11
	"""Molybdenum"""
  
	Quartz = 12
	"""Quartz"""
  
	Ge = 13
	"""Germanium"""
  
	Si = 14
	"""Silicon"""
  
	LiF = 15
	"""Lithium fluoride"""
  
	InSb = 16
	"""Indium antimonide"""
  

class _E_wave_identifier(IntFlag):
	"""Translation table for wave field types.	xpath: 	"""
  
	unspecified = 0
	"""unspecified"""
  
	EC = 1
	"""Wave field for electron cyclotron heating and current drive"""
  
	LH = 2
	"""Wave field for lower hybrid heating and current drive"""
  
	IC = 3
	"""Wave field for ion cyclotron frequency heating and current drive"""
  

class _E_midplane_identifier(IntFlag):
	"""Translation table for identifying different midplane definitions	xpath: 	"""
  
	magnetic_axis = 1
	"""Midplane defined by the height of magnetic axis
		equilibrium/time_slice/global_quantities/magnetic_axis/z"""
  
	dr_dz_zero_sep = 2
	"""Midplane defined by the height of the outboard point on the separatrix on which
		dr/dz = 0 (local maximum of the major radius of the separatrix). In case of
		multiple local maxima, the closest one from z=z_magnetic_axis is chosen.
		equilibrium/time_slice/boundary_separatrix/dr_dz_zero_point/z"""
  
	z_zero = 3
	"""Midplane defined by z = 0"""
  
	ggd_subset = 4
	"""Midplane location is specified by means of the GGD grid subset for the inner and
		outer midplanes, if the midplane choice is different from the other available
		options. If the GGD midplane subset corresponds to one of the other available
		options, select that particular option to indicate it"""
  

class _E_neutrals_identifier(IntFlag):
	"""Translation table for identifying different types of neutral. The neutrals are
		characterised by their energy and source of the neutrals.	xpath: 	"""
  
	cold = 1
	"""Cold neutrals"""
  
	thermal = 2
	"""Thermal neutrals"""
  
	fast = 3
	"""Fast neutrals"""
  
	nbi = 4
	"""NBI neutrals"""
  

class _E_midplane_identifier(IntFlag):
	"""Translation table for identifying different midplane definitions	xpath: 	"""
  
	magnetic_axis = 1
	"""Midplane defined by the height of magnetic axis
		equilibrium/time_slice/global_quantities/magnetic_axis/z"""
  
	dr_dz_zero_sep = 2
	"""Midplane defined by the height of the outboard point on the separatrix on which
		dr/dz = 0 (local maximum of the major radius of the separatrix). In case of
		multiple local maxima, the closest one from z=z_magnetic_axis is chosen.
		equilibrium/time_slice/boundary_separatrix/dr_dz_zero_point/z"""
  
	z_zero = 3
	"""Midplane defined by z = 0"""
  
	ggd_subset = 4
	"""Midplane location is specified by means of the GGD grid subset for the inner and
		outer midplanes, if the midplane choice is different from the other available
		options. If the GGD midplane subset corresponds to one of the other available
		options, select that particular option to indicate it"""
  

class _E_neutrals_identifier(IntFlag):
	"""Translation table for identifying different types of neutral. The neutrals are
		characterised by their energy and source of the neutrals.	xpath: 	"""
  
	cold = 1
	"""Cold neutrals"""
  
	thermal = 2
	"""Thermal neutrals"""
  
	fast = 3
	"""Fast neutrals"""
  
	nbi = 4
	"""NBI neutrals"""
  

class _E_midplane_identifier(IntFlag):
	"""Translation table for identifying different midplane definitions	xpath: 	"""
  
	magnetic_axis = 1
	"""Midplane defined by the height of magnetic axis
		equilibrium/time_slice/global_quantities/magnetic_axis/z"""
  
	dr_dz_zero_sep = 2
	"""Midplane defined by the height of the outboard point on the separatrix on which
		dr/dz = 0 (local maximum of the major radius of the separatrix). In case of
		multiple local maxima, the closest one from z=z_magnetic_axis is chosen.
		equilibrium/time_slice/boundary_separatrix/dr_dz_zero_point/z"""
  
	z_zero = 3
	"""Midplane defined by z = 0"""
  
	ggd_subset = 4
	"""Midplane location is specified by means of the GGD grid subset for the inner and
		outer midplanes, if the midplane choice is different from the other available
		options. If the GGD midplane subset corresponds to one of the other available
		options, select that particular option to indicate it"""
  

class _E_midplane_identifier(IntFlag):
	"""Translation table for identifying different midplane definitions	xpath: 	"""
  
	magnetic_axis = 1
	"""Midplane defined by the height of magnetic axis
		equilibrium/time_slice/global_quantities/magnetic_axis/z"""
  
	dr_dz_zero_sep = 2
	"""Midplane defined by the height of the outboard point on the separatrix on which
		dr/dz = 0 (local maximum of the major radius of the separatrix). In case of
		multiple local maxima, the closest one from z=z_magnetic_axis is chosen.
		equilibrium/time_slice/boundary_separatrix/dr_dz_zero_point/z"""
  
	z_zero = 3
	"""Midplane defined by z = 0"""
  
	ggd_subset = 4
	"""Midplane location is specified by means of the GGD grid subset for the inner and
		outer midplanes, if the midplane choice is different from the other available
		options. If the GGD midplane subset corresponds to one of the other available
		options, select that particular option to indicate it"""
  

class _E_midplane_identifier(IntFlag):
	"""Translation table for identifying different midplane definitions	xpath: 	"""
  
	magnetic_axis = 1
	"""Midplane defined by the height of magnetic axis
		equilibrium/time_slice/global_quantities/magnetic_axis/z"""
  
	dr_dz_zero_sep = 2
	"""Midplane defined by the height of the outboard point on the separatrix on which
		dr/dz = 0 (local maximum of the major radius of the separatrix). In case of
		multiple local maxima, the closest one from z=z_magnetic_axis is chosen.
		equilibrium/time_slice/boundary_separatrix/dr_dz_zero_point/z"""
  
	z_zero = 3
	"""Midplane defined by z = 0"""
  
	ggd_subset = 4
	"""Midplane location is specified by means of the GGD grid subset for the inner and
		outer midplanes, if the midplane choice is different from the other available
		options. If the GGD midplane subset corresponds to one of the other available
		options, select that particular option to indicate it"""
  

class _E_poloidal_plane_coordinates_identifier(IntFlag):
	"""List of coordinate systems for describing the poloidal plane	xpath: 	"""
  
	rectangular = 1
	"""Cylindrical R,Z ala eqdsk (R=dim1, Z=dim2). In this case the position arrays
		should not be filled since they are redundant with grid/dim1 and dim2."""
  
	inverse = 2
	"""Rhopolar_polar 2D polar coordinates (rho=dim1, theta=dim2) with magnetic axis as
		centre of grid; theta and values following the COCOS=11 convention; the polar
		angle is theta=atan2(z-zaxis,r-raxis)"""
  
	inverse_psi_straight_field_line = 11
	"""Flux surface type with psi as radial label (dim1) and the straight-field line
		poloidal angle (mod(index,10)=1) (dim2); could be non-equidistant; magnetic axis
		as centre of grid; following the COCOS=11 convention"""
  
	inverse_psi_equal_arc = 12
	"""Flux surface type with psi as radial label (dim1) and the equal arc poloidal
		angle (mod(index,10)=2) (dim2)"""
  
	inverse_psi_polar = 13
	"""Flux surface type with psi as radial label (dim1) and the polar poloidal angle
		(mod(index,10)=3) (dim2); could be non-equidistant"""
  
	inverse_psi_straight_field_line_fourier = 14
	"""Flux surface type with psi as radial label (dim1) and Fourier modes in the
		straight-field line poloidal angle (mod(index,10)=4) (dim2), could be
		non-equidistant; magnetic axis as centre of grid; following the COCOS=11
		convention"""
  
	inverse_psi_equal_arc_fourier = 15
	"""Flux surface type with psi as radial label (dim1) and Fourier modes in the equal
		arc poloidal angle (mod(index,10)=5) (dim2)"""
  
	inverse_psi_polar_fourier = 16
	"""Flux surface type with psi as radial label (dim1) and Fourier modes in the polar
		poloidal angle (mod(index,10)=6) (dim2); could be non-equidistant"""
  
	inverse_rhopolnorm_straight_field_line = 21
	"""Flux surface type with radial label sqrt[(psi-psi_axis)/(psi_edge-psi_axis)]
		(dim1) and the straight-field line poloidal angle (dim2)"""
  
	inverse_rhopolnorm_equal_arc = 22
	"""Flux surface type with radial label sqrt[(psi-psi_axis)/(psi_edge-psi_axis)]
		(dim1) and the equal arc poloidal angle (dim2)"""
  
	inverse_rhopolnorm_polar = 23
	"""Flux surface type with radial label sqrt[(psi-psi_axis)/(psi_edge-psi_axis)]
		(dim1) and the polar poloidal angle (dim2)"""
  
	inverse_rhopolnorm_straight_field_line_fourier = 24
	"""Flux surface type with radial label sqrt[(psi-psi_axis)/(psi_edge-psi_axis)]
		(dim1) and Fourier modes in the straight-field line poloidal angle (dim2)"""
  
	inverse_rhopolnorm_equal_arc_fourier = 25
	"""Flux surface type with radial label sqrt[(psi-psi_axis)/(psi_edge-psi_axis)]
		(dim1) and Fourier modes in the equal arc poloidal angle (dim2)"""
  
	inverse_rhopolnorm_polar_fourier = 26
	"""Flux surface type with radial label sqrt[(psi-psi_axis)/(psi_edge-psi_axis)]
		(dim1) and Fourier modes in the polar poloidal angle (dim2)"""
  
	inverse_rhotornorm_straight_field_line = 31
	"""Flux surface type with radial label sqrt[Phi/Phi_edge] (dim1) and the
		straight-field line poloidal angle (dim2)"""
  
	inverse_rhotornorm_equal_arc = 32
	"""Flux surface type with radial label sqrt[Phi/Phi_edge] (dim1) and the equal arc
		poloidal angle (dim2)"""
  
	inverse_rhotornorm_polar = 33
	"""Flux surface type with radial label sqrt[Phi/Phi_edge] (dim1) and the polar
		poloidal angle (dim2)"""
  
	inverse_rhotornorm_straight_field_line_fourier = 34
	"""Flux surface type with radial label sqrt[Phi/Phi_edge] (dim1) and Fourier modes
		in the straight-field line poloidal angle (dim2)"""
  
	inverse_rhotornorm_equal_arc_fourier = 35
	"""Flux surface type with radial label sqrt[Phi/Phi_edge] (dim1) and Fourier modes
		in the equal arc poloidal angle (dim2)"""
  
	inverse_rhotornorm_polar_fourier = 36
	"""Flux surface type with radial label sqrt[Phi/Phi_edge] (dim1) and Fourier modes
		in the polar poloidal angle (dim2)"""
  
	inverse_rhopol_straight_field_line = 41
	"""Flux surface type with radial label sqrt[psi-psi_axis] (dim1) and the
		straight-field line poloidal angle (dim2)"""
  
	inverse_rhopol_equal_arc = 42
	"""Flux surface type with radial label sqrt[psi-psi_axis] (dim1) and the equal arc
		poloidal angle (dim2)"""
  
	inverse_rhopol_polar = 43
	"""Flux surface type with radial label sqrt[psi-psi_axis] (dim1) and the polar
		poloidal angle (dim2)"""
  
	inverse_rhopol_straight_field_line_fourier = 44
	"""Flux surface type with radial label sqrt[psi-psi_axis] (dim1) and Fourier modes
		in the straight-field line poloidal angle (dim2)"""
  
	inverse_rhopol_equal_arc_fourier = 45
	"""Flux surface type with radial label sqrt[psi-psi_axis] (dim1) and Fourier modes
		in the equal arc poloidal angle (dim2)"""
  
	inverse_rhopol_polar_fourier = 46
	"""Flux surface type with radial label sqrt[psi-psi_axis] (dim1) and Fourier modes
		in the polar poloidal angle (dim2)"""
  
	inverse_rhotor_straight_field_line = 51
	"""Flux surface type with radial label sqrt[Phi/pi/B0] (dim1), Phi being toroidal
		flux, and the straight-field line poloidal angle (dim2)"""
  
	inverse_rhotor_equal_arc = 52
	"""Flux surface type with radial label sqrt[Phi/pi/B0] (dim1), Phi being toroidal
		flux, and the equal arc poloidal angle (dim2)"""
  
	inverse_rhotor_polar = 53
	"""Flux surface type with radial label sqrt[Phi/pi/B0] (dim1), Phi being toroidal
		flux, and the polar poloidal angle (dim2)"""
  
	inverse_rhotor_straight_field_line_fourier = 54
	"""Flux surface type with radial label sqrt[Phi/pi/B0] (dim1), Phi being toroidal
		flux, and Fourier modes in the straight-field line poloidal angle (dim2)"""
  
	inverse_rhotor_equal_arc_fourier = 55
	"""Flux surface type with radial label sqrt[Phi/pi/B0] (dim1), Phi being toroidal
		flux, and Fourier modes in the equal arc poloidal angle (dim2)"""
  
	inverse_rhotor_polar_fourier = 56
	"""Flux surface type with radial label sqrt[Phi/pi/B0] (dim1), Phi being toroidal
		flux, and Fourier modes in the polar poloidal angle (dim2)"""
  
	irregular_rz_na = 91
	"""Irregular grid, thus give list of vertices in dim1(1:ndim1), dim2(1:ndim1) and
		then all fields are on values(1:ndim1,1)"""
  

class _E_midplane_identifier(IntFlag):
	"""Translation table for identifying different midplane definitions	xpath: 	"""
  
	magnetic_axis = 1
	"""Midplane defined by the height of magnetic axis
		equilibrium/time_slice/global_quantities/magnetic_axis/z"""
  
	dr_dz_zero_sep = 2
	"""Midplane defined by the height of the outboard point on the separatrix on which
		dr/dz = 0 (local maximum of the major radius of the separatrix). In case of
		multiple local maxima, the closest one from z=z_magnetic_axis is chosen.
		equilibrium/time_slice/boundary_separatrix/dr_dz_zero_point/z"""
  
	z_zero = 3
	"""Midplane defined by z = 0"""
  
	ggd_subset = 4
	"""Midplane location is specified by means of the GGD grid subset for the inner and
		outer midplanes, if the midplane choice is different from the other available
		options. If the GGD midplane subset corresponds to one of the other available
		options, select that particular option to indicate it"""
  

class _E_poloidal_plane_coordinates_identifier(IntFlag):
	"""List of coordinate systems for describing the poloidal plane	xpath: 	"""
  
	rectangular = 1
	"""Cylindrical R,Z ala eqdsk (R=dim1, Z=dim2). In this case the position arrays
		should not be filled since they are redundant with grid/dim1 and dim2."""
  
	inverse = 2
	"""Rhopolar_polar 2D polar coordinates (rho=dim1, theta=dim2) with magnetic axis as
		centre of grid; theta and values following the COCOS=11 convention; the polar
		angle is theta=atan2(z-zaxis,r-raxis)"""
  
	inverse_psi_straight_field_line = 11
	"""Flux surface type with psi as radial label (dim1) and the straight-field line
		poloidal angle (mod(index,10)=1) (dim2); could be non-equidistant; magnetic axis
		as centre of grid; following the COCOS=11 convention"""
  
	inverse_psi_equal_arc = 12
	"""Flux surface type with psi as radial label (dim1) and the equal arc poloidal
		angle (mod(index,10)=2) (dim2)"""
  
	inverse_psi_polar = 13
	"""Flux surface type with psi as radial label (dim1) and the polar poloidal angle
		(mod(index,10)=3) (dim2); could be non-equidistant"""
  
	inverse_psi_straight_field_line_fourier = 14
	"""Flux surface type with psi as radial label (dim1) and Fourier modes in the
		straight-field line poloidal angle (mod(index,10)=4) (dim2), could be
		non-equidistant; magnetic axis as centre of grid; following the COCOS=11
		convention"""
  
	inverse_psi_equal_arc_fourier = 15
	"""Flux surface type with psi as radial label (dim1) and Fourier modes in the equal
		arc poloidal angle (mod(index,10)=5) (dim2)"""
  
	inverse_psi_polar_fourier = 16
	"""Flux surface type with psi as radial label (dim1) and Fourier modes in the polar
		poloidal angle (mod(index,10)=6) (dim2); could be non-equidistant"""
  
	inverse_rhopolnorm_straight_field_line = 21
	"""Flux surface type with radial label sqrt[(psi-psi_axis)/(psi_edge-psi_axis)]
		(dim1) and the straight-field line poloidal angle (dim2)"""
  
	inverse_rhopolnorm_equal_arc = 22
	"""Flux surface type with radial label sqrt[(psi-psi_axis)/(psi_edge-psi_axis)]
		(dim1) and the equal arc poloidal angle (dim2)"""
  
	inverse_rhopolnorm_polar = 23
	"""Flux surface type with radial label sqrt[(psi-psi_axis)/(psi_edge-psi_axis)]
		(dim1) and the polar poloidal angle (dim2)"""
  
	inverse_rhopolnorm_straight_field_line_fourier = 24
	"""Flux surface type with radial label sqrt[(psi-psi_axis)/(psi_edge-psi_axis)]
		(dim1) and Fourier modes in the straight-field line poloidal angle (dim2)"""
  
	inverse_rhopolnorm_equal_arc_fourier = 25
	"""Flux surface type with radial label sqrt[(psi-psi_axis)/(psi_edge-psi_axis)]
		(dim1) and Fourier modes in the equal arc poloidal angle (dim2)"""
  
	inverse_rhopolnorm_polar_fourier = 26
	"""Flux surface type with radial label sqrt[(psi-psi_axis)/(psi_edge-psi_axis)]
		(dim1) and Fourier modes in the polar poloidal angle (dim2)"""
  
	inverse_rhotornorm_straight_field_line = 31
	"""Flux surface type with radial label sqrt[Phi/Phi_edge] (dim1) and the
		straight-field line poloidal angle (dim2)"""
  
	inverse_rhotornorm_equal_arc = 32
	"""Flux surface type with radial label sqrt[Phi/Phi_edge] (dim1) and the equal arc
		poloidal angle (dim2)"""
  
	inverse_rhotornorm_polar = 33
	"""Flux surface type with radial label sqrt[Phi/Phi_edge] (dim1) and the polar
		poloidal angle (dim2)"""
  
	inverse_rhotornorm_straight_field_line_fourier = 34
	"""Flux surface type with radial label sqrt[Phi/Phi_edge] (dim1) and Fourier modes
		in the straight-field line poloidal angle (dim2)"""
  
	inverse_rhotornorm_equal_arc_fourier = 35
	"""Flux surface type with radial label sqrt[Phi/Phi_edge] (dim1) and Fourier modes
		in the equal arc poloidal angle (dim2)"""
  
	inverse_rhotornorm_polar_fourier = 36
	"""Flux surface type with radial label sqrt[Phi/Phi_edge] (dim1) and Fourier modes
		in the polar poloidal angle (dim2)"""
  
	inverse_rhopol_straight_field_line = 41
	"""Flux surface type with radial label sqrt[psi-psi_axis] (dim1) and the
		straight-field line poloidal angle (dim2)"""
  
	inverse_rhopol_equal_arc = 42
	"""Flux surface type with radial label sqrt[psi-psi_axis] (dim1) and the equal arc
		poloidal angle (dim2)"""
  
	inverse_rhopol_polar = 43
	"""Flux surface type with radial label sqrt[psi-psi_axis] (dim1) and the polar
		poloidal angle (dim2)"""
  
	inverse_rhopol_straight_field_line_fourier = 44
	"""Flux surface type with radial label sqrt[psi-psi_axis] (dim1) and Fourier modes
		in the straight-field line poloidal angle (dim2)"""
  
	inverse_rhopol_equal_arc_fourier = 45
	"""Flux surface type with radial label sqrt[psi-psi_axis] (dim1) and Fourier modes
		in the equal arc poloidal angle (dim2)"""
  
	inverse_rhopol_polar_fourier = 46
	"""Flux surface type with radial label sqrt[psi-psi_axis] (dim1) and Fourier modes
		in the polar poloidal angle (dim2)"""
  
	inverse_rhotor_straight_field_line = 51
	"""Flux surface type with radial label sqrt[Phi/pi/B0] (dim1), Phi being toroidal
		flux, and the straight-field line poloidal angle (dim2)"""
  
	inverse_rhotor_equal_arc = 52
	"""Flux surface type with radial label sqrt[Phi/pi/B0] (dim1), Phi being toroidal
		flux, and the equal arc poloidal angle (dim2)"""
  
	inverse_rhotor_polar = 53
	"""Flux surface type with radial label sqrt[Phi/pi/B0] (dim1), Phi being toroidal
		flux, and the polar poloidal angle (dim2)"""
  
	inverse_rhotor_straight_field_line_fourier = 54
	"""Flux surface type with radial label sqrt[Phi/pi/B0] (dim1), Phi being toroidal
		flux, and Fourier modes in the straight-field line poloidal angle (dim2)"""
  
	inverse_rhotor_equal_arc_fourier = 55
	"""Flux surface type with radial label sqrt[Phi/pi/B0] (dim1), Phi being toroidal
		flux, and Fourier modes in the equal arc poloidal angle (dim2)"""
  
	inverse_rhotor_polar_fourier = 56
	"""Flux surface type with radial label sqrt[Phi/pi/B0] (dim1), Phi being toroidal
		flux, and Fourier modes in the polar poloidal angle (dim2)"""
  
	irregular_rz_na = 91
	"""Irregular grid, thus give list of vertices in dim1(1:ndim1), dim2(1:ndim1) and
		then all fields are on values(1:ndim1,1)"""
  

class _E_poloidal_plane_coordinates_identifier(IntFlag):
	"""List of coordinate systems for describing the poloidal plane	xpath: 	"""
  
	rectangular = 1
	"""Cylindrical R,Z ala eqdsk (R=dim1, Z=dim2). In this case the position arrays
		should not be filled since they are redundant with grid/dim1 and dim2."""
  
	inverse = 2
	"""Rhopolar_polar 2D polar coordinates (rho=dim1, theta=dim2) with magnetic axis as
		centre of grid; theta and values following the COCOS=11 convention; the polar
		angle is theta=atan2(z-zaxis,r-raxis)"""
  
	inverse_psi_straight_field_line = 11
	"""Flux surface type with psi as radial label (dim1) and the straight-field line
		poloidal angle (mod(index,10)=1) (dim2); could be non-equidistant; magnetic axis
		as centre of grid; following the COCOS=11 convention"""
  
	inverse_psi_equal_arc = 12
	"""Flux surface type with psi as radial label (dim1) and the equal arc poloidal
		angle (mod(index,10)=2) (dim2)"""
  
	inverse_psi_polar = 13
	"""Flux surface type with psi as radial label (dim1) and the polar poloidal angle
		(mod(index,10)=3) (dim2); could be non-equidistant"""
  
	inverse_psi_straight_field_line_fourier = 14
	"""Flux surface type with psi as radial label (dim1) and Fourier modes in the
		straight-field line poloidal angle (mod(index,10)=4) (dim2), could be
		non-equidistant; magnetic axis as centre of grid; following the COCOS=11
		convention"""
  
	inverse_psi_equal_arc_fourier = 15
	"""Flux surface type with psi as radial label (dim1) and Fourier modes in the equal
		arc poloidal angle (mod(index,10)=5) (dim2)"""
  
	inverse_psi_polar_fourier = 16
	"""Flux surface type with psi as radial label (dim1) and Fourier modes in the polar
		poloidal angle (mod(index,10)=6) (dim2); could be non-equidistant"""
  
	inverse_rhopolnorm_straight_field_line = 21
	"""Flux surface type with radial label sqrt[(psi-psi_axis)/(psi_edge-psi_axis)]
		(dim1) and the straight-field line poloidal angle (dim2)"""
  
	inverse_rhopolnorm_equal_arc = 22
	"""Flux surface type with radial label sqrt[(psi-psi_axis)/(psi_edge-psi_axis)]
		(dim1) and the equal arc poloidal angle (dim2)"""
  
	inverse_rhopolnorm_polar = 23
	"""Flux surface type with radial label sqrt[(psi-psi_axis)/(psi_edge-psi_axis)]
		(dim1) and the polar poloidal angle (dim2)"""
  
	inverse_rhopolnorm_straight_field_line_fourier = 24
	"""Flux surface type with radial label sqrt[(psi-psi_axis)/(psi_edge-psi_axis)]
		(dim1) and Fourier modes in the straight-field line poloidal angle (dim2)"""
  
	inverse_rhopolnorm_equal_arc_fourier = 25
	"""Flux surface type with radial label sqrt[(psi-psi_axis)/(psi_edge-psi_axis)]
		(dim1) and Fourier modes in the equal arc poloidal angle (dim2)"""
  
	inverse_rhopolnorm_polar_fourier = 26
	"""Flux surface type with radial label sqrt[(psi-psi_axis)/(psi_edge-psi_axis)]
		(dim1) and Fourier modes in the polar poloidal angle (dim2)"""
  
	inverse_rhotornorm_straight_field_line = 31
	"""Flux surface type with radial label sqrt[Phi/Phi_edge] (dim1) and the
		straight-field line poloidal angle (dim2)"""
  
	inverse_rhotornorm_equal_arc = 32
	"""Flux surface type with radial label sqrt[Phi/Phi_edge] (dim1) and the equal arc
		poloidal angle (dim2)"""
  
	inverse_rhotornorm_polar = 33
	"""Flux surface type with radial label sqrt[Phi/Phi_edge] (dim1) and the polar
		poloidal angle (dim2)"""
  
	inverse_rhotornorm_straight_field_line_fourier = 34
	"""Flux surface type with radial label sqrt[Phi/Phi_edge] (dim1) and Fourier modes
		in the straight-field line poloidal angle (dim2)"""
  
	inverse_rhotornorm_equal_arc_fourier = 35
	"""Flux surface type with radial label sqrt[Phi/Phi_edge] (dim1) and Fourier modes
		in the equal arc poloidal angle (dim2)"""
  
	inverse_rhotornorm_polar_fourier = 36
	"""Flux surface type with radial label sqrt[Phi/Phi_edge] (dim1) and Fourier modes
		in the polar poloidal angle (dim2)"""
  
	inverse_rhopol_straight_field_line = 41
	"""Flux surface type with radial label sqrt[psi-psi_axis] (dim1) and the
		straight-field line poloidal angle (dim2)"""
  
	inverse_rhopol_equal_arc = 42
	"""Flux surface type with radial label sqrt[psi-psi_axis] (dim1) and the equal arc
		poloidal angle (dim2)"""
  
	inverse_rhopol_polar = 43
	"""Flux surface type with radial label sqrt[psi-psi_axis] (dim1) and the polar
		poloidal angle (dim2)"""
  
	inverse_rhopol_straight_field_line_fourier = 44
	"""Flux surface type with radial label sqrt[psi-psi_axis] (dim1) and Fourier modes
		in the straight-field line poloidal angle (dim2)"""
  
	inverse_rhopol_equal_arc_fourier = 45
	"""Flux surface type with radial label sqrt[psi-psi_axis] (dim1) and Fourier modes
		in the equal arc poloidal angle (dim2)"""
  
	inverse_rhopol_polar_fourier = 46
	"""Flux surface type with radial label sqrt[psi-psi_axis] (dim1) and Fourier modes
		in the polar poloidal angle (dim2)"""
  
	inverse_rhotor_straight_field_line = 51
	"""Flux surface type with radial label sqrt[Phi/pi/B0] (dim1), Phi being toroidal
		flux, and the straight-field line poloidal angle (dim2)"""
  
	inverse_rhotor_equal_arc = 52
	"""Flux surface type with radial label sqrt[Phi/pi/B0] (dim1), Phi being toroidal
		flux, and the equal arc poloidal angle (dim2)"""
  
	inverse_rhotor_polar = 53
	"""Flux surface type with radial label sqrt[Phi/pi/B0] (dim1), Phi being toroidal
		flux, and the polar poloidal angle (dim2)"""
  
	inverse_rhotor_straight_field_line_fourier = 54
	"""Flux surface type with radial label sqrt[Phi/pi/B0] (dim1), Phi being toroidal
		flux, and Fourier modes in the straight-field line poloidal angle (dim2)"""
  
	inverse_rhotor_equal_arc_fourier = 55
	"""Flux surface type with radial label sqrt[Phi/pi/B0] (dim1), Phi being toroidal
		flux, and Fourier modes in the equal arc poloidal angle (dim2)"""
  
	inverse_rhotor_polar_fourier = 56
	"""Flux surface type with radial label sqrt[Phi/pi/B0] (dim1), Phi being toroidal
		flux, and Fourier modes in the polar poloidal angle (dim2)"""
  
	irregular_rz_na = 91
	"""Irregular grid, thus give list of vertices in dim1(1:ndim1), dim2(1:ndim1) and
		then all fields are on values(1:ndim1,1)"""
  

class _E_poloidal_plane_coordinates_identifier(IntFlag):
	"""List of coordinate systems for describing the poloidal plane	xpath: 	"""
  
	rectangular = 1
	"""Cylindrical R,Z ala eqdsk (R=dim1, Z=dim2). In this case the position arrays
		should not be filled since they are redundant with grid/dim1 and dim2."""
  
	inverse = 2
	"""Rhopolar_polar 2D polar coordinates (rho=dim1, theta=dim2) with magnetic axis as
		centre of grid; theta and values following the COCOS=11 convention; the polar
		angle is theta=atan2(z-zaxis,r-raxis)"""
  
	inverse_psi_straight_field_line = 11
	"""Flux surface type with psi as radial label (dim1) and the straight-field line
		poloidal angle (mod(index,10)=1) (dim2); could be non-equidistant; magnetic axis
		as centre of grid; following the COCOS=11 convention"""
  
	inverse_psi_equal_arc = 12
	"""Flux surface type with psi as radial label (dim1) and the equal arc poloidal
		angle (mod(index,10)=2) (dim2)"""
  
	inverse_psi_polar = 13
	"""Flux surface type with psi as radial label (dim1) and the polar poloidal angle
		(mod(index,10)=3) (dim2); could be non-equidistant"""
  
	inverse_psi_straight_field_line_fourier = 14
	"""Flux surface type with psi as radial label (dim1) and Fourier modes in the
		straight-field line poloidal angle (mod(index,10)=4) (dim2), could be
		non-equidistant; magnetic axis as centre of grid; following the COCOS=11
		convention"""
  
	inverse_psi_equal_arc_fourier = 15
	"""Flux surface type with psi as radial label (dim1) and Fourier modes in the equal
		arc poloidal angle (mod(index,10)=5) (dim2)"""
  
	inverse_psi_polar_fourier = 16
	"""Flux surface type with psi as radial label (dim1) and Fourier modes in the polar
		poloidal angle (mod(index,10)=6) (dim2); could be non-equidistant"""
  
	inverse_rhopolnorm_straight_field_line = 21
	"""Flux surface type with radial label sqrt[(psi-psi_axis)/(psi_edge-psi_axis)]
		(dim1) and the straight-field line poloidal angle (dim2)"""
  
	inverse_rhopolnorm_equal_arc = 22
	"""Flux surface type with radial label sqrt[(psi-psi_axis)/(psi_edge-psi_axis)]
		(dim1) and the equal arc poloidal angle (dim2)"""
  
	inverse_rhopolnorm_polar = 23
	"""Flux surface type with radial label sqrt[(psi-psi_axis)/(psi_edge-psi_axis)]
		(dim1) and the polar poloidal angle (dim2)"""
  
	inverse_rhopolnorm_straight_field_line_fourier = 24
	"""Flux surface type with radial label sqrt[(psi-psi_axis)/(psi_edge-psi_axis)]
		(dim1) and Fourier modes in the straight-field line poloidal angle (dim2)"""
  
	inverse_rhopolnorm_equal_arc_fourier = 25
	"""Flux surface type with radial label sqrt[(psi-psi_axis)/(psi_edge-psi_axis)]
		(dim1) and Fourier modes in the equal arc poloidal angle (dim2)"""
  
	inverse_rhopolnorm_polar_fourier = 26
	"""Flux surface type with radial label sqrt[(psi-psi_axis)/(psi_edge-psi_axis)]
		(dim1) and Fourier modes in the polar poloidal angle (dim2)"""
  
	inverse_rhotornorm_straight_field_line = 31
	"""Flux surface type with radial label sqrt[Phi/Phi_edge] (dim1) and the
		straight-field line poloidal angle (dim2)"""
  
	inverse_rhotornorm_equal_arc = 32
	"""Flux surface type with radial label sqrt[Phi/Phi_edge] (dim1) and the equal arc
		poloidal angle (dim2)"""
  
	inverse_rhotornorm_polar = 33
	"""Flux surface type with radial label sqrt[Phi/Phi_edge] (dim1) and the polar
		poloidal angle (dim2)"""
  
	inverse_rhotornorm_straight_field_line_fourier = 34
	"""Flux surface type with radial label sqrt[Phi/Phi_edge] (dim1) and Fourier modes
		in the straight-field line poloidal angle (dim2)"""
  
	inverse_rhotornorm_equal_arc_fourier = 35
	"""Flux surface type with radial label sqrt[Phi/Phi_edge] (dim1) and Fourier modes
		in the equal arc poloidal angle (dim2)"""
  
	inverse_rhotornorm_polar_fourier = 36
	"""Flux surface type with radial label sqrt[Phi/Phi_edge] (dim1) and Fourier modes
		in the polar poloidal angle (dim2)"""
  
	inverse_rhopol_straight_field_line = 41
	"""Flux surface type with radial label sqrt[psi-psi_axis] (dim1) and the
		straight-field line poloidal angle (dim2)"""
  
	inverse_rhopol_equal_arc = 42
	"""Flux surface type with radial label sqrt[psi-psi_axis] (dim1) and the equal arc
		poloidal angle (dim2)"""
  
	inverse_rhopol_polar = 43
	"""Flux surface type with radial label sqrt[psi-psi_axis] (dim1) and the polar
		poloidal angle (dim2)"""
  
	inverse_rhopol_straight_field_line_fourier = 44
	"""Flux surface type with radial label sqrt[psi-psi_axis] (dim1) and Fourier modes
		in the straight-field line poloidal angle (dim2)"""
  
	inverse_rhopol_equal_arc_fourier = 45
	"""Flux surface type with radial label sqrt[psi-psi_axis] (dim1) and Fourier modes
		in the equal arc poloidal angle (dim2)"""
  
	inverse_rhopol_polar_fourier = 46
	"""Flux surface type with radial label sqrt[psi-psi_axis] (dim1) and Fourier modes
		in the polar poloidal angle (dim2)"""
  
	inverse_rhotor_straight_field_line = 51
	"""Flux surface type with radial label sqrt[Phi/pi/B0] (dim1), Phi being toroidal
		flux, and the straight-field line poloidal angle (dim2)"""
  
	inverse_rhotor_equal_arc = 52
	"""Flux surface type with radial label sqrt[Phi/pi/B0] (dim1), Phi being toroidal
		flux, and the equal arc poloidal angle (dim2)"""
  
	inverse_rhotor_polar = 53
	"""Flux surface type with radial label sqrt[Phi/pi/B0] (dim1), Phi being toroidal
		flux, and the polar poloidal angle (dim2)"""
  
	inverse_rhotor_straight_field_line_fourier = 54
	"""Flux surface type with radial label sqrt[Phi/pi/B0] (dim1), Phi being toroidal
		flux, and Fourier modes in the straight-field line poloidal angle (dim2)"""
  
	inverse_rhotor_equal_arc_fourier = 55
	"""Flux surface type with radial label sqrt[Phi/pi/B0] (dim1), Phi being toroidal
		flux, and Fourier modes in the equal arc poloidal angle (dim2)"""
  
	inverse_rhotor_polar_fourier = 56
	"""Flux surface type with radial label sqrt[Phi/pi/B0] (dim1), Phi being toroidal
		flux, and Fourier modes in the polar poloidal angle (dim2)"""
  
	irregular_rz_na = 91
	"""Irregular grid, thus give list of vertices in dim1(1:ndim1), dim2(1:ndim1) and
		then all fields are on values(1:ndim1,1)"""
  

class _E_poloidal_plane_coordinates_identifier(IntFlag):
	"""List of coordinate systems for describing the poloidal plane	xpath: 	"""
  
	rectangular = 1
	"""Cylindrical R,Z ala eqdsk (R=dim1, Z=dim2). In this case the position arrays
		should not be filled since they are redundant with grid/dim1 and dim2."""
  
	inverse = 2
	"""Rhopolar_polar 2D polar coordinates (rho=dim1, theta=dim2) with magnetic axis as
		centre of grid; theta and values following the COCOS=11 convention; the polar
		angle is theta=atan2(z-zaxis,r-raxis)"""
  
	inverse_psi_straight_field_line = 11
	"""Flux surface type with psi as radial label (dim1) and the straight-field line
		poloidal angle (mod(index,10)=1) (dim2); could be non-equidistant; magnetic axis
		as centre of grid; following the COCOS=11 convention"""
  
	inverse_psi_equal_arc = 12
	"""Flux surface type with psi as radial label (dim1) and the equal arc poloidal
		angle (mod(index,10)=2) (dim2)"""
  
	inverse_psi_polar = 13
	"""Flux surface type with psi as radial label (dim1) and the polar poloidal angle
		(mod(index,10)=3) (dim2); could be non-equidistant"""
  
	inverse_psi_straight_field_line_fourier = 14
	"""Flux surface type with psi as radial label (dim1) and Fourier modes in the
		straight-field line poloidal angle (mod(index,10)=4) (dim2), could be
		non-equidistant; magnetic axis as centre of grid; following the COCOS=11
		convention"""
  
	inverse_psi_equal_arc_fourier = 15
	"""Flux surface type with psi as radial label (dim1) and Fourier modes in the equal
		arc poloidal angle (mod(index,10)=5) (dim2)"""
  
	inverse_psi_polar_fourier = 16
	"""Flux surface type with psi as radial label (dim1) and Fourier modes in the polar
		poloidal angle (mod(index,10)=6) (dim2); could be non-equidistant"""
  
	inverse_rhopolnorm_straight_field_line = 21
	"""Flux surface type with radial label sqrt[(psi-psi_axis)/(psi_edge-psi_axis)]
		(dim1) and the straight-field line poloidal angle (dim2)"""
  
	inverse_rhopolnorm_equal_arc = 22
	"""Flux surface type with radial label sqrt[(psi-psi_axis)/(psi_edge-psi_axis)]
		(dim1) and the equal arc poloidal angle (dim2)"""
  
	inverse_rhopolnorm_polar = 23
	"""Flux surface type with radial label sqrt[(psi-psi_axis)/(psi_edge-psi_axis)]
		(dim1) and the polar poloidal angle (dim2)"""
  
	inverse_rhopolnorm_straight_field_line_fourier = 24
	"""Flux surface type with radial label sqrt[(psi-psi_axis)/(psi_edge-psi_axis)]
		(dim1) and Fourier modes in the straight-field line poloidal angle (dim2)"""
  
	inverse_rhopolnorm_equal_arc_fourier = 25
	"""Flux surface type with radial label sqrt[(psi-psi_axis)/(psi_edge-psi_axis)]
		(dim1) and Fourier modes in the equal arc poloidal angle (dim2)"""
  
	inverse_rhopolnorm_polar_fourier = 26
	"""Flux surface type with radial label sqrt[(psi-psi_axis)/(psi_edge-psi_axis)]
		(dim1) and Fourier modes in the polar poloidal angle (dim2)"""
  
	inverse_rhotornorm_straight_field_line = 31
	"""Flux surface type with radial label sqrt[Phi/Phi_edge] (dim1) and the
		straight-field line poloidal angle (dim2)"""
  
	inverse_rhotornorm_equal_arc = 32
	"""Flux surface type with radial label sqrt[Phi/Phi_edge] (dim1) and the equal arc
		poloidal angle (dim2)"""
  
	inverse_rhotornorm_polar = 33
	"""Flux surface type with radial label sqrt[Phi/Phi_edge] (dim1) and the polar
		poloidal angle (dim2)"""
  
	inverse_rhotornorm_straight_field_line_fourier = 34
	"""Flux surface type with radial label sqrt[Phi/Phi_edge] (dim1) and Fourier modes
		in the straight-field line poloidal angle (dim2)"""
  
	inverse_rhotornorm_equal_arc_fourier = 35
	"""Flux surface type with radial label sqrt[Phi/Phi_edge] (dim1) and Fourier modes
		in the equal arc poloidal angle (dim2)"""
  
	inverse_rhotornorm_polar_fourier = 36
	"""Flux surface type with radial label sqrt[Phi/Phi_edge] (dim1) and Fourier modes
		in the polar poloidal angle (dim2)"""
  
	inverse_rhopol_straight_field_line = 41
	"""Flux surface type with radial label sqrt[psi-psi_axis] (dim1) and the
		straight-field line poloidal angle (dim2)"""
  
	inverse_rhopol_equal_arc = 42
	"""Flux surface type with radial label sqrt[psi-psi_axis] (dim1) and the equal arc
		poloidal angle (dim2)"""
  
	inverse_rhopol_polar = 43
	"""Flux surface type with radial label sqrt[psi-psi_axis] (dim1) and the polar
		poloidal angle (dim2)"""
  
	inverse_rhopol_straight_field_line_fourier = 44
	"""Flux surface type with radial label sqrt[psi-psi_axis] (dim1) and Fourier modes
		in the straight-field line poloidal angle (dim2)"""
  
	inverse_rhopol_equal_arc_fourier = 45
	"""Flux surface type with radial label sqrt[psi-psi_axis] (dim1) and Fourier modes
		in the equal arc poloidal angle (dim2)"""
  
	inverse_rhopol_polar_fourier = 46
	"""Flux surface type with radial label sqrt[psi-psi_axis] (dim1) and Fourier modes
		in the polar poloidal angle (dim2)"""
  
	inverse_rhotor_straight_field_line = 51
	"""Flux surface type with radial label sqrt[Phi/pi/B0] (dim1), Phi being toroidal
		flux, and the straight-field line poloidal angle (dim2)"""
  
	inverse_rhotor_equal_arc = 52
	"""Flux surface type with radial label sqrt[Phi/pi/B0] (dim1), Phi being toroidal
		flux, and the equal arc poloidal angle (dim2)"""
  
	inverse_rhotor_polar = 53
	"""Flux surface type with radial label sqrt[Phi/pi/B0] (dim1), Phi being toroidal
		flux, and the polar poloidal angle (dim2)"""
  
	inverse_rhotor_straight_field_line_fourier = 54
	"""Flux surface type with radial label sqrt[Phi/pi/B0] (dim1), Phi being toroidal
		flux, and Fourier modes in the straight-field line poloidal angle (dim2)"""
  
	inverse_rhotor_equal_arc_fourier = 55
	"""Flux surface type with radial label sqrt[Phi/pi/B0] (dim1), Phi being toroidal
		flux, and Fourier modes in the equal arc poloidal angle (dim2)"""
  
	inverse_rhotor_polar_fourier = 56
	"""Flux surface type with radial label sqrt[Phi/pi/B0] (dim1), Phi being toroidal
		flux, and Fourier modes in the polar poloidal angle (dim2)"""
  
	irregular_rz_na = 91
	"""Irregular grid, thus give list of vertices in dim1(1:ndim1), dim2(1:ndim1) and
		then all fields are on values(1:ndim1,1)"""
  

class _E_neutrals_identifier(IntFlag):
	"""Translation table for identifying different types of neutral. The neutrals are
		characterised by their energy and source of the neutrals.	xpath: 	"""
  
	cold = 1
	"""Cold neutrals"""
  
	thermal = 2
	"""Thermal neutrals"""
  
	fast = 3
	"""Fast neutrals"""
  
	nbi = 4
	"""NBI neutrals"""
  

class _E_neutrals_identifier(IntFlag):
	"""Translation table for identifying different types of neutral. The neutrals are
		characterised by their energy and source of the neutrals.	xpath: 	"""
  
	cold = 1
	"""Cold neutrals"""
  
	thermal = 2
	"""Thermal neutrals"""
  
	fast = 3
	"""Fast neutrals"""
  
	nbi = 4
	"""NBI neutrals"""
  

class _E_spectrometer_x_reflector_geometry(IntFlag):
	"""Geometry of the contour of a planar or curved object	xpath: 	"""
  
	polygonal = 1
	"""Contour described by a polygonal outline in the (X1, X2) plane"""
  
	circular = 2
	"""Circle in the (X1, X2) plane, defined by its centre and radius"""
  
	rectangle = 3
	"""Rectangle in the (X1, X2) plane, defined by its centre and widths in the X1 and
		X2 directions"""
  

class _E_spectrometer_x_reflector_geometry(IntFlag):
	"""Curvature of a curved object	xpath: 	"""
  
	planar = 1
	"""Planar object, no curvature"""
  
	cylindrical_x1 = 2
	"""Cylindrical in the X1 direction, use x1_curvature"""
  
	cylindrical_x2 = 3
	"""Cylindrical in the X2 direction, use x2_curvature"""
  
	spherical = 4
	"""Spherical : same curvature radius in X1 and X2 directions, indicated in
		x1_curvature"""
  
	toroidal = 5
	"""Toroidal : x1_curvature in X1 direction and x2_curvature in X2 direction"""
  

class _E_materials(IntFlag):
	"""Materials used in the device mechanical structures	xpath: 	"""
  
	unspecified = 0
	"""unspecified"""
  
	C = 1
	"""Carbon"""
  
	W = 2
	"""Tungsten"""
  
	C_W_coating = 3
	"""Carbon with tungsten coating"""
  
	SS = 4
	"""Stainless steel"""
  
	SS_C_coating = 5
	"""Stainless steel with carbon coating"""
  
	IN = 6
	"""Inconel"""
  
	IN_C_coating = 7
	"""Inconel with carbon coating"""
  
	B_C = 8
	"""Boron carbide"""
  
	Ti_C_coating = 9
	"""Titanium with carbon coating"""
  
	Be = 10
	"""Beryllium"""
  
	Mo = 11
	"""Molybdenum"""
  
	Quartz = 12
	"""Quartz"""
  
	Ge = 13
	"""Germanium"""
  
	Si = 14
	"""Silicon"""
  
	LiF = 15
	"""Lithium fluoride"""
  
	InSb = 16
	"""Indium antimonide"""
  

class _E_materials(IntFlag):
	"""Materials used in the device mechanical structures	xpath: 	"""
  
	unspecified = 0
	"""unspecified"""
  
	C = 1
	"""Carbon"""
  
	W = 2
	"""Tungsten"""
  
	C_W_coating = 3
	"""Carbon with tungsten coating"""
  
	SS = 4
	"""Stainless steel"""
  
	SS_C_coating = 5
	"""Stainless steel with carbon coating"""
  
	IN = 6
	"""Inconel"""
  
	IN_C_coating = 7
	"""Inconel with carbon coating"""
  
	B_C = 8
	"""Boron carbide"""
  
	Ti_C_coating = 9
	"""Titanium with carbon coating"""
  
	Be = 10
	"""Beryllium"""
  
	Mo = 11
	"""Molybdenum"""
  
	Quartz = 12
	"""Quartz"""
  
	Ge = 13
	"""Germanium"""
  
	Si = 14
	"""Silicon"""
  
	LiF = 15
	"""Lithium fluoride"""
  
	InSb = 16
	"""Indium antimonide"""
  

class _E_materials(IntFlag):
	"""Materials used in the device mechanical structures	xpath: 	"""
  
	unspecified = 0
	"""unspecified"""
  
	C = 1
	"""Carbon"""
  
	W = 2
	"""Tungsten"""
  
	C_W_coating = 3
	"""Carbon with tungsten coating"""
  
	SS = 4
	"""Stainless steel"""
  
	SS_C_coating = 5
	"""Stainless steel with carbon coating"""
  
	IN = 6
	"""Inconel"""
  
	IN_C_coating = 7
	"""Inconel with carbon coating"""
  
	B_C = 8
	"""Boron carbide"""
  
	Ti_C_coating = 9
	"""Titanium with carbon coating"""
  
	Be = 10
	"""Beryllium"""
  
	Mo = 11
	"""Molybdenum"""
  
	Quartz = 12
	"""Quartz"""
  
	Ge = 13
	"""Germanium"""
  
	Si = 14
	"""Silicon"""
  
	LiF = 15
	"""Lithium fluoride"""
  
	InSb = 16
	"""Indium antimonide"""
  

class _E_midplane_identifier(IntFlag):
	"""Translation table for identifying different midplane definitions	xpath: 	"""
  
	magnetic_axis = 1
	"""Midplane defined by the height of magnetic axis
		equilibrium/time_slice/global_quantities/magnetic_axis/z"""
  
	dr_dz_zero_sep = 2
	"""Midplane defined by the height of the outboard point on the separatrix on which
		dr/dz = 0 (local maximum of the major radius of the separatrix). In case of
		multiple local maxima, the closest one from z=z_magnetic_axis is chosen.
		equilibrium/time_slice/boundary_separatrix/dr_dz_zero_point/z"""
  
	z_zero = 3
	"""Midplane defined by z = 0"""
  
	ggd_subset = 4
	"""Midplane location is specified by means of the GGD grid subset for the inner and
		outer midplanes, if the midplane choice is different from the other available
		options. If the GGD midplane subset corresponds to one of the other available
		options, select that particular option to indicate it"""
  

class _E_midplane_identifier(IntFlag):
	"""Translation table for identifying different midplane definitions	xpath: 	"""
  
	magnetic_axis = 1
	"""Midplane defined by the height of magnetic axis
		equilibrium/time_slice/global_quantities/magnetic_axis/z"""
  
	dr_dz_zero_sep = 2
	"""Midplane defined by the height of the outboard point on the separatrix on which
		dr/dz = 0 (local maximum of the major radius of the separatrix). In case of
		multiple local maxima, the closest one from z=z_magnetic_axis is chosen.
		equilibrium/time_slice/boundary_separatrix/dr_dz_zero_point/z"""
  
	z_zero = 3
	"""Midplane defined by z = 0"""
  
	ggd_subset = 4
	"""Midplane location is specified by means of the GGD grid subset for the inner and
		outer midplanes, if the midplane choice is different from the other available
		options. If the GGD midplane subset corresponds to one of the other available
		options, select that particular option to indicate it"""
  

class _E_poloidal_plane_coordinates_identifier(IntFlag):
	"""List of coordinate systems for describing the poloidal plane	xpath: 	"""
  
	rectangular = 1
	"""Cylindrical R,Z ala eqdsk (R=dim1, Z=dim2). In this case the position arrays
		should not be filled since they are redundant with grid/dim1 and dim2."""
  
	inverse = 2
	"""Rhopolar_polar 2D polar coordinates (rho=dim1, theta=dim2) with magnetic axis as
		centre of grid; theta and values following the COCOS=11 convention; the polar
		angle is theta=atan2(z-zaxis,r-raxis)"""
  
	inverse_psi_straight_field_line = 11
	"""Flux surface type with psi as radial label (dim1) and the straight-field line
		poloidal angle (mod(index,10)=1) (dim2); could be non-equidistant; magnetic axis
		as centre of grid; following the COCOS=11 convention"""
  
	inverse_psi_equal_arc = 12
	"""Flux surface type with psi as radial label (dim1) and the equal arc poloidal
		angle (mod(index,10)=2) (dim2)"""
  
	inverse_psi_polar = 13
	"""Flux surface type with psi as radial label (dim1) and the polar poloidal angle
		(mod(index,10)=3) (dim2); could be non-equidistant"""
  
	inverse_psi_straight_field_line_fourier = 14
	"""Flux surface type with psi as radial label (dim1) and Fourier modes in the
		straight-field line poloidal angle (mod(index,10)=4) (dim2), could be
		non-equidistant; magnetic axis as centre of grid; following the COCOS=11
		convention"""
  
	inverse_psi_equal_arc_fourier = 15
	"""Flux surface type with psi as radial label (dim1) and Fourier modes in the equal
		arc poloidal angle (mod(index,10)=5) (dim2)"""
  
	inverse_psi_polar_fourier = 16
	"""Flux surface type with psi as radial label (dim1) and Fourier modes in the polar
		poloidal angle (mod(index,10)=6) (dim2); could be non-equidistant"""
  
	inverse_rhopolnorm_straight_field_line = 21
	"""Flux surface type with radial label sqrt[(psi-psi_axis)/(psi_edge-psi_axis)]
		(dim1) and the straight-field line poloidal angle (dim2)"""
  
	inverse_rhopolnorm_equal_arc = 22
	"""Flux surface type with radial label sqrt[(psi-psi_axis)/(psi_edge-psi_axis)]
		(dim1) and the equal arc poloidal angle (dim2)"""
  
	inverse_rhopolnorm_polar = 23
	"""Flux surface type with radial label sqrt[(psi-psi_axis)/(psi_edge-psi_axis)]
		(dim1) and the polar poloidal angle (dim2)"""
  
	inverse_rhopolnorm_straight_field_line_fourier = 24
	"""Flux surface type with radial label sqrt[(psi-psi_axis)/(psi_edge-psi_axis)]
		(dim1) and Fourier modes in the straight-field line poloidal angle (dim2)"""
  
	inverse_rhopolnorm_equal_arc_fourier = 25
	"""Flux surface type with radial label sqrt[(psi-psi_axis)/(psi_edge-psi_axis)]
		(dim1) and Fourier modes in the equal arc poloidal angle (dim2)"""
  
	inverse_rhopolnorm_polar_fourier = 26
	"""Flux surface type with radial label sqrt[(psi-psi_axis)/(psi_edge-psi_axis)]
		(dim1) and Fourier modes in the polar poloidal angle (dim2)"""
  
	inverse_rhotornorm_straight_field_line = 31
	"""Flux surface type with radial label sqrt[Phi/Phi_edge] (dim1) and the
		straight-field line poloidal angle (dim2)"""
  
	inverse_rhotornorm_equal_arc = 32
	"""Flux surface type with radial label sqrt[Phi/Phi_edge] (dim1) and the equal arc
		poloidal angle (dim2)"""
  
	inverse_rhotornorm_polar = 33
	"""Flux surface type with radial label sqrt[Phi/Phi_edge] (dim1) and the polar
		poloidal angle (dim2)"""
  
	inverse_rhotornorm_straight_field_line_fourier = 34
	"""Flux surface type with radial label sqrt[Phi/Phi_edge] (dim1) and Fourier modes
		in the straight-field line poloidal angle (dim2)"""
  
	inverse_rhotornorm_equal_arc_fourier = 35
	"""Flux surface type with radial label sqrt[Phi/Phi_edge] (dim1) and Fourier modes
		in the equal arc poloidal angle (dim2)"""
  
	inverse_rhotornorm_polar_fourier = 36
	"""Flux surface type with radial label sqrt[Phi/Phi_edge] (dim1) and Fourier modes
		in the polar poloidal angle (dim2)"""
  
	inverse_rhopol_straight_field_line = 41
	"""Flux surface type with radial label sqrt[psi-psi_axis] (dim1) and the
		straight-field line poloidal angle (dim2)"""
  
	inverse_rhopol_equal_arc = 42
	"""Flux surface type with radial label sqrt[psi-psi_axis] (dim1) and the equal arc
		poloidal angle (dim2)"""
  
	inverse_rhopol_polar = 43
	"""Flux surface type with radial label sqrt[psi-psi_axis] (dim1) and the polar
		poloidal angle (dim2)"""
  
	inverse_rhopol_straight_field_line_fourier = 44
	"""Flux surface type with radial label sqrt[psi-psi_axis] (dim1) and Fourier modes
		in the straight-field line poloidal angle (dim2)"""
  
	inverse_rhopol_equal_arc_fourier = 45
	"""Flux surface type with radial label sqrt[psi-psi_axis] (dim1) and Fourier modes
		in the equal arc poloidal angle (dim2)"""
  
	inverse_rhopol_polar_fourier = 46
	"""Flux surface type with radial label sqrt[psi-psi_axis] (dim1) and Fourier modes
		in the polar poloidal angle (dim2)"""
  
	inverse_rhotor_straight_field_line = 51
	"""Flux surface type with radial label sqrt[Phi/pi/B0] (dim1), Phi being toroidal
		flux, and the straight-field line poloidal angle (dim2)"""
  
	inverse_rhotor_equal_arc = 52
	"""Flux surface type with radial label sqrt[Phi/pi/B0] (dim1), Phi being toroidal
		flux, and the equal arc poloidal angle (dim2)"""
  
	inverse_rhotor_polar = 53
	"""Flux surface type with radial label sqrt[Phi/pi/B0] (dim1), Phi being toroidal
		flux, and the polar poloidal angle (dim2)"""
  
	inverse_rhotor_straight_field_line_fourier = 54
	"""Flux surface type with radial label sqrt[Phi/pi/B0] (dim1), Phi being toroidal
		flux, and Fourier modes in the straight-field line poloidal angle (dim2)"""
  
	inverse_rhotor_equal_arc_fourier = 55
	"""Flux surface type with radial label sqrt[Phi/pi/B0] (dim1), Phi being toroidal
		flux, and Fourier modes in the equal arc poloidal angle (dim2)"""
  
	inverse_rhotor_polar_fourier = 56
	"""Flux surface type with radial label sqrt[Phi/pi/B0] (dim1), Phi being toroidal
		flux, and Fourier modes in the polar poloidal angle (dim2)"""
  
	irregular_rz_na = 91
	"""Irregular grid, thus give list of vertices in dim1(1:ndim1), dim2(1:ndim1) and
		then all fields are on values(1:ndim1,1)"""
  

class _E_materials(IntFlag):
	"""Materials used in the device mechanical structures	xpath: 	"""
  
	unspecified = 0
	"""unspecified"""
  
	C = 1
	"""Carbon"""
  
	W = 2
	"""Tungsten"""
  
	C_W_coating = 3
	"""Carbon with tungsten coating"""
  
	SS = 4
	"""Stainless steel"""
  
	SS_C_coating = 5
	"""Stainless steel with carbon coating"""
  
	IN = 6
	"""Inconel"""
  
	IN_C_coating = 7
	"""Inconel with carbon coating"""
  
	B_C = 8
	"""Boron carbide"""
  
	Ti_C_coating = 9
	"""Titanium with carbon coating"""
  
	Be = 10
	"""Beryllium"""
  
	Mo = 11
	"""Molybdenum"""
  
	Quartz = 12
	"""Quartz"""
  
	Ge = 13
	"""Germanium"""
  
	Si = 14
	"""Silicon"""
  
	LiF = 15
	"""Lithium fluoride"""
  
	InSb = 16
	"""Indium antimonide"""
  

class _T_identifier(SpTree):
	"""Standard type for identifiers (constant). The three fields: name, index and
		description are all representations of the same information. Associated with
		each application of this identifier-type, there should be a translation table
		defining the three fields for all objects to be identified."""

	name  :str =  sp_property(type="constant")
	""" Short string identifier"""

	index  :int =  sp_property(type="constant")
	""" Integer identifier (enumeration index within a list). Private identifier values
		must be indicated by a negative index."""

	description  :str =  sp_property(type="constant")
	""" Verbose description"""


class _T_identifier_static(SpTree):
	"""Standard type for identifiers (static). The three fields: name, index and
		description are all representations of the same information. Associated with
		each application of this identifier-type, there should be a translation table
		defining the three fields for all objects to be identified."""

	name  :str =  sp_property(type="static")
	""" Short string identifier"""

	index  :int =  sp_property(type="static")
	""" Integer identifier (enumeration index within a list). Private identifier values
		must be indicated by a negative index."""

	description  :str =  sp_property(type="static")
	""" Verbose description"""


class _T_identifier_static_1d(SpTree):
	"""Standard type for identifiers (static, 1D). The three fields: name, index and
		description are all representations of the same information. Associated with
		each application of this identifier-type, there should be a translation table
		defining the three fields for all objects to be identified."""

	names  :List[str] =  sp_property(type="static",coordinate1="1...N")
	""" Short string identifiers"""

	indices  :array_type =  sp_property(type="static",coordinate1="../names")
	""" Integer identifiers (enumeration index within a list). Private identifier values
		must be indicated by a negative index."""

	descriptions  :List[str] =  sp_property(type="static",coordinate1="../names")
	""" Verbose description"""


class _T_identifier_dynamic_aos3_1d(SpTree):
	"""Standard type for identifiers (1D arrays for each node), dynamic within type 3
		array of structures (index on time). The three fields: name, index and
		description are all representations of the same information. Associated with
		each application of this identifier-type, there should be a translation table
		defining the three fields for all objects to be identified.
	aos3Parent: yes"""

	names  :List[str] =  sp_property(type="dynamic",coordinate1="1...N")
	""" Short string identifiers"""

	indices  :array_type =  sp_property(type="dynamic",coordinate1="../names")
	""" Integer identifiers (enumeration index within a list). Private identifier values
		must be indicated by a negative index."""

	descriptions  :List[str] =  sp_property(type="dynamic",coordinate1="../names")
	""" Verbose description"""


class _T_identifier_dynamic_aos3(SpTree):
	"""Standard type for identifiers (dynamic within type 3 array of structures (index
		on time)). The three fields: name, index and description are all representations
		of the same information. Associated with each application of this
		identifier-type, there should be a translation table defining the three fields
		for all objects to be identified.
	aos3Parent: yes"""

	name  :str =  sp_property(type="dynamic")
	""" Short string identifier"""

	index  :int =  sp_property(type="dynamic")
	""" Integer identifier (enumeration index within a list). Private identifier values
		must be indicated by a negative index."""

	description  :str =  sp_property(type="dynamic")
	""" Verbose description"""


class _T_data_flt_0d_constant_validity(SpTree):
	"""Constant data (FLT_0D) with validity flag"""

	data  :float =  sp_property(type="constant",units="as_parent")
	""" Data"""

	validity  :int =  sp_property(type="constant")
	""" Indicator of the validity of the data for the whole acquisition period. 0: valid
		from automated processing, 1: valid and certified by the diagnostic RO; - 1
		means problem identified in the data processing (request verification by the
		diagnostic RO), -2: invalid data, should not be used (values lower than -2 have
		a code-specific meaning detailing the origin of their invalidity)"""


class _T_physical_quantity_flt_1d_time_1(SpTree):
	"""Similar to a signal (FLT_1D) but with time base one level above (NB : since this
		is described in the utilities section, the timebase must be directly below the
		closest AoS)"""

	data  :Expression  =  sp_property(type="dynamic",units="as_parent",coordinate1="../../time",utilities_aoscontext="yes")
	""" Data"""

	validity_timed  :array_type =  sp_property(type="dynamic",coordinate1="../../time",utilities_aoscontext="yes")
	""" Indicator of the validity of the data for each time slice. 0: valid from
		automated processing, 1: valid and certified by the diagnostic RO; - 1 means
		problem identified in the data processing (request verification by the
		diagnostic RO), -2: invalid data, should not be used (values lower than -2 have
		a code-specific meaning detailing the origin of their invalidity)"""

	validity  :int =  sp_property(type="constant")
	""" Indicator of the validity of the data for the whole acquisition period. 0: valid
		from automated processing, 1: valid and certified by the diagnostic RO; - 1
		means problem identified in the data processing (request verification by the
		diagnostic RO), -2: invalid data, should not be used (values lower than -2 have
		a code-specific meaning detailing the origin of their invalidity)"""


class _T_physical_quantity_flt_2d_time_1(SpTree):
	"""Similar to a signal (FLT_2D) but with time base one level above (NB : since this
		is described in the utilities section, the timebase must be directly below the
		closest AoS)"""

	data  :array_type =  sp_property(type="dynamic",units="as_parent",coordinate1="1...N",coordinate2="../../time",utilities_aoscontext="yes")
	""" Data"""

	validity_timed  :array_type =  sp_property(type="dynamic",coordinate1="../../time",utilities_aoscontext="yes")
	""" Indicator of the validity of the data for each time slice. 0: valid from
		automated processing, 1: valid and certified by the diagnostic RO; - 1 means
		problem identified in the data processing (request verification by the
		diagnostic RO), -2: invalid data, should not be used (values lower than -2 have
		a code-specific meaning detailing the origin of their invalidity)"""

	validity  :int =  sp_property(type="constant")
	""" Indicator of the validity of the data for the whole acquisition period. 0: valid
		from automated processing, 1: valid and certified by the diagnostic RO; - 1
		means problem identified in the data processing (request verification by the
		diagnostic RO), -2: invalid data, should not be used (values lower than -2 have
		a code-specific meaning detailing the origin of their invalidity)"""


class _T_plasma_composition_ion_state_constant(SpTree):
	"""Definition of an ion state (when describing the plasma composition) (constant)"""

	z_min  :float =  sp_property(units="Elementary Charge Unit",type="constant")
	""" Minimum Z of the charge state bundle (z_min = z_max = 0 for a neutral)"""

	z_max  :float =  sp_property(units="Elementary Charge Unit",type="constant")
	""" Maximum Z of the charge state bundle (equal to z_min if no bundle)"""

	label  :str =  sp_property(type="constant")
	""" String identifying ion state (e.g. C+, C+2 , C+3, C+4, C+5, C+6, ...)"""

	electron_configuration  :str =  sp_property(type="constant")
	""" Configuration of atomic orbitals of this state, e.g. 1s2-2s1"""

	vibrational_level  :float =  sp_property(units="Elementary Charge Unit",type="constant")
	""" Vibrational level (can be bundled)"""

	vibrational_mode  :str =  sp_property(type="constant")
	""" Vibrational mode of this state, e.g. _A_g_. Need to define, or adopt a standard
		nomenclature."""


class _T_plasma_composition_ion_state(SpTree):
	"""Definition of an ion state (when describing the plasma composition) (within a
		type 3 AoS)
	aos3Parent: yes"""

	z_min  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Minimum Z of the charge state bundle (z_min = z_max = 0 for a neutral)"""

	z_max  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Maximum Z of the charge state bundle (equal to z_min if no bundle)"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying ion state (e.g. C+, C+2 , C+3, C+4, C+5, C+6, ...)"""

	electron_configuration  :str =  sp_property(type="dynamic")
	""" Configuration of atomic orbitals of this state, e.g. 1s2-2s1"""

	vibrational_level  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Vibrational level (can be bundled)"""

	vibrational_mode  :str =  sp_property(type="dynamic")
	""" Vibrational mode of this state, e.g. _A_g_. Need to define, or adopt a standard
		nomenclature."""


class _T_plasma_composition_species(SpTree):
	"""Description of simple species (elements) without declaration of their ionisation
		state"""

	a  :float =  sp_property(units="Atomic Mass Unit",type="constant")
	""" Mass of atom"""

	z_n  :float =  sp_property(units="Elementary Charge Unit",type="constant")
	""" Nuclear charge"""

	label  :str =  sp_property(type="constant")
	""" String identifying the species (e.g. H, D, T, ...)"""


class _T_plasma_composition_neutral_element_constant(SpTree):
	"""Element entering in the composition of the neutral atom or molecule (constant)"""

	a  :float =  sp_property(units="Atomic Mass Unit",type="constant")
	""" Mass of atom"""

	z_n  :float =  sp_property(units="Elementary Charge Unit",type="constant")
	""" Nuclear charge"""

	atoms_n  :int =  sp_property(type="constant")
	""" Number of atoms of this element in the molecule"""


class _T_plasma_composition_neutral_element(SpTree):
	"""Element entering in the composition of the neutral atom or molecule (within a
		type 3 AoS)
	aos3Parent: yes"""

	a  :float =  sp_property(units="Atomic Mass Unit",type="dynamic")
	""" Mass of atom"""

	z_n  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Nuclear charge"""

	atoms_n  :int =  sp_property(type="dynamic")
	""" Number of atoms of this element in the molecule"""


class _T_code_partial_constant(SpTree):
	"""Description of code-specific parameters and constant output flag"""

	parameters  :str =  sp_property(type="constant")
	""" List of the code specific parameters in XML format"""

	output_flag  :int =  sp_property(type="constant")
	""" Output flag : 0 means the run is successful, other values mean some difficulty
		has been encountered, the exact meaning is then code specific. Negative values
		mean the result shall not be used."""


class _T_code_constant(SpTree):
	"""Description of code-specific parameters without dynamic output_flag parameter"""

	name  :str =  sp_property(type="constant")
	""" Name of software used"""

	commit  :str =  sp_property(type="constant")
	""" Unique commit reference of software"""

	version  :str =  sp_property(type="constant")
	""" Unique version (tag) of software"""

	repository  :str =  sp_property(type="constant")
	""" URL of software repository"""

	parameters  :str =  sp_property(type="constant")
	""" List of the code specific parameters in XML format"""


class _T_library(SpTree):
	"""Library used by the code that has produced this IDS"""

	name  :str =  sp_property(type="constant")
	""" Name of software"""

	commit  :str =  sp_property(type="constant")
	""" Unique commit reference of software"""

	version  :str =  sp_property(type="constant")
	""" Unique version (tag) of software"""

	repository  :str =  sp_property(type="constant")
	""" URL of software repository"""

	parameters  :str =  sp_property(type="constant")
	""" List of the code specific parameters in XML format"""


class _T_b_tor_vacuum_1(SpTree):
	"""Characteristics of the vacuum toroidal field. Time coordinate at the root of the
		IDS"""

	r0  :float =  sp_property(type="constant",units="m")
	""" Reference major radius where the vacuum toroidal magnetic field is given
		(usually a fixed position such as the middle of the vessel at the equatorial
		midplane)"""

	b0  :Expression  =  sp_property(type="dynamic",units="T",coordinate1="/time",cocos_label_transformation="b0_like",cocos_transformation_expression=".sigma_b0_eff",cocos_leaf_name_aos_indices="IDSPATH.b0")
	""" Vacuum toroidal field at R0 [T]; Positive sign means anti-clockwise when viewing
		from above. The product R0B0 must be consistent with the b_tor_vacuum_r field of
		the tf IDS."""


class _T_b_tor_vacuum_aos3(SpTree):
	"""Characteristics of the vacuum toroidal field, dynamic within a type 3 AoS
	aos3Parent: yes"""

	r0  :float =  sp_property(type="dynamic",units="m")
	""" Reference major radius where the vacuum toroidal magnetic field is given
		(usually a fixed position such as the middle of the vessel at the equatorial
		midplane)"""

	b0  :float =  sp_property(type="dynamic",units="T")
	""" Vacuum toroidal field at b0. Positive sign means anti-clockwise when viewing
		from above. The product r0*b0 must be consistent with the b_tor_vacuum_r field
		of the tf IDS."""


class _T_core_profiles_vector_components_1(SpTree):
	"""Vector components in predefined directions for 1D profiles, assuming
		core_radial_grid one level above
	aos3Parent: yes"""

	radial  :Expression  =  sp_property(type="dynamic",coordinate1="../../grid/rho_tor_norm",units="as_parent")
	""" Radial component"""

	diamagnetic  :Expression  =  sp_property(type="dynamic",coordinate1="../../grid/rho_tor_norm",units="as_parent")
	""" Diamagnetic component"""

	parallel  :Expression  =  sp_property(type="dynamic",coordinate1="../../grid/rho_tor_norm",units="as_parent")
	""" Parallel component"""

	poloidal  :Expression  =  sp_property(type="dynamic",coordinate1="../../grid/rho_tor_norm",units="as_parent")
	""" Poloidal component"""

	toroidal  :Expression  =  sp_property(type="dynamic",coordinate1="../../grid/rho_tor_norm",units="as_parent")
	""" Toroidal component"""


class _T_core_profiles_vector_components_2(SpTree):
	"""Vector components in predefined directions for 1D profiles, assuming
		core_radial_grid two levels above
	aos3Parent: yes"""

	radial  :Expression  =  sp_property(type="dynamic",coordinate1="../../../grid/rho_tor_norm",units="as_parent")
	""" Radial component"""

	diamagnetic  :Expression  =  sp_property(type="dynamic",coordinate1="../../../grid/rho_tor_norm",units="as_parent")
	""" Diamagnetic component"""

	parallel  :Expression  =  sp_property(type="dynamic",coordinate1="../../../grid/rho_tor_norm",units="as_parent")
	""" Parallel component"""

	poloidal  :Expression  =  sp_property(type="dynamic",coordinate1="../../../grid/rho_tor_norm",units="as_parent")
	""" Poloidal component"""

	toroidal  :Expression  =  sp_property(type="dynamic",coordinate1="../../../grid/rho_tor_norm",units="as_parent")
	""" Toroidal component"""


class _T_core_profiles_vector_components_3(SpTree):
	"""Vector components in predefined directions for 1D profiles, assuming
		core_radial_grid 3 levels above
	aos3Parent: yes"""

	radial  :Expression  =  sp_property(type="dynamic",coordinate1="../../../../grid/rho_tor_norm",units="as_parent")
	""" Radial component"""

	diamagnetic  :Expression  =  sp_property(type="dynamic",coordinate1="../../../../grid/rho_tor_norm",units="as_parent")
	""" Diamagnetic component"""

	parallel  :Expression  =  sp_property(type="dynamic",coordinate1="../../../../grid/rho_tor_norm",units="as_parent")
	""" Parallel component"""

	poloidal  :Expression  =  sp_property(type="dynamic",coordinate1="../../../../grid/rho_tor_norm",units="as_parent")
	""" Poloidal component"""

	toroidal  :Expression  =  sp_property(type="dynamic",coordinate1="../../../../grid/rho_tor_norm",units="as_parent")
	""" Toroidal component"""


class _T_core_radial_grid(SpTree):
	"""1D radial grid for core* IDSs
	aos3Parent: yes"""

	rho_tor_norm  :array_type =  sp_property(type="dynamic",coordinate1="1...N",units="-")
	""" Normalised toroidal flux coordinate. The normalizing value for rho_tor_norm, is
		the toroidal flux coordinate at the equilibrium boundary (LCFS or 99.x % of the
		LCFS in case of a fixed boundary equilibium calculation, see
		time_slice/boundary/b_flux_pol_norm in the equilibrium IDS)"""

	rho_tor  :Expression  =  sp_property(type="dynamic",coordinate1="../rho_tor_norm",units="m")
	""" Toroidal flux coordinate. rho_tor = sqrt(b_flux_tor/(pi*b0)) ~
		sqrt(pi*r^2*b0/(pi*b0)) ~ r [m]. The toroidal field used in its definition is
		indicated under vacuum_toroidal_field/b0"""

	rho_pol_norm  :Expression  =  sp_property(type="dynamic",coordinate1="../rho_tor_norm",units="-")
	""" Normalised poloidal flux coordinate = sqrt((psi(rho)-psi(magnetic_axis)) /
		(psi(LCFS)-psi(magnetic_axis)))"""

	psi  :Expression  =  sp_property(coordinate1="../rho_tor_norm",units="Wb",type="dynamic",cocos_label_transformation="psi_like",cocos_transformation_expression=".fact_psi",cocos_leaf_name_aos_indices="IDSPATH.grid.psi")
	""" Poloidal magnetic flux"""

	volume  :Expression  =  sp_property(type="dynamic",coordinate1="../rho_tor_norm",units="m^3")
	""" Volume enclosed inside the magnetic surface"""

	area  :Expression  =  sp_property(type="dynamic",coordinate1="../rho_tor_norm",units="m^2")
	""" Cross-sectional area of the flux surface"""

	surface  :Expression  =  sp_property(type="dynamic",coordinate1="../rho_tor_norm",units="m^2")
	""" Surface area of the toroidal flux surface"""

	psi_magnetic_axis  :float =  sp_property(type="dynamic",units="Wb")
	""" Value of the poloidal magnetic flux at the magnetic axis (useful to normalize
		the psi array values when the radial grid doesn't go from the magnetic axis to
		the plasma boundary)"""

	psi_boundary  :float =  sp_property(type="dynamic",units="Wb")
	""" Value of the poloidal magnetic flux at the plasma boundary (useful to normalize
		the psi array values when the radial grid doesn't go from the magnetic axis to
		the plasma boundary)"""


class _T_detector_energy_band(SpTree):
	"""Detector energy band"""

	lower_bound  :float =  sp_property(type="static",units="eV")
	""" Lower bound of the energy band"""

	upper_bound  :float =  sp_property(type="static",units="eV")
	""" Upper bound of the energy band"""

	energies  :array_type =  sp_property(type="static",units="eV",coordinate1="1...N")
	""" Array of discrete energy values inside the band"""

	detection_efficiency  :array_type =  sp_property(type="static",units="-",coordinate1="../energies")
	""" Probability of detection of a photon impacting the detector as a function of its
		energy"""


class _T_detector_wavelength(SpTree):
	"""Detector wavelength range and detection efficiency"""

	wavelength_lower  :float =  sp_property(type="constant",units="m")
	""" Lower bound of the detector wavelength range"""

	wavelength_upper  :float =  sp_property(type="constant",units="m")
	""" Upper bound of the detector wavelength range"""

	wavelengths  :array_type =  sp_property(type="static",units="m",coordinate1="1...N")
	""" Array of wavelength values"""

	detection_efficiency  :array_type =  sp_property(type="static",units="-",coordinate1="../wavelengths")
	""" Probability of detection of a photon impacting the detector as a function of its
		wavelength"""


class _T_filter_wavelength(SpTree):
	"""Spectrocscopy filter wavelength range and detection efficiency"""

	wavelength_lower  :float =  sp_property(type="constant",units="m")
	""" Lower bound of the filter wavelength range"""

	wavelength_upper  :float =  sp_property(type="constant",units="m")
	""" Upper bound of the filter wavelength range"""

	wavelengths  :array_type =  sp_property(type="static",units="m",coordinate1="1...N")
	""" Array of wavelength values"""

	detection_efficiency  :array_type =  sp_property(type="static",units="-",coordinate1="../wavelengths")
	""" Probability of detection of a photon impacting the detector as a function of its
		wavelength"""


class _T_distribution_markers_orbit_instant(SpTree):
	"""Test particles for a given time slice : orbit integrals
	aos3Parent: yes"""

	expressions  :List[str] =  sp_property(coordinate1="1...N",type="dynamic")
	""" List of the expressions f(eq) used in the orbit integrals"""

	time_orbit  :array_type =  sp_property(coordinate1="1...N",type="dynamic",units="s")
	""" Time array along the markers last orbit"""

	values  :array_type =  sp_property(coordinate1="../expressions",coordinate2="../../weights",coordinate3="../time_orbit",units="-",type="dynamic")
	""" Values of the orbit integrals"""


class _T_distribution_markers_orbit(SpTree):
	"""Test particles for a given time slice : orbit integrals
	aos3Parent: yes"""

	expressions  :List[str] =  sp_property(coordinate1="1...N",type="dynamic")
	""" List of the expressions f(n_tor,m_pol,k,q,...) used in the orbit integrals"""

	n_tor  :List[int] =  sp_property(coordinate1="1...N",type="dynamic")
	""" Array of toroidal mode numbers, n_tor, where quantities vary as exp(i.n_tor.phi)
		and phi runs anticlockwise when viewed from above"""

	m_pol  :List[int] =  sp_property(coordinate1="1...N",type="dynamic")
	""" Array of poloidal mode numbers, where quantities vary as exp(-i.m_pol.theta) and
		theta is the angle defined by the choice of ../../coordinate_identifier, with
		its centre at the magnetic axis recalled at the root of this IDS"""

	bounce_harmonics  :List[int] =  sp_property(coordinate1="1...N",type="dynamic")
	""" Array of bounce harmonics k"""

	values  :array_type =  sp_property(coordinate1="../expressions",coordinate2="../../weights",coordinate3="../n_tor",coordinate4="../m_pol",coordinate5="../bounce_harmonics",units="-",type="dynamic")
	""" Values of the orbit integrals"""


class _T_generic_grid_scalar_single_position(SpTree):
	"""Scalar values at a single position on a generic grid (dynamic within a type 3
		AoS)
	aos3Parent: yes"""

	grid_index  :int =  sp_property(type="dynamic")
	""" Index of the grid used to represent this quantity"""

	grid_subset_index  :int =  sp_property(type="dynamic")
	""" Index of the grid subset the data is provided on"""

	value  :float =  sp_property(type="dynamic",units="as_parent")
	""" Scalar value of the quantity on the grid subset (corresponding to a single local
		position or to an integrated value over the subset)"""


class _T_generic_grid_scalar(SpTree):
	"""Scalar values on a generic grid (dynamic within a type 3 AoS)
	aos3Parent: yes"""

	grid_index  :int =  sp_property(type="dynamic")
	""" Index of the grid used to represent this quantity"""

	grid_subset_index  :int =  sp_property(type="dynamic")
	""" Index of the grid subset the data is provided on"""

	values  :array_type =  sp_property(type="dynamic",coordinate1="1...N",units="as_parent")
	""" One scalar value is provided per element in the grid subset."""

	coefficients  :array_type =  sp_property(type="dynamic",coordinate1="../values",coordinate2="1...N",units="as_parent")
	""" Interpolation coefficients, to be used for a high precision evaluation of the
		physical quantity with finite elements, provided per element in the grid subset
		(first dimension)."""


class _T_generic_grid_vector(SpTree):
	"""Vector values on a generic grid (dynamic within a type 3 AoS)
	aos3Parent: yes"""

	grid_index  :int =  sp_property(type="dynamic")
	""" Index of the grid used to represent this quantity"""

	grid_subset_index  :int =  sp_property(type="dynamic")
	""" Index of the grid subset the data is provided on"""

	values  :array_type =  sp_property(type="dynamic",coordinate1="1...N",coordinate2="1...N",units="as_parent")
	""" List of vector components, one list per element in the grid subset. First
		dimenstion: element index. Second dimension: vector component index."""

	coefficients  :array_type =  sp_property(type="dynamic",coordinate1="../values",coordinate2="1...N",coordinate3="1...N",units="as_parent")
	""" Interpolation coefficients, to be used for a high precision evaluation of the
		physical quantity with finite elements, provided per element in the grid subset
		(first dimension). Second dimension: vector component index. Third dimension:
		coefficient index"""


class _T_generic_grid_vector_components(SpTree):
	"""Vector components in predefined directions on a generic grid (dynamic within a
		type 3 AoS)
	aos3Parent: yes"""

	grid_index  :int =  sp_property(type="dynamic")
	""" Index of the grid used to represent this quantity"""

	grid_subset_index  :int =  sp_property(type="dynamic")
	""" Index of the grid subset the data is provided on"""

	radial  :array_type =  sp_property(type="dynamic",coordinate1="1...N",units="as_parent")
	""" Radial component, one scalar value is provided per element in the grid subset."""

	radial_coefficients  :array_type =  sp_property(type="dynamic",coordinate1="1...N",coordinate1_same_as="../radial",coordinate2="1...N",units="as_parent")
	""" Interpolation coefficients for the radial component, to be used for a high
		precision evaluation of the physical quantity with finite elements, provided per
		element in the grid subset (first dimension)."""

	diamagnetic  :array_type =  sp_property(type="dynamic",coordinate1="1...N",coordinate1_same_as="../radial",units="as_parent")
	""" Diamagnetic component, one scalar value is provided per element in the grid
		subset."""

	diamagnetic_coefficients  :array_type =  sp_property(type="dynamic",coordinate1="1...N",coordinate1_same_as="../radial",coordinate2="1...N",units="as_parent")
	""" Interpolation coefficients for the diamagnetic component, to be used for a high
		precision evaluation of the physical quantity with finite elements, provided per
		element in the grid subset (first dimension)."""

	parallel  :array_type =  sp_property(type="dynamic",coordinate1="1...N",coordinate1_same_as="../radial",units="as_parent")
	""" Parallel component, one scalar value is provided per element in the grid subset."""

	parallel_coefficients  :array_type =  sp_property(type="dynamic",coordinate1="1...N",coordinate1_same_as="../radial",coordinate2="1...N",units="as_parent")
	""" Interpolation coefficients for the parallel component, to be used for a high
		precision evaluation of the physical quantity with finite elements, provided per
		element in the grid subset (first dimension)."""

	poloidal  :array_type =  sp_property(type="dynamic",coordinate1="1...N",coordinate1_same_as="../radial",units="as_parent")
	""" Poloidal component, one scalar value is provided per element in the grid subset."""

	poloidal_coefficients  :array_type =  sp_property(type="dynamic",coordinate1="1...N",coordinate1_same_as="../radial",coordinate2="1...N",units="as_parent")
	""" Interpolation coefficients for the poloidal component, to be used for a high
		precision evaluation of the physical quantity with finite elements, provided per
		element in the grid subset (first dimension)."""

	toroidal  :array_type =  sp_property(type="dynamic",coordinate1="1...N",coordinate1_same_as="../radial",units="as_parent")
	""" Toroidal component, one scalar value is provided per element in the grid subset."""

	toroidal_coefficients  :array_type =  sp_property(type="dynamic",coordinate1="1...N",coordinate1_same_as="../radial",coordinate2="1...N",units="as_parent")
	""" Interpolation coefficients for the toroidal component, to be used for a high
		precision evaluation of the physical quantity with finite elements, provided per
		element in the grid subset (first dimension)."""

	r  :array_type =  sp_property(type="dynamic",coordinate1="1...N",coordinate1_same_as="../radial",units="as_parent",introduced_after_version="3.37.2")
	""" Component along the major radius axis, one scalar value is provided per element
		in the grid subset."""

	r_coefficients  :array_type =  sp_property(type="dynamic",coordinate1="1...N",coordinate1_same_as="../radial",coordinate2="1...N",units="as_parent",introduced_after_version="3.37.2")
	""" Interpolation coefficients for the component along the major radius axis, to be
		used for a high precision evaluation of the physical quantity with finite
		elements, provided per element in the grid subset (first dimension)."""

	z  :array_type =  sp_property(type="dynamic",coordinate1="1...N",coordinate1_same_as="../radial",units="as_parent",introduced_after_version="3.37.2")
	""" Component along the height axis, one scalar value is provided per element in the
		grid subset."""

	z_coefficients  :array_type =  sp_property(type="dynamic",coordinate1="1...N",coordinate1_same_as="../radial",coordinate2="1...N",units="as_parent",introduced_after_version="3.37.2")
	""" Interpolation coefficients for the component along the height axis, to be used
		for a high precision evaluation of the physical quantity with finite elements,
		provided per element in the grid subset (first dimension)."""


class _T_generic_grid_matrix(SpTree):
	"""Matrix values on a generic grid (dynamic within a type 3 AoS)
	aos3Parent: yes"""

	grid_index  :int =  sp_property(type="dynamic")
	""" Index of the grid used to represent this quantity"""

	grid_subset_index  :int =  sp_property(type="dynamic")
	""" Index of the grid subset the data is provided on"""

	values  :array_type =  sp_property(type="dynamic",coordinate1="1...N",coordinate2="1...N",coordinate3="1...N",units="as_parent")
	""" List of matrix components, one list per element in the grid subset. First
		dimenstion: element index. Second dimension: first matrix index. Third
		dimension: second matrix index."""

	coefficients  :array_type =  sp_property(type="dynamic",coordinate1="../values",coordinate2="1...N",coordinate3="1...N",coordinate4="1...N",units="as_parent")
	""" Interpolation coefficients, to be used for a high precision evaluation of the
		physical quantity with finite elements, provided per element in the grid subset
		(first dimension). Second dimension: first matrix index. Third dimension: second
		matrix index. Fourth dimension: coefficient index"""


class _T_generic_grid_dynamic_space_dimension_object_boundary(SpTree):
	"""Generic grid, description of an object boundary and its neighbours (dynamic
		within a type 3 AoS)
	aos3Parent: yes"""

	index  :int =  sp_property(type="dynamic")
	""" Index of this (n-1)-dimensional boundary object"""

	neighbours  :List[int] =  sp_property(coordinate1="1...N",type="dynamic")
	""" List of indices of the n-dimensional objects adjacent to the given n-dimensional
		object. An object can possibly have multiple neighbours on a boundary"""


class _T_generic_grid_dynamic_grid_subset_element_object(SpTree):
	"""Generic grid, object part of an element part of a grid_subset (dynamic within a
		type 3 AoS)
	aos3Parent: yes"""

	space  :int =  sp_property(type="dynamic")
	""" Index of the space from which that object is taken"""

	dimension  :int =  sp_property(type="dynamic")
	""" Dimension of the object"""

	index  :int =  sp_property(type="dynamic")
	""" Object index"""


class _T_generic_grid_dynamic_grid_subset_metric(SpTree):
	"""Generic grid, metric description for a given grid_subset and base (dynamic
		within a type 3 AoS)
	aos3Parent: yes"""

	jacobian  :array_type =  sp_property(type="dynamic",coordinate1="../../element",units="mixed")
	""" Metric Jacobian"""

	tensor_covariant  :array_type =  sp_property(type="dynamic",coordinate1="../../element",coordinate2="1...N",coordinate3="1...N",units="mixed")
	""" Covariant metric tensor, given on each element of the subgrid (first dimension)"""

	tensor_contravariant  :array_type =  sp_property(type="dynamic",coordinate1="../../element",coordinate2="1...N",coordinate2_same_as="../tensor_covariant",coordinate3="1...N",coordinate3_same_as="../tensor_covariant",units="mixed")
	""" Contravariant metric tensor, given on each element of the subgrid (first
		dimension)"""


class _T_equilibrium_profiles_2d_grid(SpTree):
	"""Definition of the 2D grid
	aos3Parent: yes"""

	dim1  :array_type =  sp_property(type="dynamic",coordinate1="1...N",units="mixed",cocos_label_transformation="grid_type_dim1_like",cocos_transformation_expression="grid_type_transformation(index_grid_type,1)",cocos_leaf_name_aos_indices="IDSPATH.grid.dim1")
	""" First dimension values"""

	dim2  :array_type =  sp_property(type="dynamic",coordinate1="1...N",units="mixed",cocos_label_transformation="grid_type_dim2_like",cocos_transformation_expression="grid_type_transformation(index_grid_type,2)",cocos_leaf_name_aos_indices="IDSPATH.grid.dim2")
	""" Second dimension values"""

	volume_element  :array_type =  sp_property(type="dynamic",coordinate1="../dim1",coordinate2="../dim2",units="m^3")
	""" Elementary plasma volume of plasma enclosed in the cell formed by the nodes
		[dim1(i) dim2(j)], [dim1(i+1) dim2(j)], [dim1(i) dim2(j+1)] and [dim1(i+1)
		dim2(j+1)]"""


class _T_delta_rzphi0d_static(SpTree):
	"""Structure for R, Z, Phi relative positions (0D, static)"""

	delta_r  :float =  sp_property(type="static",units="m")
	""" Major radius (relative to a reference point)"""

	delta_z  :float =  sp_property(type="static",units="m")
	""" Height (relative to a reference point)"""

	delta_phi  :float =  sp_property(type="static",units="rad")
	""" Toroidal angle (relative to a reference point)"""


class _T_delta_rzphi1d_static(SpTree):
	"""Structure for R, Z, Phi relative positions (1D, static)"""

	delta_r  :array_type =  sp_property(type="static",units="m",coordinate1="1...N")
	""" Major radii (relative to a reference point)"""

	delta_z  :array_type =  sp_property(type="static",units="m",coordinate1="../delta_r")
	""" Heights (relative to a reference point)"""

	delta_phi  :array_type =  sp_property(type="static",units="rad",coordinate1="../delta_r")
	""" Toroidal angles (relative to a reference point)"""


class _T_rzphi0d_static(SpTree):
	"""Structure for R, Z, Phi positions (0D, static)"""

	r  :float =  sp_property(type="static",units="m")
	""" Major radius"""

	z  :float =  sp_property(type="static",units="m")
	""" Height"""

	phi  :float =  sp_property(type="static",units="rad")
	""" Toroidal angle (oriented counter-clockwise when viewing from above)"""


class _T_rzphi0d_dynamic_aos3(SpTree):
	"""Structure for R, Z, Phi positions (0D, dynamic within a type 3 array of
		structures (index on time))
	aos3Parent: yes"""

	r  :float =  sp_property(type="dynamic",units="m")
	""" Major radius"""

	z  :float =  sp_property(type="dynamic",units="m")
	""" Height"""

	phi  :float =  sp_property(type="dynamic",units="rad")
	""" Toroidal angle (oriented counter-clockwise when viewing from above)"""


class _T_rzphi1d_grid(SpTree):
	"""R, Z, Phi structured grid, in which R, Z and phi don't necessarily have the same
		number of elements"""

	r  :array_type =  sp_property(type="constant",units="m",coordinate1="1...N")
	""" Major radius"""

	z  :array_type =  sp_property(type="constant",units="m",coordinate1="1...N")
	""" Height"""

	phi  :array_type =  sp_property(type="constant",units="rad",coordinate1="1...N")
	""" Toroidal angle (oriented counter-clockwise when viewing from above)"""


class _T_rzphi1d_static(SpTree):
	"""Structure for list of R, Z, Phi positions (1D, static)"""

	r  :array_type =  sp_property(type="static",units="m",coordinate1="1...N")
	""" Major radius"""

	z  :array_type =  sp_property(type="static",units="m",coordinate1="../r")
	""" Height"""

	phi  :array_type =  sp_property(type="static",units="rad",coordinate1="../r")
	""" Toroidal angle (oriented counter-clockwise when viewing from above)"""


class _T_rzphi2d_static(SpTree):
	"""Structure for list of R, Z, Phi positions (2D, static)"""

	r  :array_type =  sp_property(type="static",units="m",coordinate1="1...N",coordinate2="1...N")
	""" Major radius"""

	z  :array_type =  sp_property(type="static",units="m",coordinate1="1...N",coordinate1_same_as="../r",coordinate2="1...N",coordinate2_same_as="../r")
	""" Height"""

	phi  :array_type =  sp_property(type="static",units="rad",coordinate1="1...N",coordinate1_same_as="../r",coordinate2="1...N",coordinate2_same_as="../r")
	""" Toroidal angle (oriented counter-clockwise when viewing from above)"""


class _T_rzphirhopsitheta1d_dynamic_aos1_common_time_1(SpTree):
	"""Structure for list of R, Z, Phi, rho_tor_norm, psi, theta positions (1D, dynamic
		within a type 1 array of structures, assuming a common time array one level
		above"""

	r  :Expression  =  sp_property(type="dynamic",units="m",coordinate1="../../time",utilities_aoscontext="yes",change_nbc_version="3.26.0",change_nbc_description="leaf_renamed",change_nbc_previous_name="r/data")
	""" Major radius"""

	z  :Expression  =  sp_property(type="dynamic",units="m",coordinate1="../../time",utilities_aoscontext="yes",change_nbc_version="3.26.0",change_nbc_description="leaf_renamed",change_nbc_previous_name="z/data")
	""" Height"""

	phi  :Expression  =  sp_property(type="dynamic",units="rad",coordinate1="../../time",utilities_aoscontext="yes",change_nbc_version="3.26.0",change_nbc_description="leaf_renamed",change_nbc_previous_name="phi/data")
	""" Toroidal angle (oriented counter-clockwise when viewing from above)"""

	psi  :Expression  =  sp_property(type="dynamic",units="W",coordinate1="../../time",utilities_aoscontext="yes",change_nbc_version="3.26.0",change_nbc_description="leaf_renamed",change_nbc_previous_name="psi/data")
	""" Poloidal flux"""

	rho_tor_norm  :Expression  =  sp_property(units="-",type="dynamic",coordinate1="../../time",utilities_aoscontext="yes",change_nbc_version="3.26.0",change_nbc_description="leaf_renamed",change_nbc_previous_name="rho_tor_norm/data")
	""" Normalised toroidal flux coordinate"""

	theta  :Expression  =  sp_property(units="rad",type="dynamic",coordinate1="../../time",utilities_aoscontext="yes",change_nbc_version="3.26.0",change_nbc_description="leaf_renamed",change_nbc_previous_name="theta/data")
	""" Poloidal angle (oriented clockwise when viewing the poloidal cross section on
		the right hand side of the tokamak axis of symmetry, with the origin placed on
		the plasma magnetic axis)"""


class _T_rzphi1d_dynamic_aos3(SpTree):
	"""Structure for R, Z, Phi positions (1D, dynamic within a type 3 array of
		structure)
	aos3Parent: yes"""

	r  :array_type =  sp_property(type="dynamic",units="m",coordinate1="1...N")
	""" Major radius"""

	z  :array_type =  sp_property(type="dynamic",units="m",coordinate1="../r")
	""" Height"""

	phi  :array_type =  sp_property(type="dynamic",units="rad",coordinate1="../r")
	""" Toroidal angle (oriented counter-clockwise when viewing from above)"""


class _T_rzphipsitheta1d_dynamic_aos3(SpTree):
	"""Structure for R, Z, Phi, Psi, Theta positions (1D, dynamic within a type 3 array
		of structures)
	aos3Parent: yes"""

	r  :array_type =  sp_property(type="dynamic",units="m",coordinate1="1...N")
	""" Major radius"""

	z  :array_type =  sp_property(type="dynamic",units="m",coordinate1="../r")
	""" Height"""

	phi  :array_type =  sp_property(type="dynamic",units="rad",coordinate1="../r")
	""" Toroidal angle (oriented counter-clockwise when viewing from above)"""

	psi  :array_type =  sp_property(type="dynamic",units="Wb",coordinate1="../r")
	""" Poloidal flux"""

	theta  :array_type =  sp_property(type="dynamic",units="rad",coordinate1="../r")
	""" Poloidal angle (oriented clockwise when viewing the poloidal cross section on
		the right hand side of the tokamak axis of symmetry, with the origin placed on
		the plasma magnetic axis)"""


class _T_rz1d_constant(SpTree):
	"""Structure for list of R, Z positions (1D, constant)"""

	r  :array_type =  sp_property(type="constant",units="m",coordinate1="1...n_points")
	""" Major radius"""

	z  :array_type =  sp_property(type="constant",units="m",coordinate1="../r")
	""" Height"""


class _T_rz0d_dynamic_aos(SpTree):
	"""Structure for scalar R, Z positions, dynamic within a type 3 array of structures
		(index on time)
	aos3Parent: yes"""

	r  :float =  sp_property(type="dynamic",units="m")
	""" Major radius"""

	z  :float =  sp_property(type="dynamic",units="m")
	""" Height"""


class _T_rz1d_dynamic_aos(SpTree):
	"""Structure for list of R, Z positions (1D list of Npoints, dynamic within a type
		3 array of structures (index on time))
	aos3Parent: yes"""

	r  :array_type =  sp_property(type="dynamic",units="m",coordinate1="1...N")
	""" Major radius"""

	z  :array_type =  sp_property(type="dynamic",units="m",coordinate1="../r")
	""" Height"""


class _T_rz1d_dynamic_1(SpTree):
	"""Structure for list of R, Z positions (1D, dynamic), time at the root of the IDS"""

	r  :Expression  =  sp_property(type="dynamic",units="m",coordinate1="/time")
	""" Major radius"""

	z  :Expression  =  sp_property(type="dynamic",units="m",coordinate1="/time")
	""" Height"""


class _T_rz1d_static_closed_flag(SpTree):
	"""Structure for list of R, Z positions (1D, constant) and closed flag"""

	r  :array_type =  sp_property(type="static",units="m",coordinate1="1...N")
	""" Major radius"""

	z  :array_type =  sp_property(type="static",units="m",coordinate1="../r")
	""" Height"""

	closed  :int =  sp_property(type="static")
	""" Flag identifying whether the contour is closed (1) or open (0)"""


class _T_rz1d_static(SpTree):
	"""Structure for list of R, Z positions (1D, constant)"""

	r  :array_type =  sp_property(type="static",units="m",coordinate1="1...N")
	""" Major radius"""

	z  :array_type =  sp_property(type="static",units="m",coordinate1="../r")
	""" Height"""


class _T_x1x21d_static(SpTree):
	"""Structure for list of X1, X2 positions (1D, static)"""

	x1  :array_type =  sp_property(type="static",units="m",coordinate1="1...N")
	""" Positions along x1 axis"""

	x2  :array_type =  sp_property(type="static",units="m",coordinate1="../x1")
	""" Positions along x2 axis"""


class _T_xyz0d_static(SpTree):
	"""Structure for list of X, Y, Z components (0D, static)"""

	x  :float =  sp_property(type="static",units="m")
	""" Component along X axis"""

	y  :float =  sp_property(type="static",units="m")
	""" Component along Y axis"""

	z  :float =  sp_property(type="static",units="m")
	""" Component along Z axis"""


class _T_xyz2d_static(SpTree):
	"""Structure for list of X, Y, Z components (2D, static)"""

	x  :array_type =  sp_property(type="static",units="m",coordinate1="1...N",coordinate2="1...N")
	""" Component along X axis"""

	y  :array_type =  sp_property(type="static",units="m",coordinate1="1...N",coordinate1_same_as="../x",coordinate2="1...N",coordinate2_same_as="../x")
	""" Component along Y axis"""

	z  :array_type =  sp_property(type="static",units="m",coordinate1="1...N",coordinate1_same_as="../x",coordinate2="1...N",coordinate2_same_as="../x")
	""" Component along Z axis"""


class _T_rz0d_static(SpTree):
	"""Structure for a single R, Z position (0D, static)"""

	r  :float =  sp_property(type="static",units="m")
	""" Major radius"""

	z  :float =  sp_property(type="static",units="m")
	""" Height"""


class _T_rz0d_constant(SpTree):
	"""Structure for a single R, Z position (0D, constant)"""

	r  :float =  sp_property(type="constant",units="m")
	""" Major radius"""

	z  :float =  sp_property(type="constant",units="m")
	""" Height"""


class _T_entry_tag(SpTree):
	"""Tag qualifying an entry or a list of entries"""

	name  :str =  sp_property(type="constant")
	""" Name of the tag"""

	comment  :str =  sp_property(type="constant")
	""" Any comment describing the content of the tagged list of entries"""


class _T_oblique_static(SpTree):
	"""Description of a 2D parallelogram"""

	r  :float =  sp_property(type="static",units="m",url="utilities/parallelogram.svg")
	""" Major radius of the reference point (from which the alpha and beta angles are
		defined, marked by a + on the diagram)"""

	z  :float =  sp_property(type="static",units="m",url="utilities/parallelogram.svg")
	""" Height of the reference point (from which the alpha and beta angles are defined,
		marked by a + on the diagram)"""

	length_alpha  :float =  sp_property(type="static",units="m",url="utilities/parallelogram.svg")
	""" Length of the parallelogram side inclined with angle alpha with respect to the
		major radius axis"""

	length_beta  :float =  sp_property(type="static",units="m",url="utilities/parallelogram.svg")
	""" Length of the parallelogram side inclined with angle beta with respect to the
		height axis"""

	alpha  :float =  sp_property(type="static",units="rad",url="utilities/parallelogram.svg")
	""" Inclination of first angle measured counter-clockwise from horizontal outwardly
		directed radial vector (grad R)."""

	beta  :float =  sp_property(type="static",units="rad",url="utilities/parallelogram.svg")
	""" Inclination of second angle measured counter-clockwise from vertically upwards
		directed vector (grad Z). If both alpha and beta are zero (rectangle) then the
		simpler rectangular elements description should be used."""


class _T_arcs_of_circle_static(SpTree):
	"""Arcs of circle description of a 2D contour"""

	r  :array_type =  sp_property(type="static",units="m",coordinate1="1...N")
	""" Major radii of the start point of each arc of circle"""

	z  :array_type =  sp_property(type="static",units="m",coordinate1="../r")
	""" Height of the start point of each arc of circle"""

	curvature_radii  :array_type =  sp_property(type="static",units="m",coordinate1="../r")
	""" Curvature radius of each arc of circle"""


class _T_rectangle_static(SpTree):
	"""Rectangular description of a 2D object"""

	r  :float =  sp_property(type="static",units="m")
	""" Geometric centre R"""

	z  :float =  sp_property(type="static",units="m")
	""" Geometric centre Z"""

	width  :float =  sp_property(type="static",units="m")
	""" Horizontal full width"""

	height  :float =  sp_property(type="static",units="m")
	""" Vertical full height"""


class _T_annulus_static(SpTree):
	"""Annulus description (2D object)"""

	r  :float =  sp_property(type="static",units="m")
	""" Centre major radius"""

	z  :float =  sp_property(type="static",units="m")
	""" Centre height"""

	radius_inner  :float =  sp_property(type="static",units="m")
	""" Inner radius"""

	radius_outer  :float =  sp_property(type="static",units="m")
	""" Outer radius"""


class _T_temperature_reference(SpTree):
	"""Structure describing the reference temperature for which static data are given"""

	description  :str =  sp_property(type="static")
	""" Description of how the reference temperature is defined : for which object, at
		which location, ..."""

	data  :float =  sp_property(type="static",units="K")
	""" Reference temperature"""


class _T_version_dd_al(SpTree):
	"""Version of the access layer package used to PUT this IDS"""

	data_dictionary  :str =  sp_property(type="constant")
	""" Version of Data Dictionary used to PUT this IDS"""

	access_layer  :str =  sp_property(type="constant")
	""" Version of Access Layer used to PUT this IDS"""

	access_layer_language  :str =  sp_property(type="constant")
	""" Programming language of the Access Layer high level API used to PUT this IDS"""


class _T_data_entry(SpTree):
	"""Definition of a data entry"""

	user  :str =  sp_property(type="constant")
	""" Username"""

	machine  :str =  sp_property(type="constant")
	""" Name of the experimental device to which this data is related"""

	pulse_type  :str =  sp_property(type="constant")
	""" Type of the data entry, e.g. _pulse_, _simulation_, ..."""

	pulse  :int =  sp_property(type="constant")
	""" Pulse number"""

	run  :int =  sp_property(type="constant")
	""" Run number"""


class _T_ids_provenance_node(SpTree):
	"""Provenance information for a given node of the IDS"""

	path  :str =  sp_property(type="constant",url="utilities/IDS-path-syntax.md")
	""" Path of the node within the IDS, following the syntax given in the link below.
		If empty, means the provenance information applies to the whole IDS."""

	sources  :List[str] =  sp_property(type="constant",coordinate1="1...N",url="utilities/IMAS-URI-scheme.md")
	""" List of sources used to import or calculate this node, identified as explained
		below. In case the node is the result of of a calculation / data processing, the
		source is an input to the process described in the _code_ structure at the root
		of the IDS. The source can be an IDS (identified by a URI or a persitent
		identifier, see syntax in the link below) or non-IDS data imported directly from
		an non-IMAS database (identified by the command used to import the source, or
		the persistent identifier of the data source). Often data are obtained by a
		chain of processes, however only the last process input are recorded here. The
		full chain of provenance has then to be reconstructed recursively from the
		provenance information contained in the data sources."""


class _T_signal_flt_1d(SpTree):
	"""Signal (FLT_1D) with its time base"""

	data  :Expression  =  sp_property(type="dynamic",units="as_parent",coordinate1="../time")
	""" Data"""

	time  :array_type =  sp_property(type="dynamic",units="s",coordinate1="1...N")
	""" Time"""


class _T_signal_flt_1d_units_level_2(SpTree):
	"""Signal (FLT_1D) with its time base, data units 2 levels above"""

	data  :Expression  =  sp_property(type="dynamic",units="as_parent_level_2",coordinate1="../time")
	""" Data"""

	time  :array_type =  sp_property(type="dynamic",units="s",coordinate1="1...N")
	""" Time"""


class _T_signal_flt_1d_validity(SpTree):
	"""Signal (FLT_1D) with its time base and validity flags"""

	data  :Expression  =  sp_property(type="dynamic",units="as_parent",coordinate1="../time")
	""" Data"""

	validity_timed  :array_type =  sp_property(type="dynamic",coordinate1="../time")
	""" Indicator of the validity of the data for each time slice. 0: valid from
		automated processing, 1: valid and certified by the diagnostic RO; - 1 means
		problem identified in the data processing (request verification by the
		diagnostic RO), -2: invalid data, should not be used (values lower than -2 have
		a code-specific meaning detailing the origin of their invalidity)"""

	validity  :int =  sp_property(type="constant")
	""" Indicator of the validity of the data for the whole acquisition period. 0: valid
		from automated processing, 1: valid and certified by the diagnostic RO; - 1
		means problem identified in the data processing (request verification by the
		diagnostic RO), -2: invalid data, should not be used (values lower than -2 have
		a code-specific meaning detailing the origin of their invalidity)"""

	time  :array_type =  sp_property(type="dynamic",units="s",coordinate1="1...N")
	""" Time"""


class _T_signal_flt_1d_validity_position(SpTree):
	"""Signal (FLT_1D) with its time base and validity flags and rho_tor_norm position"""

	data  :Expression  =  sp_property(type="dynamic",units="as_parent",coordinate1="../time")
	""" Data"""

	rho_tor_norm  :Expression  =  sp_property(type="dynamic",units="-",coordinate1="../time")
	""" Normalised toroidal flux coordinate of the measurement"""

	validity_timed  :array_type =  sp_property(type="dynamic",coordinate1="../time")
	""" Indicator of the validity of the data for each time slice. 0: valid from
		automated processing, 1: valid and certified by the diagnostic RO; - 1 means
		problem identified in the data processing (request verification by the
		diagnostic RO), -2: invalid data, should not be used (values lower than -2 have
		a code-specific meaning detailing the origin of their invalidity)"""

	validity  :int =  sp_property(type="constant")
	""" Indicator of the validity of the data for the whole acquisition period. 0: valid
		from automated processing, 1: valid and certified by the diagnostic RO; - 1
		means problem identified in the data processing (request verification by the
		diagnostic RO), -2: invalid data, should not be used (values lower than -2 have
		a code-specific meaning detailing the origin of their invalidity)"""

	time  :array_type =  sp_property(type="dynamic",units="s",coordinate1="1...N")
	""" Time"""


class _T_signal_flt_2d(SpTree):
	"""Signal (FLT_2D) with its time base"""

	data  :array_type =  sp_property(type="dynamic",units="as_parent",coordinate1="1...N",coordinate2="../time")
	""" Data"""

	time  :array_type =  sp_property(type="dynamic",units="s",coordinate1="1...N")
	""" Time"""


class _T_signal_flt_2d_validity(SpTree):
	"""Signal (FLT_2D) with its time base and validity flags"""

	data  :array_type =  sp_property(type="dynamic",units="as_parent",coordinate1="1...N",coordinate2="../time")
	""" Data"""

	validity_timed  :array_type =  sp_property(type="dynamic",coordinate1="../time")
	""" Indicator of the validity of the data for each time slice. 0: valid from
		automated processing, 1: valid and certified by the diagnostic RO; - 1 means
		problem identified in the data processing (request verification by the
		diagnostic RO), -2: invalid data, should not be used (values lower than -2 have
		a code-specific meaning detailing the origin of their invalidity)"""

	validity  :int =  sp_property(type="constant")
	""" Indicator of the validity of the data for the whole acquisition period. 0: valid
		from automated processing, 1: valid and certified by the diagnostic RO; - 1
		means problem identified in the data processing (request verification by the
		diagnostic RO), -2: invalid data, should not be used (values lower than -2 have
		a code-specific meaning detailing the origin of their invalidity)"""

	time  :array_type =  sp_property(type="dynamic",units="s",coordinate1="1...N")
	""" Time"""


class _T_signal_flt_3d(SpTree):
	"""Signal (FLT_3D) with its time base"""

	data  :array_type =  sp_property(type="dynamic",units="as_parent",coordinate1="as_parent",coordinate2="as_parent",coordinate3="../time")
	""" Data"""

	time  :array_type =  sp_property(type="dynamic",units="s",coordinate1="1...N")
	""" Time"""


class _T_signal_flt_4d(SpTree):
	"""Signal (FLT_4D) with its time base"""

	data  :array_type =  sp_property(type="dynamic",units="as_parent",coordinate1="as_parent",coordinate2="as_parent",coordinate3="as_parent",coordinate4="../time")
	""" Data"""

	time  :array_type =  sp_property(type="dynamic",units="s",coordinate1="1...N")
	""" Time"""


class _T_signal_flt_5d(SpTree):
	"""Signal (FLT_5D) with its time base"""

	data  :array_type =  sp_property(type="dynamic",units="as_parent",coordinate1="as_parent",coordinate2="as_parent",coordinate3="as_parent",coordinate4="as_parent",coordinate5="../time")
	""" Data"""

	time  :array_type =  sp_property(type="dynamic",units="s",coordinate1="1...N")
	""" Time"""


class _T_signal_flt_6d(SpTree):
	"""Signal (FLT_6D) with its time base"""

	data  :array_type =  sp_property(type="dynamic",units="as_parent",coordinate1="as_parent",coordinate2="as_parent",coordinate3="as_parent",coordinate4="as_parent",coordinate5="as_parent",coordinate6="../time")
	""" Data"""

	time  :array_type =  sp_property(type="dynamic",units="s",coordinate1="1...N")
	""" Time"""


class _T_signal_int_1d(SpTree):
	"""Signal (INT_1D) with its time base"""

	data  :array_type =  sp_property(type="dynamic",coordinate1="../time")
	""" Data"""

	time  :array_type =  sp_property(type="dynamic",units="s",coordinate1="1...N")
	""" Time"""


class _T_signal_int_2d(SpTree):
	"""Signal (INT_2D) with its time base"""

	data  :array_type =  sp_property(type="dynamic",coordinate1="as_parent",coordinate2="../time")
	""" Data"""

	time  :array_type =  sp_property(type="dynamic",units="s",coordinate1="1...N")
	""" Time"""


class _T_signal_int_3d(SpTree):
	"""Signal (INT_3D) with its time base"""

	data  :array_type =  sp_property(type="dynamic",coordinate1="as_parent",coordinate2="as_parent",coordinate3="../time")
	""" Data"""

	time  :array_type =  sp_property(type="dynamic",units="s",coordinate1="1...N")
	""" Time"""


class _T_plasma_composition_neutral_state_constant(SpTree):
	"""Definition of a neutral state (when describing the plasma composition)
		(constant)"""

	label  :str =  sp_property(type="constant")
	""" String identifying neutral state"""

	electron_configuration  :str =  sp_property(type="constant")
	""" Configuration of atomic orbitals of this state, e.g. 1s2-2s1"""

	vibrational_level  :float =  sp_property(units="Elementary Charge Unit",type="constant")
	""" Vibrational level (can be bundled)"""

	vibrational_mode  :str =  sp_property(type="constant")
	""" Vibrational mode of this state, e.g. _A_g_. Need to define, or adopt a standard
		nomenclature."""

	neutral_type  :_E_neutrals_identifier =  sp_property(doc_identifier="utilities/neutrals_identifier.xml")
	""" Neutral type, in terms of energy. ID =1: cold; 2: thermal; 3: fast; 4: NBI"""


class _T_plasma_composition_ions_constant(SpTree):
	"""Description of plasma ions (constant)"""

	element  :AoS[_T_plasma_composition_neutral_element_constant] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	z_ion  :float =  sp_property(type="constant",units="Elementary Charge Unit")
	""" Ion charge (of the dominant ionisation state; lumped ions are allowed)"""

	label  :str =  sp_property(type="constant")
	""" String identifying ion (e.g. H+, D+, T+, He+2, C+, ...)"""

	state  :_T_plasma_composition_ion_state_constant =  sp_property()
	""" Quantities related to the different states of the species (ionisation, energy,
		excitation, ...)"""


class _T_gas_mixture_constant(SpTree):
	"""Description of a neutral species within a gas mixture (constant)
	coordinate1: 1...N"""

	element  :AoS[_T_plasma_composition_neutral_element_constant] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	label  :str =  sp_property(type="constant")
	""" String identifying neutral (e.g. H, D, T, He, C, ...)"""

	fraction  :float =  sp_property(type="constant",units="-")
	""" Relative fraction of this species (in molecules) in the gas mixture"""


class _T_plasma_composition_ions(SpTree):
	"""Array of plasma ions (within a type 3 AoS)
	aos3Parent: yes"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	z_ion  :float =  sp_property(type="dynamic",units="Elementary Charge Unit")
	""" Ion charge (of the dominant ionisation state; lumped ions are allowed)"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying ion (e.g. H+, D+, T+, He+2, C+, ...)"""

	multiple_states_flag  :int =  sp_property(type="constant")
	""" Multiple states calculation flag : 0-Only one state is considered; 1-Multiple
		states are considered and are described in the state structure"""

	state  :AoS[_T_plasma_composition_ion_state] =  sp_property(coordinate1="1...N")
	""" Quantities related to the different states of the species (ionisation, energy,
		excitation, ...)"""


class _T_plasma_composition_neutral(SpTree):
	"""Definition of a neutral atom or molecule"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	type  :AoS[_T_identifier] =  sp_property(coordinate1="1...N")
	""" List of neutral types, in terms of energy, considered for that neutral species.
		ID =1: cold; 2: thermal; 3: fast; 4: NBI"""

	label  :str =  sp_property(type="constant")
	""" String identifying the atom or molecule (e.g. D2, DT, CD4, ...)"""


class _T_psi_normalization(SpTree):
	"""Quantities used to normalize psi, as a function of time"""

	psi_magnetic_axis  :Expression  =  sp_property(type="dynamic",units="Wb",coordinate1="../time")
	""" Value of the poloidal magnetic flux at the magnetic axis"""

	psi_boundary  :Expression  =  sp_property(type="dynamic",units="Wb",coordinate1="../time")
	""" Value of the poloidal magnetic flux at the plasma boundary"""

	time  :array_type =  sp_property(units="s",type="dynamic",coordinate1="1...N")
	""" Time for the R,Z,phi coordinates"""


class _T_core_profiles_1D_fit(SpTree):
	"""Core profile fit information
	aos3Parent: yes"""

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


class _T_core_profiles_neutral_state(SpTree):
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

	temperature  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="eV",type="dynamic")
	""" Temperature"""

	density  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="m^-3",type="dynamic")
	""" Density (thermal+non-thermal)"""

	density_thermal  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="m^-3",type="dynamic")
	""" Density of thermal particles"""

	density_fast  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="m^-3",type="dynamic")
	""" Density of fast (non-thermal) particles"""

	pressure  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Pressure (thermal+non-thermal)"""

	pressure_thermal  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Pressure (thermal) associated with random motion ~average((v-average(v))^2)"""

	pressure_fast_perpendicular  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Fast (non-thermal) perpendicular pressure"""

	pressure_fast_parallel  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Fast (non-thermal) parallel pressure"""


class _T_distribution_markers(TimeSlice):
	"""Test particles for a given time slice
	aos3Parent: yes"""

	coordinate_identifier  :AoS[_E_coordinate] =  sp_property(coordinate1="1...N",units="W.m^-3",doc_identifier="utilities/coordinate_identifier.xml")
	""" Set of coordinate identifiers, coordinates on which the markers are represented"""

	weights  :array_type =  sp_property(coordinate1="1...N",units="-",type="dynamic")
	""" Weight of the markers, i.e. number of real particles represented by each marker.
		The dimension of the vector correspond to the number of markers"""

	positions  :array_type =  sp_property(coordinate1="../weights",coordinate2="../coordinate_identifier",units="mixed",type="dynamic")
	""" Position of the markers in the set of coordinates. The first dimension
		corresponds to the number of markers, the second dimension to the set of
		coordinates"""

	orbit_integrals  :_T_distribution_markers_orbit =  sp_property()
	""" Integrals along the markers orbit. These dimensionless expressions are of the
		form: (1/tau) integral (f(n_tor,m_pol,k,eq,...) dt) from time - tau to time,
		where tau is the transit/trapping time of the marker and f() a dimensionless
		function (phase factor,drift,etc) of the equilibrium (e.g. q) and perturbation
		(Fourier harmonics n_tor,m_pol and bounce harmonic k) along the particles
		orbits. In fact the integrals are taken during the last orbit of each marker at
		the time value of the time node below"""

	orbit_integrals_instant  :_T_distribution_markers_orbit_instant =  sp_property()
	""" Integrals/quantities along the markers orbit. These dimensionless expressions
		are of the form: (1/tau) integral ( f(eq) dt) from time - tau to time_orbit for
		different values of time_orbit in the interval from time - tau to time, where
		tau is the transit/trapping time of the marker and f(eq) a dimensionless
		function (phase, drift,q,etc) of the equilibrium along the markers orbits. The
		integrals are taken during the last orbit of each marker at the time value of
		the time node below"""

	toroidal_mode  :int =  sp_property(type="dynamic")
	""" In case the orbit integrals are calculated for a given MHD perturbation, index
		of the toroidal mode considered. Refers to the time_slice/toroidal_mode array of
		the MHD_LINEAR IDS in which this perturbation is described"""


class _T_distribution_process_identifier(SpTree):
	"""Identifier an NBI or fusion reaction process intervening affecting a
		distribution function"""

	type  :_E_distribution_source_identifier =  sp_property(doc_identifier="utilities/distribution_source_identifier.xml")
	""" Process type. index=1 for NBI; index=2 for nuclear reaction (reaction
		unspecified); index=3 for nuclear reaction: T(d,n)4He [D+T->He4+n]; index=4 for
		nuclear reaction: He3(d,p)4He [He3+D->He4+p]; index=5 for nuclear reaction:
		D(d,p)T [D+D->T+p]; index=6 for nuclear reaction: D(d,n)3He [D+D->He3+n];
		index=7 for runaway processes"""

	reactant_energy  :_T_identifier =  sp_property()
	""" For nuclear reaction source, energy of the reactants. index = 0 for a sum over
		all energies; index = 1 for thermal-thermal; index = 2 for beam-beam; index = 3
		for beam-thermal"""

	nbi_energy  :_T_identifier =  sp_property()
	""" For NBI source, energy of the accelerated species considered. index = 0 for a
		sum over all energies; index = 1 for full energiy; index = 2 for half energy;
		index = 3 for third energy"""

	nbi_unit  :int =  sp_property(type="constant")
	""" Index of the NBI unit considered. Refers to the _unit_ array of the NBI IDS. 0
		means sum over all NBI units."""

	nbi_beamlets_group  :int =  sp_property(type="constant")
	""" Index of the NBI beamlets group considered. Refers to the _unit/beamlets_group_
		array of the NBI IDS. 0 means sum over all beamlets groups."""


class _T_generic_grid_identifier(SpTree):
	"""Identifier values on a generic grid (dynamic within a type 3 AoS)
	aos3Parent: yes"""

	grid_index  :int =  sp_property(type="dynamic")
	""" Index of the grid used to represent this quantity"""

	grid_subset_index  :int =  sp_property(type="dynamic")
	""" Index of the grid subset the data is provided on"""

	identifiers  :_T_identifier_dynamic_aos3_1d =  sp_property()
	""" Identifier values, one value is provided per element in the grid subset. If the
		size of the child arrays is 1, their value applies to all elements of the
		subset."""


class _T_generic_grid_dynamic_space_dimension_object(SpTree):
	"""Generic grid, list of objects of a given dimension within a space (dynamic
		within a type 3 AoS)
	aos3Parent: yes"""

	boundary  :AoS[_T_generic_grid_dynamic_space_dimension_object_boundary] =  sp_property(coordinate1="1...N")
	""" Set of (n-1)-dimensional objects defining the boundary of this n-dimensional
		object"""

	geometry  :array_type =  sp_property(coordinate1="1...N",units="mixed",type="dynamic")
	""" Geometry data associated with the object, its detailed content is defined by
		../../geometry_content. Its dimension depends on the type of object, geometry
		and coordinate considered."""

	nodes  :List[int] =  sp_property(coordinate1="1...N",type="dynamic")
	""" List of nodes forming this object (indices to objects_per_dimension(1)%object(:)
		in Fortran notation)"""

	measure  :float =  sp_property(units="m^dimension",type="dynamic")
	""" Measure of the space object, i.e. physical size (length for 1d, area for 2d,
		volume for 3d objects,...)"""

	geometry_2d  :array_type =  sp_property(coordinate1="1...N",coordinate2="1...N",units="mixed",type="dynamic",introduced_after_version="3.35.0")
	""" 2D geometry data associated with the object. Its dimension depends on the type
		of object, geometry and coordinate considered. Typically, the first dimension
		represents the object coordinates, while the second dimension would represent
		the values of the various degrees of freedom of the finite element attached to
		the object."""


class _T_generic_grid_dynamic_grid_subset_element(SpTree):
	"""Generic grid, element part of a grid_subset (dynamic within a type 3 AoS)
	aos3Parent: yes"""

	object  :AoS[_T_generic_grid_dynamic_grid_subset_element_object] =  sp_property(coordinate1="1...N")
	""" Set of objects defining the element"""


class _T_geometry_matrix_emission(SpTree):
	"""Emission grid for the geometry matrix of a detector"""

	grid_type  :_E_spectrometer_visible_emissivity_grid_identifier =  sp_property(doc_identifier="utilities/emission_grid_identifier.xml")
	""" Grid type"""

	dim1  :array_type =  sp_property(type="static",coordinate1="1...N",units="mixed")
	""" First dimension values"""

	dim2  :array_type =  sp_property(type="static",coordinate1="1...N",units="mixed")
	""" Second dimension values"""

	dim3  :array_type =  sp_property(type="static",coordinate1="1...N",units="mixed")
	""" Third dimension values"""


class _T_equilibrium_coordinate_system(SpTree):
	"""Flux surface coordinate system on a square grid of flux and poloidal angle
	aos3Parent: yes"""

	grid_type  :_T_identifier_dynamic_aos3 =  sp_property()
	""" Type of coordinate system"""

	grid  :_T_equilibrium_profiles_2d_grid =  sp_property()
	""" Definition of the 2D grid"""

	r  :Field =  sp_property(type="dynamic",coordinate1="../grid/dim1",coordinate2="../grid/dim2",units="m")
	""" Values of the major radius on the grid"""

	z  :Field =  sp_property(type="dynamic",coordinate1="../grid/dim1",coordinate2="../grid/dim2",units="m")
	""" Values of the Height on the grid"""

	jacobian  :Field =  sp_property(type="dynamic",coordinate1="../grid/dim1",coordinate2="../grid/dim2",units="mixed")
	""" Absolute value of the jacobian of the coordinate system"""

	tensor_covariant  :array_type =  sp_property(type="dynamic",coordinate1="../grid/dim1",coordinate2="../grid/dim2",coordinate3="1...3",coordinate4="1...3",units="mixed",cocos_label_transformation="grid_type_tensor_covariant_like",cocos_transformation_expression="grid_type_transformation(index_grid_type,4)",cocos_leaf_name_aos_indices="IDSPATH.tensor_covariant")
	""" Covariant metric tensor on every point of the grid described by grid_type"""

	tensor_contravariant  :array_type =  sp_property(type="dynamic",coordinate1="../grid/dim1",coordinate2="../grid/dim2",coordinate3="1...3",coordinate4="1...3",units="mixed",cocos_label_transformation="grid_type_tensor_contravariant_like",cocos_transformation_expression="grid_type_transformation(index_grid_type,4)",cocos_leaf_name_aos_indices="IDSPATH.tensor_contravariant")
	""" Contravariant metric tensor on every point of the grid described by grid_type"""


class _T_rzphi1d_dynamic_aos1_common_time(SpTree):
	"""Structure for R, Z, Phi positions (1D, dynamic within a type 1 array of
		structure and with a common time base at the same level)"""

	r  :Expression  =  sp_property(type="dynamic",units="m",coordinate1="../time")
	""" Major radius"""

	z  :Expression  =  sp_property(type="dynamic",units="m",coordinate1="../time")
	""" Height"""

	phi  :Expression  =  sp_property(type="dynamic",units="rad",coordinate1="../time")
	""" Toroidal angle"""

	time  :array_type =  sp_property(units="s",type="dynamic",coordinate1="1...N")
	""" Time for the R,Z,phi coordinates"""


class _T_rz1d_dynamic_aos_time(TimeSlice):
	"""Structure for list of R, Z positions (1D list of Npoints, dynamic within a type
		3 array of structures (index on time), with time as sibling)
	aos3Parent: yes"""

	r  :array_type =  sp_property(type="dynamic",units="m",coordinate1="1...N")
	""" Major radius"""

	z  :array_type =  sp_property(type="dynamic",units="m",coordinate1="../r")
	""" Height"""


class _T_filter_window(SpTree):
	"""Characteristics of the filter window (largely derived from curved_object), with
		some filter specific additions"""

	identifier  :str =  sp_property(type="static")
	""" ID of the filter"""

	geometry_type  :_E_spectrometer_x_reflector_geometry =  sp_property(doc_identifier="utilities/curved_object_geometry_identifier.xml")
	""" Geometry of the filter contour. Note that there is some flexibility in the
		choice of the local coordinate system (X1,X2,X3). The data provider should
		choose the most convenient coordinate system for the filter, respecting the
		definitions of (X1,X2,X3) indicated below."""

	curvature_type  :_E_spectrometer_x_reflector_geometry =  sp_property(doc_identifier="utilities/curved_object_curvature_identifier.xml")
	""" Curvature of the filter."""

	centre  :_T_rzphi0d_static =  sp_property()
	""" Coordinates of the origin of the local coordinate system (X1,X2,X3) describing
		the filter. This origin is located within the filter area and should be the
		middle point of the filter surface. If geometry_type=2, it's the centre of the
		circular filter. If geometry_type=3, it's the centre of the rectangular filter."""

	radius  :float =  sp_property(type="static",units="m")
	""" Radius of the circle, used only if geometry_type/index = 2"""

	x1_unit_vector  :_T_xyz0d_static =  sp_property(url="utilities/detector_aperture_coordinates.svg")
	""" Components of the X1 direction unit vector in the (X,Y,Z) coordinate system,
		where X is the major radius axis for phi = 0, Y is the major radius axis for phi
		= pi/2, and Z is the height axis. The X1 vector is more horizontal than X2 (has
		a smaller abs(Z) component) and oriented in the positive phi direction
		(counter-clockwise when viewing from above)."""

	x2_unit_vector  :_T_xyz0d_static =  sp_property(url="utilities/detector_aperture_coordinates.svg")
	""" Components of the X2 direction unit vector in the (X,Y,Z) coordinate system,
		where X is the major radius axis for phi = 0, Y is the major radius axis for phi
		= pi/2, and Z is the height axis. The X2 axis is orthonormal so that uX2 = uX3 x
		uX1."""

	x3_unit_vector  :_T_xyz0d_static =  sp_property(url="utilities/detector_aperture_coordinates.svg")
	""" Components of the X3 direction unit vector in the (X,Y,Z) coordinate system,
		where X is the major radius axis for phi = 0, Y is the major radius axis for phi
		= pi/2, and Z is the height axis. The X3 axis is normal to the filter surface
		and oriented towards the plasma."""

	x1_width  :float =  sp_property(type="static",units="m")
	""" Full width of the filter in the X1 direction, used only if geometry_type/index =
		3"""

	x2_width  :float =  sp_property(type="static",units="m")
	""" Full width of the filter in the X2 direction, used only if geometry_type/index =
		3"""

	outline  :_T_x1x21d_static =  sp_property()
	""" Irregular outline of the filter in the (X1, X2) coordinate system, used only if
		geometry_type/index=1. Do NOT repeat the first point."""

	x1_curvature  :float =  sp_property(type="static",units="m")
	""" Radius of curvature in the X1 direction, to be filled only for
		curvature_type/index = 2, 4 or 5"""

	x2_curvature  :float =  sp_property(type="static",units="m")
	""" Radius of curvature in the X2 direction, to be filled only for
		curvature_type/index = 3 or 5"""

	surface  :float =  sp_property(type="static",units="m^2")
	""" Surface of the filter, derived from the above geometric data"""

	material  :_E_materials =  sp_property(doc_identifier="utilities/materials_identifier.xml")
	""" Material of the filter window"""

	thickness  :float =  sp_property(type="static",units="m")
	""" Thickness of the filter window"""

	wavelength_lower  :float =  sp_property(type="constant",units="m")
	""" Lower bound of the filter wavelength range"""

	wavelength_upper  :float =  sp_property(type="constant",units="m")
	""" Upper bound of the filter wavelength range"""

	wavelengths  :array_type =  sp_property(type="static",units="m",coordinate1="1...N")
	""" Array of wavelength values"""

	photon_absorption  :array_type =  sp_property(type="static",units="-",coordinate1="../wavelengths")
	""" Probability of absorbing a photon passing through the filter as a function of
		its wavelength"""


class _T_detector_aperture(SpTree):
	"""Generic description of a plane detector or collimating aperture"""

	geometry_type  :int =  sp_property(Type="static")
	""" Type of geometry used to describe the surface of the detector or aperture
		(1:'outline', 2:'circular', 3:'rectangle'). In case of 'outline', the surface is
		described by an outline of point in a local coordinate system defined by a
		centre and three unit vectors X1, X2, X3. Note that there is some flexibility
		here and the data provider should choose the most convenient coordinate system
		for the object, respecting the definitions of (X1,X2,X3) indicated below. In
		case of 'circular', the surface is a circle defined by its centre, radius, and
		normal vector oriented towards the plasma X3. In case of 'rectangle', the
		surface is a rectangle defined by its centre, widths in the X1 and X2
		directions, and normal vector oriented towards the plasma X3."""

	centre  :_T_rzphi0d_static =  sp_property()
	""" If geometry_type=2, coordinates of the centre of the circle. If geometry_type=1
		or 3, coordinates of the origin of the local coordinate system (X1,X2,X3)
		describing the plane detector/aperture. This origin is located within the
		detector/aperture area."""

	radius  :float =  sp_property(type="static",units="m")
	""" Radius of the circle, used only if geometry_type = 2"""

	x1_unit_vector  :_T_xyz0d_static =  sp_property(url="utilities/detector_aperture_coordinates.svg")
	""" Components of the X1 direction unit vector in the (X,Y,Z) coordinate system,
		where X is the major radius axis for phi = 0, Y is the major radius axis for phi
		= pi/2, and Z is the height axis. The X1 vector is more horizontal than X2 (has
		a smaller abs(Z) component) and oriented in the positive phi direction
		(counter-clockwise when viewing from above)."""

	x2_unit_vector  :_T_xyz0d_static =  sp_property(url="utilities/detector_aperture_coordinates.svg")
	""" Components of the X2 direction unit vector in the (X,Y,Z) coordinate system,
		where X is the major radius axis for phi = 0, Y is the major radius axis for phi
		= pi/2, and Z is the height axis. The X2 axis is orthonormal so that uX2 = uX3 x
		uX1."""

	x3_unit_vector  :_T_xyz0d_static =  sp_property(url="utilities/detector_aperture_coordinates.svg")
	""" Components of the X3 direction unit vector in the (X,Y,Z) coordinate system,
		where X is the major radius axis for phi = 0, Y is the major radius axis for phi
		= pi/2, and Z is the height axis. The X3 axis is normal to the detector/aperture
		plane and oriented towards the plasma."""

	x1_width  :float =  sp_property(type="static",units="m")
	""" Full width of the aperture in the X1 direction, used only if geometry_type = 3"""

	x2_width  :float =  sp_property(type="static",units="m")
	""" Full width of the aperture in the X2 direction, used only if geometry_type = 3"""

	outline  :_T_x1x21d_static =  sp_property()
	""" Irregular outline of the detector/aperture in the (X1, X2) coordinate system. Do
		NOT repeat the first point."""

	surface  :float =  sp_property(type="static",units="m^2")
	""" Surface of the detector/aperture, derived from the above geometric data"""


class _T_curved_object(SpTree):
	"""Generic description of a small plane or curved object (crystal, reflector, ...),
		using a generalization of the detector_aperture complexType"""

	identifier  :str =  sp_property(type="static")
	""" ID of the object"""

	geometry_type  :_E_spectrometer_x_reflector_geometry =  sp_property(doc_identifier="utilities/curved_object_geometry_identifier.xml")
	""" Geometry of the object contour. Note that there is some flexibility in the
		choice of the local coordinate system (X1,X2,X3). The data provider should
		choose the most convenient coordinate system for the object, respecting the
		definitions of (X1,X2,X3) indicated below."""

	curvature_type  :_E_spectrometer_x_reflector_geometry =  sp_property(doc_identifier="utilities/curved_object_curvature_identifier.xml")
	""" Curvature of the object."""

	material  :_E_materials =  sp_property(doc_identifier="utilities/materials_identifier.xml")
	""" Material of the object"""

	centre  :_T_rzphi0d_static =  sp_property()
	""" Coordinates of the origin of the local coordinate system (X1,X2,X3) describing
		the object. This origin is located within the object area and should be the
		middle point of the object surface. If geometry_type=2, it's the centre of the
		circular object. If geometry_type=3, it's the centre of the rectangular object."""

	radius  :float =  sp_property(type="static",units="m")
	""" Radius of the circle, used only if geometry_type/index = 2"""

	x1_unit_vector  :_T_xyz0d_static =  sp_property(url="utilities/detector_aperture_coordinates.svg")
	""" Components of the X1 direction unit vector in the (X,Y,Z) coordinate system,
		where X is the major radius axis for phi = 0, Y is the major radius axis for phi
		= pi/2, and Z is the height axis. The X1 vector is more horizontal than X2 (has
		a smaller abs(Z) component) and oriented in the positive phi direction
		(counter-clockwise when viewing from above)."""

	x2_unit_vector  :_T_xyz0d_static =  sp_property(url="utilities/detector_aperture_coordinates.svg")
	""" Components of the X2 direction unit vector in the (X,Y,Z) coordinate system,
		where X is the major radius axis for phi = 0, Y is the major radius axis for phi
		= pi/2, and Z is the height axis. The X2 axis is orthonormal so that uX2 = uX3 x
		uX1."""

	x3_unit_vector  :_T_xyz0d_static =  sp_property(url="utilities/detector_aperture_coordinates.svg")
	""" Components of the X3 direction unit vector in the (X,Y,Z) coordinate system,
		where X is the major radius axis for phi = 0, Y is the major radius axis for phi
		= pi/2, and Z is the height axis. The X3 axis is normal to the object surface
		and oriented towards the plasma."""

	x1_width  :float =  sp_property(type="static",units="m")
	""" Full width of the object in the X1 direction, used only if geometry_type/index =
		3"""

	x2_width  :float =  sp_property(type="static",units="m")
	""" Full width of the object in the X2 direction, used only if geometry_type/index =
		3"""

	outline  :_T_x1x21d_static =  sp_property()
	""" Irregular outline of the object in the (X1, X2) coordinate system, used only if
		geometry_type/index=1. Do NOT repeat the first point."""

	x1_curvature  :float =  sp_property(type="static",units="m")
	""" Radius of curvature in the X1 direction, to be filled only for
		curvature_type/index = 2, 4 or 5"""

	x2_curvature  :float =  sp_property(type="static",units="m")
	""" Radius of curvature in the X2 direction, to be filled only for
		curvature_type/index = 3 or 5"""

	surface  :float =  sp_property(type="static",units="m^2")
	""" Surface of the object, derived from the above geometric data"""


class _T_polarizer(SpTree):
	"""Generic description of a polarizer (extension of the detector_aperture complex
		type)"""

	centre  :_T_rzphi0d_static =  sp_property()
	""" If geometry_type=2, coordinates of the centre of the circle. If geometry_type=1
		or 3, coordinates of the origin of the local coordinate system (X1,X2,X3)
		describing the plane polarizer. This origin is located within the polarizer
		area. Note that there is some flexibility here and the data provider should
		choose the most convenient coordinate system for the object, respecting the
		definitions of (X1,X2,X3) indicated below."""

	radius  :float =  sp_property(type="static",units="m")
	""" Radius of the circle, used only if geometry_type = 2"""

	x1_unit_vector  :_T_xyz0d_static =  sp_property()
	""" Components of the X1 direction unit vector in the (X,Y,Z) coordinate system,
		where X is the major radius axis for phi = 0, Y is the major radius axis for phi
		= pi/2, and Z is the height axis. The X1 vector is more horizontal than X2 (has
		a smaller abs(Z) component) and oriented in the positive phi direction
		(counter-clockwise when viewing from above)."""

	x2_unit_vector  :_T_xyz0d_static =  sp_property()
	""" Components of the X2 direction unit vector in the (X,Y,Z) coordinate system,
		where X is the major radius axis for phi = 0, Y is the major radius axis for phi
		= pi/2, and Z is the height axis. The X2 axis is orthonormal so that uX2 = uX3 x
		uX1."""

	x3_unit_vector  :_T_xyz0d_static =  sp_property()
	""" Components of the X3 direction unit vector in the (X,Y,Z) coordinate system,
		where X is the major radius axis for phi = 0, Y is the major radius axis for phi
		= pi/2, and Z is the height axis. The X3 axis is normal to the polarizer plane
		and oriented towards the plasma."""

	polarization_angle  :float =  sp_property(type="static",units="rad")
	""" Alignment angle of the polarizer in the (x1,x2) plane. Electric fields parallel
		to the polarizer angle will be reflected. The angle is defined with respect to
		the x1 unit vector, positive in the counter-clockwise direction when looking
		towards the plasma"""


class _T_line_of_sight_2points_rz(SpTree):
	"""Generic description of a line of sight, defined by two points, in R and Z only"""

	first_point  :_T_rz0d_static =  sp_property()
	""" Position of the first point"""

	second_point  :_T_rz0d_static =  sp_property()
	""" Position of the second point"""


class _T_line_of_sight_2points(SpTree):
	"""Generic description of a line of sight, defined by two points"""

	first_point  :_T_rzphi0d_static =  sp_property()
	""" Position of the first point"""

	second_point  :_T_rzphi0d_static =  sp_property()
	""" Position of the second point"""


class _T_line_of_sight_2points_rzphi_2d(SpTree):
	"""Generic description of a line of sight, defined by two points"""

	first_point  :_T_rzphi2d_static =  sp_property()
	""" Position of the first point"""

	second_point  :_T_rzphi2d_static =  sp_property()
	""" Position of the second point"""


class _T_line_of_sight_2points_dynamic_aos3(SpTree):
	"""Generic description of a line of sight, defined by two points, dynamic within a
		type 3 array of structures (index on time)
	aos3Parent: yes"""

	first_point  :_T_rzphi0d_dynamic_aos3 =  sp_property()
	""" Position of the first point"""

	second_point  :_T_rzphi0d_dynamic_aos3 =  sp_property()
	""" Position of the second point"""


class _T_line_of_sight_3points(SpTree):
	"""Generic description of a line of sight, defined by two points (one way) and an
		optional third point to indicate the direction of reflection if the second point
		is e.g. the position of a mirror reflecting the line-of-sight"""

	first_point  :_T_rzphi0d_static =  sp_property()
	""" Position of the first point"""

	second_point  :_T_rzphi0d_static =  sp_property()
	""" Position of the second point"""

	third_point  :_T_rzphi0d_static =  sp_property()
	""" Position of the third point"""


class _T_thick_line_static(SpTree):
	"""2D contour approximated by two points and a thickness (in the direction
		perpendicular to the segment) in the poloidal cross-section"""

	first_point  :_T_rz0d_static =  sp_property()
	""" Position of the first point"""

	second_point  :_T_rz0d_static =  sp_property()
	""" Position of the second point"""

	thickness  :float =  sp_property(type="static",units="m")
	""" Thickness"""


class _T_vessel_2d_annular(SpTree):
	"""2D vessel annular description"""

	outline_inner  :_T_rz1d_static_closed_flag =  sp_property()
	""" Inner vessel outline. Do NOT repeat the first point for closed contours"""

	outline_outer  :_T_rz1d_static_closed_flag =  sp_property()
	""" Outer vessel outline. Do NOT repeat the first point for closed contours"""

	centreline  :_T_rz1d_static_closed_flag =  sp_property()
	""" Centreline, i.e. middle of the vessel layer as a series of point. Do NOT repeat
		the first point for closed contours"""

	thickness  :array_type =  sp_property(type="static",units="m",coordinate1="../centreline/r")
	""" Thickness of the vessel layer in the perpendicular direction to the centreline.
		Thickness(i) is the thickness of the layer between centreline/r(i),z(i) and
		centreline/r(i+1),z(i+1)"""

	resistivity  :float =  sp_property(type="static",units="ohm.m")
	""" Resistivity of the vessel unit"""


class _T_waves_coherent_wave_identifier(SpTree):
	"""Wave identifier"""

	type  :_E_wave_identifier =  sp_property(doc_identifier="utilities/wave_identifier.xml")
	""" Wave/antenna type. index=1 for name=EC; index=2 for name=IC; index=3 for name=LH"""

	antenna_name  :str =  sp_property(type="constant")
	""" Name of the antenna that launches this wave. Corresponds to the name specified
		in antennas/ec(i)/name, or antennas/ic(i)/name or antennas/lh(i)/name (depends
		of antenna/wave type) in the ANTENNAS IDS."""

	index_in_antenna  :int =  sp_property(type="constant")
	""" Index of the wave (starts at 1), separating different waves generated from a
		single antenna."""


class _T_ids_provenance(SpTree):
	"""Provenance information about the IDS"""

	node  :AoS[_T_ids_provenance_node] =  sp_property(type="constant",coordinate1="1...N")
	""" Set of IDS nodes for which the provenance is given. The provenance information
		applies to the whole structure below the IDS node. For documenting provenance
		information for the whole IDS, set the size of this array of structure to 1 and
		leave the child _path_ node empty"""


class _T_ids_identification(SpTree):
	"""Identifier of an IDS"""

	name  :str =  sp_property(type="constant")
	""" IDS name"""

	occurrence  :int =  sp_property(type="constant")
	""" IDS occurrence"""

	data_entry  :_T_data_entry =  sp_property()
	""" Data entry to which this IDS belongs"""


class _T_plasma_composition_neutral_constant(SpTree):
	"""Definition of plasma neutral (constant)
	coordinate1: 1...N"""

	element  :AoS[_T_plasma_composition_neutral_element_constant] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	label  :str =  sp_property(type="constant")
	""" String identifying neutral (e.g. H, D, T, He, C, ...)"""

	state  :_T_plasma_composition_neutral_state_constant =  sp_property()
	""" State of the species (energy, excitation, ...)"""


class _T_code_with_timebase(SpTree):
	"""Description of code-specific parameters when they are gathered below an array of
		structure (e.g. in case of multiple models or sources gathered in a single IDS).
		The only difference with the generic code element is the existence of a
		data+time structure for the dynamic signals (output_flag)"""

	name  :str =  sp_property(type="constant")
	""" Name of software used"""

	commit  :str =  sp_property(type="constant")
	""" Unique commit reference of software"""

	version  :str =  sp_property(type="constant")
	""" Unique version (tag) of software"""

	repository  :str =  sp_property(type="constant")
	""" URL of software repository"""

	parameters  :str =  sp_property(type="constant")
	""" List of the code specific parameters in XML format"""

	output_flag  :Signal =  sp_property()
	""" Output flag : 0 means the run is successful, other values mean some difficulty
		has been encountered, the exact meaning is then code specific. Negative values
		mean the result shall not be used."""


class _T_core_profiles_ions_charge_states2(SpTree):
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

	z_average_1d  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="-",type="dynamic")
	""" Average charge profile of the charge state bundle (equal to z_min if no bundle),
		= sum (Z*x_z) where x_z is the relative concentration of a given charge state in
		the bundle, i.e. sum(x_z) = 1 over the bundle."""

	z_average_square_1d  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="-",type="dynamic")
	""" Average square charge profile of the charge state bundle (equal to z_min squared
		if no bundle), = sum (Z^2*x_z) where x_z is the relative concentration of a
		given charge state in the bundle, i.e. sum(x_z) = 1 over the bundle."""

	ionisation_potential  :float =  sp_property(units="eV",type="dynamic")
	""" Cumulative and average ionisation potential to reach a given bundle. Defined as
		sum (x_z* (sum of Epot from z'=0 to z-1)), where Epot is the ionisation
		potential of ion Xz’+, and x_z is the relative concentration of a given charge
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

	rotation_frequency_tor  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="rad.s^-1",type="dynamic")
	""" Toroidal rotation frequency (i.e. toroidal velocity divided by the major radius
		at which the toroidal velocity is taken)"""

	temperature  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="eV",type="dynamic")
	""" Temperature"""

	density  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="m^-3",type="dynamic")
	""" Density (thermal+non-thermal)"""

	density_fit  :_T_core_profiles_1D_fit =  sp_property(units="m^-3")
	""" Information on the fit used to obtain the density profile"""

	density_thermal  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="m^-3",type="dynamic")
	""" Density of thermal particles"""

	density_fast  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="m^-3",type="dynamic")
	""" Density of fast (non-thermal) particles"""

	pressure  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Pressure (thermal+non-thermal)"""

	pressure_thermal  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Pressure (thermal) associated with random motion ~average((v-average(v))^2)"""

	pressure_fast_perpendicular  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Fast (non-thermal) perpendicular pressure"""

	pressure_fast_parallel  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Fast (non-thermal) parallel pressure"""


class _T_core_profile_neutral(SpTree):
	"""Quantities related to a given neutral species
	aos3Parent: yes"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying the species (e.g. H, D, T, He, C, D2, DT, CD4, ...)"""

	ion_index  :int =  sp_property(type="dynamic")
	""" Index of the corresponding ion species in the ../../ion array"""

	temperature  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="eV",type="dynamic")
	""" Temperature (average over charge states when multiple charge states are
		considered)"""

	density  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="m^-3",type="dynamic")
	""" Density (thermal+non-thermal) (sum over charge states when multiple charge
		states are considered)"""

	density_thermal  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="m^-3",type="dynamic")
	""" Density (thermal) (sum over charge states when multiple charge states are
		considered)"""

	density_fast  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="m^-3",type="dynamic")
	""" Density of fast (non-thermal) particles (sum over charge states when multiple
		charge states are considered)"""

	pressure  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Pressure (thermal+non-thermal) (sum over charge states when multiple charge
		states are considered)"""

	pressure_thermal  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Pressure (thermal) associated with random motion ~average((v-average(v))^2) (sum
		over charge states when multiple charge states are considered)"""

	pressure_fast_perpendicular  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Fast (non-thermal) perpendicular pressure (sum over charge states when multiple
		charge states are considered)"""

	pressure_fast_parallel  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Fast (non-thermal) parallel pressure (sum over charge states when multiple
		charge states are considered)"""

	multiple_states_flag  :int =  sp_property(type="dynamic")
	""" Multiple states calculation flag : 0-Only one state is considered; 1-Multiple
		states are considered and are described in the state structure"""

	state  :AoS[_T_core_profiles_neutral_state] =  sp_property(coordinate1="1...N")
	""" Quantities related to the different states of the species (energy, excitation,
		...)"""


class _T_core_profiles_profiles_1d_electrons(SpTree):
	"""Quantities related to electrons
	aos3Parent: yes"""

	temperature  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="eV",type="dynamic")
	""" Temperature"""

	temperature_validity  :int =  sp_property(type="dynamic")
	""" Indicator of the validity of the temperature profile. 0: valid from automated
		processing, 1: valid and certified by the RO; - 1 means problem identified in
		the data processing (request verification by the RO), -2: invalid data, should
		not be used"""

	temperature_fit  :_T_core_profiles_1D_fit =  sp_property(units="eV")
	""" Information on the fit used to obtain the temperature profile"""

	density  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="m^-3",type="dynamic")
	""" Density (thermal+non-thermal)"""

	density_validity  :int =  sp_property(type="dynamic")
	""" Indicator of the validity of the density profile. 0: valid from automated
		processing, 1: valid and certified by the RO; - 1 means problem identified in
		the data processing (request verification by the RO), -2: invalid data, should
		not be used"""

	density_fit  :_T_core_profiles_1D_fit =  sp_property(units="m^-3")
	""" Information on the fit used to obtain the density profile"""

	density_thermal  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="m^-3",type="dynamic")
	""" Density of thermal particles"""

	density_fast  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="m^-3",type="dynamic")
	""" Density of fast (non-thermal) particles"""

	pressure  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Pressure (thermal+non-thermal)"""

	pressure_thermal  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Pressure (thermal) associated with random motion ~average((v-average(v))^2)"""

	pressure_fast_perpendicular  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Fast (non-thermal) perpendicular pressure"""

	pressure_fast_parallel  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Fast (non-thermal) parallel pressure"""

	collisionality_norm  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="-",type="dynamic")
	""" Collisionality normalised to the bounce frequency"""


class _T_generic_grid_dynamic_space_dimension(SpTree):
	"""Generic grid, list of dimensions within a space (dynamic within a type 3 AoS)
	aos3Parent: yes"""

	object  :AoS[_T_generic_grid_dynamic_space_dimension_object] =  sp_property(coordinate1="1...N")
	""" Set of objects for a given dimension"""

	geometry_content  :_E_ggd_space_identifier =  sp_property(doc_identifier="utilities/ggd_geometry_content_identifier.xml",introduced_after_version="3.33.0")
	""" Content of the ../object/geometry node for this dimension"""


class _T_generic_grid_dynamic_grid_subset(SpTree):
	"""Generic grid grid_subset (dynamic within a type 3 AoS)
	aos3Parent: yes"""

	identifier  :_E_ggd_subset_identifier =  sp_property(doc_identifier="utilities/ggd_subset_identifier.xml",url="utilities/LFS_snowflake_GGD_subsets.png")
	""" Grid subset identifier"""

	dimension  :int =  sp_property(type="dynamic")
	""" Space dimension of the grid subset elements. This must be equal to the sum of
		the dimensions of the individual objects forming the element."""

	element  :AoS[_T_generic_grid_dynamic_grid_subset_element] =  sp_property(coordinate1="1...N")
	""" Set of elements defining the grid subset. An element is defined by a combination
		of objects from potentially all spaces"""

	base  :AoS[_T_generic_grid_dynamic_grid_subset_metric] =  sp_property(coordinate1="1...N")
	""" Set of bases for the grid subset. For each base, the structure describes the
		projection of the base vectors on the canonical frame of the grid."""

	metric  :_T_generic_grid_dynamic_grid_subset_metric =  sp_property()
	""" Metric of the canonical frame onto Cartesian coordinates"""


class _T_rzphi1d_dynamic_aos1(SpTree):
	"""Structure for list of R, Z, Phi positions (1D, dynamic within a type 1 array of
		structures (indexed on objects, data/time structure)"""

	r  :Signal =  sp_property(units="m")
	""" Major radius"""

	z  :Signal =  sp_property(units="m")
	""" Height"""

	phi  :Signal =  sp_property(units="rad")
	""" Toroidal angle (oriented counter-clockwise when viewing from above)"""


class _T_rzphirhopsitheta1d_dynamic_aos1(SpTree):
	"""Structure for list of R, Z, Phi, rho_tor_norm, psi, theta positions (1D, dynamic
		within a type 1 array of structures (indexed on objects, data/time structure)"""

	r  :Signal =  sp_property(units="m")
	""" Major radius"""

	z  :Signal =  sp_property(units="m")
	""" Height"""

	phi  :Signal =  sp_property(units="rad")
	""" Toroidal angle (oriented counter-clockwise when viewing from above)"""

	psi  :Signal =  sp_property(units="W")
	""" Poloidal flux"""

	rho_tor_norm  :Signal =  sp_property(units="-")
	""" Normalised toroidal flux coordinate"""

	theta  :Signal =  sp_property(units="rad")
	""" Poloidal angle (oriented clockwise when viewing the poloidal cross section on
		the right hand side of the tokamak axis of symmetry, with the origin placed on
		the plasma magnetic axis)"""


class _T_rzphi1d_dynamic_aos1_definition(SpTree):
	"""Structure for list of R, Z, Phi positions (1D, dynamic within a type 1 array of
		structures (indexed on objects, data/time structure), including a definition of
		the reference point"""

	definition  :str =  sp_property(type="static")
	""" Definition of the reference point"""

	r  :Signal =  sp_property(units="m")
	""" Major radius"""

	z  :Signal =  sp_property(units="m")
	""" Height"""

	phi  :Signal =  sp_property(units="rad")
	""" Toroidal angle (oriented counter-clockwise when viewing from above)"""


class _T_line_of_sight_2points_dynamic_aos1(SpTree):
	"""Generic description of a line of sight, defined by two points, dynamic within an
		AoS1 (1st point fixed, 2nd point is dynamic)"""

	first_point  :_T_rzphi0d_static =  sp_property()
	""" Position of the first point"""

	second_point  :_T_rzphi1d_dynamic_aos1_common_time =  sp_property()
	""" Position of the second point (possibly dynamic)"""

	moving_mode  :_T_identifier =  sp_property()
	""" Moving mode of the line of sight. Index = 0 : no movement, fixed position. Index
		= 1 : oscillating"""

	position_parameter  :Signal =  sp_property(units="mixed")
	""" In case of line of sight moving during a pulse, position parameter allowing to
		record and compute the line of sight position as a function of time"""

	amplitude_parameter  :float =  sp_property(type="static",units="mixed")
	""" Amplitude of the line of sight position parameter oscillation (in case
		moving_mode/index = 1)"""

	period  :float =  sp_property(type="static",units="s")
	""" Period of the line of sight oscillation (in case moving_mode/index = 1)"""


class _T_camera_geometry(SpTree):
	"""Camera geometry. The orientation of the camera is described as follows : pixels
		are aligned along x1 and x2 unit vectors while x3 is normal to the detector
		plane."""

	identifier  :str =  sp_property(type="static")
	""" ID of the camera"""

	pixel_dimensions  :array_type =  sp_property(type="static",coordinate1="1...2",units="m")
	""" Pixel dimension in each direction (x1, x2)"""

	pixels_n  :array_type =  sp_property(type="static",coordinate1="1...2")
	""" Number of pixels in each direction (x1, x2)"""

	pixel_position  :_T_rzphi2d_static =  sp_property()
	""" Position of the centre of each pixel. First dimension : line index (x1 axis).
		Second dimension: column index (x2 axis)."""

	camera_dimensions  :array_type =  sp_property(type="static",coordinate1="1...2",units="m")
	""" Total camera dimension in each direction (x1, x2)"""

	centre  :_T_rzphi0d_static =  sp_property()
	""" Position of the camera centre"""

	x1_unit_vector  :_T_xyz0d_static =  sp_property(url="utilities/detector_aperture_coordinates.svg")
	""" Components of the X1 direction unit vector in the (X,Y,Z) coordinate system,
		where X is the major radius axis for phi = 0, Y is the major radius axis for phi
		= pi/2, and Z is the height axis. The X1 vector is more horizontal than X2 (has
		a smaller abs(Z) component) and oriented in the positive phi direction
		(counter-clockwise when viewing from above)."""

	x2_unit_vector  :_T_xyz0d_static =  sp_property(url="utilities/detector_aperture_coordinates.svg")
	""" Components of the X2 direction unit vector in the (X,Y,Z) coordinate system,
		where X is the major radius axis for phi = 0, Y is the major radius axis for phi
		= pi/2, and Z is the height axis. The X2 axis is orthonormal so that uX2 = uX3 x
		uX1."""

	x3_unit_vector  :_T_xyz0d_static =  sp_property()
	""" Components of the X3 direction unit vector in the (X,Y,Z) coordinate system,
		where X is the major radius axis for phi = 0, Y is the major radius axis for phi
		= pi/2, and Z is the height axis. The X3 axis is normal to the camera plane and
		oriented towards the plasma."""

	line_of_sight  :_T_line_of_sight_2points_rzphi_2d =  sp_property()
	""" Description of the line of sight for each pixel, given by 2 points. For each
		coordinate : first dimension : line index (x1 axis); second dimension: column
		index (x2 axis)."""


class _T_outline_2d_geometry_static(SpTree):
	"""Description of 2D geometry"""

	geometry_type  :int =  sp_property(Type="static")
	""" Type used to describe the element shape (1:'outline', 2:'rectangle',
		3:'oblique', 4:'arcs of circle, 5: 'annulus', 6 : 'thick line')"""

	outline  :_T_rz1d_static =  sp_property()
	""" Irregular outline of the element. Do NOT repeat the first point."""

	rectangle  :_T_rectangle_static =  sp_property()
	""" Rectangular description of the element"""

	oblique  :_T_oblique_static =  sp_property()
	""" Parallelogram description of the element"""

	arcs_of_circle  :_T_arcs_of_circle_static =  sp_property()
	""" Description of the element contour by a set of arcs of circle. For each of
		these, the position of the start point is given together with the curvature
		radius. The end point is given by the start point of the next arc of circle."""

	annulus  :_T_annulus_static =  sp_property(introduced_after_version="3.34.0")
	""" The element is an annulus of centre R, Z, with inner radius radius_inner and
		outer radius radius_outer"""

	thick_line  :_T_thick_line_static =  sp_property(introduced_after_version="3.36.0")
	""" The element is approximated by a rectangle defined by a central segment and a
		thickness in the direction perpendicular to the segment"""


class _T_vessel_2d_element(SpTree):
	"""2D vessel block element description"""

	name  :str =  sp_property(type="static")
	""" Name of the block element"""

	outline  :_T_rz1d_static_closed_flag =  sp_property()
	""" Outline of the block element. Do NOT repeat the first point for closed contours"""

	resistivity  :float =  sp_property(type="static",units="ohm.m")
	""" Resistivity of the block element"""

	j_tor  :Signal =  sp_property(units="A")
	""" Toroidal current induced in this block element"""

	resistance  :float =  sp_property(type="static",units="Ohm")
	""" Resistance of the block element"""


class _T_core_profile_ions(SpTree):
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

	z_ion_1d  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="-",type="dynamic")
	""" Average charge of the ion species (sum of states charge weighted by state
		density and divided by ion density)"""

	z_ion_square_1d  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="-",type="dynamic")
	""" Average square charge of the ion species (sum of states square charge weighted
		by state density and divided by ion density)"""

	temperature  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="eV",type="dynamic")
	""" Temperature (average over charge states when multiple charge states are
		considered)"""

	temperature_validity  :int =  sp_property(type="dynamic")
	""" Indicator of the validity of the temperature profile. 0: valid from automated
		processing, 1: valid and certified by the RO; - 1 means problem identified in
		the data processing (request verification by the RO), -2: invalid data, should
		not be used"""

	temperature_fit  :_T_core_profiles_1D_fit =  sp_property(units="eV")
	""" Information on the fit used to obtain the temperature profile"""

	density  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="m^-3",type="dynamic")
	""" Density (thermal+non-thermal) (sum over charge states when multiple charge
		states are considered)"""

	density_validity  :int =  sp_property(type="dynamic")
	""" Indicator of the validity of the density profile. 0: valid from automated
		processing, 1: valid and certified by the RO; - 1 means problem identified in
		the data processing (request verification by the RO), -2: invalid data, should
		not be used"""

	density_fit  :_T_core_profiles_1D_fit =  sp_property(units="m^-3")
	""" Information on the fit used to obtain the density profile"""

	density_thermal  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="m^-3",type="dynamic")
	""" Density (thermal) (sum over charge states when multiple charge states are
		considered)"""

	density_fast  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="m^-3",type="dynamic")
	""" Density of fast (non-thermal) particles (sum over charge states when multiple
		charge states are considered)"""

	pressure  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Pressure (thermal+non-thermal) (sum over charge states when multiple charge
		states are considered)"""

	pressure_thermal  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Pressure (thermal) associated with random motion ~average((v-average(v))^2) (sum
		over charge states when multiple charge states are considered)"""

	pressure_fast_perpendicular  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Fast (non-thermal) perpendicular pressure (sum over charge states when multiple
		charge states are considered)"""

	pressure_fast_parallel  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Fast (non-thermal) parallel pressure (sum over charge states when multiple
		charge states are considered)"""

	rotation_frequency_tor  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="rad.s^-1",type="dynamic")
	""" Toroidal rotation frequency (i.e. toroidal velocity divided by the major radius
		at which the toroidal velocity is taken) (average over charge states when
		multiple charge states are considered)"""

	velocity  :_T_core_profiles_vector_components_2 =  sp_property(units="m.s^-1")
	""" Velocity (average over charge states when multiple charge states are considered)
		at the position of maximum major radius on every flux surface"""

	multiple_states_flag  :int =  sp_property(type="dynamic")
	""" Multiple states calculation flag : 0-Only the 'ion' level is considered and the
		'state' array of structure is empty; 1-Ion states are considered and are
		described in the 'state' array of structure"""

	state  :AoS[_T_core_profiles_ions_charge_states2] =  sp_property(coordinate1="1...N")
	""" Quantities related to the different states of the species (ionisation, energy,
		excitation, ...)"""


class _T_distribution_species(SpTree):
	"""Description of a species in a distribution function related IDS"""

	type  :_E_species_identifier =  sp_property(doc_identifier="utilities/species_reference_identifier.xml")
	""" Species type. index=1 for electron; index=2 for ion species in a single/average
		state (refer to ion structure); index=3 for ion species in a particular state
		(refer to ion/state structure); index=4 for neutral species in a single/average
		state (refer to neutral structure); index=5 for neutral species in a particular
		state (refer to neutral/state structure); index=6 for neutron; index=7 for
		photon"""

	ion  :_T_plasma_composition_ions_constant =  sp_property()
	""" Description of the ion or neutral species, used if type/index = 2 or 3"""

	neutral  :_T_plasma_composition_neutral_constant =  sp_property()
	""" Description of the neutral species, used if type/index = 4 or 5"""


class _T_generic_grid_dynamic_space(SpTree):
	"""Generic grid space (dynamic within a type 3 AoS)
	aos3Parent: yes"""

	identifier  :_E_ggd_space_identifier =  sp_property(doc_identifier="utilities/ggd_space_identifier.xml")
	""" Space identifier"""

	geometry_type  :_T_identifier_dynamic_aos3 =  sp_property()
	""" Type of space geometry (0: standard, 1:Fourier, >1: Fourier with periodicity)"""

	coordinates_type  :AoS[_E_coordinate] =  sp_property(coordinate1="1...N",type="dynamic",doc_identifier="utilities/coordinate_identifier.xml")
	""" Type of coordinates describing the physical space, for every coordinate of the
		space. The size of this node therefore defines the dimension of the space. The
		meaning of these predefined integer constants can be found in the Data
		Dictionary under utilities/coordinate_identifier.xml"""

	objects_per_dimension  :AoS[_T_generic_grid_dynamic_space_dimension] =  sp_property(coordinate1="1...N")
	""" Definition of the space objects for every dimension (from one to the dimension
		of the highest-dimensional objects). The index correspond to 1=nodes, 2=edges,
		3=faces, 4=cells/volumes, .... For every index, a collection of objects of that
		dimension is described."""


class _T_pf_coils_elements(SpTree):
	"""Each PF coil is comprised of a number of cross-section elements described
		individually"""

	name  :str =  sp_property(type="static")
	""" Name of this element"""

	identifier  :str =  sp_property(type="static")
	""" Identifier of this element"""

	turns_with_sign  :float =  sp_property(type="static",units="-")
	""" Number of effective turns in the element for calculating magnetic fields of the
		coil/loop; includes the sign of the number of turns (positive means current is
		counter-clockwise when seen from above)"""

	area  :float =  sp_property(type="static",units="m^2")
	""" Cross-sectional areas of the element"""

	geometry  :_T_outline_2d_geometry_static =  sp_property()
	""" Cross-sectional shape of the element"""


class _T_vessel_2d_unit(SpTree):
	"""2D vessel unit description"""

	name  :str =  sp_property(type="static")
	""" Name of the unit"""

	identifier  :str =  sp_property(type="static")
	""" Identifier of the unit"""

	annular  :_T_vessel_2d_annular =  sp_property()
	""" Annular representation of a layer by two contours, inner and outer.
		Alternatively, the layer can be described by a centreline and thickness."""

	element  :AoS[_T_vessel_2d_element] =  sp_property(coordinate1="1...N")
	""" Set of block elements"""


class _T_core_profiles_profiles_1d(TimeSlice):
	"""1D radial profiles for core and edge
	aos3Parent: yes"""

	grid  :_T_core_radial_grid =  sp_property()
	""" Radial grid"""

	electrons  :_T_core_profiles_profiles_1d_electrons =  sp_property()
	""" Quantities related to the electrons"""

	ion  :AoS[_T_core_profile_ions] =  sp_property(coordinate1="1...N")
	""" Quantities related to the different ion species, in the sense of isonuclear or
		isomolecular sequences. Ionisation states (or other types of states) must be
		differentiated at the state level below"""

	neutral  :AoS[_T_core_profile_neutral] =  sp_property(coordinate1="1...N")
	""" Quantities related to the different neutral species"""

	t_i_average  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="eV",type="dynamic")
	""" Ion temperature (averaged on charge states and ion species)"""

	t_i_average_fit  :_T_core_profiles_1D_fit =  sp_property(units="eV")
	""" Information on the fit used to obtain the t_i_average profile"""

	n_i_total_over_n_e  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="-",type="dynamic")
	""" Ratio of total ion density (sum over species and charge states) over electron
		density. (thermal+non-thermal)"""

	n_i_thermal_total  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="m^-3",type="dynamic")
	""" Total ion thermal density (sum over species and charge states)"""

	momentum_tor  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",type="dynamic",units="kg.m^-1.s^-1")
	""" Total plasma toroidal momentum, summed over ion species and electrons weighted
		by their density and major radius, i.e. sum_over_species(n*R*m*Vphi)"""

	zeff  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",type="dynamic",units="-")
	""" Effective charge"""

	zeff_fit  :_T_core_profiles_1D_fit =  sp_property(units="-")
	""" Information on the fit used to obtain the zeff profile"""

	pressure_ion_total  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Total (sum over ion species) thermal ion pressure"""

	pressure_thermal  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Thermal pressure (electrons+ions)"""

	pressure_perpendicular  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Total perpendicular pressure (electrons+ions, thermal+non-thermal)"""

	pressure_parallel  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Total parallel pressure (electrons+ions, thermal+non-thermal)"""

	j_total  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="A/m^2",type="dynamic")
	""" Total parallel current density = average(jtot.B) / B0, where B0 =
		Core_Profiles/Vacuum_Toroidal_Field/ B0"""

	current_parallel_inside  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="A",type="dynamic")
	""" Parallel current driven inside the flux surface. Cumulative surface integral of
		j_total"""

	j_tor  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="A/m^2",type="dynamic")
	""" Total toroidal current density = average(J_Tor/R) / average(1/R)"""

	j_ohmic  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="A/m^2",type="dynamic")
	""" Ohmic parallel current density = average(J_Ohmic.B) / B0, where B0 =
		Core_Profiles/Vacuum_Toroidal_Field/ B0"""

	j_non_inductive  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="A/m^2",type="dynamic")
	""" Non-inductive (includes bootstrap) parallel current density = average(jni.B) /
		B0, where B0 = Core_Profiles/Vacuum_Toroidal_Field/ B0"""

	j_bootstrap  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="A/m^2",type="dynamic")
	""" Bootstrap current density = average(J_Bootstrap.B) / B0, where B0 =
		Core_Profiles/Vacuum_Toroidal_Field/ B0"""

	conductivity_parallel  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="ohm^-1.m^-1",type="dynamic")
	""" Parallel conductivity"""

	e_field  :_T_core_profiles_vector_components_1 =  sp_property(units="V.m^-1")
	""" Electric field, averaged on the magnetic surface. E.g for the parallel
		component, average(E.B) / B0, using core_profiles/vacuum_toroidal_field/b0"""

	phi_potential  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",type="dynamic",units="V")
	""" Electrostatic potential, averaged on the magnetic flux surface"""

	rotation_frequency_tor_sonic  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="s^-1",type="dynamic",url="https://doi.org/10.1063/1.865350")
	""" Derivative of the flux surface averaged electrostatic potential with respect to
		the poloidal flux, multiplied by -1. This quantity is the toroidal angular
		rotation frequency due to the ExB drift, introduced in formula (43) of Hinton
		and Wong, Physics of Fluids 3082 (1985), also referred to as sonic flow in
		regimes in which the toroidal velocity is dominant over the poloidal velocity"""

	q  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",type="dynamic",units="-",cocos_label_transformation="q_like",cocos_transformation_expression=".fact_q",cocos_leaf_name_aos_indices="IDSPATH.q")
	""" Safety factor (IMAS uses COCOS=11: only positive when toroidal current and
		magnetic field are in same direction)"""

	magnetic_shear  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",units="-",type="dynamic")
	""" Magnetic shear, defined as rho_tor/q . dq/drho_tor"""


class _T_generic_grid_dynamic(SpTree):
	"""Generic grid (dynamic within a type 3 AoS)
	aos3Parent: yes"""

	identifier  :_E_ggd_identifier =  sp_property(doc_identifier="utilities/ggd_identifier.xml")
	""" Grid identifier"""

	path  :str =  sp_property(type="dynamic",url="utilities/IDS-path-syntax.md")
	""" Path of the grid, including the IDS name, in case of implicit reference to a
		grid_ggd node described in another IDS. To be filled only if the grid is not
		described explicitly in this grid_ggd structure. Example syntax:
		'wall:0/description_ggd(1)/grid_ggd', means that the grid is located in the wall
		IDS, occurrence 0, with ids path 'description_ggd(1)/grid_ggd'. See the link
		below for more details about IDS paths"""

	space  :AoS[_T_generic_grid_dynamic_space] =  sp_property(coordinate1="1...N",url_protected="https://confluence.iter.org/download/attachments/178133297/GGDguide.pdf")
	""" Set of grid spaces"""

	grid_subset  :AoS[_T_generic_grid_dynamic_grid_subset] =  sp_property(coordinate1="1...N")
	""" Grid subsets"""


class _T_generic_grid_aos3_root(TimeSlice):
	"""Generic grid (being itself the root of a type 3 AoS)
	aos3Parent: yes"""

	identifier  :_E_ggd_identifier =  sp_property(doc_identifier="utilities/ggd_identifier.xml")
	""" Grid identifier"""

	path  :str =  sp_property(type="dynamic")
	""" Path of the grid, including the IDS name, in case of implicit reference to a
		grid_ggd node described in another IDS. To be filled only if the grid is not
		described explicitly in this grid_ggd structure. Example syntax:
		IDS::wall/0/description_ggd(1)/grid_ggd, means that the grid is located in the
		wall IDS, occurrence 0, with relative path description_ggd(1)/grid_ggd, using
		Fortran index convention (here : first index of the array)"""

	space  :AoS[_T_generic_grid_dynamic_space] =  sp_property(coordinate1="1...N",url_protected="https://confluence.iter.org/download/attachments/178133297/GGDguide.pdf")
	""" Set of grid spaces"""

	grid_subset  :AoS[_T_generic_grid_dynamic_grid_subset] =  sp_property(coordinate1="1...N")
	""" Grid subsets"""


class _T_vessel_2d(SpTree):
	"""2D vessel description"""

	type  :_T_identifier_static =  sp_property()
	""" Type of the description. index = 0 for the official single/multiple annular
		representation and 1 for the official block element representation for each
		unit. Additional representations needed on a code-by-code basis follow same
		incremental pair tagging starting on index=2"""

	unit  :AoS[_T_vessel_2d_unit] =  sp_property(coordinate1="1...N")
	""" Set of units"""


class _T_plasma_composition(SpTree):
	"""Generic declaration of Plasma Composition for a simulation"""
  

	ion  :AoS[_T_plasma_composition_ions] =  sp_property(coordinate1="1...N")
	""" Array of plasma ions"""


class _T_code(SpTree):
	"""Generic decription of the code-specific parameters for the code that has
		produced this IDS"""
  

	name  :str =  sp_property(type="constant")
	""" Name of software generating IDS"""

	commit  :str =  sp_property(type="constant")
	""" Unique commit reference of software"""

	version  :str =  sp_property(type="constant")
	""" Unique version (tag) of software"""

	repository  :str =  sp_property(type="constant")
	""" URL of software repository"""

	parameters  :str =  sp_property(type="constant")
	""" List of the code specific parameters in XML format"""

	output_flag  :array_type =  sp_property(coordinate1="/time",type="dynamic")
	""" Output flag : 0 means the run is successful, other values mean some difficulty
		has been encountered, the exact meaning is then code specific. Negative values
		mean the result shall not be used."""

	library  :AoS[_T_library] =  sp_property(coordinate1="1...N")
	""" List of external libraries used by the code that has produced this IDS"""


class _T_parameters_input(SpTree):
	"""Code parameters block passed from the wrapper to the subroutine. Does not appear
		as such in the data structure. This is inserted in DD_Support.xsd for automatic
		declaration in the Fortran and C++ type definitions."""
  

	parameters_value  :str =  sp_property(type="constant")
	""" Actual value of the code parameters (instance of Code_Parameters/Parameters in
		XML format)"""

	parameters_default  :str =  sp_property(type="constant")
	""" Default value of the code parameters (instance of Code_Parameters/Parameters in
		XML format)"""

	schema  :str =  sp_property(type="constant")
	""" Code parameters schema"""


class _T_error_description(SpTree):
	"""Error description, an array of this structure is passed as argument of the
		access layer calls (get and put) for handling errorbars. Does not appear as such
		in the data structure. This is inserted in dd_support.xsd for automatic
		declaration in the Fortran and C++ type definitions."""
  

	symmetric  :int =  sp_property(type="constant")
	""" Flag indicating whether the error is “+/-“ symmetric (1) or not (0)"""

	type  :_T_identifier =  sp_property()
	""" Type of error bar description which is used (assumed to be identical for the
		lower and upper error):
		constant_absolute|constant_relative|explicit_values|expression"""

	expression_upper_0d  :str =  sp_property(type="constant")
	""" Upper error expression (absolute value taken), for 1D dynamic quantities"""

	expression_upper_1d  :List[str] =  sp_property(type="constant")
	""" Upper error expression (absolute value taken), for 2D dynamic quantities. If its
		dimension is equal to 1, the same error expression is applied to all indices of
		the original physical quantity"""

	expression_lower_0d  :str =  sp_property(type="constant")
	""" Lower error expression (absolute value taken), for 1D dynamic quantities"""

	expression_lower_1d  :List[str] =  sp_property(type="constant")
	""" Lower error expression (absolute value taken), for 2D dynamic quantities. If its
		dimension is equal to 1, the same error expression is applied to all indices of
		the original physical quantity"""


class _T_ids_properties(SpTree):
	"""Interface Data Structure properties. This element identifies the node above as
		an IDS"""
  

	comment  :str =  sp_property(type="constant")
	""" Any comment describing the content of this IDS"""

	homogeneous_time  :int =  sp_property(type="constant")
	""" This node must be filled (with 0, 1, or 2) for the IDS to be valid. If 1, the
		time of this IDS is homogeneous, i.e. the time values for this IDS are stored in
		the time node just below the root of this IDS. If 0, the time values are stored
		in the various time fields at lower levels in the tree. In the case only
		constant or static nodes are filled within the IDS, homogeneous_time must be set
		to 2"""

	provider  :str =  sp_property(type="constant")
	""" Name of the person in charge of producing this data"""

	creation_date  :str =  sp_property(type="constant")
	""" Date at which this data has been produced"""

	version_put  :_T_version_dd_al =  sp_property()
	""" Version of the access layer package used to PUT this IDS"""

	provenance  :_T_ids_provenance =  sp_property(lifecycle_status="alpha",lifecycle_version="3.34.0")
	""" Provenance information about this IDS"""


class _T_time(SpTree):
	"""Generic time
	coordinate1: 1...N
	type: dynamic
	units: s"""
  
