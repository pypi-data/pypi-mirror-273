"""
  This module containes the _FyTok_ wrapper of IMAS/dd/reflectometer_profile
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_line_of_sight_2points,_T_signal_flt_2d,_T_psi_normalization

class _T_reflectometer_profile_position(SpTree):
	"""R, Z, Phi, psi, rho_tor_norm and theta positions associated to the electron
		density reconstruction (2D, dynamic within a type 1 array of structure)"""

	r  :array_type =  sp_property(type="dynamic",units="m",coordinate1="1...N",coordinate1_same_as="../../n_e/data",coordinate2="../../n_e/time",change_nbc_version="3.23.3",change_nbc_description="leaf_renamed",change_nbc_previous_name="r/data")
	""" Major radius"""

	z  :array_type =  sp_property(type="dynamic",units="m",coordinate1="1...N",coordinate1_same_as="../../n_e/data",coordinate2="../../n_e/time",change_nbc_version="3.23.3",change_nbc_description="leaf_renamed",change_nbc_previous_name="z/data")
	""" Height"""

	phi  :array_type =  sp_property(type="dynamic",units="rad",coordinate1="1...N",coordinate1_same_as="../../n_e/data",coordinate2="../../n_e/time",change_nbc_version="3.23.3",change_nbc_description="leaf_renamed",change_nbc_previous_name="phi/data")
	""" Toroidal angle (oriented counter-clockwise when viewing from above)"""

	psi  :array_type =  sp_property(type="dynamic",units="W",coordinate1="1...N",coordinate1_same_as="../../n_e/data",coordinate2="../../n_e/time")
	""" Poloidal flux"""

	rho_tor_norm  :array_type =  sp_property(type="dynamic",units="-",coordinate1="1...N",coordinate1_same_as="../../n_e/data",coordinate2="../../n_e/time")
	""" Normalised toroidal flux coordinate"""

	theta  :array_type =  sp_property(type="dynamic",units="rad",coordinate1="1...N",coordinate1_same_as="../../n_e/data",coordinate2="../../n_e/time")
	""" Poloidal angle (oriented clockwise when viewing the poloidal cross section on
		the right hand side of the tokamak axis of symmetry, with the origin placed on
		the plasma magnetic axis)"""


class _T_reflectometer_channel(SpTree):
	"""Reflectometer channel"""

	name  :str =  sp_property(type="static")
	""" Name of the channel"""

	identifier  :str =  sp_property(type="static")
	""" ID of the channel"""

	mode  :str =  sp_property(type="static")
	""" Detection mode _X_ or _O_"""

	line_of_sight_emission  :_T_line_of_sight_2points =  sp_property()
	""" Description of the line of sight of the emission antenna. The first point
		corresponds to the antenna mouth. The second point correspond to the
		interception of the line of sight with the reflection surface on the inner wall."""

	line_of_sight_detection  :_T_line_of_sight_2points =  sp_property()
	""" Description of the line of sight of the detection antenna, to be filled only if
		its position is distinct from the emission antenna. The first point corresponds
		to the antenna mouth. The second point correspond to the interception of the
		line of sight with the reflection surface on the inner wall."""

	sweep_time  :float =  sp_property(type="static",units="s")
	""" Duration of a sweep"""

	frequencies  :array_type =  sp_property(type="static",units="Hz",coordinate1="1...N")
	""" Array of frequencies scanned during a sweep"""

	phase  :SignalND =  sp_property(coordinate1="../frequencies",coordinate2="time",units="rad")
	""" Measured phase of the probing wave for each frequency and time slice
		(corresponding to the begin time of a sweep), relative to the phase at launch"""

	position  :_T_reflectometer_profile_position =  sp_property()
	""" Position of the density measurements"""

	n_e  :SignalND =  sp_property(coordinate1="1...N",coordinate2="time",units="m^-3")
	""" Electron density"""

	cut_off_frequency  :array_type =  sp_property(type="dynamic",coordinate1="1...N",coordinate1_same_as="../n_e/data",coordinate2="../n_e/time",units="Hz")
	""" Cut-off frequency as a function of measurement position and time"""


class _T_reflectometer_profile(IDS):
	"""Profile reflectometer diagnostic. Multiple reflectometers are considered as
		independent diagnostics to be handled with different occurrence numbers
	lifecycle_status: alpha
	lifecycle_version: 3.11.0
	lifecycle_last_change: 3.33.0"""

	dd_version="v3_38_1_dirty"
	ids_name="reflectometer_profile"

	type  :str =  sp_property(type="static")
	""" Type of reflectometer (frequency_swept, radar, ...)"""

	channel  :AoS[_T_reflectometer_channel] =  sp_property(coordinate1="1...N")
	""" Set of channels, e.g. different reception antennas or frequency bandwidths of
		the reflectometer"""

	position  :_T_reflectometer_profile_position =  sp_property()
	""" Position associated to the density reconstruction from multiple channels"""

	n_e  :SignalND =  sp_property(coordinate1="1...N",coordinate2="time",units="m^-3")
	""" Electron density reconstructed from multiple channels"""

	psi_normalization  :_T_psi_normalization =  sp_property()
	""" Quantities to use to normalize psi, as a function of time"""

	latency  :float =  sp_property(type="static",units="s",introduced_after_version="3.32.1")
	""" Upper bound of the delay between physical information received by the detector
		and data available on the real-time (RT) network."""
