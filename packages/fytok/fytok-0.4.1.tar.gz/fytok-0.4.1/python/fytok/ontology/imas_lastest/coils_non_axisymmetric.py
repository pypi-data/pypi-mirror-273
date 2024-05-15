"""
  This module containes the _FyTok_ wrapper of IMAS/dd/coils_non_axisymmetric
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_rzphi1d_static,_T_delta_rzphi1d_static,_T_signal_flt_1d

class _T_coil_conductor_elements(SpTree):
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


class _T_coil_conductor(SpTree):
	"""Description of a conductor"""

	elements  :_T_coil_conductor_elements =  sp_property()
	""" Set of geometrical elements (line segments and/or arcs of a circle) describing
		the contour of the conductor centre"""

	cross_section  :_T_delta_rzphi1d_static =  sp_property()
	""" The cross-section perpendicular to the conductor contour is described by a
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


class _T_coil(SpTree):
	"""Description of a given coil"""

	name  :str =  sp_property(type="static")
	""" Name of the coil"""

	identifier  :str =  sp_property(type="static")
	""" Alphanumeric identifier of coil"""

	conductor  :AoS[_T_coil_conductor] =  sp_property(type="static",coordinate1="1...N")
	""" Set of conductors inside the coil. The structure can be used with size 1 for a
		simplified description as a single conductor. A conductor is composed of several
		elements, serially connected, i.e. transporting the same current."""

	turns  :float =  sp_property(type="static",units="-")
	""" Number of total turns in the coil. May be a fraction when describing the coil
		connections."""

	resistance  :float =  sp_property(type="static",units="Ohm")
	""" Coil resistance"""

	current  :Signal =  sp_property(units="A")
	""" Current in one turn of the coil (to be multiplied by the number of turns to
		calculate the magnetic field generated). Sign convention : a positive current
		generates a positive radial magnetic field"""

	voltage  :Signal =  sp_property(units="V")
	""" Voltage on the coil terminals. Sign convention : a positive power supply voltage
		(and power supply current) generates a positive radial magnetic field"""


class _T_coils_non_axisymmetric(IDS):
	"""Non axisymmetric active coils system (e.g. ELM control coils, error field
		correction coils, ...)
	lifecycle_status: alpha
	lifecycle_version: 3.19.1
	lifecycle_last_change: 3.33.0"""

	dd_version="v3_38_1_dirty"
	ids_name="coils_non_axisymmetric"

	coil  :AoS[_T_coil] =  sp_property(type="static",coordinate1="1...N")
	""" Set of coils"""

	latency  :float =  sp_property(type="static",units="s",introduced_after_version="3.32.1")
	""" Upper bound of the delay between input command received from the RT network and
		actuator starting to react. Applies globally to the system described by this IDS
		unless specific latencies (e.g. channel-specific or antenna-specific) are
		provided at a deeper level in the IDS structure."""
