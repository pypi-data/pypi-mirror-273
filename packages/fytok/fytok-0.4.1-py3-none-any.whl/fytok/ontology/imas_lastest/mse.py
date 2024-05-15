"""
  This module containes the _FyTok_ wrapper of IMAS/dd/mse
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_rzphi0d_dynamic_aos3,_T_detector_aperture,_T_line_of_sight_2points,_T_signal_flt_1d_validity

class _T_mse_channel_intersection(SpTree):
	"""MSE beam-los intersection"""

	r  :float =  sp_property(type="static",units="m")
	""" Major radius"""

	z  :float =  sp_property(type="static",units="m")
	""" Height"""

	phi  :float =  sp_property(type="static",units="rad")
	""" Toroidal angle"""

	delta_r  :float =  sp_property(type="static",units="m")
	""" Full width along major radius"""

	delta_z  :float =  sp_property(type="static",units="m")
	""" Full width in height"""

	delta_phi  :float =  sp_property(type="static",units="rad")
	""" Full width in toroidal angle"""


class _T_mse_channel_resolution(TimeSlice):
	"""In case of active spectroscopy, spatial resolution of the measurement"""

	centre  :_T_rzphi0d_dynamic_aos3 =  sp_property()
	""" Position of the centre of the spatially resolved zone"""

	width  :_T_rzphi0d_dynamic_aos3 =  sp_property()
	""" Full width of the spatially resolved zone in the R, Z and phi directions"""

	geometric_coefficients  :array_type =  sp_property(type="dynamic",coordinate1="1...9",units="mixed")
	""" Set of 9 geometric coefficients providing the MSE polarisation angle as a
		function of the local electric and magnetic field components (these are related
		to the angle between beam and line of sight). The list is ordered as follows :
		coefficients of BZ, BR, Bphi, ER (numerator of the MSE angle expression);
		coefficients of BZ, BR, Bphi, ER, EZ (denominator)"""


class _T_mse_channel(SpTree):
	"""MSE channel"""

	name  :str =  sp_property(type="static")
	""" Name of the channel"""

	detector  :DetectorAperture =  sp_property()
	""" Detector description"""

	aperture  :AoS[DetectorAperture] =  sp_property(coordinate1="1...N")
	""" Description of a set of collimating apertures"""

	line_of_sight  :_T_line_of_sight_2points =  sp_property()
	""" Description of the line of sight of the channel, given by 2 points"""

	active_spatial_resolution  :TimeSeriesAoS[_T_mse_channel_resolution] =  sp_property(coordinate1="time",type="dynamic")
	""" Spatial resolution of the measurement, calculated as a convolution of the atomic
		smearing, magnetic and beam geometry smearing and detector projection, for a set
		of time slices (use a single time slice for the whole pulse if the beam and the
		line of sight are not moving during the pulse)"""

	polarisation_angle  :Signal =  sp_property(units="rad")
	""" MSE polarisation angle"""


class _T_mse(IDS):
	"""Motional Stark Effect diagnostic
	lifecycle_status: alpha
	lifecycle_version: 3.16.0
	lifecycle_last_change: 3.33.0"""

	dd_version="v3_38_1_dirty"
	ids_name="mse"

	channel  :AoS[_T_mse_channel] =  sp_property(coordinate1="1...N")
	""" Set of channels (lines of sight)"""

	latency  :float =  sp_property(type="static",units="s",introduced_after_version="3.32.1")
	""" Upper bound of the delay between physical information received by the detector
		and data available on the real-time (RT) network."""
