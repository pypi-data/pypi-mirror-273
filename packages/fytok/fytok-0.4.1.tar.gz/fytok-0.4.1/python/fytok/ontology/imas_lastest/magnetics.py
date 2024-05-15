"""
  This module containes the _FyTok_ wrapper of IMAS/dd/magnetics
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_identifier_static,_T_rzphi0d_static,_T_signal_flt_1d_validity,_T_signal_flt_1d,_T_line_of_sight_2points_rz

class _E_magnetics_rogowski_measured(IntFlag):
	"""Quantity measured by the Rogowski coil	xpath: 	"""
  
	plasma = 1
	"""Plasma current"""
  
	plasma_eddy = 2
	"""Plasma and eddy currents"""
  
	eddy = 3
	"""Eddy currents"""
  
	halo = 4
	"""Halo currents"""
  
	compound = 5
	"""Sensor composed of multiple partial Rogowskis"""
  

class _E_magnetics_flux_loop_type(IntFlag):
	"""Type of flux loop	xpath: 	"""
  
	toroidal = 1
	"""Toroidal flux loop"""
  
	saddle = 2
	"""Saddle loop"""
  
	diamagnetic_internal = 3
	"""Diamagnetic internal loop"""
  
	diamagnetic_external = 4
	"""Diamagnetic external loop"""
  
	diamagnetic_compensation = 5
	"""Diamagnetic compensation loop"""
  
	diamagnetic_differential = 6
	"""Diamagnetic differential loop"""
  

class _E_magnetics_probe_type(IntFlag):
	"""Type of magnetic field probe	xpath: 	"""
  
	position = 1
	"""Position measurement probe"""
  
	mirnov = 2
	"""Mirnov probe"""
  
	hall = 3
	"""Hall probe"""
  
	flux_gate = 4
	"""Flux gate probe"""
  
	faraday_fiber = 5
	"""Faraday fiber"""
  
	differential = 6
	"""Differential probe"""
  

class _T_magnetics_bpol_probe_non_linear(SpTree):
	"""Non-linear response of the probe"""

	b_field_linear  :array_type =  sp_property(type="static",coordinate1="1...N",units="T")
	""" Array of magnetic field values (corresponding to the assumption of a linear
		relation between magnetic field and probe coil current), for each of which the
		probe non-linear response is given in ../b_field_non_linear"""

	b_field_non_linear  :array_type =  sp_property(type="static",coordinate1="../b_field_linear",units="T")
	""" Magnetic field value taking into account the non-linear response of the probe"""


class _T_magnetics_rogowski(SpTree):
	"""Rogowski coil"""

	name  :str =  sp_property(type="static")
	""" Name of the coil"""

	identifier  :str =  sp_property(type="static")
	""" ID of the coil"""

	measured_quantity  :_E_magnetics_rogowski_measured =  sp_property(doc_identifier="magnetics/magnetics_rogowski_measured_identifier.xml")
	""" Quantity measured by the sensor"""

	position  :AoS[_T_rzphi0d_static] =  sp_property(type="static",coordinate1="1...N")
	""" List of (R,Z,phi) points defining the position of the coil guiding centre"""

	indices_compound  :List[int] =  sp_property(type="static",coordinate1="1...N")
	""" Indices (from the rogowski_coil array of structure) of the partial Rogoswkis
		used to build the coumpound signal (sum of the partial Rogoswki signals) Use
		only if ../measure_quantity/index = 5, leave empty otherwise"""

	area  :float =  sp_property(type="static",units="m^2")
	""" Effective area of the loop wrapped around the guiding centre. In case of
		multiple layers, sum of the areas of each layer"""

	turns_per_metre  :float =  sp_property(type="static",units="m^-1")
	""" Number of turns per unit length. In case of multiple layers, turns are counted
		for a single layer"""

	current  :Signal =  sp_property(units="A")
	""" Measured current inside the Rogowski coil contour. The normal direction to the
		Rogowski coil is defined by the order of points in the list of guiding centre
		positions. The current is positive when oriented in the same direction as the
		normal."""


class _T_magnetics_flux_loop(SpTree):
	"""Flux loops"""

	name  :str =  sp_property(type="static")
	""" Name of the flux loop"""

	identifier  :str =  sp_property(type="static")
	""" ID of the flux loop"""

	type  :_E_magnetics_flux_loop_type =  sp_property(doc_identifier="magnetics/magnetics_flux_loop_type_identifier.xml")
	""" Flux loop type"""

	position  :AoS[_T_rzphi0d_static] =  sp_property(type="static",coordinate1="1...N")
	""" List of (R,Z,phi) points defining the position of the loop (see data structure
		documentation FLUXLOOPposition.pdf)"""

	indices_differential  :array_type =  sp_property(type="static",coordinate1="1...2")
	""" Indices (from the flux_loop array of structure) of the two flux loops used to
		build the flux difference flux(second index) - flux(first index). Use only if
		../type/index = 6, leave empty otherwise"""

	area  :float =  sp_property(type="static",units="m^2")
	""" Effective area (ratio between flux and average magnetic field over the loop)"""

	gm9  :float =  sp_property(type="static",units="m")
	""" Integral of 1/R over the loop area (ratio between flux and magnetic rigidity
		R0.B0). Use only if ../type/index = 3 to 6, leave empty otherwise."""

	flux  :Signal =  sp_property(units="Wb",cocos_label_transformation="psi_like",cocos_transformation_expression=".fact_psi",cocos_leaf_name_aos_indices="magnetics.flux_loop{i}.flux.data")
	""" Measured magnetic flux over loop in which Z component of normal to loop is
		directed downwards (negative grad Z direction)"""

	voltage  :Signal =  sp_property(units="V")
	""" Measured voltage between the loop terminals"""


class _T_magnetics_bpol_probe(SpTree):
	"""Poloidal field probes"""

	name  :str =  sp_property(type="static")
	""" Name of the probe"""

	identifier  :str =  sp_property(type="static")
	""" ID of the probe"""

	type  :_E_magnetics_probe_type =  sp_property(doc_identifier="magnetics/magnetics_probe_type_identifier.xml")
	""" Probe type"""

	position  :_T_rzphi0d_static =  sp_property()
	""" R, Z, Phi position of the coil centre"""

	poloidal_angle  :float =  sp_property(type="static",units="rad",url="magnetics/magnetics_angles.svg",cocos_label_transformation="pol_angle_like",cocos_transformation_expression=".fact_dtheta",cocos_leaf_name_aos_indices="magnetics.bpol_probe{i}.poloidal_angle")
	""" Angle of the sensor normal vector (vector parallel to the the axis of the coil,
		n on the diagram) with respect to horizontal plane (clockwise theta-like angle).
		Zero if sensor normal vector fully in the horizontal plane and oriented towards
		increasing major radius. Values in [0 , 2Pi]"""

	toroidal_angle  :float =  sp_property(type="static",units="rad",url="magnetics/magnetics_angles.svg",cocos_label_transformation="tor_angle_like",cocos_transformation_expression=".sigma_rphiz_eff",cocos_leaf_name_aos_indices="magnetics.bpol_probe{i}.toroidal_angle")
	""" Angle of the projection of the sensor normal vector (n) in the horizontal plane
		with the increasing R direction (i.e. grad(R)) (angle is counter-clockwise from
		above as in cocos=11 phi-like angle). Values should be taken modulo pi with
		values within (-pi/2,pi/2]. Zero if projected sensor normal is parallel to
		grad(R), pi/2 if it is parallel to grad(phi)."""

	indices_differential  :array_type =  sp_property(type="static",coordinate1="1...2")
	""" Indices (from the bpol_probe array of structure) of the two probes used to build
		the field difference field(second index) - field(first index). Use only if
		../type/index = 6, leave empty otherwise"""

	bandwidth_3db  :array_type =  sp_property(type="static",coordinate1="1...2",units="Hz")
	""" 3dB bandwith (first index : lower frequency bound, second index : upper
		frequency bound)"""

	area  :float =  sp_property(type="static",units="m^2")
	""" Area of each turn of the sensor; becomes effective area when multiplied by the
		turns"""

	length  :float =  sp_property(type="static",units="m")
	""" Length of the sensor along it's normal vector (n)"""

	turns  :int =  sp_property(type="static")
	""" Turns in the coil, including sign"""

	field  :Signal =  sp_property(units="T",cocos_label_transformation="one_like",cocos_transformation_expression="'1'",cocos_leaf_name_aos_indices="magnetics.bpol_probe{i}.field.data")
	""" Magnetic field component in direction of sensor normal axis (n) averaged over
		sensor volume defined by area and length, where n =
		cos(poloidal_angle)*cos(toroidal_angle)*grad(R) - sin(poloidal_angle)*grad(Z) +
		cos(poloidal_angle)*sin(toroidal_angle)*grad(Phi)/norm(grad(Phi))"""

	voltage  :Signal =  sp_property(units="V")
	""" Voltage on the coil terminals"""

	non_linear_response  :_T_magnetics_bpol_probe_non_linear =  sp_property()
	""" Non-linear response of the probe (typically in case of a Hall probe)"""


class _T_magnetics_method(SpTree):
	"""Processed quantities derived from the magnetic measurements, using various
		methods"""

	name  :str =  sp_property(type="static")
	""" Name of the data processing method"""

	ip  :Signal =  sp_property(units="A",cocos_label_transformation="ip_like",cocos_transformation_expression=".sigma_ip_eff",cocos_leaf_name_aos_indices="magnetics.method{i}.ip.data")
	""" Plasma current. Positive sign means anti-clockwise when viewed from above."""


class _T_magnetics_method_distinct(SpTree):
	"""Processed quantities derived from the magnetic measurements, using various
		methods"""

	method_name  :str =  sp_property(type="static")
	""" Name of the calculation method"""

	data  :Expression  =  sp_property(type="dynamic",units="as_parent",coordinate1="../time")
	""" Data"""

	time  :array_type =  sp_property(type="dynamic",units="s",coordinate1="1...N")
	""" Time"""


class _T_magnetics_shunt(SpTree):
	"""Shunt for current measurement (often located in the divertor structure)"""

	name  :str =  sp_property(type="static")
	""" Name of the shunt"""

	identifier  :str =  sp_property(type="static")
	""" Alphanumeric identifier of the shunt"""

	position  :_T_line_of_sight_2points_rz =  sp_property()
	""" Position of shunt terminals"""

	resistance  :float =  sp_property(type="static",units="Ohm")
	""" Shunt resistance"""

	voltage  :Signal =  sp_property(units="V")
	""" Voltage on the shunt terminals (Vfirst_point-Vsecond_point)"""

	divertor_index  :int =  sp_property(type="static")
	""" If the shunt is located on a given divertor, index of that divertor in the
		divertors IDS"""

	target_index  :int =  sp_property(type="static")
	""" If the shunt is located on a divertor target, index of that target in the
		divertors IDS"""

	tile_index  :int =  sp_property(type="static")
	""" If the shunt is located on a divertor tile, index of that tile in the divertors
		IDS"""


class _T_magnetics(IDS):
	"""Magnetic diagnostics for equilibrium identification and plasma shape control.
	lifecycle_status: active
	lifecycle_version: 3.24.0
	lifecycle_last_change: 3.33.0"""

	dd_version="v3_38_1_dirty"
	ids_name="magnetics"

	flux_loop  :AoS[_T_magnetics_flux_loop] =  sp_property(coordinate1="1...N")
	""" Flux loops; partial flux loops can be described"""

	b_field_pol_probe  :AoS[_T_magnetics_bpol_probe] =  sp_property(coordinate1="1...N",cocos_alias="bpol",cocos_replace="b_field_pol")
	""" Poloidal field probes"""

	b_field_tor_probe  :AoS[_T_magnetics_bpol_probe] =  sp_property(coordinate1="1...N",cocos_alias="bpol",cocos_replace="b_field_tor")
	""" Toroidal field probes"""

	rogowski_coil  :AoS[_T_magnetics_rogowski] =  sp_property(coordinate1="1...N")
	""" Set of Rogowski coils"""

	shunt  :AoS[_T_magnetics_shunt] =  sp_property(coordinate1="1...N",introduced_after_version="3.32.1")
	""" Set of shunt resistances through which currents in the divertor structure are
		measured. Shunts are modelled as piecewise straight line segments in the
		poloidal plane."""

	ip  :AoS[Signal] =  sp_property(coordinate1="1...N",units="A",cocos_label_transformation="ip_like",cocos_transformation_expression=".sigma_ip_eff",cocos_leaf_name_aos_indices="magnetics.ip{i}.data")
	""" Plasma current. Positive sign means anti-clockwise when viewed from above. The
		array of structure corresponds to a set of calculation methods (starting with
		the generally recommended method)."""

	diamagnetic_flux  :AoS[Signal] =  sp_property(coordinate1="1...N",units="Wb",cocos_label_transformation="b0_like",cocos_transformation_expression=".sigma_b0_eff",cocos_leaf_name_aos_indices="magnetics.diamagnetic_flux{i}.data")
	""" Diamagnetic flux. The array of structure corresponds to a set of calculation
		methods (starting with the generally recommended method)."""

	latency  :float =  sp_property(type="static",units="s",introduced_after_version="3.32.1")
	""" Upper bound of the delay between physical information received by the detector
		and data available on the real-time (RT) network."""
