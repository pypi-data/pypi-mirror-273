"""
  This module containes the _FyTok_ wrapper of IMAS/dd/camera_ir
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_identifier_static
from .utilities import _E_midplane_identifier

class _T_camera_ir_calibration(SpTree):
	"""Calibration data"""

	luminance_to_temperature  :array_type =  sp_property(type="static",coordinate1="1...N",coordinate2="1...2")
	""" Luminance to temperature conversion table"""

	transmission_barrel  :array_type =  sp_property(type="static",coordinate1="1...N",coordinate1_same_as="../../frame/image_raw",coordinate2="1...N",coordinate2_same_as="../../frame/image_raw")
	""" Transmission of the optical barrel"""

	transmission_mirror  :array_type =  sp_property(type="static",coordinate1="1...N",coordinate1_same_as="../../frame/image_raw",coordinate2="1...N",coordinate2_same_as="../../frame/image_raw")
	""" Transmission of the mirror"""

	transmission_window  :array_type =  sp_property(type="static",coordinate1="1...N",coordinate1_same_as="../../frame/image_raw",coordinate2="1...N",coordinate2_same_as="../../frame/image_raw")
	""" Transmission of the window"""

	optical_temperature  :array_type =  sp_property(type="static",coordinate1="1...N",coordinate2="1...N")
	""" Temperature of the optical components (digital levels)"""


class _T_camera_ir_frame_analysis(TimeSlice):
	"""Frame analysis"""

	sol_heat_decay_length  :float =  sp_property(type="dynamic",units="m")
	""" Heat flux decay length in SOL at divertor entrance, mapped to the mid-plane,
		this is the lambda_q parameter defined in reference T. Eich et al, Nucl. Fusion
		53 (2013) 093031"""

	distance_separatrix_midplane  :array_type =  sp_property(type="dynamic",units="m",coordinate1="1...N")
	""" Distance between the measurement position and the separatrix, mapped along flux
		surfaces to the outboard midplane, in the major radius direction. Positive value
		means the measurement is outside of the separatrix."""

	power_flux_parallel  :array_type =  sp_property(type="dynamic",units="W.m^-2",coordinate1="../distance_separatrix_midplane")
	""" Parallel heat flux received by the element monitored by the camera, along the
		distance_separatrix_midplane coordinate"""


class _T_camera_ir_frame(TimeSlice):
	"""Frame of a camera"""

	surface_temperature  :array_type =  sp_property(type="dynamic",coordinate1="1...N",coordinate2="1...N",units="K",introduced_after_version="3.34.0")
	""" Surface temperature image. First dimension : line index (horizontal axis).
		Second dimension: column index (vertical axis)."""


class _T_camera_ir(IDS):
	"""Infrared camera for monitoring of Plasma Facing Components
	lifecycle_status: alpha
	lifecycle_version: 3.23.4
	lifecycle_last_change: 3.35.0"""

	dd_version="v3_38_1_dirty"
	ids_name="camera_ir"

	name  :str =  sp_property(type="static")
	""" Name of the camera"""

	calibration  :_T_camera_ir_calibration =  sp_property()
	""" Calibration data"""

	frame  :TimeSeriesAoS[_T_camera_ir_frame] =  sp_property(coordinate1="time",type="dynamic")
	""" Set of frames"""

	midplane  :_E_midplane_identifier =  sp_property(doc_identifier="utilities/midplane_identifier.xml",introduced_after_version="3.32.1")
	""" Choice of midplane definition for the mapping of measurements on an equilibrium"""

	frame_analysis  :TimeSeriesAoS[_T_camera_ir_frame_analysis] =  sp_property(coordinate1="time",type="dynamic",introduced_after_version="3.32.1")
	""" Quantities deduced from frame analysis for a set of time slices"""

	latency  :float =  sp_property(type="static",units="s",introduced_after_version="3.32.1")
	""" Upper bound of the delay between physical information received by the detector
		and data available on the real-time (RT) network."""
