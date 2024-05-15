"""
  This module containes the _FyTok_ wrapper of IMAS/dd/pulse_schedule
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_signal_flt_1d,_T_identifier,_T_identifier_static,_T_gas_mixture_constant,_T_signal_int_1d,_T_plasma_composition_neutral_element_constant,_T_line_of_sight_3points

class _T_pulse_schedule_reference(SpTree):
	"""General structure for pulse schedule reference. NB: we propose to use the
		automatically generated reference/data_error_upper and
		reference/data_error_lower nodes to describe the upper of lower bound of the
		envelope of the waveform, since they almost have the same meaning and are
		already set on the same time base as reference/data."""

	reference_name  :str =  sp_property(type="constant")
	""" Reference name (e.g. in the native pulse schedule system of the device)"""

	reference  :Signal =  sp_property(units="mixed")
	""" Reference waveform. Caution : error bars of the reference/data node are not used
		in the usual sense, instead they are used to describe the control envelope, with
		a meaning depending on the chosen envelope_type option."""

	reference_type  :int =  sp_property(type="constant")
	""" Reference type: 0:relative (don't use for the moment, to be defined later when
		segments are introduced in the IDS structure); 1: absolute: the reference time
		trace is provided in the reference/data node"""

	envelope_type  :int =  sp_property(type="constant")
	""" Envelope type: 0:relative: means that the envelope upper and lower bound values
		are defined respectively as reference.data * reference.data_error_upper and
		reference.data * reference.data_error_lower. 1: absolute: the envelope upper and
		lower bound values are given respectively by reference/data_error_upper and
		reference/data_error_lower. Lower are upper are taken in the strict mathematical
		sense, without considering absolute values of the data"""


class _T_pulse_schedule_event(SpTree):
	"""Event"""

	type  :_T_identifier =  sp_property()
	""" Type of this event"""

	identifier  :str =  sp_property(type="constant")
	""" Unique identifier of this event provided by the scheduling / event handler"""

	time_stamp  :float =  sp_property(type="constant",units="s")
	""" Time stamp of this event"""

	duration  :float =  sp_property(type="constant",units="s")
	""" Duration of this event"""

	acquisition_strategy  :_T_identifier =  sp_property()
	""" Acquisition strategy related to this event: index = 1 : on-trigger; index = 2 :
		pre-trigger; index = 3 : post-trigger"""

	acquisition_state  :_T_identifier =  sp_property()
	""" Acquisition state of the related system : index = 1 : armed; index = 2 : on;
		index = 3 : off; index = 4 : closed"""

	provider  :str =  sp_property(type="constant")
	""" System having generated this event"""

	listeners  :List[str] =  sp_property(type="constant",coordinate1="1...N")
	""" Systems listening to this event"""


class _T_pulse_schedule_rz(SpTree):
	"""R,Z position"""

	r  :_T_pulse_schedule_reference =  sp_property(units="m")
	""" Major radius"""

	z  :_T_pulse_schedule_reference =  sp_property(units="m")
	""" Height"""


class _T_pulse_schedule_gap(SpTree):
	"""Gap for describing the plasma boundary"""

	name  :str =  sp_property(type="static")
	""" Name of the gap"""

	identifier  :str =  sp_property(type="static")
	""" Identifier of the gap"""

	r  :float =  sp_property(units="m",type="constant")
	""" Major radius of the reference point"""

	z  :float =  sp_property(units="m",type="constant")
	""" Height of the reference point"""

	angle  :float =  sp_property(units="rad",type="constant")
	""" Angle between the direction in which the gap is measured (in the poloidal
		cross-section) and the horizontal axis."""

	value  :_T_pulse_schedule_reference =  sp_property(units="m")
	""" Value of the gap, i.e. distance between the reference point and the separatrix
		along the gap direction"""


class _T_pulse_schedule_outline(SpTree):
	"""RZ outline"""

	r  :_T_pulse_schedule_reference =  sp_property(units="m")
	""" Major radius"""

	z  :_T_pulse_schedule_reference =  sp_property(units="m")
	""" Height"""


class _T_pulse_schedule_ic_antenna(SpTree):
	"""IC antenna"""

	name  :str =  sp_property(type="static")
	""" Name of the antenna"""

	identifier  :str =  sp_property(type="static")
	""" Identifier of the antenna"""

	power_type  :_T_identifier_static =  sp_property()
	""" Type of power used in the sibling power node (defining which power is referred
		to in this pulse_schedule). Index = 1: power_launched, 2: power_forward (see
		definitions in the ic_antennas IDS)"""

	power  :_T_pulse_schedule_reference =  sp_property(units="W")
	""" Power"""

	phase  :_T_pulse_schedule_reference =  sp_property(units="rad")
	""" Phase"""

	frequency  :_T_pulse_schedule_reference =  sp_property(units="Hz")
	""" Frequency"""


class _T_pulse_schedule_ec_antenna(SpTree):
	"""EC antenna"""

	name  :str =  sp_property(type="static")
	""" Name of the launcher"""

	identifier  :str =  sp_property(type="static")
	""" Identifier of the launcher"""

	power  :_T_pulse_schedule_reference =  sp_property(units="W")
	""" Power launched from this launcher into the vacuum vessel"""

	frequency  :_T_pulse_schedule_reference =  sp_property(units="Hz")
	""" Frequency"""

	deposition_rho_tor_norm  :_T_pulse_schedule_reference =  sp_property(units="-")
	""" Normalised toroidal flux coordinate at which the main deposition should occur"""

	steering_angle_pol  :_T_pulse_schedule_reference =  sp_property(units="rad",change_nbc_version="3.26.0",change_nbc_description="structure_renamed",change_nbc_previous_name="launching_angle_pol")
	""" Steering angle of the EC beam in the R,Z plane (from the -R axis towards the -Z
		axis), angle_pol=atan2(-k_Z,-k_R), where k_Z and k_R are the Z and R components
		of the mean wave vector in the EC beam"""

	steering_angle_tor  :_T_pulse_schedule_reference =  sp_property(units="rad",change_nbc_version="3.26.0",change_nbc_description="structure_renamed",change_nbc_previous_name="launching_angle_tor")
	""" Steering angle of the EC beam away from the poloidal plane that is increasing
		towards the positive phi axis, angle_tor=arcsin(k_phi/k), where k_phi is the
		component of the wave vector in the phi direction and k is the length of the
		wave vector. Here the term wave vector refers to the mean wave vector in the EC
		beam"""


class _T_pulse_schedule_lh_antenna(SpTree):
	"""LH antenna"""

	name  :str =  sp_property(type="static")
	""" Name of the antenna"""

	identifier  :str =  sp_property(type="static")
	""" Identifier of the antenna"""

	power_type  :_T_identifier_static =  sp_property()
	""" Type of power used in the sibling power node (defining which power is referred
		to in this pulse_schedule). Index = 1: power_launched, 2: power_forward (see
		definitions in the lh_antennas IDS)"""

	power  :_T_pulse_schedule_reference =  sp_property(units="W")
	""" Power"""

	phase  :_T_pulse_schedule_reference =  sp_property(units="rad")
	""" Phasing between neighbour waveguides (in the toroidal direction)"""

	n_parallel  :_T_pulse_schedule_reference =  sp_property(units="-")
	""" Main parallel refractive index of the injected wave power spectrum"""

	frequency  :_T_pulse_schedule_reference =  sp_property(units="Hz")
	""" Frequency"""


class _T_pulse_schedule_nbi_unit(SpTree):
	"""NBI unit"""

	name  :str =  sp_property(type="static")
	""" Name of the NBI unit"""

	identifier  :str =  sp_property(type="static")
	""" Identifier of the NBI unit"""

	species  :AoS[_T_gas_mixture_constant] =  sp_property(coordinate1="1...N")
	""" Species injected by the NBI unit (may be more than one in case the unit injects
		a gas mixture)"""

	power  :_T_pulse_schedule_reference =  sp_property(units="W")
	""" Power launched from this unit into the vacuum vessel"""

	energy  :_T_pulse_schedule_reference =  sp_property(units="eV")
	""" Full energy of the injected species (acceleration of a single atom)"""


class _T_pulse_schedule_density_control_ion(SpTree):
	"""References for ion species"""

	element  :AoS[_T_plasma_composition_neutral_element_constant] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	z_ion  :float =  sp_property(type="constant",units="Elementary Charge Unit")
	""" Ion charge"""

	label  :str =  sp_property(type="constant")
	""" String identifying ion (e.g. H, D, T, He, C, D2, ...)"""

	n_i_volume_average  :_T_pulse_schedule_reference =  sp_property(units="m^-3")
	""" Volume averaged ion density (average over the plasma volume up to the LCFS)"""


class _T_pulse_schedule_density_control_valve(SpTree):
	"""Gas injection valve"""

	name  :str =  sp_property(type="static")
	""" Name of the valve"""

	identifier  :str =  sp_property(type="static")
	""" Identifier of the valve"""

	flow_rate  :_T_pulse_schedule_reference =  sp_property(units="Pa.m^3.s^-1")
	""" Flow rate of the valve"""

	species  :AoS[_T_gas_mixture_constant] =  sp_property(coordinate1="1...N")
	""" Species injected by the valve (may be more than one in case the valve injects a
		gas mixture)"""


class _T_pulse_schedule_flux_control(SpTree):
	"""Flux control references"""

	i_plasma  :_T_pulse_schedule_reference =  sp_property(units="A")
	""" Plasma current"""

	loop_voltage  :_T_pulse_schedule_reference =  sp_property(units="V")
	""" Loop voltage"""

	li_3  :_T_pulse_schedule_reference =  sp_property(units="-")
	""" Internal inductance"""

	beta_normal  :_T_pulse_schedule_reference =  sp_property(units="-")
	""" Normalised toroidal beta, defined as 100 * beta_tor * a[m] * B0 [T] / ip [MA]"""

	mode  :Signal =  sp_property()
	""" Control mode (operation mode and/or settings used by the controller)"""


class _T_pulse_schedule_pf_active_supply(SpTree):
	"""PF supply"""

	name  :str =  sp_property(type="static")
	""" Name of the supply"""

	identifier  :str =  sp_property(type="static")
	""" Identifier of the supply"""

	voltage  :_T_pulse_schedule_reference =  sp_property(units="V")
	""" Voltage at the supply output (Vside1-Vside2)"""


class _T_pulse_schedule_pf_active_coil(SpTree):
	"""PF coil"""

	name  :str =  sp_property(type="static")
	""" Name of the coil"""

	identifier  :str =  sp_property(type="static")
	""" Identifier of the coil"""

	current  :_T_pulse_schedule_reference =  sp_property(units="A",change_nbc_version="3.37.1",change_nbc_description="structure_renamed",change_nbc_previous_name="currrent")
	""" Current fed in the coil (for 1 turn, to be multiplied by the number of turns to
		obtain the generated magnetic field), positive when flowing from side 1 to side
		2 of the coil (inside the coil), this numbering being made consistently with the
		convention that the current is counter-clockwise when seen from above."""

	resistance_additional  :_T_pulse_schedule_reference =  sp_property(units="Ohm")
	""" Additional resistance due to e.g. dynamically switchable resistors"""


class _T_pulse_schedule_tf(SpTree):
	"""Toroidal field references"""

	b_field_tor_vacuum_r  :_T_pulse_schedule_reference =  sp_property(units="T.m")
	""" Vacuum field times major radius in the toroidal field magnet. Positive sign
		means anti-clockwise when viewed from above"""

	mode  :Signal =  sp_property()
	""" Control mode (operation mode and/or settings used by the controller)"""


class _T_pulse_schedule_nbi(SpTree):
	"""Neutral beam heating and current drive system"""

	unit  :AoS[_T_pulse_schedule_nbi_unit] =  sp_property(coordinate1="1...N")
	""" Set of NBI units"""

	mode  :Signal =  sp_property()
	""" Control mode (operation mode and/or settings used by the controller)"""

	power  :_T_pulse_schedule_reference =  sp_property(units="W",introduced_after_version="3.34.0")
	""" Total NBI power (sum over the units)"""


class _T_pulse_schedule_ic(SpTree):
	"""Ion cyclotron heating and current drive system"""

	antenna  :AoS[_T_pulse_schedule_ic_antenna] =  sp_property(coordinate1="1...N")
	""" Set of ICRH antennas"""

	mode  :Signal =  sp_property()
	""" Control mode (operation mode and/or settings used by the controller)"""


class _T_pulse_schedule_lh(SpTree):
	"""Lower hybrid heating and current drive system"""

	antenna  :AoS[_T_pulse_schedule_lh_antenna] =  sp_property(coordinate1="1...N")
	""" Set of LH antennas"""

	mode  :Signal =  sp_property()
	""" Control mode (operation mode and/or settings used by the controller)"""


class _T_pulse_schedule_ec(SpTree):
	"""Electron cyclotron heating and current drive system"""

	launcher  :AoS[_T_pulse_schedule_ec_antenna] =  sp_property(coordinate1="1...N",change_nbc_version="3.26.0",change_nbc_description="aos_renamed",change_nbc_previous_name="antenna")
	""" Set of ECRH launchers"""

	mode  :Signal =  sp_property()
	""" Control mode (operation mode and/or settings used by the controller)"""

	power  :_T_pulse_schedule_reference =  sp_property(units="W",introduced_after_version="3.34.0")
	""" Total EC power (sum over the launchers)"""


class _T_pulse_schedule_density_control(SpTree):
	"""Gas injection system"""

	valve  :AoS[_T_pulse_schedule_density_control_valve] =  sp_property(coordinate1="1...N")
	""" Set of injection valves. Time-dependent"""

	n_e_line  :_T_pulse_schedule_reference =  sp_property(units="m^-2")
	""" Line integrated electron density"""

	n_e_line_method  :_T_identifier_static =  sp_property(introduced_after_version="3.34.0")
	""" Method for n_e_line calculation : Index = 1: integral over a line of sight in
		the whole vacuum chamber, 2 : integral over a line of sight within the LCFS, 3 :
		integral of a 1D core profile over rho_tor_norm up to the LCFS"""

	n_e_line_of_sight  :_T_line_of_sight_3points =  sp_property(introduced_after_version="3.34.0")
	""" Description of the line of sight for calculating n_e, defined by two points when
		the beam is not reflected, a third point is added to define the reflected beam
		path"""

	n_e_volume_average  :_T_pulse_schedule_reference =  sp_property(units="m^-3",introduced_after_version="3.34.0")
	""" Volume averaged electron density (average over the plasma volume up to the LCFS)"""

	zeff  :_T_pulse_schedule_reference =  sp_property(units="-")
	""" Line averaged effective charge"""

	zeff_method  :_T_identifier_static =  sp_property(introduced_after_version="3.34.0")
	""" Method for zeff calculation : Index = 1: average over a line of sight in the
		whole vacuum chamber, 2 : average over a line of sight within the LCFS, 3 :
		average of a 1D core profile over rho_tor_norm up to the LCFS"""

	zeff_line_of_sight  :_T_line_of_sight_3points =  sp_property(introduced_after_version="3.34.0")
	""" Description of the line of sight for calculating zeff, defined by two points
		when the beam is not reflected, a third point is added to define the reflected
		beam path"""

	n_t_over_n_d  :_T_pulse_schedule_reference =  sp_property(units="-")
	""" Average ratio of tritium over deuterium density"""

	n_h_over_n_d  :_T_pulse_schedule_reference =  sp_property(units="-")
	""" Average ratio of hydrogen over deuterium density"""

	mode  :Signal =  sp_property()
	""" Control mode (operation mode and/or settings used by the controller)"""

	ion  :AoS[_T_pulse_schedule_density_control_ion] =  sp_property(introduced_after_version="3.34.0",coordinate1="1...N")
	""" Quantities related to the different ion species, in the sense of isonuclear or
		isomolecular sequences"""


class _T_pulse_schedule_pf_active(SpTree):
	"""PF coils references"""

	coil  :AoS[_T_pulse_schedule_pf_active_coil] =  sp_property(coordinate1="1...N")
	""" Set of poloidal field coils"""

	supply  :AoS[_T_pulse_schedule_pf_active_supply] =  sp_property(coordinate1="1...N")
	""" Set of PF power supplies"""

	mode  :Signal =  sp_property()
	""" Control mode (operation mode and/or settings used by the controller)"""


class _T_pulse_schedule_position(SpTree):
	"""Flux control references"""

	magnetic_axis  :_T_pulse_schedule_rz =  sp_property()
	""" Magnetic axis position"""

	geometric_axis  :_T_pulse_schedule_rz =  sp_property()
	""" RZ position of the geometric axis (defined as (Rmin+Rmax) / 2 and (Zmin+Zmax) /
		2 of the boundary)"""

	minor_radius  :_T_pulse_schedule_reference =  sp_property(units="m")
	""" Minor radius of the plasma boundary (defined as (Rmax-Rmin) / 2 of the boundary)"""

	elongation  :_T_pulse_schedule_reference =  sp_property(units="-")
	""" Elongation of the plasma boundary"""

	elongation_upper  :_T_pulse_schedule_reference =  sp_property(units="-")
	""" Elongation (upper half w.r.t. geometric axis) of the plasma boundary"""

	elongation_lower  :_T_pulse_schedule_reference =  sp_property(units="-")
	""" Elongation (lower half w.r.t. geometric axis) of the plasma boundary"""

	triangularity  :_T_pulse_schedule_reference =  sp_property(units="-")
	""" Triangularity of the plasma boundary"""

	triangularity_upper  :_T_pulse_schedule_reference =  sp_property(units="-")
	""" Upper triangularity of the plasma boundary"""

	triangularity_lower  :_T_pulse_schedule_reference =  sp_property(units="-")
	""" Lower triangularity of the plasma boundary"""

	x_point  :AoS[_T_pulse_schedule_rz] =  sp_property(coordinate1="1...N")
	""" Array of X-points, for each of them the RZ position is given"""

	strike_point  :AoS[_T_pulse_schedule_rz] =  sp_property(coordinate1="1...N")
	""" Array of strike points, for each of them the RZ position is given"""

	active_limiter_point  :_T_pulse_schedule_rz =  sp_property()
	""" RZ position of the active limiter point (point of the plasma boundary in contact
		with the limiter)"""

	boundary_outline  :AoS[_T_pulse_schedule_outline] =  sp_property(coordinate1="1...N")
	""" Set of (R,Z) points defining the outline of the plasma boundary"""

	gap  :AoS[_T_pulse_schedule_gap] =  sp_property(coordinate1="1...N")
	""" Set of gaps, defined by a reference point and a direction."""

	mode  :Signal =  sp_property()
	""" Control mode (operation mode and/or settings used by the controller)"""


class _T_pulse_schedule(IDS):
	"""Description of Pulse Schedule, described by subsystems waveform references and
		an enveloppe around them. The controllers, pulse schedule and SDN are defined in
		separate IDSs. All names and identifiers of subsystems appearing in the
		pulse_schedule must be identical to those used in the IDSs describing the
		related subsystems.
	lifecycle_status: alpha
	lifecycle_version: 3.6.0
	lifecycle_last_change: 3.37.1"""

	dd_version="v3_38_1_dirty"
	ids_name="pulse_schedule"

	ic  :_T_pulse_schedule_ic =  sp_property()
	""" Ion cyclotron heating and current drive system"""

	ec  :_T_pulse_schedule_ec =  sp_property()
	""" Electron cyclotron heating and current drive system"""

	lh  :_T_pulse_schedule_lh =  sp_property()
	""" Lower Hybrid heating and current drive system"""

	nbi  :_T_pulse_schedule_nbi =  sp_property()
	""" Neutral beam heating and current drive system"""

	density_control  :_T_pulse_schedule_density_control =  sp_property()
	""" Gas injection system and density control references"""

	event  :AoS[_T_pulse_schedule_event] =  sp_property(coordinate1="1...N")
	""" List of events, either predefined triggers or events recorded during the pulse"""

	flux_control  :_T_pulse_schedule_flux_control =  sp_property()
	""" Magnetic flux control references"""

	pf_active  :_T_pulse_schedule_pf_active =  sp_property(introduced_after_version="3.36.0")
	""" Poloidal field coil references"""

	position_control  :_T_pulse_schedule_position =  sp_property()
	""" Plasma position and shape control references"""

	tf  :_T_pulse_schedule_tf =  sp_property()
	""" Toroidal field references"""
