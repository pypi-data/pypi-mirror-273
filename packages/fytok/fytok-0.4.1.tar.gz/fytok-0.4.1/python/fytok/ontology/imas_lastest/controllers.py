"""
  This module containes the _FyTok_ wrapper of IMAS/dd/controllers
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_signal_flt_3d,_T_signal_flt_1d,_T_signal_flt_2d

class _T_controllers_statespace(SpTree):
	"""type for a statespace controller"""

	state_names  :List[str] =  sp_property(type="constant",coordinate1="1...N")
	""" Names of the states"""

	a  :SignalND =  sp_property(coordinate1="../state_names",coordinate2="../state_names",coordinate3="time",units="mixed")
	""" A matrix"""

	b  :SignalND =  sp_property(coordinate1="../state_names",coordinate2="../../input_names",coordinate3="time",units="mixed")
	""" B matrix"""

	c  :SignalND =  sp_property(units="mixed",coordinate1="../state_names",coordinate2="../../output_names",coordinate3="time")
	""" C matrix"""

	d  :SignalND =  sp_property(units="mixed",coordinate1="../state_names",coordinate2="../../output_names",coordinate3="time")
	""" D matrix, normally proper and D=0"""

	deltat  :Signal =  sp_property(units="s")
	""" Discrete time sampling interval ; if less than 1e-10, the controller is
		considered to be expressed in continuous time"""


class _T_controllers_pid(SpTree):
	"""type for a MIMO PID controller"""

	p  :SignalND =  sp_property(units="mixed",coordinate1="../../output_names",coordinate2="../../input_names",coordinate3="time")
	""" Proportional term"""

	i  :SignalND =  sp_property(units="mixed",coordinate1="../../output_names",coordinate2="../../input_names",coordinate3="time")
	""" Integral term"""

	d  :SignalND =  sp_property(units="mixed",coordinate1="../../output_names",coordinate2="../../input_names",coordinate3="time")
	""" Derivative term"""

	tau  :Signal =  sp_property(units="s")
	""" Filter time-constant for the D-term"""


class _T_controllers_nonlinear_controller(SpTree):
	"""Type for a nonlinear controller"""

	name  :str =  sp_property(type="constant")
	""" Name of this controller"""

	description  :str =  sp_property(type="constant")
	""" Description of this controller"""

	controller_class  :str =  sp_property(type="constant")
	""" One of a known class of controllers"""

	input_names  :List[str] =  sp_property(type="constant",coordinate1="1...N")
	""" Names of the input signals, following the SDN convention"""

	output_names  :List[str] =  sp_property(type="constant",coordinate1="1...N")
	""" Output signal names following the SDN convention"""

	function  :str =  sp_property(type="constant")
	""" Method to be defined"""

	inputs  :SignalND =  sp_property(units="mixed",coordinate1="../input_names",coordinate2="time")
	""" Input signals; the timebase is common to inputs and outputs for any particular
		controller"""

	outputs  :SignalND =  sp_property(units="mixed",coordinate1="../output_names",coordinate2="time")
	""" Output signals; the timebase is common to inputs and outputs for any particular
		controller"""


class _T_controllers_linear_controller(SpTree):
	"""type for a linear controller"""

	name  :str =  sp_property(type="constant")
	""" Name of this controller"""

	description  :str =  sp_property(type="constant")
	""" Description of this controller"""

	controller_class  :str =  sp_property(type="constant")
	""" One of a known class of controllers"""

	input_names  :List[str] =  sp_property(type="constant",coordinate1="1...N")
	""" Names of the input signals, following the SDN convention"""

	output_names  :List[str] =  sp_property(type="constant",coordinate1="1...N")
	""" Names of the output signals following the SDN convention"""

	statespace  :_T_controllers_statespace =  sp_property()
	""" Statespace controller in discrete or continuous time"""

	pid  :_T_controllers_pid =  sp_property()
	""" Filtered PID controller"""

	inputs  :SignalND =  sp_property(units="mixed",coordinate1="../input_names",coordinate2="time")
	""" Input signals; the timebase is common to inputs and outputs for any particular
		controller"""

	outputs  :SignalND =  sp_property(units="mixed",coordinate1="../output_names",coordinate2="time")
	""" Output signals; the timebase is common to inputs and outputs for any particular
		controller"""


class _T_controllers(IDS):
	"""Feedback and feedforward controllers
	lifecycle_status: alpha
	lifecycle_version: 3.0.0
	lifecycle_last_change: 3.15.1"""

	dd_version="v3_38_1_dirty"
	ids_name="controllers"

	linear_controller  :AoS[_T_controllers_linear_controller] =  sp_property(coordinate1="1...N")
	""" A linear controller, this is rather conventional"""

	nonlinear_controller  :AoS[_T_controllers_nonlinear_controller] =  sp_property(coordinate1="1...N")
	""" A non-linear controller, this is less conventional and will have to be developed"""
