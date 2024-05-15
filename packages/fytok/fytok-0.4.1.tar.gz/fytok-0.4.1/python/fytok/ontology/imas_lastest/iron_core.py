"""
  This module containes the _FyTok_ wrapper of IMAS/dd/iron_core
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_outline_2d_geometry_static,_T_signal_flt_1d

class _T_iron_core_segment(SpTree):
	"""Segment of the iron core"""

	name  :str =  sp_property(type="static")
	""" Name of the segment"""

	identifier  :str =  sp_property(type="static")
	""" ID of the segment"""

	b_field  :array_type =  sp_property(type="static",units="T",coordinate1="1...N")
	""" Array of magnetic field values, for each of which the relative permeability is
		given"""

	permeability_relative  :array_type =  sp_property(type="static",units="-",coordinate1="../b_field")
	""" Relative permeability of the iron segment"""

	geometry  :_T_outline_2d_geometry_static =  sp_property()
	""" Cross-sectional shape of the segment"""

	magnetisation_r  :Signal =  sp_property(units="T")
	""" Magnetisation M of the iron segment along the major radius axis, assumed to be
		constant inside a given iron segment. Reminder : H = 1/mu0 * B - mur * M;"""

	magnetisation_z  :Signal =  sp_property(units="T")
	""" Magnetisation M of the iron segment along the vertical axis, assumed to be
		constant inside a given iron segment. Reminder : H = 1/mu0 * B - mur * M;"""


class _T_iron_core(IDS):
	"""Iron core description
	lifecycle_status: alpha
	lifecycle_version: 3.2.3
	lifecycle_last_change: 3.12.1"""

	dd_version="v3_38_1_dirty"
	ids_name="iron_core"

	segment  :AoS[_T_iron_core_segment] =  sp_property(coordinate1="1...N")
	""" The iron core is describred as a set of segments"""
