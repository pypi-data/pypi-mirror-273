"""
  This module containes the _FyTok_ wrapper of IMAS/dd/camera_x_rays
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_detector_aperture,_T_camera_geometry,_T_filter_window,_T_signal_flt_1d

class _T_camera_x_rays_frame(TimeSlice):
	"""Frame of a camera"""

	counts_n  :array_type =  sp_property(type="dynamic",coordinate1="1...N",coordinate2="1...N")
	""" Number of counts detected on each pixel during one exposure time. First
		dimension : line index (horizontal axis). Second dimension: column index
		(vertical axis)."""


class _T_camera_x_rays(IDS):
	"""X-rays imaging camera (can be used for soft or hard X-rays imaging systems)
	lifecycle_status: alpha
	lifecycle_version: 3.35.0
	lifecycle_last_change: 3.35.0"""

	dd_version="v3_38_1_dirty"
	ids_name="camera_x_rays"

	name  :str =  sp_property(type="static")
	""" Name of the camera"""

	frame  :TimeSeriesAoS[_T_camera_x_rays_frame] =  sp_property(coordinate1="time",type="dynamic")
	""" Set of frames. Each time step corresponds to the beginning of the photon
		integration of each image"""

	photon_energy  :array_type =  sp_property(type="static",coordinate1="1...N",units="eV")
	""" List of values of the photon energy (coordinate for quantum_effiency)"""

	quantum_efficiency  :array_type =  sp_property(type="static",coordinate1="1...N",coordinate1_same_as="../frame/counts_n OR 1",coordinate2="1...N",coordinate2_same_as="../frame/counts_n OR 1",coordinate3="../photon_energy",units="-")
	""" Quantum efficiency of the detector, i.e. conversion factor multiplying the
		number of counts to obtain the number of photons impacting the detector,
		tabulated as a function of the photon energy, for each pixel of the detector. If
		all pixels have the same quantum efficiency, just set the size of the first and
		second dimensions to 1"""

	energy_threshold_lower  :array_type =  sp_property(type="static",units="eV",coordinate1="1...N",coordinate1_same_as="../frame/counts_n",coordinate2="1...N",coordinate2_same_as="../frame/counts_n")
	""" Lower energy detection threshold on each pixel of the detector (photons are
		counted only if their energy is above this value)"""

	energy_configuration_name  :str =  sp_property(type="static")
	""" Name of the chosen energy configuration (energy detection threshold)"""

	pixel_status  :array_type =  sp_property(type="static",coordinate1="1...N",coordinate1_same_as="../frame/counts_n",coordinate2="1...N",coordinate2_same_as="../frame/counts_n")
	""" Status of each pixel : +1 for valid pixels, -1 for inactive pixels, -2 for
		mis-calibrated pixels."""

	aperture  :DetectorAperture =  sp_property()
	""" Description of the collimating aperture of the diagnostic"""

	camera  :_T_camera_geometry =  sp_property()
	""" Characteristics of the camera used. The orientation of the camera is described
		as follows : pixels are aligned along x1 and x2 unit vectors while x3 is normal
		to the detector plane."""

	filter_window  :_T_filter_window =  sp_property()
	""" Characteristics of the filter window"""

	exposure_time  :float =  sp_property(type="constant",units="s")
	""" Exposure time"""

	readout_time  :float =  sp_property(type="constant",units="s")
	""" Time used to read out each frame on the detector"""

	latency  :float =  sp_property(type="static",units="s")
	""" Upper bound of the delay between physical information received by the detector
		and data available on the real-time (RT) network."""

	detector_humidity  :Signal =  sp_property(units="-")
	""" Fraction of humidity (0-1) measured at the detector level"""

	detector_temperature  :Signal =  sp_property(units="K")
	""" Temperature measured at the detector level"""
