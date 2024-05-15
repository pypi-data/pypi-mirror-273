"""
  This module containes the _FyTok_ wrapper of IMAS/dd/real_time_data
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_signal_flt_1d,_T_signal_int_1d

class _T_rtd_allocatable_signals(SpTree):
	"""List of signals which can be allocated to the SDN"""

	name  :str =  sp_property(type="constant")
	""" Signal name"""

	definition  :str =  sp_property(type="constant")
	""" Signal definition"""

	allocated_position  :int =  sp_property(type="constant")
	""" Allocation of signal to a position in the SDN (1..N); this will be
		implementation specific"""

	value  :Signal =  sp_property(units="mixed")
	""" Signal value"""

	quality  :Signal =  sp_property()
	""" Indicator of the quality of the signal. Following ITER PCS documentation
		(https://user.iter.org/?uid=354SJ3&action=get_document), possible values are: 1
		- GOOD (the nominal state); 2 - INVALID (data no usable); 3 - DATA INTEGRITY
		ERROR (e.g. out of bounds with respect to expectations, calibration error,...)"""


class _T_rtd_topic(SpTree):
	"""List of the topics"""

	name  :str =  sp_property(type="constant")
	""" Topic name"""

	signal  :AoS[_T_rtd_allocatable_signals] =  sp_property(coordinate1="1...N")
	""" List of signals that are allocated to the PCS interface"""


class _T_real_time_data(IDS):
	"""Description of the data bus circulating on the real time data network of the
		machine. This is typically used (but not only) as an interface to the Plasma
		Control System (PCS)
	lifecycle_status: alpha
	lifecycle_version: 3.34.0
	lifecycle_last_change: 3.34.0"""

	dd_version="v3_38_1_dirty"
	ids_name="real_time_data"

	topic  :AoS[_T_rtd_topic] =  sp_property(coordinate1="1...N")
	""" List of topics. Signals are grouped by topic"""
