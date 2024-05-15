"""
  This module containes the _FyTok_ wrapper of IMAS/dd/turbulence
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_plasma_composition_neutral_element,_T_identifier
from .utilities import _E_poloidal_plane_coordinates_identifier

class _T_turbulence_profiles_2d_electrons(SpTree):
	"""Quantities related to electrons"""

	temperature  :array_type =  sp_property(coordinate1="../../../grid_2d(itime)/dim1",coordinate2="../../../grid_2d(itime)/dim2",units="eV",type="dynamic")
	""" Temperature"""

	density  :array_type =  sp_property(coordinate1="../../../grid_2d(itime)/dim1",coordinate2="../../../grid_2d(itime)/dim2",units="m^-3",type="dynamic")
	""" Density (thermal+non-thermal)"""

	density_thermal  :array_type =  sp_property(coordinate1="../../../grid_2d(itime)/dim1",coordinate2="../../../grid_2d(itime)/dim2",units="m^-3",type="dynamic")
	""" Density of thermal particles"""


class _T_turbulence_profiles_2d_neutral(SpTree):
	"""Quantities related to a given neutral species"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying ion (e.g. H+, D+, T+, He+2, C+, ...)"""

	ion_index  :int =  sp_property(type="dynamic")
	""" Index of the corresponding ion species in the ../../ion array"""

	temperature  :array_type =  sp_property(coordinate1="../../../grid_2d(itime)/dim1",coordinate2="../../../grid_2d(itime)/dim2",units="eV",type="dynamic")
	""" Temperature (average over charge states when multiple charge states are
		considered)"""

	density  :array_type =  sp_property(coordinate1="../../../grid_2d(itime)/dim1",coordinate2="../../../grid_2d(itime)/dim2",units="m^-3",type="dynamic")
	""" Density (thermal+non-thermal) (sum over charge states when multiple charge
		states are considered)"""

	density_thermal  :array_type =  sp_property(coordinate1="../../../grid_2d(itime)/dim1",coordinate2="../../../grid_2d(itime)/dim2",units="m^-3",type="dynamic")
	""" Density (thermal) (sum over charge states when multiple charge states are
		considered)"""


class _T_turbulence_profiles_2d_ions(SpTree):
	"""Quantities related to a given ion species"""

	element  :AoS[_T_plasma_composition_neutral_element] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	z_ion  :float =  sp_property(type="dynamic",units="Elementary Charge Unit")
	""" Ion charge (of the dominant ionisation state; lumped ions are allowed), volume
		averaged over plasma radius"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying ion (e.g. H+, D+, T+, He+2, C+, ...)"""

	neutral_index  :int =  sp_property(type="dynamic")
	""" Index of the corresponding neutral species in the ../../neutral array"""

	temperature  :array_type =  sp_property(coordinate1="../../../grid_2d(itime)/dim1",coordinate2="../../../grid_2d(itime)/dim2",units="eV",type="dynamic")
	""" Temperature (average over charge states when multiple charge states are
		considered)"""

	density  :array_type =  sp_property(coordinate1="../../../grid_2d(itime)/dim1",coordinate2="../../../grid_2d(itime)/dim2",units="m^-3",type="dynamic")
	""" Density (thermal+non-thermal) (sum over charge states when multiple charge
		states are considered)"""

	density_thermal  :array_type =  sp_property(coordinate1="../../../grid_2d(itime)/dim1",coordinate2="../../../grid_2d(itime)/dim2",units="m^-3",type="dynamic")
	""" Density (thermal) (sum over charge states when multiple charge states are
		considered)"""


class _T_turbulence_profiles_2d_grid(TimeSlice):
	"""Definition of the 2D grid with time"""

	dim1  :array_type =  sp_property(type="dynamic",coordinate1="1...N",units="mixed")
	""" First dimension values"""

	dim2  :array_type =  sp_property(type="dynamic",coordinate1="1...N",units="mixed")
	""" Second dimension values"""


class _T_turbulence_profiles_2d(TimeSlice):
	"""Fluctuating physical quantities for various time slices"""

	electrons  :_T_turbulence_profiles_2d_electrons =  sp_property()
	""" Quantities related to electrons"""

	ion  :AoS[_T_turbulence_profiles_2d_ions] =  sp_property(coordinate1="1...N")
	""" Quantities related to the various ion species"""

	neutral  :AoS[_T_turbulence_profiles_2d_neutral] =  sp_property(coordinate1="1...N")
	""" Quantities related to the various neutral species"""


class _T_turbulence(IDS):
	"""Description of plasma turbulence
	lifecycle_status: alpha
	lifecycle_version: 3.12.1
	lifecycle_last_change: 3.12.1"""

	dd_version="v3_38_1_dirty"
	ids_name="turbulence"

	grid_2d_type  :_E_poloidal_plane_coordinates_identifier =  sp_property(doc_identifier="utilities/poloidal_plane_coordinates_identifier.xml")
	""" Selection of one of a set of grid types for grid_2d"""

	grid_2d  :TimeSeriesAoS[_T_turbulence_profiles_2d_grid] =  sp_property(coordinate1="time",type="dynamic")
	""" Values for the 2D grid, for various time slices. The timebase of this array of
		structure must be a subset of the profiles_2d timebase"""

	profiles_2d  :TimeSeriesAoS[_T_turbulence_profiles_2d] =  sp_property(coordinate1="time",type="dynamic")
	""" Fluctuating physical quantities for various time slices"""
