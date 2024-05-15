"""
  This module containes the _FyTok_ wrapper of IMAS/dd/pf_passive
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_pf_coils_elements

class _T_pf_passive_loops(SpTree):
	"""Passive axisymmetric conductor description in the form of non-connected loops;
		any connected loops are expressed as active coil circuits with no power supply
		attached."""

	name  :str =  sp_property(type="static")
	""" Name of the loop"""

	resistance  :float =  sp_property(Type="static",Units="Ohm")
	""" Passive loop resistance"""

	resistivity  :float =  sp_property(Type="static",Units="Ohm.m")
	""" Passive loop resistivity"""

	element  :AoS[_T_pf_coils_elements] =  sp_property(coordinate1="1...N")
	""" Each loop is comprised of a number of cross-section elements described
		individually"""

	current  :Expression  =  sp_property(Type="dynamic",coordinate1="../time",Units="A")
	""" Passive loop current"""

	time  :array_type =  sp_property(coordinate1="1...N",type="dynamic",units="s")
	""" Timebase for the dynamic nodes of this loop located at this level of the IDS
		structure"""


class _T_pf_passive(IDS):
	"""Description of the axisymmetric passive conductors, currents flowing in them
	lifecycle_status: alpha
	lifecycle_version: 3.0.0
	lifecycle_last_change: 3.37.0"""

	dd_version="v3_38_1_dirty"
	ids_name="pf_passive"

	loop  :AoS[_T_pf_passive_loops] =  sp_property(coordinate1="1...N")
	""" Passive axisymmetric conductor description in the form of non-connected loops;
		any connected loops are expressed as active coil circuits with no power supply
		attached."""
