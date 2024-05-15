"""
  This module containes the _FyTok_ wrapper of IMAS/dd/neutron_diagnostic
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_identifier_static,_T_rzphi1d_grid,_T_signal_flt_1d,_T_identifier,_T_rzphi0d_static,_T_detector_aperture,_T_detector_energy_band,_T_signal_int_2d,_T_rz0d_static

class _E_neutron_event(IntFlag):
	"""Translation table for type of events measured in the neutron detector	xpath: 	"""
  
	energy_neutron = 1
	"""Neutron energy in the detector [eV]"""
  
	voltage = 2
	"""Voltage in the detector [V]"""
  
	time_of_flight = 3
	"""Time of flight [s]"""
  
	trajectory_length = 4
	"""Particle trajectory length [m]"""
  
	energy_deposited = 5
	"""Deposited energy [eV]"""
  
	light_yield = 6
	"""Light yield [eVee]"""
  
	count_rate = 7
	"""Number of events/reactions per second [s^-1]"""
  

class _T_xyz3d_static(SpTree):
	"""Structure for list of X, Y, Z components (3D, static), one set of X,Y,Z
		components being given for each voxel of the emission grid"""

	x  :array_type =  sp_property(type="static",units="m",coordinate1="../../emission_grid/r",coordinate2="../../emission_grid/z",coordinate3="../../emission_grid/phi")
	""" Components along X axis for each voxel"""

	y  :array_type =  sp_property(type="static",units="m",coordinate1="../../emission_grid/r",coordinate2="../../emission_grid/z",coordinate3="../../emission_grid/phi")
	""" Component along Y axis for each voxel"""

	z  :array_type =  sp_property(type="static",units="m",coordinate1="../../emission_grid/r",coordinate2="../../emission_grid/z",coordinate3="../../emission_grid/phi")
	""" Component along Z axis for each voxel"""


class _T_neutron_diagnostic_adc(SpTree):
	"""ADC"""

	power_switch  :int =  sp_property(type="static")
	""" Power switch (1=on, 0=off)"""

	discriminator_level_lower  :int =  sp_property(type="static")
	""" Lower level discriminator of ADC"""

	discriminator_level_upper  :int =  sp_property(type="static")
	""" Upper level discriminator of ADC"""

	sampling_rate  :int =  sp_property(type="static")
	""" Number of samples recorded per second"""

	bias  :float =  sp_property(units="V",type="static")
	""" ADC signal bias"""

	input_range  :float =  sp_property(units="V",type="static")
	""" ADC input range"""

	impedance  :float =  sp_property(units="ohm",type="static")
	""" ADC impedance"""


class _T_neutron_diagnostic_characteristics_reaction_mode(SpTree):
	""""""

	index  :int =  sp_property(type="static")
	""" Index of Measuring Mode"""

	name  :str =  sp_property(type="static")
	""" Name of Measuring Mode"""

	count_limit_max  :float =  sp_property(type="static",units="cps")
	""" Maximum count limit of recent Measuring Mode and plasma reaction"""

	count_limit_min  :float =  sp_property(type="static",units="cps")
	""" Minimum count limit of recent Measuring Mode and plasma reaction"""


class _T_neutron_diagnostic_detectors_radiation(SpTree):
	""""""

	index  :int =  sp_property(type="static")
	""" Index of radiation type"""

	converter_name  :str =  sp_property(type="static")
	""" Name of detector's converter for resent particle"""

	converter_volume  :float =  sp_property(type="static",units="m^3")
	""" Volume of detector's converter for resent particle"""

	converter_nuclear_density  :float =  sp_property(type="static",units="m^-3")
	""" Nuclear density of detector's converter for resent particle"""

	converter_temperature  :Expression  =  sp_property(type="dynamic",coordinate1="/time",units="K")
	""" Temperature of detector's converter"""


class _T_neutron_diagnostic_synthetic_signals(SpTree):
	""""""

	total_neutron_flux  :Expression  =  sp_property(type="dynamic",coordinate1="../../time",units="s^-1")
	""" Total Neutron Flux in Dynamic"""

	fusion_power  :Expression  =  sp_property(type="dynamic",coordinate1="../../time",units="W")
	""" Fusion Power"""


class _T_neutron_diagnostic_unit_source_radiation_reaction(SpTree):
	""""""

	energy  :array_type =  sp_property(type="static",coordinate1="1...N",units="eV")
	""" Energy boundaries for Detector Radiator Flux"""

	flux  :array_type =  sp_property(type="static",coordinate1="../../../../detectors",coordinate2="../energy",units="m^-2")
	""" Radiation flux from Unit Ring Source in recent detector's converter"""

	d2flux_drdz  :array_type =  sp_property(type="static",coordinate1="../../../../detectors",coordinate2="../energy",units="m^-4")
	""" Second deriviation of Radiation flux from Unit Ring Source in recent detector's
		converter for _spline_ reconstruction"""

	reaction_rate  :array_type =  sp_property(type="static",coordinate1="../../../../detectors",coordinate2="../energy",units="m^-3")
	""" Reaction Rate on converter's material from Unit Ring Source in recent detector's
		converter"""

	sensitivity  :array_type =  sp_property(type="static",coordinate1="../../../../detectors",coordinate2="../energy",units="cps.m^2.s")
	""" Sensitivity of converter's material in recent detector's converter"""


class _T_neutron_diagnostic_event(SpTree):
	"""Event in the detector"""

	type  :_E_neutron_event =  sp_property(doc_identifier="neutron_diagnostic/neutron_event_identifier.xml")
	""" Type of the event"""

	values  :array_type =  sp_property(type="static",units="mixed",coordinate1="1...N")
	""" Array of values for the event"""


class _T_neutron_diagnostic_field_of_view(SpTree):
	"""Field of view"""

	solid_angle  :array_type =  sp_property(type="static",units="sr",coordinate1="../emission_grid/r",coordinate2="../emission_grid/z",coordinate3="../emission_grid/phi")
	""" Average solid angle that the detector covers within the voxel"""

	emission_grid  :_T_rzphi1d_grid =  sp_property()
	""" Grid defining the neutron emission cells in the plasma"""

	direction_to_detector  :_T_xyz3d_static =  sp_property()
	""" Vector that points from the centre of the voxel to the centre of the detector,
		described in the (X,Y,Z) coordinate system, where X is the major radius axis for
		phi = 0, Y is the major radius axis for phi = pi/2, and Z is the height axis."""


class _T_neutron_diagnostic_temperature_sensor(SpTree):
	"""Temperature sensor"""

	power_switch  :int =  sp_property(type="static")
	""" Power switch (1=on, 0=off)"""

	temperature  :Signal =  sp_property(units="K")
	""" Temperature measured by the sensor"""


class _T_neutron_diagnostic_b_field_sensor(SpTree):
	"""Magnetic field sensor"""

	power_switch  :int =  sp_property(type="static")
	""" Power switch (1=on, 0=off)"""

	b_field  :Signal =  sp_property(units="T")
	""" Magnetic field measured by the sensor"""


class _T_neutron_diagnostic_test_generator(SpTree):
	"""Test generator"""

	power_switch  :int =  sp_property(type="static")
	""" Power switch (1=on, 0=off)"""

	shape  :_T_identifier =  sp_property()
	""" Signal shape. Index : 1 – rectangular, 2 – gaussian"""

	rise_time  :float =  sp_property(type="constant",units="s")
	""" Peak rise time"""

	fall_time  :float =  sp_property(type="constant",units="s")
	""" Peak fall time"""

	frequency  :Signal =  sp_property(units="Hz")
	""" Generated signal frequency"""

	amplitude  :Signal =  sp_property(units="V")
	""" Generated signal amplitude"""


class _T_neutron_diagnostic_supply(SpTree):
	"""Power supply"""

	power_switch  :int =  sp_property(type="static")
	""" Power switch (1=on, 0=off)"""

	voltage_set  :Signal =  sp_property(units="V")
	""" Voltage set"""

	voltage_out  :Signal =  sp_property(units="V")
	""" Voltage at the supply output"""


class _T_neutron_diagnostic_characteristics_reaction(SpTree):
	""""""

	index  :int =  sp_property(type="static")
	""" Index of plasma reaction type"""

	error  :float =  sp_property(type="static",units="-")
	""" Diagnostic's relative uncertainty for recent plasma reaction"""

	probability_overlap  :float =  sp_property(type="static",units="-")
	""" Pulse probability overlap for recent plasma reaction"""

	mode  :AoS[_T_neutron_diagnostic_characteristics_reaction_mode] =  sp_property(coordinate1="index")
	""" Characteristics of counting linear limits in recent Measuring modes for recent
		Plasma reaction type"""


class _T_neutron_diagnostic_detectors_mode(SpTree):
	""""""

	name  :str =  sp_property(type="static")
	""" Name of Measuring Mode"""

	counting  :Signal =  sp_property(units="cps")
	""" Counting in Measuring Mode in Dynamic"""


class _T_neutron_diagnostic_unit_source_radiation(SpTree):
	""""""

	reaction  :AoS[_T_neutron_diagnostic_unit_source_radiation_reaction] =  sp_property(coordinate1="1...2")
	""" Plasma reaction (1 - 'DT'; 2 - 'DD')"""


class _T_neutron_diagnostic_green(SpTree):
	"""Green functions"""

	source_neutron_energies  :array_type =  sp_property(type="static",units="eV",coordinate1="1...N")
	""" Array of source neutron energy bins"""

	event_in_detector_neutron_flux  :_T_neutron_diagnostic_event =  sp_property(introduced_after_version="3.38.0",change_nbc_version="3.38.1",change_nbc_description="structure_renamed",change_nbc_previous_name="event_in_detector")
	""" 5th dimension for the neutron_flux Green function representing values of events
		measured in the detector. The type of events monitored depends on the detector
		and can be defined by the user. It can be energy of neutrons, or electrical
		signal, or time of flight ... (defined by type below)"""

	neutron_flux  :array_type =  sp_property(type="static",units="m^-2.neutron^-1",coordinate1="../../field_of_view/emission_grid/r",coordinate2="../../field_of_view/emission_grid/z",coordinate3="../../field_of_view/emission_grid/phi",coordinate4="../source_neutron_energies",coordinate5="../event_in_detector_neutron_flux/values")
	""" Grouped neutron flux in the detector from one neutron energy bin emitted by the
		current plasma voxel towards the detector"""

	event_in_detector_response_function  :_T_neutron_diagnostic_event =  sp_property(introduced_after_version="3.38.0",change_nbc_version="3.38.1",change_nbc_description="structure_renamed",change_nbc_previous_name="event_in_detector")
	""" 5th dimension for the response_function Green function representing values of
		events measured in the detector. The type of events monitored depends on the
		detector and can be defined by the user. It can be energy of neutrons, or
		electrical signal, or time of flight ... (defined by type below)"""

	response_function  :array_type =  sp_property(type="static",units="events.neutron^-1",coordinate1="../../field_of_view/emission_grid/r",coordinate2="../../field_of_view/emission_grid/z",coordinate3="../../field_of_view/emission_grid/phi",coordinate4="../source_neutron_energies",coordinate5="../event_in_detector_response_function/values")
	""" Number of events occurring in the detector from one neutron energy bin emitted
		by the current plasma voxel towards the detector"""


class _T_neutron_diagnostic_characteristics(SpTree):
	""""""

	dead_time  :float =  sp_property(type="static",units="s")
	""" Dead time of detectors"""

	pulse_length  :float =  sp_property(type="static",units="s")
	""" Lower counting limit of recent Measuring Mode and plasma reaction"""

	reaction  :AoS[_T_neutron_diagnostic_characteristics_reaction] =  sp_property(coordinate1="index")
	""" Plasma reaction (1 -'DT'; 2 - 'DD')"""


class _T_neutron_diagnostic_unit_source(SpTree):
	"""Unit ring sources distribution"""

	position  :_T_rz0d_static =  sp_property()
	""" Position of ring unit sources inside ITER vacuum vessel"""

	radiation  :AoS[_T_neutron_diagnostic_unit_source_radiation] =  sp_property(coordinate1="1...2")
	""" Radiation type on detector's converter (1 - 'neutrons'; 2 - 'gamma-rays')"""


class _T_neutron_diagnostic_detectors(SpTree):
	""""""

	name  :str =  sp_property(type="static")
	""" Name of Detector"""

	radiation  :AoS[_T_neutron_diagnostic_detectors_radiation] =  sp_property(coordinate1="index")
	""" Radiation type on detector's converter (1 - 'neutrons'; 2 - 'gamma-rays')"""

	position  :_T_rzphi0d_static =  sp_property()
	""" Detector Position Data SHOULD BE REMOVED, REDUNDANT WITH THE NEW DETECTOR
		DESCRIPTION"""

	detector  :DetectorAperture =  sp_property()
	""" Detector description"""

	aperture  :AoS[DetectorAperture] =  sp_property(coordinate1="1...N")
	""" Description of a set of collimating apertures"""

	mode  :AoS[_T_neutron_diagnostic_detectors_mode] =  sp_property(type="static",coordinate1="1...N")
	""" Measuring Mode Properties and Data"""

	energy_band  :AoS[_T_detector_energy_band] =  sp_property(coordinate1="1...N")
	""" Set of energy bands in which neutrons are counted by the detector"""

	start_time  :float =  sp_property(type="constant",units="s")
	""" Time stamp of the moment diagnostic starts recording data"""

	end_time  :float =  sp_property(type="constant",units="s")
	""" Time stamp of the moment diagnostic ends recording data"""

	spectrum_sampling_time  :float =  sp_property(type="constant",units="s")
	""" Sampling time used to obtain one spectrum time slice"""

	amplitude_raw  :Signal =  sp_property(units="V")
	""" Raw amplitude of the measured signal"""

	amplitude_peak  :Signal =  sp_property(units="V")
	""" Processed peak amplitude of the measured signal"""

	spectrum_total  :array_type =  sp_property(type="constant",coordinate1="../energy_band")
	""" Detected count per energy channel, integrated over the whole acquisition
		duration"""

	spectrum  :SignalND =  sp_property(coordinate1="../energy_band",coordinate2="time")
	""" Detected count per energy channel as a function of time"""

	adc  :_T_neutron_diagnostic_adc =  sp_property()
	""" Description of analogic-digital converter"""

	supply_high_voltage  :_T_neutron_diagnostic_supply =  sp_property()
	""" Description of high voltage power supply"""

	supply_low_voltage  :_T_neutron_diagnostic_supply =  sp_property()
	""" Description of low voltage power supply"""

	test_generator  :_T_neutron_diagnostic_test_generator =  sp_property()
	""" Test generator characteristics"""

	b_field_sensor  :_T_neutron_diagnostic_test_generator =  sp_property()
	""" Magnetic field sensor"""

	temperature_sensor  :_T_neutron_diagnostic_test_generator =  sp_property()
	""" Temperature sensor"""

	field_of_view  :_T_neutron_diagnostic_field_of_view =  sp_property()
	""" Field of view associated to this detector. The field of view is described by a
		voxelized plasma volume. Each voxel, with indexes i_R, i_Z, and i_phi, has an
		associated solid angle scalar and a detector direction vector."""

	green_functions  :_T_neutron_diagnostic_green =  sp_property()
	""" Green function coefficients used to represent the detector response based on its
		field of view"""


class _T_neutron_diagnostic(IDS):
	"""Neutron diagnostic such as DNFM, NFM or MFC
	lifecycle_status: alpha
	lifecycle_version: 3.6.0
	lifecycle_last_change: 3.38.1"""

	dd_version="v3_38_1_dirty"
	ids_name="neutron_diagnostic"

	characteristics  :_T_neutron_diagnostic_characteristics =  sp_property()
	""" Description of Diagnostic's module detection characteristics for differen plasma
		modes based on Design Description"""

	detectors  :AoS[_T_neutron_diagnostic_detectors] =  sp_property(coordinate1="1...N")
	""" Description of Detectors properties and Data in Neutron Diagnostic Module"""

	synthetic_signals  :_T_neutron_diagnostic_synthetic_signals =  sp_property()
	""" Output Data from Neutron Diagnostic's Module"""

	unit_source  :AoS[_T_neutron_diagnostic_unit_source] =  sp_property(coordinate1="1...N")
	""" Unit ring sources description"""

	latency  :float =  sp_property(type="static",units="s",introduced_after_version="3.32.1")
	""" Upper bound of the delay between physical information received by the detector
		and data available on the real-time (RT) network."""
