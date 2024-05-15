"""
  This module containes the _FyTok_ wrapper of IMAS/dd/langmuir_probes
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_physical_quantity_flt_1d_time_1,_T_rzphi0d_static,_T_ids_identification,_T_identifier_static
from .utilities import _E_midplane_identifier

class _T_langmuir_probes_plunge_physical_quantity_2(SpTree):
	"""Similar to a signal (FLT_1D) but dynamic signals use here a specific time base
		time_within_plunge located two levels above"""

	data  :array_type =  sp_property(type="dynamic",units="as_parent",coordinate1="../../../time_within_plunge")
	""" Data"""

	validity_timed  :array_type =  sp_property(type="dynamic",coordinate1="../../../time_within_plunge")
	""" Indicator of the validity of the data for each time slice. 0: valid from
		automated processing, 1: valid and certified by the diagnostic RO; - 1 means
		problem identified in the data processing (request verification by the
		diagnostic RO), -2: invalid data, should not be used (values lower than -2 have
		a code-specific meaning detailing the origin of their invalidity)"""

	validity  :int =  sp_property(type="dynamic")
	""" Indicator of the validity of the data for the whole plunge. 0: valid from
		automated processing, 1: valid and certified by the diagnostic RO; - 1 means
		problem identified in the data processing (request verification by the
		diagnostic RO), -2: invalid data, should not be used (values lower than -2 have
		a code-specific meaning detailing the origin of their invalidity)"""


class _T_langmuir_probes_plunge_physical_quantity(SpTree):
	"""Similar to a signal (FLT_1D) but dynamic signals use here a specific time base
		time_within_plunge base located one level above"""

	data  :array_type =  sp_property(type="dynamic",units="as_parent",coordinate1="../../time_within_plunge")
	""" Data"""

	validity_timed  :array_type =  sp_property(type="dynamic",coordinate1="../../time_within_plunge")
	""" Indicator of the validity of the data for each time slice. 0: valid from
		automated processing, 1: valid and certified by the diagnostic RO; - 1 means
		problem identified in the data processing (request verification by the
		diagnostic RO), -2: invalid data, should not be used (values lower than -2 have
		a code-specific meaning detailing the origin of their invalidity)"""

	validity  :int =  sp_property(type="dynamic")
	""" Indicator of the validity of the data for the whole plunge. 0: valid from
		automated processing, 1: valid and certified by the diagnostic RO; - 1 means
		problem identified in the data processing (request verification by the
		diagnostic RO), -2: invalid data, should not be used (values lower than -2 have
		a code-specific meaning detailing the origin of their invalidity)"""


class _T_langmuir_probes_position_reciprocating_2(SpTree):
	"""Structure for R, Z, Phi positions (1D, dynamic within a type 1 array of
		structure and with a common time base two levels above)
	aos3Parent: yes"""

	r  :array_type =  sp_property(type="dynamic",units="m",coordinate1="../../../time_within_plunge")
	""" Major radius"""

	z  :array_type =  sp_property(type="dynamic",units="m",coordinate1="../../../time_within_plunge")
	""" Height"""

	phi  :array_type =  sp_property(type="dynamic",units="rad",coordinate1="../../../time_within_plunge")
	""" Toroidal angle"""

	validity_timed  :array_type =  sp_property(type="dynamic",coordinate1="../../../time_within_plunge")
	""" Indicator of the validity of the position data for each time slice. 0: valid
		from automated processing, 1: valid and certified by the diagnostic RO; - 1
		means problem identified in the data processing (request verification by the
		diagnostic RO), -2: invalid data, should not be used (values lower than -2 have
		a code-specific meaning detailing the origin of their invalidity)"""

	validity  :int =  sp_property(type="dynamic")
	""" Indicator of the validity of the position data for the whole plunge. 0: valid
		from automated processing, 1: valid and certified by the diagnostic RO; - 1
		means problem identified in the data processing (request verification by the
		diagnostic RO), -2: invalid data, should not be used (values lower than -2 have
		a code-specific meaning detailing the origin of their invalidity)"""


class _T_langmuir_probes_position_reciprocating(SpTree):
	"""Structure for R, Z, Phi positions (1D, dynamic within a type 1 array of
		structure and with a common time base one level above)
	aos3Parent: yes"""

	r  :array_type =  sp_property(type="dynamic",units="m",coordinate1="../../time_within_plunge")
	""" Major radius"""

	z  :array_type =  sp_property(type="dynamic",units="m",coordinate1="../../time_within_plunge")
	""" Height"""

	phi  :array_type =  sp_property(type="dynamic",units="rad",coordinate1="../../time_within_plunge")
	""" Toroidal angle"""

	validity_timed  :array_type =  sp_property(type="dynamic",coordinate1="../../time_within_plunge")
	""" Indicator of the validity of the position data for each time slice. 0: valid
		from automated processing, 1: valid and certified by the diagnostic RO; - 1
		means problem identified in the data processing (request verification by the
		diagnostic RO), -2: invalid data, should not be used (values lower than -2 have
		a code-specific meaning detailing the origin of their invalidity)"""

	validity  :int =  sp_property(type="dynamic")
	""" Indicator of the validity of the position data for the whole plunge. 0: valid
		from automated processing, 1: valid and certified by the diagnostic RO; - 1
		means problem identified in the data processing (request verification by the
		diagnostic RO), -2: invalid data, should not be used (values lower than -2 have
		a code-specific meaning detailing the origin of their invalidity)"""


class _T_langmuir_probes_plunge_collector(SpTree):
	"""Probe collector"""

	position  :_T_langmuir_probes_position_reciprocating =  sp_property()
	""" Position of the collector"""

	v_floating  :_T_langmuir_probes_plunge_physical_quantity_2 =  sp_property(units="V")
	""" Floating potential"""

	v_floating_sigma  :_T_langmuir_probes_plunge_physical_quantity_2 =  sp_property(units="V",introduced_after_version="3.32.1")
	""" Standard deviation of the floating potential, corresponding to the fluctuations
		of the quantity over time"""

	t_e  :_T_langmuir_probes_plunge_physical_quantity_2 =  sp_property(units="eV")
	""" Electron temperature"""

	t_i  :_T_langmuir_probes_plunge_physical_quantity_2 =  sp_property(units="eV")
	""" Ion temperature"""

	j_i_parallel  :_T_langmuir_probes_plunge_physical_quantity_2 =  sp_property(units="A.m^-2")
	""" Ion parallel current density at the probe position"""

	ion_saturation_current  :_T_langmuir_probes_plunge_physical_quantity_2 =  sp_property(units="A")
	""" Ion saturation current measured by the probe"""

	j_i_saturation  :_T_langmuir_probes_plunge_physical_quantity_2 =  sp_property(units="A.m^-2",introduced_after_version="3.32.1")
	""" Ion saturation current density"""

	j_i_skew  :_T_langmuir_probes_plunge_physical_quantity_2 =  sp_property(units="-",introduced_after_version="3.32.1")
	""" Skew of the ion saturation current density"""

	j_i_kurtosis  :_T_langmuir_probes_plunge_physical_quantity_2 =  sp_property(units="-",introduced_after_version="3.32.1")
	""" Pearson kurtosis of the ion saturation current density"""

	j_i_sigma  :_T_langmuir_probes_plunge_physical_quantity_2 =  sp_property(units="A.m^-2",introduced_after_version="3.32.1")
	""" Standard deviation of the ion saturation current density, corresponding to the
		fluctuations of the quantity over time"""

	heat_flux_parallel  :_T_langmuir_probes_plunge_physical_quantity_2 =  sp_property(units="W.m^-2")
	""" Parallel heat flux at the probe position"""


class _T_langmuir_probes_multi_temperature(SpTree):
	"""Structure for multi-temperature fits"""

	t_e  :_T_physical_quantity_flt_1d_time_1 =  sp_property(units="eV")
	""" Electron temperature"""

	t_i  :_T_physical_quantity_flt_1d_time_1 =  sp_property(units="eV")
	""" Ion temperature"""

	time  :array_type =  sp_property(coordinate1="1...N",type="dynamic",units="s")
	""" Timebase for the dynamic nodes of this probe located at this level of the IDS
		structure"""


class _T_langmuir_probes_embedded(SpTree):
	"""Embedded Langmuir probe description"""

	name  :str =  sp_property(type="static")
	""" Name of the probe"""

	identifier  :str =  sp_property(type="static")
	""" ID of the probe"""

	position  :_T_rzphi0d_static =  sp_property()
	""" Position of the measurements"""

	surface_area  :float =  sp_property(type="static",units="m^2")
	""" Area of the probe surface exposed to the plasma (use when assuming constant
		effective collection area)"""

	surface_area_effective  :_T_physical_quantity_flt_1d_time_1 =  sp_property(units="m^2")
	""" Effective collection area of the probe surface, varying with time due to e.g.
		changes in the magnetic field line incidence angle"""

	v_floating  :_T_physical_quantity_flt_1d_time_1 =  sp_property(units="V",change_nbc_version="3.30.0",change_nbc_description="structure_renamed",change_nbc_previous_name="potential_floating")
	""" Floating potential"""

	v_floating_sigma  :_T_physical_quantity_flt_1d_time_1 =  sp_property(units="V",introduced_after_version="3.32.1")
	""" Standard deviation of the floating potential, corresponding to the fluctuations
		of the quantity over time"""

	v_plasma  :_T_physical_quantity_flt_1d_time_1 =  sp_property(units="V",change_nbc_version="3.30.0",change_nbc_description="structure_renamed",change_nbc_previous_name="potential_plasma")
	""" Plasma potential"""

	t_e  :_T_physical_quantity_flt_1d_time_1 =  sp_property(units="eV")
	""" Electron temperature"""

	n_e  :_T_physical_quantity_flt_1d_time_1 =  sp_property(units="m^-3")
	""" Electron density"""

	t_i  :_T_physical_quantity_flt_1d_time_1 =  sp_property(units="eV")
	""" Ion temperature"""

	j_i_parallel  :_T_physical_quantity_flt_1d_time_1 =  sp_property(units="A.m^-2",change_nbc_version="3.30.0",change_nbc_description="structure_renamed",change_nbc_previous_name="j_ion_parallel")
	""" Ion parallel current density at the probe position"""

	j_i_parallel_sigma  :_T_physical_quantity_flt_1d_time_1 =  sp_property(units="A.m^-2",introduced_after_version="3.32.1")
	""" Standard deviation of ion parallel current density at the probe position"""

	ion_saturation_current  :_T_physical_quantity_flt_1d_time_1 =  sp_property(units="A",change_nbc_version="3.30.0",change_nbc_description="structure_renamed",change_nbc_previous_name="saturation_current_ion")
	""" Ion saturation current measured by the probe"""

	j_i_saturation  :_T_physical_quantity_flt_1d_time_1 =  sp_property(units="A.m^-2",introduced_after_version="3.32.1")
	""" Ion saturation current density"""

	j_i_saturation_skew  :_T_physical_quantity_flt_1d_time_1 =  sp_property(units="-",introduced_after_version="3.32.1")
	""" Skew of the ion saturation current density"""

	j_i_saturation_kurtosis  :_T_physical_quantity_flt_1d_time_1 =  sp_property(units="-",introduced_after_version="3.32.1")
	""" Pearson kurtosis of the ion saturation current density"""

	j_i_saturation_sigma  :_T_physical_quantity_flt_1d_time_1 =  sp_property(units="A.m^-2",introduced_after_version="3.32.1")
	""" Standard deviation of the ion saturation current density, corresponding to the
		fluctuations of the quantity over time"""

	heat_flux_parallel  :_T_physical_quantity_flt_1d_time_1 =  sp_property(units="W.m^-2")
	""" Parallel heat flux at the probe position"""

	b_field_angle  :_T_physical_quantity_flt_1d_time_1 =  sp_property(units="rad")
	""" Incident angle of the magnetic field with respect to PFC surface"""

	distance_separatrix_midplane  :_T_physical_quantity_flt_1d_time_1 =  sp_property(units="m",change_nbc_version="3.33.0",change_nbc_description="structure_renamed",change_nbc_previous_name="distance_separatrix",introduced_after_version="3.32.1")
	""" Distance between the measurement position and the separatrix, mapped along flux
		surfaces to the outboard midplane, in the major radius direction. Positive value
		means the measurement is outside of the separatrix."""

	multi_temperature_fits  :AoS[_T_langmuir_probes_multi_temperature] =  sp_property(coordinate1="1...N")
	""" Set of temperatures describing the electron and ion distribution functions in
		case of multi-temperature fits"""

	time  :array_type =  sp_property(coordinate1="1...N",type="dynamic",units="s")
	""" Timebase for the dynamic nodes of this probe located at this level of the IDS
		structure"""


class _T_langmuir_probes_plunge(TimeSlice):
	"""Plunge of a reciprocating probe"""

	position_average  :_T_langmuir_probes_position_reciprocating =  sp_property()
	""" Average position of the measurements derived from multiple collectors"""

	collector  :AoS[_T_langmuir_probes_plunge_collector] =  sp_property(coordinate1="1...N")
	""" Set of probe collectors including measurements specific to each collector"""

	v_plasma  :_T_langmuir_probes_plunge_physical_quantity =  sp_property(units="V",change_nbc_version="3.30.0",change_nbc_description="structure_renamed",change_nbc_previous_name="potential_plasma")
	""" Plasma potential"""

	t_e_average  :_T_langmuir_probes_plunge_physical_quantity =  sp_property(units="eV")
	""" Electron temperature (upstream to downstream average)"""

	t_i_average  :_T_langmuir_probes_plunge_physical_quantity =  sp_property(units="eV")
	""" Ion temperature (upstream to downstream average)"""

	n_e  :_T_langmuir_probes_plunge_physical_quantity =  sp_property(units="m^-3")
	""" Electron density"""

	b_field_angle  :_T_langmuir_probes_plunge_physical_quantity =  sp_property(units="rad")
	""" Incident angle of the magnetic field with respect to PFC surface"""

	distance_separatrix_midplane  :_T_langmuir_probes_plunge_physical_quantity =  sp_property(change_nbc_version="3.33.0",change_nbc_description="structure_renamed",change_nbc_previous_name="distance_separatrix",introduced_after_version="3.32.1",units="m")
	""" Distance between the measurement position and the separatrix, mapped along flux
		surfaces to the outboard midplane, in the major radius direction. Positive value
		means the measurement is outside of the separatrix."""

	distance_x_point_z  :_T_langmuir_probes_plunge_physical_quantity =  sp_property(units="m",introduced_after_version="3.32.1")
	""" Distance in the z direction of the measurement position to the closest X-point
		(Zmeasurement-Zx_point)"""

	mach_number_parallel  :_T_langmuir_probes_plunge_physical_quantity =  sp_property(units="-")
	""" Parallel Mach number"""

	time_within_plunge  :array_type =  sp_property(units="s",type="dynamic",coordinate1="1...N")
	""" Time vector for describing the dynamics within the plunge"""


class _T_langmuir_probes_reciprocating(SpTree):
	"""Reciprocating probe"""

	name  :str =  sp_property(type="static")
	""" Name of the probe"""

	identifier  :str =  sp_property(type="static")
	""" ID of the probe"""

	surface_area  :array_type =  sp_property(type="static",units="m^2",coordinate1="plunge/collector")
	""" Area of the surface exposed to the plasma of each collector (constant assuming
		negligible dependence on e.g. the magnetic field line angle)"""

	plunge  :TimeSeriesAoS[_T_langmuir_probes_plunge] =  sp_property(coordinate1="time",type="dynamic")
	""" Set of plunges of this probe during the pulse, each plunge being recorded as a
		time slice from the Access Layer point of view. The time child node corresponds
		to the time of maximum penetration of the probe during a given plunge. The
		dynamics of physicas quantities within the plunge are described via the
		time_within_plunge vector."""


class _T_langmuir_probes(IDS):
	"""Langmuir probes
	lifecycle_status: alpha
	lifecycle_version: 3.22.0
	lifecycle_last_change: 3.33.0"""

	dd_version="v3_38_1_dirty"
	ids_name="langmuir_probes"

	equilibrium_id  :_T_ids_identification =  sp_property(introduced_after_version="3.32.1")
	""" ID of the IDS equilibrium used to map measurements - we may decide that this is
		superseeded when the systematic documentation of input provenance is adopted"""

	midplane  :_E_midplane_identifier =  sp_property(doc_identifier="utilities/midplane_identifier.xml",introduced_after_version="3.32.1")
	""" Choice of midplane definition for the mapping of measurements on an equilibrium
		(use the lowest index number if more than one value is relevant)"""

	embedded  :AoS[_T_langmuir_probes_embedded] =  sp_property(coordinate1="1...N")
	""" Set of embedded (in a plasma facing component) probes"""

	reciprocating  :AoS[_T_langmuir_probes_reciprocating] =  sp_property(coordinate1="1...N")
	""" Set of reciprocating probes"""

	latency  :float =  sp_property(type="static",units="s",introduced_after_version="3.32.1")
	""" Upper bound of the delay between physical information received by the detector
		and data available on the real-time (RT) network."""
