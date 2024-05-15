"""
  This module containes the _FyTok_ wrapper of IMAS/dd/tf
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_rzphi1d_static,_T_delta_rzphi1d_static,_T_signal_flt_1d,_T_generic_grid_dynamic,_T_generic_grid_scalar

class _T_tf_coil_conductor_elements(SpTree):
	"""Elements descibring the conductor contour"""

	names  :List[str] =  sp_property(type="static",coordinate1="1...N")
	""" Name or description of every element"""

	types  :array_type =  sp_property(type="static",coordinate1="../names")
	""" Type of every element: 1: line segment, its ends are given by the start and end
		points; index = 2: arc of a circle; index = 3: full circle"""

	start_points  :_T_rzphi1d_static =  sp_property()
	""" Position of the start point of every element"""

	intermediate_points  :_T_rzphi1d_static =  sp_property()
	""" Position of an intermediate point along the arc of circle, for every element,
		providing the orientation of the element (must define with the corresponding
		start point an aperture angle strictly inferior to PI). Meaningful only if
		type/index = 2, fill with default/empty value otherwise"""

	end_points  :_T_rzphi1d_static =  sp_property()
	""" Position of the end point of every element. Meaningful only if type/index = 1 or
		2, fill with default/empty value otherwise"""

	centres  :_T_rzphi1d_static =  sp_property()
	""" Position of the centre of the arc of a circle of every element (meaningful only
		if type/index = 2 or 3, fill with default/empty value otherwise)"""


class _T_tf_ggd(TimeSlice):
	"""Toroidal field map represented on ggd"""

	grid  :_T_generic_grid_dynamic =  sp_property()
	""" Grid description"""

	b_field_r  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="T")
	""" R component of the vacuum magnetic field, given on various grid subsets"""

	b_field_z  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="T")
	""" Z component of the vacuum magnetic field, given on various grid subsets"""

	b_field_tor  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="T")
	""" Toroidal component of the vacuum magnetic field, given on various grid subsets"""

	a_field_r  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="T.m")
	""" R component of the vacuum vector potential, given on various grid subsets"""

	a_field_z  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="T.m")
	""" Z component of the vacuum vector potential, given on various grid subsets"""

	a_field_tor  :AoS[_T_generic_grid_scalar] =  sp_property(coordinate1="1...N",units="T.m")
	""" Toroidal component of the vacuum vector potential, given on various grid subsets"""


class _T_tf_coil_conductor(SpTree):
	"""Description of a conductor"""

	elements  :_T_tf_coil_conductor_elements =  sp_property()
	""" Set of geometrical elements (line segments and/or arcs of a circle) describing
		the contour of the TF conductor centre"""

	cross_section  :_T_delta_rzphi1d_static =  sp_property()
	""" The cross-section perpendicular to the TF conductor contour is described by a
		series of contour points, given by their relative position with respect to the
		start point of the first element. This cross-section is assumed constant for all
		elements."""

	resistance  :float =  sp_property(type="static",units="Ohm")
	""" conductor resistance"""

	current  :Signal =  sp_property(units="A")
	""" Current in the conductor (positive when it flows from the first to the last
		element)"""

	voltage  :Signal =  sp_property(units="V")
	""" Voltage on the conductor terminals"""


class _T_tf_coil(SpTree):
	"""Description of a given coil"""

	name  :str =  sp_property(type="static")
	""" Name of the coil"""

	identifier  :str =  sp_property(type="static")
	""" Alphanumeric identifier of coil used for convenience"""

	conductor  :AoS[_T_tf_coil_conductor] =  sp_property(type="static",coordinate1="1...N")
	""" Set of conductors inside the coil. The structure can be used with size 1 for a
		simplified description as a single conductor. A conductor is composed of several
		elements, serially connected, i.e. transporting the same current."""

	turns  :float =  sp_property(type="static",units="-")
	""" Number of total turns in a toroidal field coil. May be a fraction when
		describing the coil connections."""

	resistance  :float =  sp_property(type="static",units="Ohm")
	""" Coil resistance"""

	current  :Signal =  sp_property(units="A")
	""" Current in the coil"""

	voltage  :Signal =  sp_property(units="V")
	""" Voltage on the coil terminals"""


class _T_tf(IDS):
	"""Toroidal field coils
	lifecycle_status: alpha
	lifecycle_version: 3.0.0
	lifecycle_last_change: 3.33.0"""

	dd_version="v3_38_1_dirty"
	ids_name="tf"

	r0  :float =  sp_property(type="static",units="m")
	""" Reference major radius of the device (from the official description of the
		device). This node is the placeholder for this official machine description
		quantity (typically the middle of the vessel at the equatorial midplane,
		although the exact definition may depend on the device)"""

	is_periodic  :int =  sp_property(type="static")
	""" Flag indicating whether coils are described one by one in the coil() structure
		(flag=0) or whether the coil structure represents only coils having different
		characteristics (flag = 1, n_coils must be filled in that case). In the latter
		case, the coil() sequence is repeated periodically around the torus."""

	coils_n  :int =  sp_property(type="static")
	""" Number of coils around the torus, in case is_periodic = 1"""

	coil  :AoS[_T_tf_coil] =  sp_property(type="static",coordinate1="1...N")
	""" Set of coils around the tokamak"""

	field_map  :TimeSeriesAoS[_T_tf_ggd] =  sp_property(coordinate1="time",type="dynamic")
	""" Map of the vacuum field at various time slices, represented using the generic
		grid description"""

	b_field_tor_vacuum_r  :Signal =  sp_property(units="T.m",cocos_label_transformation="b0_like",cocos_transformation_expression=".sigma_b0_eff",cocos_leaf_name_aos_indices="tf.b_field_tor_vacuum_r.data")
	""" Vacuum field times major radius in the toroidal field magnet. Positive sign
		means anti-clockwise when viewed from above"""

	delta_b_field_tor_vacuum_r  :Signal =  sp_property(units="T.m")
	""" Variation of (vacuum field times major radius in the toroidal field magnet) from
		the start of the plasma."""

	latency  :float =  sp_property(type="static",units="s",introduced_after_version="3.32.1")
	""" Upper bound of the delay between input command received from the RT network and
		actuator starting to react. Applies globally to the system described by this IDS
		unless specific latencies (e.g. channel-specific or antenna-specific) are
		provided at a deeper level in the IDS structure."""
