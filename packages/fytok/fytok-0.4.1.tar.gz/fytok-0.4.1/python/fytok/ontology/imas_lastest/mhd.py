"""
  This module containes the _FyTok_ wrapper of IMAS/dd/mhd
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_generic_grid_scalar,_T_generic_grid_aos3_root

class _T_mhd_ggd_electrons(SpTree):
	"""Quantities related to electrons"""

	temperature  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="eV")
	""" Temperature, given on various grid subsets"""


class _T_mhd_ggd(TimeSlice):
	"""MHD description for a given time slice on the GGD"""

	electrons  :_T_mhd_ggd_electrons =  sp_property()
	""" Quantities related to the electrons"""

	t_i_average  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="eV")
	""" Ion temperature (averaged on ion species), given on various grid subsets"""

	n_i_total  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="m^-3")
	""" Total ion density (sum over ion species and thermal+non-thermal), given on
		various grid subsets"""

	zeff  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="-")
	""" Effective charge, given on various grid subsets"""

	b_field_r  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="T")
	""" R component of the magnetic field, given on various grid subsets"""

	b_field_z  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="T")
	""" Z component of the magnetic field, given on various grid subsets"""

	b_field_tor  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="T")
	""" Toroidal component of the magnetic field, given on various grid subsets"""

	a_field_r  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="T.m")
	""" R component of the magnetic vector potential, given on various grid subsets"""

	a_field_z  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="T.m")
	""" Z component of the magnetic vector potential, given on various grid subsets"""

	a_field_tor  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="T.m")
	""" Toroidal component of the magnetic vector potential, given on various grid
		subsets"""

	psi  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="Wb")
	""" Poloidal flux, given on various grid subsets"""

	velocity_r  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="m.s^-1")
	""" R component of the plasma velocity, given on various grid subsets"""

	velocity_z  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="m.s^-1")
	""" Z component of the plasma velocity, given on various grid subsets"""

	velocity_tor  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="m.s^-1")
	""" Toroidal component of the plasma velocity, given on various grid subsets"""

	velocity_parallel  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="m.s^-1")
	""" Parallel (to magnetic field) component of the plasma velocity, given on various
		grid subsets"""

	velocity_parallel_over_b_field  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="m.s^-1.T^-1",introduced_after_version="3.36.0")
	""" Parallel (to magnetic field) component of the plasma velocity divided by the
		modulus of the local magnetic field, given on various grid subsets"""

	phi_potential  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="V")
	""" Electric potential, given on various grid subsets"""

	vorticity  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="s^-1")
	""" Vorticity, given on various grid subsets"""

	vorticity_over_r  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="m^-1.s^-1",introduced_after_version="3.36.0")
	""" Vorticity divided by the local major radius, given on various grid subsets"""

	j_r  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="A.m^-2")
	""" R component of the current density, given on various grid subsets"""

	j_z  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="A.m^-2")
	""" Z component of the current density, given on various grid subsets"""

	j_tor  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="A.m^-2")
	""" Toroidal component of the current density, given on various grid subsets"""

	j_tor_r  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="A.m^-1",introduced_after_version="3.36.0")
	""" Toroidal component of the current density multiplied by the local major radius,
		given on various grid subsets"""

	mass_density  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="kg.m^-3")
	""" Mass density, given on various grid subsets"""


class _T_mhd(IDS):
	"""Magnetohydrodynamic activity, description of perturbed fields and profiles using
		the Generic Grid Description.
	lifecycle_status: alpha
	lifecycle_version: 3.20.0
	lifecycle_last_change: 3.37.0"""

	dd_version="v3_38_1_dirty"
	ids_name="mhd"

	grid_ggd  :TimeSeriesAoS[_T_generic_grid_aos3_root] =  sp_property(coordinate1="time",type="dynamic")
	""" Grid (using the Generic Grid Description), for various time slices. The timebase
		of this array of structure must be a subset of the ggd timebase"""

	ggd  :TimeSeriesAoS[_T_mhd_ggd] =  sp_property(coordinate1="time",type="dynamic")
	""" Edge plasma quantities represented using the general grid description, for
		various time slices."""
