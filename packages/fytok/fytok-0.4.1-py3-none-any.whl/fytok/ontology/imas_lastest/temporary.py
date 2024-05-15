"""
  This module containes the _FyTok_ wrapper of IMAS/dd/temporary
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_identifier,_T_signal_flt_1d,_T_signal_int_1d,_T_signal_flt_2d,_T_signal_int_2d,_T_signal_flt_3d,_T_signal_int_3d,_T_signal_flt_4d,_T_signal_flt_5d,_T_signal_flt_6d

class _T_temporary_constant_quantities_float_0d(SpTree):
	"""Temporary constant Float_0D"""

	value  :float =  sp_property(type="constant",units="-")
	""" Value"""

	identifier  :_T_identifier =  sp_property()
	""" Description of the quantity using the standard identifier structure"""


class _T_temporary_constant_quantities_int_0d(SpTree):
	"""Temporary constant INT_0D"""

	value  :int =  sp_property(type="constant")
	""" Value"""

	identifier  :_T_identifier =  sp_property()
	""" Description of the quantity using the standard identifier structure"""


class _T_temporary_constant_quantities_string_0d(SpTree):
	"""Temporary constant STR_0D"""

	value  :str =  sp_property(type="constant")
	""" Value"""

	identifier  :_T_identifier =  sp_property()
	""" Description of the quantity using the standard identifier structure"""


class _T_temporary_constant_quantities_float_1d(SpTree):
	"""Temporary constant Float_1D"""

	value  :array_type =  sp_property(type="constant",units="-",coordinate1="1...N")
	""" Value"""

	identifier  :_T_identifier =  sp_property()
	""" Description of the quantity using the standard identifier structure"""


class _T_temporary_constant_quantities_int_1d(SpTree):
	"""Temporary constant INT_1D"""

	value  :List[int] =  sp_property(type="constant",coordinate1="1...N")
	""" Value"""

	identifier  :_T_identifier =  sp_property()
	""" Description of the quantity using the standard identifier structure"""


class _T_temporary_constant_quantities_string_1d(SpTree):
	"""Temporary constant STR_1D"""

	value  :List[str] =  sp_property(type="constant",coordinate1="1...N")
	""" Value"""

	identifier  :_T_identifier =  sp_property()
	""" Description of the quantity using the standard identifier structure"""


class _T_temporary_dynamic_quantities_float_1d(SpTree):
	"""Temporary dynamic Float_1D"""

	value  :Signal =  sp_property(units="mixed")
	""" Value"""

	identifier  :_T_identifier =  sp_property()
	""" Description of the quantity using the standard identifier structure"""


class _T_temporary_dynamic_quantities_int_1d(SpTree):
	"""Temporary dynamic Int_1D"""

	value  :Signal =  sp_property()
	""" Value"""

	identifier  :_T_identifier =  sp_property()
	""" Description of the quantity using the standard identifier structure"""


class _T_temporary_constant_quantities_float_2d(SpTree):
	"""Temporary constant Float_2D"""

	value  :array_type =  sp_property(type="constant",coordinate1="1...N",coordinate2="1...N",units="mixed")
	""" Value"""

	identifier  :_T_identifier =  sp_property()
	""" Description of the quantity using the standard identifier structure"""


class _T_temporary_constant_quantities_int_2d(SpTree):
	"""Temporary constant INT_2D"""

	value  :array_type =  sp_property(type="constant",coordinate1="1...N",coordinate2="1...N")
	""" Value"""

	identifier  :_T_identifier =  sp_property()
	""" Description of the quantity using the standard identifier structure"""


class _T_temporary_dynamic_quantities_float_2d(SpTree):
	"""Temporary dynamic Float_2D"""

	value  :SignalND =  sp_property(units="mixed",coordinate1="1...N",coordinate2="time")
	""" Value"""

	identifier  :_T_identifier =  sp_property()
	""" Description of the quantity using the standard identifier structure"""


class _T_temporary_dynamic_quantities_int_2d(SpTree):
	"""Temporary dynamic INT_2D"""

	value  :SignalND =  sp_property(coordinate1="1...N",coordinate2="time")
	""" Value"""

	identifier  :_T_identifier =  sp_property()
	""" Description of the quantity using the standard identifier structure"""


class _T_temporary_constant_quantities_float_3d(SpTree):
	"""Temporary constant Float_3D"""

	value  :array_type =  sp_property(type="constant",coordinate1="1...N",coordinate2="1...N",coordinate3="1...N",units="mixed")
	""" Value"""

	identifier  :_T_identifier =  sp_property()
	""" Description of the quantity using the standard identifier structure"""


class _T_temporary_constant_quantities_int_3d(SpTree):
	"""Temporary constant INT_3D"""

	value  :array_type =  sp_property(type="constant",coordinate1="1...N",coordinate2="1...N",coordinate3="1...N")
	""" Value"""

	identifier  :_T_identifier =  sp_property()
	""" Description of the quantity using the standard identifier structure"""


class _T_temporary_dynamic_quantities_float_3d(SpTree):
	"""Temporary dynamic Float_3D"""

	value  :SignalND =  sp_property(units="mixed",coordinate1="1...N",coordinate2="1...N",coordinate3="time")
	""" Value"""

	identifier  :_T_identifier =  sp_property()
	""" Description of the quantity using the standard identifier structure"""


class _T_temporary_dynamic_quantities_int_3d(SpTree):
	"""Temporary dynamic INT_3D"""

	value  :SignalND =  sp_property(coordinate1="1...N",coordinate2="1...N",coordinate3="time")
	""" Value"""

	identifier  :_T_identifier =  sp_property()
	""" Description of the quantity using the standard identifier structure"""


class _T_temporary_dynamic_quantities_float_4d(SpTree):
	"""Temporary dynamic Float_4D"""

	value  :SignalND =  sp_property(units="mixed",coordinate1="1...N",coordinate2="1...N",coordinate3="1...N",coordinate4="time")
	""" Value"""

	identifier  :_T_identifier =  sp_property()
	""" Description of the quantity using the standard identifier structure"""


class _T_temporary_constant_quantities_float_4d(SpTree):
	"""Temporary constant Float_4D"""

	value  :array_type =  sp_property(type="constant",coordinate1="1...N",coordinate2="1...N",coordinate3="1...N",coordinate4="1...N",units="mixed")
	""" Value"""

	identifier  :_T_identifier =  sp_property()
	""" Description of the quantity using the standard identifier structure"""


class _T_temporary_dynamic_quantities_float_5d(SpTree):
	"""Temporary dynamic Float_5D"""

	value  :SignalND =  sp_property(units="mixed",coordinate1="1...N",coordinate2="1...N",coordinate3="1...N",coordinate4="1...N",coordinate5="time")
	""" Value"""

	identifier  :_T_identifier =  sp_property()
	""" Description of the quantity using the standard identifier structure"""


class _T_temporary_constant_quantities_float_5d(SpTree):
	"""Temporary constant Float_5D"""

	value  :array_type =  sp_property(type="constant",coordinate1="1...N",coordinate2="1...N",coordinate3="1...N",coordinate4="1...N",coordinate5="1...N",units="mixed")
	""" Value"""

	identifier  :_T_identifier =  sp_property()
	""" Description of the quantity using the standard identifier structure"""


class _T_temporary_dynamic_quantities_float_6d(SpTree):
	"""Temporary dynamic Float_6D"""

	value  :SignalND =  sp_property(units="mixed",coordinate1="1...N",coordinate2="1...N",coordinate3="1...N",coordinate4="1...N",coordinate5="1...N",coordinate6="time")
	""" Value"""

	identifier  :_T_identifier =  sp_property()
	""" Description of the quantity using the standard identifier structure"""


class _T_temporary_constant_quantities_float_6d(SpTree):
	"""Temporary constant Float_6D"""

	value  :array_type =  sp_property(type="constant",coordinate1="1...N",coordinate2="1...N",coordinate3="1...N",coordinate4="1...N",coordinate5="1...N",coordinate6="1...N",units="mixed")
	""" Value"""

	identifier  :_T_identifier =  sp_property()
	""" Description of the quantity using the standard identifier structure"""


class _T_temporary(IDS):
	"""Storage of undeclared data model components
	lifecycle_status: alpha
	lifecycle_version: 3.0.0
	lifecycle_last_change: 3.0.4"""

	dd_version="v3_38_1_dirty"
	ids_name="temporary"

	constant_float0d  :AoS[_T_temporary_constant_quantities_float_0d] =  sp_property(coordinate1="1...N",units="mixed")
	""" Constant 0D float"""

	constant_integer0d  :AoS[_T_temporary_constant_quantities_int_0d] =  sp_property(coordinate1="1...N")
	""" Constant 0D integer"""

	constant_string0d  :AoS[_T_temporary_constant_quantities_string_0d] =  sp_property(coordinate1="1...N")
	""" Constant 0D string"""

	constant_integer1d  :AoS[_T_temporary_constant_quantities_int_1d] =  sp_property(coordinate1="1...N")
	""" Constant 1D integer"""

	constant_string1d  :AoS[_T_temporary_constant_quantities_string_1d] =  sp_property(coordinate1="1...N")
	""" Constant 1D string"""

	constant_float1d  :AoS[_T_temporary_constant_quantities_float_1d] =  sp_property(coordinate1="1...N",units="mixed")
	""" Constant 1D float"""

	dynamic_float1d  :AoS[_T_temporary_dynamic_quantities_float_1d] =  sp_property(coordinate1="1...N")
	""" Dynamic 1D float"""

	dynamic_integer1d  :AoS[_T_temporary_dynamic_quantities_int_1d] =  sp_property(coordinate1="1...N")
	""" Dynamic 1D integer"""

	constant_float2d  :AoS[_T_temporary_constant_quantities_float_2d] =  sp_property(coordinate1="1...N")
	""" Constant 2D float"""

	constant_integer2d  :AoS[_T_temporary_constant_quantities_int_2d] =  sp_property(coordinate1="1...N")
	""" Constant 2D integer"""

	dynamic_float2d  :AoS[_T_temporary_dynamic_quantities_float_2d] =  sp_property(coordinate1="1...N")
	""" Dynamic 2D float"""

	dynamic_integer2d  :AoS[_T_temporary_dynamic_quantities_int_2d] =  sp_property(coordinate1="1...N")
	""" Dynamic 2D integer"""

	constant_float3d  :AoS[_T_temporary_constant_quantities_float_3d] =  sp_property(coordinate1="1...N")
	""" Constant 3D float"""

	constant_integer3d  :AoS[_T_temporary_constant_quantities_int_3d] =  sp_property(coordinate1="1...N")
	""" Constant 3D integer"""

	dynamic_float3d  :AoS[_T_temporary_dynamic_quantities_float_3d] =  sp_property(coordinate1="1...N")
	""" Dynamic 3D float"""

	dynamic_integer3d  :AoS[_T_temporary_dynamic_quantities_int_3d] =  sp_property(coordinate1="1...N")
	""" Dynamic 3D integer"""

	constant_float4d  :AoS[_T_temporary_constant_quantities_float_4d] =  sp_property(coordinate1="1...N")
	""" Constant 4D float"""

	dynamic_float4d  :AoS[_T_temporary_dynamic_quantities_float_4d] =  sp_property(coordinate1="1...N")
	""" Dynamic 4D float"""

	constant_float5d  :AoS[_T_temporary_constant_quantities_float_5d] =  sp_property(coordinate1="1...N")
	""" Constant 5D float"""

	dynamic_float5d  :AoS[_T_temporary_dynamic_quantities_float_5d] =  sp_property(coordinate1="1...N")
	""" Dynamic 5D float"""

	constant_float6d  :AoS[_T_temporary_constant_quantities_float_6d] =  sp_property(coordinate1="1...N")
	""" Constant 6D float"""

	dynamic_float6d  :AoS[_T_temporary_dynamic_quantities_float_6d] =  sp_property(coordinate1="1...N")
	""" Dynamic 6D float"""
