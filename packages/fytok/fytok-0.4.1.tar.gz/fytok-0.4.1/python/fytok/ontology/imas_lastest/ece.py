"""
  This module containes the _FyTok_ wrapper of IMAS/dd/ece
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_signal_flt_2d,_T_signal_flt_1d,_T_physical_quantity_flt_1d_time_1,_T_rzphirhopsitheta1d_dynamic_aos1_common_time_1,_T_signal_flt_1d_validity,_T_line_of_sight_2points,_T_signal_flt_1d_validity_position,_T_polarizer,_T_psi_normalization

class _T_ece_channel_beam_spot(SpTree):
	"""Spot ellipse characteristics"""

	size  :SignalND =  sp_property(coordinate1="1...2",coordinate2="time",units="m")
	""" Size of the spot ellipse"""

	angle  :Signal =  sp_property(units="rad")
	""" Rotation angle for the spot ellipse"""


class _T_ece_channel_beam_phase(SpTree):
	"""Phase ellipse characteristics"""

	curvature  :SignalND =  sp_property(coordinate1="1...2",coordinate2="time",units="m^-1")
	""" Inverse curvature radii for the phase ellipse, positive/negative for
		divergent/convergent beams"""

	angle  :Signal =  sp_property(units="rad")
	""" Rotation angle for the phase ellipse"""


class _T_ece_channel_beam(SpTree):
	"""Beam characteristics"""

	spot  :_T_ece_channel_beam_spot =  sp_property()
	""" Spot ellipse characteristics"""

	phase  :_T_ece_channel_beam_phase =  sp_property()
	""" Phase ellipse characteristics"""


class _T_ece_channel(SpTree):
	"""Charge exchange channel"""

	name  :str =  sp_property(type="static")
	""" Name of the channel"""

	identifier  :str =  sp_property(type="static")
	""" ID of the channel"""

	frequency  :_T_physical_quantity_flt_1d_time_1 =  sp_property(units="Hz")
	""" Frequency of the channel"""

	harmonic  :_T_physical_quantity_flt_1d_time_1 =  sp_property()
	""" Harmonic detected by the channel. 1 corresponds to the _O1_ mode, while 2
		corresponds to the _X2_ mode."""

	if_bandwidth  :float =  sp_property(type="static",units="Hz")
	""" Full-width of the Intermediate Frequency (IF) bandpass filter"""

	position  :_T_rzphirhopsitheta1d_dynamic_aos1_common_time_1 =  sp_property()
	""" Position of the measurements (taking into account the suprathermal shift)"""

	delta_position_suprathermal  :_T_rzphirhopsitheta1d_dynamic_aos1_common_time_1 =  sp_property()
	""" Simple estimate of the difference in position induced by the presence of
		suprathermal electrons. Position without corrections = position -
		delta_position_suprathermal"""

	t_e  :_T_physical_quantity_flt_1d_time_1 =  sp_property(units="eV")
	""" Electron temperature"""

	t_e_voltage  :Signal =  sp_property(units="V")
	""" Raw voltage measured on each channel, from which the calibrated temperature data
		is then derived"""

	optical_depth  :_T_physical_quantity_flt_1d_time_1 =  sp_property(units="-")
	""" Optical depth of the plasma at the position of the measurement. This parameter
		is a proxy for the local / non-local character of the ECE emission. It must be
		greater than 1 to guarantee that the measurement is dominated by local ECE
		emission (non-local otherwise)"""

	time  :array_type =  sp_property(coordinate1="1...N",type="dynamic",units="s")
	""" Timebase for the processed dynamic data of this channel (outside of the beam
		structure)"""

	beam  :_T_ece_channel_beam =  sp_property()
	""" ECE Gaussian optics parameters taken at the line_of_sight/first_point position
		(for synthetic modelling of the ECE emission)"""


class _T_ece(IDS):
	"""Electron cyclotron emission diagnostic
	lifecycle_status: alpha
	lifecycle_version: 3.2.1
	lifecycle_last_change: 3.33.0"""

	dd_version="v3_38_1_dirty"
	ids_name="ece"

	line_of_sight  :_T_line_of_sight_2points =  sp_property()
	""" Description of the line of sight of the diagnostic (valid for all channels),
		defined by two points. By convention, the first point is the closest to the
		diagnostic"""

	t_e_central  :_T_signal_flt_1d_validity_position =  sp_property(units="eV")
	""" Electron temperature from the closest channel to the magnetic axis, together
		with its radial location"""

	channel  :AoS[_T_ece_channel] =  sp_property(coordinate1="1...N")
	""" Set of channels (frequency)"""

	polarizer  :AoS[_T_polarizer] =  sp_property(coordinate1="1...N")
	""" Set of polarizers placed in front of the diagnostic (if any). Polarizers are
		assumed to be orthogonal to the line of sight, so that the x3 unit vector is
		aligned with the line of sight"""

	psi_normalization  :_T_psi_normalization =  sp_property()
	""" Quantities to use to normalize psi, as a function of time"""

	latency  :float =  sp_property(type="static",units="s",introduced_after_version="3.32.1")
	""" Upper bound of the delay between physical information received by the detector
		and data available on the real-time (RT) network."""
