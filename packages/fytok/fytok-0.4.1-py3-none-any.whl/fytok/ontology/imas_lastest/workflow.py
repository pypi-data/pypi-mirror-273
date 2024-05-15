"""
  This module containes the _FyTok_ wrapper of IMAS/dd/workflow
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_code_constant

class _T_workflow_component(SpTree):
	"""Control parameters for the set of participting components defined in
		../../component_list"""

	index  :int =  sp_property(type="dynamic")
	""" Index of the component in the ../../../component array"""

	execution_mode  :int =  sp_property(type="dynamic")
	""" Component execution mode for current workflow cycle. 0 means the component is
		not executed and the workflow uses results from previous workflow cycle. 1 means
		the component is executed for this workflow cycle."""

	time_interval  :float =  sp_property(type="dynamic",units="s")
	""" Simulation time interval during which this component has to compute its results."""

	control_float  :array_type =  sp_property(type="dynamic",units="mixed",coordinate1="1...N")
	""" Array of real workflow control parameters used by this component (component
		specific)"""

	control_integer  :List[int] =  sp_property(type="dynamic",coordinate1="1...N")
	""" Array of integer workflow control parameters used by this component (component
		specific)"""


class _T_workflow_cycle(TimeSlice):
	"""Control structure for the time associated with the workflow cycle"""

	component  :AoS[_T_workflow_component] =  sp_property(coordinate1="1...N")
	""" Control parameters for the set of participting components defined in
		../../component"""


class _T_workflow_time_loop(SpTree):
	"""Description of a workflow with a main time loop"""

	component  :AoS[_T_code_constant] =  sp_property(coordinate1="1...N")
	""" List of components partcipating in the workflow"""

	time_end  :float =  sp_property(type="constant",units="s")
	""" Termination time for the workflow main time loop"""

	workflow_cycle  :TimeSeriesAoS[_T_workflow_cycle] =  sp_property(coordinate1="time",type="dynamic")
	""" Set of time slices corresponding to the beginning of workflow cycles (main time
		loop of the workflow). During each workflow cycle, active components compute
		their result during their given time_interval. Components having completed their
		computation are frozen until the end of the workflow cycle. The next workflow
		cycle begins when the maximum time_interval (over the components) has been
		reached."""


class _T_workflow(IDS):
	"""Description of the workflow that has produced this data entry. The workflow IDS
		can also be used to communicate information about workflow state between
		workflow components.
	lifecycle_status: alpha
	lifecycle_version: 3.34.0
	lifecycle_last_change: 3.34.0"""

	dd_version="v3_38_1_dirty"
	ids_name="workflow"

	time_loop  :_T_workflow_time_loop =  sp_property()
	""" Description of a workflow based on a time loop which calls components defined in
		component_list sequentially during each cycle of the loop (workflow_cycle)."""
