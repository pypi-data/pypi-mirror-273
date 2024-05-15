"""
  This module containes the _FyTok_ wrapper of IMAS/dd/gas_injection
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_gas_mixture_constant,_T_signal_flt_1d,_T_rzphi0d_static

class _T_gas_injection_valve_response(SpTree):
	"""Gas injection valve response curve"""

	voltage  :array_type =  sp_property(units="V",coordinate1="1...N",type="static")
	""" Voltage applied to open the valve"""

	flow_rate  :array_type =  sp_property(units="Pa.m^3.s^-1",coordinate1="../voltage",type="static")
	""" Flow rate at the exit of the valve"""


class _T_gas_injection_pipe_valve(SpTree):
	"""Gas injection valve"""

	name  :str =  sp_property(type="static")
	""" Name of the valve"""

	identifier  :str =  sp_property(type="static")
	""" ID of the valve"""

	species  :AoS[_T_gas_mixture_constant] =  sp_property(coordinate1="1...N")
	""" Species injected by the valve (may be more than one in case the valve injects a
		gas mixture)"""

	flow_rate_min  :float =  sp_property(type="static",units="Pa.m^3.s^-1")
	""" Minimum flow rate of the valve"""

	flow_rate_max  :float =  sp_property(type="static",units="Pa.m^3.s^-1")
	""" Maximum flow rate of the valve"""

	flow_rate  :Signal =  sp_property(units="Pa.m^3.s^-1")
	""" Flow rate at the exit of the valve"""

	electron_rate  :Signal =  sp_property(units="s^-1")
	""" Number of electrons injected per second"""

	pipe_indices  :List[int] =  sp_property(type="static",coordinate1="1...N")
	""" Indices (from the ../../pipe array of structure) of the pipe(s) that are fed by
		this valve"""

	voltage  :Signal =  sp_property(units="V",introduced_after_version="3.35.0")
	""" Voltage applied to open the valve (raw data used to compute the gas flow rate)"""

	response_curve  :_T_gas_injection_valve_response =  sp_property(introduced_after_version="3.35.0")
	""" Response curve of the valve, i.e. gas flow rate obtained as a function of the
		applied voltage."""


class _T_gas_injection_pipe(SpTree):
	"""Gas injection pipe"""

	name  :str =  sp_property(type="static")
	""" Name of the injection pipe"""

	identifier  :str =  sp_property(type="static")
	""" ID of the injection pipe"""

	species  :AoS[_T_gas_mixture_constant] =  sp_property(coordinate1="1...N")
	""" Species injected by the pipe (may be more than one in case the valve injects a
		gas mixture)"""

	length  :float =  sp_property(type="static",units="m")
	""" Pipe length"""

	exit_position  :_T_rzphi0d_static =  sp_property()
	""" Exit position of the pipe in the vaccum vessel"""

	second_point  :_T_rzphi0d_static =  sp_property()
	""" Second point indicating (combined with the exit_position) the direction of the
		gas injection towards the plasma"""

	flow_rate  :Signal =  sp_property(units="Pa.m^3.s^-1")
	""" Flow rate at the exit of the pipe"""

	valve_indices  :List[int] =  sp_property(type="static",introduced_after_version="3.33.0",coordinate1="1...N")
	""" Indices (from the ../../valve array of structure) of the valve(s) that are
		feeding this pipe"""


class _T_gas_injection(IDS):
	"""Gas injection by a system of pipes and valves
	lifecycle_status: alpha
	lifecycle_version: 3.10.2
	lifecycle_last_change: 3.36.0"""

	dd_version="v3_38_1_dirty"
	ids_name="gas_injection"

	pipe  :AoS[_T_gas_injection_pipe] =  sp_property(coordinate1="1...N")
	""" Set of gas injection pipes"""

	valve  :AoS[_T_gas_injection_pipe_valve] =  sp_property(coordinate1="1...N",introduced_after_version="3.33.0")
	""" Set of valves connecting a gas bottle to pipes"""

	latency  :float =  sp_property(type="static",units="s",introduced_after_version="3.32.1")
	""" Upper bound of the delay between input command received from the RT network and
		actuator starting to react. Applies globally to the system described by this IDS
		unless specific latencies (e.g. channel-specific or antenna-specific) are
		provided at a deeper level in the IDS structure."""
