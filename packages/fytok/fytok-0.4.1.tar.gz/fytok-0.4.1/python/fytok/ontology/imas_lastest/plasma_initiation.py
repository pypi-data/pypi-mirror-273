"""
  This module containes the _FyTok_ wrapper of IMAS/dd/plasma_initiation
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_identifier_dynamic_aos3,_T_equilibrium_profiles_2d_grid,_T_rz1d_dynamic_aos
from .utilities import _E_poloidal_plane_coordinates_identifier

class _T_plasma_initiation_global_quantities(SpTree):
	"""Global quantities"""

	b_field_stray  :Expression  =  sp_property(coordinate1="../../time",units="T",type="dynamic")
	""" Stray magnetic field at plasma position"""

	b_field_perpendicular  :Expression  =  sp_property(coordinate1="../../time",units="T",type="dynamic")
	""" Perpendicular magnetic field at plasma position. b_field_perpendicular =
		sqrt(b_field_stray^2+b_field_eddy^2)"""

	connection_length  :Expression  =  sp_property(coordinate1="../../time",units="m",type="dynamic")
	""" Average length of open magnetic field lines. In the case of fully closed field
		lines, connection_length = 1"""

	coulomb_logarithm  :Expression  =  sp_property(coordinate1="../../time",units="-",type="dynamic")
	""" Coulomb logarithm"""


class _T_plasma_initiation_field_lines(TimeSlice):
	"""Field lines tracing at a given time slice
	type: dynamic"""

	grid_type  :_E_poloidal_plane_coordinates_identifier =  sp_property(doc_identifier="utilities/poloidal_plane_coordinates_identifier.xml")
	""" Selection of one of a set of grid types"""

	grid  :_T_equilibrium_profiles_2d_grid =  sp_property(cocos_alias="IDSPATH",cocos_replace="equilibrium.time_slice{i}.profiles_2d{j}")
	""" Definition of the 2D grid (the content of dim1 and dim2 is defined by the
		selected grid_type)"""

	townsend_or_closed_positions  :CurveRZ =  sp_property()
	""" List of all R, Z positions along all field lines encoutering Townsend condition
		or being closed field lines"""

	townsend_or_closed_grid_positions  :CurveRZ =  sp_property()
	""" List of all R, Z grid positions (from ../grid) containing field lines
		encoutering Townsend condition or being closed field lines"""

	starting_positions  :CurveRZ =  sp_property()
	""" Starting position to initiate field line tracing, for each field line"""

	e_field_townsend  :array_type =  sp_property(type="dynamic",coordinate1="../starting_positions/r",units="V.m^-1")
	""" Townsend electric field along each field line"""

	e_field_parallel  :array_type =  sp_property(type="dynamic",coordinate1="../starting_positions/r",units="V.m^-1")
	""" Parallel electric field along each field line"""

	lengths  :array_type =  sp_property(type="dynamic",coordinate1="../starting_positions/r",units="m")
	""" Length of each field line"""

	pressure  :float =  sp_property(type="dynamic",units="Pa")
	""" Prefill gas pressure used in Townsend E field calculation"""

	open_fraction  :float =  sp_property(type="dynamic",units="-")
	""" Fraction of open field lines : ratio open fields lines / (open+closed field
		lines)"""


class _T_plasma_initiation(IDS):
	"""Description the early phases of the plasma, before an equilibrium can be
		calculated
	lifecycle_status: alpha
	lifecycle_version: 3.38.0
	lifecycle_last_change: 3.38.0"""

	dd_version="v3_38_1_dirty"
	ids_name="plasma_initiation"

	global_quantities  :_T_plasma_initiation_global_quantities =  sp_property()
	""" Global quantities"""

	b_field_lines  :TimeSeriesAoS[_T_plasma_initiation_field_lines] =  sp_property(coordinate1="time",type="dynamic")
	""" Magnetic field line tracing results, given at various time slices"""
