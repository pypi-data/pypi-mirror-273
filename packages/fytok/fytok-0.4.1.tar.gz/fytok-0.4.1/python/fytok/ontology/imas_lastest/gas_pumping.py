"""
  This module containes the _FyTok_ wrapper of IMAS/dd/gas_pumping
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_plasma_composition_neutral_element_constant,_T_signal_flt_1d

class _T_gas_pumping_species(SpTree):
	"""Description of a pumped molecular species
	coordinate1: 1...N"""

	element  :AoS[_T_plasma_composition_neutral_element_constant] =  sp_property(coordinate1="1...N")
	""" List of elements forming the gas molecule"""

	label  :str =  sp_property(type="constant")
	""" String identifying the neutral molecule (e.g. H2, D2, T2, N2, ...)"""

	flow_rate  :Signal =  sp_property(units="Pa.m^3.s^-1")
	""" Pumping flow rate of that species"""


class _T_gas_pumping_duct(SpTree):
	"""Gas pumping duct"""

	name  :str =  sp_property(type="static")
	""" Name of the pumping duct"""

	identifier  :str =  sp_property(type="static")
	""" ID of the pumping duct"""

	species  :AoS[_T_gas_pumping_species] =  sp_property(coordinate1="1...N")
	""" Molecular species pumped via this duct"""

	flow_rate  :Signal =  sp_property(units="Pa.m^3.s^-1")
	""" Total pumping flow rate via this duct"""


class _T_gas_pumping(IDS):
	"""Gas pumping by a set of ducts
	lifecycle_status: alpha
	lifecycle_version: 3.31.0
	lifecycle_last_change: 3.31.0"""

	dd_version="v3_38_1_dirty"
	ids_name="gas_pumping"

	duct  :AoS[_T_gas_pumping_duct] =  sp_property(coordinate1="1...N")
	""" Set of gas pumping ducts"""
