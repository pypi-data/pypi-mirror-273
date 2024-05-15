"""
  This module containes the _FyTok_ wrapper of IMAS/dd/calorimetry
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_signal_flt_1d_validity,_T_data_flt_0d_constant_validity

class _T_calorimetry_cooling_loop(SpTree):
	"""Cooling loop"""

	name  :str =  sp_property(type="static")
	""" Name of the loop"""

	identifier  :str =  sp_property(type="static")
	""" ID of the loop"""

	temperature_in  :Signal =  sp_property(units="K")
	""" Temperature of the coolant when entering the loop"""

	temperature_out  :Signal =  sp_property(units="K")
	""" Temperature of the coolant when exiting the loop"""

	mass_flow  :Signal =  sp_property(units="kg.s^-1")
	""" Mass flow of the coolant going through the loop"""


class _T_calorimetry_group_component(SpTree):
	"""Component"""

	name  :str =  sp_property(type="static")
	""" Name of the component"""

	identifier  :str =  sp_property(type="static")
	""" ID of the component"""

	power  :Signal =  sp_property(units="W")
	""" Power extracted from the component"""

	energy_cumulated  :Signal =  sp_property(units="J")
	""" Energy extracted from the component since the start of the pulse"""

	energy_total  :_T_data_flt_0d_constant_validity =  sp_property(units="J")
	""" Energy extracted from the component on the whole plasma discharge, including the
		return to thermal equilibrium of the component in the post-pulse phase"""

	temperature_in  :Signal =  sp_property(units="K")
	""" Temperature of the coolant when entering the component"""

	temperature_out  :Signal =  sp_property(units="K")
	""" Temperature of the coolant when exiting the component"""

	mass_flow  :Signal =  sp_property(units="kg.s^-1")
	""" Mass flow of the coolant going through the component"""

	transit_time  :Signal =  sp_property(units="s")
	""" Transit time for the coolant to go from the input to the output of the component"""


class _T_calorimetry_group(SpTree):
	"""Group of components on which calorimetry measurements are carried out"""

	name  :str =  sp_property(type="static")
	""" Name of the group"""

	identifier  :str =  sp_property(type="static")
	""" ID of the group"""

	component  :AoS[_T_calorimetry_group_component] =  sp_property(coordinate1="1...N")
	""" Set of components on which calorimetry measurements are carried out"""


class _T_calorimetry(IDS):
	"""Calometry measurements on various tokamak subsystems
	lifecycle_status: alpha
	lifecycle_version: 3.23.4
	lifecycle_last_change: 3.33.0"""

	dd_version="v3_38_1_dirty"
	ids_name="calorimetry"

	group  :AoS[_T_calorimetry_group] =  sp_property(coordinate1="1...N")
	""" Set of groups of components on which calorimetry measurements are carried out
		(grouped by tokamak subsystems or localisation on the machine)"""

	cooling_loop  :AoS[_T_calorimetry_cooling_loop] =  sp_property(coordinate1="1...N")
	""" Set of cooling loops"""

	latency  :float =  sp_property(type="static",units="s",introduced_after_version="3.32.1")
	""" Upper bound of the delay between physical information received by the detector
		and data available on the real-time (RT) network."""
