"""
  This module containes the _FyTok_ wrapper of IMAS/dd/pf_active
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_signal_flt_1d,_T_identifier_static,_T_pf_coils_elements

class _E_pf_active_coil_function(IntFlag):
	"""Functions of PF coils	xpath: 	"""
  
	flux = 0
	"""Generate flux (drive toroidal current)"""
  
	b_field_shaping = 1
	"""Generate magnetic field for shaping"""
  
	b_field_fb = 2
	"""Generate magnetic field for vertical force balance"""
  

class _T_pf_supplies(SpTree):
	"""PF power supplies"""

	name  :str =  sp_property(type="static")
	""" Name of the PF supply"""

	identifier  :str =  sp_property(type="static")
	""" Identifier of the supply"""

	type  :int =  sp_property(type="static")
	""" Type of the supply; TBD add free description of non-linear power supplies"""

	resistance  :float =  sp_property(type="static",units="Ohm")
	""" Power supply internal resistance"""

	delay  :float =  sp_property(type="static",units="s")
	""" Pure delay in the supply"""

	filter_numerator  :array_type =  sp_property(type="static",coordinate1="1...N",units="mixed")
	""" Coefficients of the numerator, in increasing order : a0 + a1*s + ... + an*s^n;
		used for a linear supply description"""

	filter_denominator  :array_type =  sp_property(coordinate1="1...N",type="static",units="mixed")
	""" Coefficients of the denominator, in increasing order : b0 + b1*s + ... + bm*s^m;
		used for a linear supply description"""

	current_limit_max  :float =  sp_property(type="static",units="A")
	""" Maximum current in the supply"""

	current_limit_min  :float =  sp_property(type="static",units="A")
	""" Minimum current in the supply"""

	voltage_limit_max  :float =  sp_property(type="static",units="V")
	""" Maximum voltage from the supply"""

	voltage_limit_min  :float =  sp_property(type="static",units="V")
	""" Minimum voltage from the supply"""

	current_limiter_gain  :float =  sp_property(type="static",units="V")
	""" Gain to prevent overcurrent in a linear model of the supply"""

	energy_limit_max  :float =  sp_property(type="static",units="J")
	""" Maximum energy to be dissipated in the supply during a pulse"""

	nonlinear_model  :str =  sp_property(type="static")
	""" Description of the nonlinear transfer function of the supply"""

	voltage  :Signal =  sp_property(units="V")
	""" Voltage at the supply output (Vside1-Vside2)"""

	current  :Signal =  sp_property(units="A",cocos_label_transformation="ip_like",cocos_transformation_expression=".sigma_ip_eff",cocos_leaf_name_aos_indices="pf_active.supply{i}.current.data")
	""" Current at the supply output, defined positive if it flows from point 1 to point
		2 in the circuit connected to the supply (outside the supply)"""


class _T_pf_circuits(SpTree):
	"""Circuits, connecting multiple PF coils to multiple supplies, defining the
		current and voltage relationships in the system"""

	name  :str =  sp_property(type="static")
	""" Name of the circuit"""

	identifier  :str =  sp_property(type="static")
	""" ID of the circuit"""

	type  :str =  sp_property(type="static")
	""" Type of the circuit"""

	connections  :array_type =  sp_property(type="static",coordinate1="1...N",coordinate2="1...N",url="pf_active/PFConnections.html")
	""" Description of the supplies and coils connections (nodes) across the circuit.
		Nodes of the circuit are listed as the first dimension of the matrix. Supplies
		(listed first) and coils (listed second) SIDES are listed as the second
		dimension. Thus the second dimension has a size equal to 2*(N_supplies+N_coils).
		N_supplies (resp. N_coils) is the total number of supplies (resp. coils) listed
		in the supply (resp.coil) array of structure, i.e. including also supplies/coils
		that are not part of the actual circuit. The (i,j) matrix elements are 1 if the
		j-th supply or coil side is connected to the i-th node, or 0 otherwise. For
		coils, sides are listed so that a current flowing from side 1 to side 2 (inside
		the coil) is positive (i.e. counter-clockwise when seen from above)."""

	voltage  :Signal =  sp_property(units="V")
	""" Voltage on the circuit between the sides of the group of supplies (only for
		circuits with a single supply or in which supplies are grouped)"""

	current  :Signal =  sp_property(units="A",cocos_label_transformation="ip_like",cocos_transformation_expression=".sigma_ip_eff",cocos_leaf_name_aos_indices="pf_active.circuit{i}.current.data")
	""" Current in the circuit between the sides of the group of supplies (only for
		circuits with a single supply or in which supplies are grouped)"""


class _T_pf_coils(SpTree):
	"""Active PF coils"""

	name  :str =  sp_property(type="static")
	""" Name of the coil"""

	identifier  :str =  sp_property(type="static")
	""" Alphanumeric identifier of coils used for convenience"""

	function  :AoS[_E_pf_active_coil_function] =  sp_property(introduced_after_version="3.34.0",coordinate1="1...N",doc_identifier="pf_active/pf_active_coil_function_identifier.xml")
	""" Set of functions for which this coil may be used"""

	resistance  :float =  sp_property(type="static",units="Ohm")
	""" Coil resistance"""

	resistance_additional  :Signal =  sp_property(units="Ohm",introduced_after_version="3.36.0")
	""" Additional resistance due to e.g. dynamically switchable resistors. The coil
		effective resistance is obtained by adding this dynamic quantity to the static
		resistance of the coil."""

	energy_limit_max  :float =  sp_property(type="static",units="J")
	""" Maximum Energy to be dissipated in the coil"""

	current_limit_max  :array_type =  sp_property(type="static",units="A",coordinate1="../b_field_max",coordinate2="../temperature")
	""" Maximum tolerable current in the conductor"""

	b_field_max  :array_type =  sp_property(type="static",units="T",coordinate1="1...N")
	""" List of values of the maximum magnetic field on the conductor surface
		(coordinate for current_limit_max)"""

	temperature  :array_type =  sp_property(type="static",units="K",coordinate1="1...N")
	""" List of values of the conductor temperature (coordinate for current_limit_max)"""

	b_field_max_timed  :Signal =  sp_property(units="T")
	""" Maximum absolute value of the magnetic field on the conductor surface"""

	element  :AoS[_T_pf_coils_elements] =  sp_property(coordinate1="1...N")
	""" Each PF coil is comprised of a number of cross-section elements described
		individually"""

	current  :Signal =  sp_property(units="A",cocos_label_transformation="ip_like",cocos_transformation_expression=".sigma_ip_eff",cocos_leaf_name_aos_indices="pf_active.coil{i}.current.data")
	""" Current fed in the coil (for 1 turn, to be multiplied by the number of turns to
		obtain the generated magnetic field), positive when flowing from side 1 to side
		2 of the coil (inside the coil), this numbering being made consistently with the
		convention that the current is counter-clockwise when seen from above."""

	voltage  :Signal =  sp_property(units="V")
	""" Voltage on the coil terminals (Vside1-Vside2) - including additional resistors
		if any"""


class _T_pf_forces(SpTree):
	"""Forces on the axisymmetric PF+CS coil system"""

	name  :str =  sp_property(type="static")
	""" Name of the force combination"""

	combination  :array_type =  sp_property(type="static",coordinate1="1...N",units="-")
	""" Coils involved in the force combinations. Normally the force would be the full
		set of coils, but in some cases, we want to have a difference in forces, such as
		a CS coil separation force. We therefore give each coil a force weight which we
		call the combination"""

	limit_max  :float =  sp_property(type="static",units="N")
	""" Maximum force combination limit"""

	limit_min  :float =  sp_property(type="static",units="N")
	""" Minimum force combination limit"""

	force  :Signal =  sp_property(units="N")
	""" Force (positive when upwards for a vertical force, positive when outwards for a
		radial force)"""


class _T_pf_active(IDS):
	"""Description of the axisymmetric active poloidal field (PF) coils and supplies;
		includes the limits of these systems; includes the forces on them; does not
		include non-axisymmetric coil systems
	lifecycle_status: alpha
	lifecycle_version: 3.0.0
	lifecycle_last_change: 3.37.0"""

	dd_version="v3_38_1_dirty"
	ids_name="pf_active"

	coil  :AoS[_T_pf_coils] =  sp_property(coordinate1="1...N")
	""" Active PF coils"""

	vertical_force  :AoS[_T_pf_forces] =  sp_property(coordinate1="1...N")
	""" Vertical forces on the axisymmetric PF coil system"""

	radial_force  :AoS[_T_pf_forces] =  sp_property(coordinate1="1...N")
	""" Radial forces on the axisymmetric PF coil system"""

	circuit  :AoS[_T_pf_circuits] =  sp_property(coordinate1="1...N")
	""" Circuits, connecting multiple PF coils to multiple supplies, defining the
		current and voltage relationships in the system"""

	supply  :AoS[_T_pf_supplies] =  sp_property(coordinate1="1...N")
	""" PF power supplies"""

	latency  :float =  sp_property(type="static",units="s",introduced_after_version="3.32.1")
	""" Upper bound of the delay between input command received from the RT network and
		actuator starting to react. Applies globally to the system described by this IDS
		unless specific latencies (e.g. channel-specific or antenna-specific) are
		provided at a deeper level in the IDS structure."""
