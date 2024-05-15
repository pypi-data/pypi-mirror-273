"""
  This module containes the _FyTok_ wrapper of IMAS/dd/camera_visible
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_geometry_matrix_emission,_T_detector_aperture

class _T_camera_visible_geometry_matrix_step2(SpTree):
	"""Geometry matrix of the detector"""

	data  :array_type =  sp_property(type="static",coordinate1="1...N",units="m")
	""" The Ray Transfer Matrix (RTM, or geometry matrix) here provides transformation
		of the signal from each individual unit light source (voxel) to each pixel of
		the receiver (detector). The emission profile has [photons.m^-3.s^-1.sr^-1]
		units and radiance signal has [photons.m^-2.s^-1.sr^-1] units. So the RTM has
		[m] units. This data is stored in a sparse form, i.e. the array contains only
		the non-zero element of the Ray transfer matrix. The voxel index corresponding
		to an element of this array can be found in voxel_indices. The pixel indices
		corresponding to an element of this array can be found in pixel_indices"""

	voxel_indices  :array_type =  sp_property(type="static",coordinate1="../data")
	""" List of voxel indices (defined in the voxel map) used in the sparse data array"""

	pixel_indices  :array_type =  sp_property(type="static",coordinate1="../data",coordinate2="1...2")
	""" List of pixel indices used in the sparse data array. The first dimension refers
		to the data array index. The second dimension lists the line index (horizontal
		axis) in first position, then the column index (vertical axis)."""


class _T_camera_visible_geometry_matrix_interpolated(SpTree):
	"""Interpolated geometry matrix"""

	r  :array_type =  sp_property(type="constant",units="m",coordinate1="1...N")
	""" Major radius of interpolation knots"""

	z  :array_type =  sp_property(type="constant",units="m",coordinate1="../r")
	""" Height of interpolation knots"""

	phi  :array_type =  sp_property(type="constant",units="rad",coordinate1="../r")
	""" Toroidal angle (oriented counter-clockwise when viewing from above) of
		interpolation knots"""

	data  :array_type =  sp_property(type="constant",coordinate1="1...N",coordinate1_same_as="../../../frame/image_raw",coordinate2="1...N",coordinate2_same_as="../../../frame/image_raw",coordinate3="../r",units="m^-2")
	""" Interpolated Ray Transfer Matrix (RTM, or geometry matrix), which provides
		transformation of the reflected light from each interpolation knot to the
		receiver (detector pixel). When convolving with an emission profile, the values
		must be interpolated to the emission grid and multiplied by the volume of the
		grid cells. The interpolated matrix is given on an array of interpolation knots
		of coordinates r, z and phi (third dimension of this array). The first two
		dimension correspond to the detector pixels : first dimension : line index
		(horizontal axis); second dimension: column index (vertical axis)."""


class _T_camera_visible_geometry_matrix(SpTree):
	"""Geometry matrix of the camera"""

	with_reflections  :_T_camera_visible_geometry_matrix_step2 =  sp_property(introduced_after_version="3.37.2")
	""" Geometry matrix with reflections"""

	without_reflections  :_T_camera_visible_geometry_matrix_step2 =  sp_property(introduced_after_version="3.37.2")
	""" Geometry matrix without reflections"""

	interpolated  :_T_camera_visible_geometry_matrix_interpolated =  sp_property(introduced_after_version="3.37.2")
	""" Interpolated geometry matrix for reflected light"""

	voxel_map  :array_type =  sp_property(type="static",coordinate1="../emission_grid/r",coordinate2="../emission_grid/z",coordinate3="../emission_grid/phi")
	""" Voxel map for geometry matrix. The cells with same number are merged in the
		computation into a single emission source meta-cell (the voxel). Cells with
		number -1 are excluded. Voxel count starts from 0."""

	voxels_n  :int =  sp_property(type="static",introduced_after_version="3.37.2")
	""" Number of voxels defined in the voxel_map."""

	emission_grid  :_T_geometry_matrix_emission =  sp_property()
	""" Grid defining the light emission cells"""


class _T_camera_visible_frame(TimeSlice):
	"""Frame of a camera"""

	image_raw  :array_type =  sp_property(type="dynamic",coordinate1="1...N",coordinate2="1...N")
	""" Raw image (unprocessed) (digital levels). First dimension : line index
		(horizontal axis). Second dimension: column index (vertical axis)."""

	radiance  :array_type =  sp_property(type="dynamic",coordinate1="1...N",coordinate1_same_as="../image_raw",coordinate2="1...N",coordinate2_same_as="../image_raw",units="photons.m^-2.s^-1.sr^-1")
	""" Radiance image. First dimension : line index (horizontal axis). Second
		dimension: column index (vertical axis)."""


class _T_camera_visible_detector(SpTree):
	"""Detector for a visible camera"""

	pixel_to_alpha  :array_type =  sp_property(type="static",units="rad",coordinate1="1...N",coordinate1_same_as="../frame/image_raw")
	""" Alpha angle of each pixel in the horizontal axis"""

	pixel_to_beta  :array_type =  sp_property(type="static",units="rad",coordinate1="1...N")
	""" Beta angle of each pixel in the vertical axis"""

	wavelength_lower  :float =  sp_property(type="static",units="m")
	""" Lower bound of the detector wavelength range"""

	wavelength_upper  :float =  sp_property(type="static",units="m")
	""" Upper bound of the detector wavelength range"""

	counts_to_radiance  :array_type =  sp_property(type="static",coordinate1="1...N",coordinate1_same_as="../frame/image_raw",coordinate2="1...N",coordinate2_same_as="../frame/image_raw",units="photons.m^-2.s^-1.sr^-1.counts^-1")
	""" Counts to radiance factor, for each pixel of the detector. Includes both the
		transmission losses in the relay optics and the quantum efficiency of the camera
		itself, integrated over the wavelength range"""

	exposure_time  :float =  sp_property(type="static",units="s")
	""" Exposure time"""

	noise  :float =  sp_property(type="static",units="-")
	""" Detector noise (e.g. read-out noise) (rms counts per second exposure time)"""

	columns_n  :int =  sp_property(type="static",introduced_after_version="3.37.2")
	""" Number of pixel columns in the horizontal direction"""

	lines_n  :int =  sp_property(type="static",introduced_after_version="3.37.2")
	""" Number of pixel lines in the vertical direction"""

	frame  :TimeSeriesAoS[_T_camera_visible_frame] =  sp_property(coordinate1="time",type="dynamic")
	""" Set of frames"""

	geometry_matrix  :_T_camera_visible_geometry_matrix =  sp_property()
	""" Description of geometry matrix (ray transfer matrix)"""


class _T_camera_visible_channel(SpTree):
	"""Channel of a camera"""

	name  :str =  sp_property(type="static")
	""" Name of the channel"""

	aperture  :AoS[DetectorAperture] =  sp_property(coordinate1="1...N")
	""" Description of apertures between plasma and the detectors (position, outline
		shape and orientation)"""

	viewing_angle_alpha_bounds  :array_type =  sp_property(type="static",units="rad",coordinate1="1...2")
	""" Minimum and maximum values of alpha angle of the field of view, where alpha is
		the agle between the axis X3 and projection of the chord of view on the plane
		X1X3 counted clockwise from the top view of X2 axis. X1, X2, X3 are the ones of
		the first aperture (i.e. the closest to the plasma)."""

	viewing_angle_beta_bounds  :array_type =  sp_property(type="static",units="rad",coordinate1="1...2")
	""" Minimum and maximum values of beta angle of the field of view, where beta is the
		angle between the axis X3 and projection of the chord of view on the plane X2X3
		counted clockwise from the top view of X1 axis. X1, X2, X3 are the ones of the
		first aperture (i.e. the closest to the plasma)."""

	detector  :AoS[_T_camera_visible_detector] =  sp_property(coordinate1="1...N")
	""" Set of detectors"""


class _T_camera_visible(IDS):
	"""Camera in the visible light range
	lifecycle_status: alpha
	lifecycle_version: 3.27.0
	lifecycle_last_change: 3.38.0"""

	dd_version="v3_38_1_dirty"
	ids_name="camera_visible"

	name  :str =  sp_property(type="static")
	""" Name of the camera"""

	channel  :AoS[_T_camera_visible_channel] =  sp_property(coordinate1="1...N")
	""" Set of channels (a front aperture, possibly followed by others, viewing the
		plasma recorded by one or more detectors e.g. for different wavelength ranges)"""

	latency  :float =  sp_property(type="static",units="s",introduced_after_version="3.32.1")
	""" Upper bound of the delay between physical information received by the detector
		and data available on the real-time (RT) network."""
