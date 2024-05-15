"""
  This module containes the _FyTok_ wrapper of IMAS/dd/pellets
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_plasma_composition_neutral_element,_T_identifier_dynamic_aos3,_T_rzphi1d_dynamic_aos3,_T_line_of_sight_2points_dynamic_aos3

class _T_pellets_time_slice_pellet_species(SpTree):
	"""Species included in pellet compoisition"""

	a  :float =  sp_property(units="Atomic Mass Unit",type="dynamic")
	""" Mass of atom"""

	z_n  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Nuclear charge"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying the species (e.g. H, D, T, ...)"""

	density  :float =  sp_property(type="dynamic",units="atoms.m^-3")
	""" Material density of the species in the pellet"""

	fraction  :float =  sp_property(type="dynamic",units="-")
	""" Atomic fraction of the species in the pellet"""

	sublimation_energy  :float =  sp_property(type="dynamic",units="eV")
	""" Sublimation energy per atom"""


class _T_pellets_propellant_gas(SpTree):
	"""Description of the propellant gas with its number of atoms
	coordinate1: 1...N"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the gas molecule"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying the neutral molecule (e.g. H2, D2, T2, N2, ...)"""

	molecules_n  :float =  sp_property(type="dynamic",units="-")
	""" Number of molecules of the propellant gas injected in the vacuum vessel when
		launching the pellet"""


class _T_pellets_time_slice_pellet_shape(SpTree):
	"""Initial shape of a pellet at launch"""

	type  :_T_identifier_dynamic_aos3 =  sp_property()
	""" Identifier structure for the shape type: 1-spherical; 2-cylindrical;
		3-rectangular"""

	size  :array_type =  sp_property(type="dynamic",coordinate1="1...N",units="m")
	""" Size of the pellet in the various dimensions, depending on the shape type.
		Spherical pellets: size(1) is the radius of the pellet. Cylindrical pellets:
		size(1) is the radius and size(2) is the height of the cylinder. Rectangular
		pellets: size(1) is the height, size(2) is the width and size(3) is the length"""


class _T_pellets_time_slice_pellet_path_profiles(SpTree):
	"""1-D profiles of plasma and pellet along the pellet path"""

	distance  :array_type =  sp_property(units="m",type="dynamic",coordinate1="1...N")
	""" Distance along the pellet path, with the origin taken at
		path_geometry/first_point. Used as the main coordinate for the path_profiles
		structure"""

	rho_tor_norm  :array_type =  sp_property(units="-",type="dynamic",coordinate1="../distance")
	""" Normalised toroidal coordinate along the pellet path"""

	psi  :array_type =  sp_property(units="Wb",type="dynamic",coordinate1="../distance")
	""" Poloidal flux along the pellet path"""

	velocity  :array_type =  sp_property(units="m.s^-1",type="dynamic",coordinate1="../distance")
	""" Pellet velocity along the pellet path"""

	n_e  :array_type =  sp_property(units="m^-3",type="dynamic",coordinate1="../distance")
	""" Electron density along the pellet path"""

	t_e  :array_type =  sp_property(units="eV",type="dynamic",coordinate1="../distance")
	""" Electron temperature along the pellet path"""

	ablation_rate  :array_type =  sp_property(units="s^-1",type="dynamic",coordinate1="../distance")
	""" Ablation rate (electrons) along the pellet path"""

	ablated_particles  :array_type =  sp_property(units="-",type="dynamic",coordinate1="../distance")
	""" Number of ablated particles (electrons) along the pellet path"""

	rho_tor_norm_drift  :array_type =  sp_property(units="-",type="dynamic",coordinate1="../distance")
	""" Difference to due ExB drifts between the ablation and the final deposition
		locations, in terms of the normalised toroidal flux coordinate"""

	position  :_T_rzphi1d_dynamic_aos3 =  sp_property()
	""" Position along the pellet path"""


class _T_pellets_time_slice_pellet(SpTree):
	"""Description of a pellet"""

	shape  :_T_pellets_time_slice_pellet_shape =  sp_property()
	""" Initial shape of a pellet at launch"""

	species  :AoS[_T_pellets_time_slice_pellet_species] =  sp_property(coordinate1="1...N")
	""" Set of atomic species included in the pellet composition"""

	velocity_initial  :float =  sp_property(units="m.s^-1",type="dynamic")
	""" Initial velocity of the pellet as it enters the vaccum chamber"""

	path_geometry  :_T_line_of_sight_2points_dynamic_aos3 =  sp_property()
	""" Geometry of the pellet path in the vaccuum chamber"""

	path_profiles  :_T_pellets_time_slice_pellet_path_profiles =  sp_property()
	""" 1-D profiles of plasma and pellet along the pellet path"""

	propellant_gas  :_T_pellets_propellant_gas =  sp_property()
	""" Propellant gas"""


class _T_pellets_time_slice(TimeSlice):
	"""Time slice description of pellets"""

	pellet  :AoS[_T_pellets_time_slice_pellet] =  sp_property(coordinate1="1...N")
	""" Set of pellets ablated in the plasma at a given time"""


class _T_pellets(IDS):
	"""Description of pellets launched into the plasma
	lifecycle_status: alpha
	lifecycle_version: 3.0.4
	lifecycle_last_change: 3.33.0"""

	dd_version="v3_38_1_dirty"
	ids_name="pellets"

	time_slice  :TimeSeriesAoS[_T_pellets_time_slice] =  sp_property(coordinate1="time",type="dynamic")
	""" Description of the pellets launched at various time slices. The time of this
		structure corresponds to the full ablation of the pellet inside the plasma."""

	latency  :float =  sp_property(type="static",units="s",introduced_after_version="3.32.1")
	""" Upper bound of the delay between input command received from the RT network and
		actuator starting to react. Applies globally to the system described by this IDS
		unless specific latencies (e.g. channel-specific or antenna-specific) are
		provided at a deeper level in the IDS structure."""
