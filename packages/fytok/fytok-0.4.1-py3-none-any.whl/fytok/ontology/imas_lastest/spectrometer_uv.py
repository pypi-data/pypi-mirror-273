"""
  This module containes the _FyTok_ wrapper of IMAS/dd/spectrometer_uv
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_signal_flt_1d,_T_identifier_static,_T_rzphi0d_static,_T_xyz0d_static,_T_x1x21d_static,_T_detector_aperture,_T_line_of_sight_2points_dynamic_aos1,_T_signal_flt_2d,_T_signal_int_2d

class _T_spectro_uv_detector(SpTree):
	"""Characteristics of the detector"""

	pixel_dimensions  :array_type =  sp_property(type="static",coordinate1="1...2",units="m")
	""" Pixel dimension in each direction (horizontal, vertical)"""

	pixel_n  :array_type =  sp_property(type="static",coordinate1="1...2")
	""" Number of pixels in each direction (horizontal, vertical)"""

	detector_dimensions  :array_type =  sp_property(type="static",coordinate1="1...2",units="m")
	""" Total detector dimension in each direction (horizontal, vertical)"""


class _T_spectro_uv_channel_wavelength_calibration(SpTree):
	"""Wavelength calibration"""

	offset  :float =  sp_property(type="static",units="m")
	""" Offset"""

	gain  :float =  sp_property(type="static",units="m")
	""" Gain"""


class _T_spectro_uv_supply(SpTree):
	"""Power supply"""

	object  :str =  sp_property(type="static")
	""" Name of the object connected to the power supply"""

	voltage_set  :Signal =  sp_property(units="V")
	""" Voltage set at the power supply"""


class _T_spectro_uv_channel_processed_line(SpTree):
	"""Description of a processed line"""

	label  :str =  sp_property(type="constant")
	""" String identifying the processed line. To avoid ambiguities, the following
		syntax is used : element with ionization state_wavelength in Angstrom (e.g.
		WI_4000)"""

	wavelength_central  :float =  sp_property(type="constant",units="m")
	""" Central wavelength of the processed line"""

	radiance  :Signal =  sp_property(units="m^-2.s^-1.sr^-1")
	""" Calibrated, background subtracted radiance (integrated over the spectrum for
		this line)"""

	intensity  :Signal =  sp_property(units="s^-1")
	""" Non-calibrated intensity (integrated over the spectrum for this line)"""


class _T_spectro_uv_channel_grating_image(SpTree):
	"""Grating image_field"""

	geometry_type  :_T_identifier_static =  sp_property()
	""" Surface geometry. Index = 1 : spherical. Index = 2 : plane"""

	centre  :_T_rzphi0d_static =  sp_property()
	""" Centre of the image surface in case it is spherical, or position of a point on
		the surface in case it is a plane"""

	curvature_radius  :float =  sp_property(type="static",units="m")
	""" Curvature radius of the image surface"""

	x3_unit_vector  :_T_xyz0d_static =  sp_property()
	""" Components of the X3 direction unit vector in the (X,Y,Z) coordinate system,
		where X is the major radius axis for phi = 0, Y is the major radius axis for phi
		= pi/2, and Z is the height axis. The X3 axis is normal to the surface ( in case
		it is plane) and oriented towards the plasma."""


class _T_spectro_uv_channel_grating(SpTree):
	"""Grating description"""

	type  :_T_identifier_static =  sp_property()
	""" Grating type. Index = 1 : ruled. Index = 2 : holographic"""

	groove_density  :float =  sp_property(type="static",units="m^-1")
	""" Number of grooves per unit length"""

	geometry_type  :_T_identifier_static =  sp_property()
	""" Grating geometry. Index = 1 : spherical. Index = 2 : toric"""

	centre  :_T_rzphi0d_static =  sp_property()
	""" Centre of the grating sphere (if grating is spherical) or torus (if grating is
		toric)"""

	curvature_radius  :float =  sp_property(type="static",units="m")
	""" Curvature radius of the spherical grating"""

	summit  :_T_rzphi0d_static =  sp_property()
	""" Position of the grating summit (defined as the point of contact of its concave
		side if the grating were put on a table). Used as the origin of the x1, x2, x3
		vectors defined below"""

	x1_unit_vector  :_T_xyz0d_static =  sp_property()
	""" Components of the X1 direction unit vector in the (X,Y,Z) coordinate system,
		where X is the major radius axis for phi = 0, Y is the major radius axis for phi
		= pi/2, and Z is the height axis. The X1 vector is horizontal and oriented in
		the positive phi direction (counter-clockwise when viewing from above)."""

	x2_unit_vector  :_T_xyz0d_static =  sp_property()
	""" Components of the X2 direction unit vector in the (X,Y,Z) coordinate system,
		where X is the major radius axis for phi = 0, Y is the major radius axis for phi
		= pi/2, and Z is the height axis. The X2 axis is orthonormal so that uX2 = uX3 x
		uX1."""

	x3_unit_vector  :_T_xyz0d_static =  sp_property()
	""" Components of the X3 direction unit vector in the (X,Y,Z) coordinate system,
		where X is the major radius axis for phi = 0, Y is the major radius axis for phi
		= pi/2, and Z is the height axis. The X3 axis is normal to the grating at its
		summit and oriented towards the plasma."""

	outline  :_T_x1x21d_static =  sp_property()
	""" List of the 4 extreme points of the spherical grating in the (X1, X2) coordinate
		system, using the summit as the origin. Do NOT repeat the first point."""

	image_field  :_T_spectro_uv_channel_grating_image =  sp_property()
	""" Surface on which the grating image is focused"""


class _T_spectro_uv_channel(SpTree):
	"""Charge exchange channel"""

	name  :str =  sp_property(type="static")
	""" Name of the channel"""

	detector_layout  :_T_spectro_uv_detector =  sp_property()
	""" Dimensions of pixels and detector"""

	detector  :DetectorAperture =  sp_property()
	""" Description of the front face of the micro channel plate"""

	detector_position_parameter  :Signal =  sp_property(units="mixed")
	""" In case of detector moving during a pulse, position parameter allowing to record
		and compute the detector position as a function of time"""

	aperture  :AoS[DetectorAperture] =  sp_property(coordinate1="1...N")
	""" Description of a set of collimating apertures"""

	line_of_sight  :_T_line_of_sight_2points_dynamic_aos1 =  sp_property()
	""" Description of the line of sight of the channel, given by 2 points. The 2nd
		point is allowed to evolve in case of dynamic line of sight."""

	supply_high_voltage  :AoS[_T_spectro_uv_supply] =  sp_property(coordinate1="1...N")
	""" Set of high voltage power supplies applied to various parts of the diagnostic"""

	grating  :_T_spectro_uv_channel_grating =  sp_property()
	""" Description of the grating"""

	wavelengths  :array_type =  sp_property(type="constant",units="m",coordinate1="1...N")
	""" Measured wavelengths"""

	radiance_spectral  :SignalND =  sp_property(units="(photons).m^-2.s^-1.sr^-1.m^-1",coordinate1="../wavelengths",coordinate2="time")
	""" Calibrated spectral radiance (radiance per unit wavelength)"""

	intensity_spectrum  :SignalND =  sp_property(units="(counts) s^-1",coordinate1="../wavelengths",coordinate2="time")
	""" Intensity spectrum (not calibrated), i.e. number of photoelectrons detected by
		unit time by a wavelength pixel of the channel, taking into account electronic
		gain compensation and channels relative calibration"""

	exposure_time  :float =  sp_property(type="constant",units="s")
	""" Exposure time"""

	processed_line  :AoS[_T_spectro_uv_channel_processed_line] =  sp_property(coordinate1="1...N")
	""" Set of processed spectral lines"""

	radiance_calibration  :array_type =  sp_property(type="static",units="m^-3.sr^-1",coordinate1="../wavelengths")
	""" Radiance calibration"""

	radiance_calibration_date  :str =  sp_property(type="static")
	""" Date of the radiance calibration (yyyy_mm_dd)"""

	wavelength_calibration  :_T_spectro_uv_channel_wavelength_calibration =  sp_property()
	""" Wavelength calibration data. The wavelength is obtained from the pixel index k
		by: wavelength = k * gain + offset. k is starting from 1."""

	wavelength_calibration_date  :str =  sp_property(type="static")
	""" Date of the wavelength calibration (yyyy_mm_dd)"""

	validity_timed  :SignalND =  sp_property(coordinate1="../wavelengths")
	""" Indicator of the validity of the data for each wavelength and each time slice.
		0: valid from automated processing, 1: valid and certified by the diagnostic RO;
		- 1 means problem identified in the data processing (request verification by the
		diagnostic RO), -2: invalid data, should not be used (values lower than -2 have
		a code-specific meaning detailing the origin of their invalidity)"""

	validity  :int =  sp_property(type="static")
	""" Indicator of the validity of the data for the whole acquisition period. 0: valid
		from automated processing, 1: valid and certified by the diagnostic RO; - 1
		means problem identified in the data processing (request verification by the
		diagnostic RO), -2: invalid data, should not be used (values lower than -2 have
		a code-specific meaning detailing the origin of their invalidity)"""


class _T_spectrometer_uv(IDS):
	"""Spectrometer in uv light range diagnostic
	lifecycle_status: alpha
	lifecycle_version: 3.29.0
	lifecycle_last_change: 3.33.0"""

	dd_version="v3_38_1_dirty"
	ids_name="spectrometer_uv"

	etendue  :float =  sp_property(type="static",units="m^2.sr")
	""" Etendue (geometric extent) of the optical system"""

	etendue_method  :_T_identifier_static =  sp_property()
	""" Method used to calculate the etendue. Index = 0 : exact calculation with a 4D
		integral; 1 : approximation with first order formula (detector surface times
		solid angle subtended by the apertures); 2 : other methods"""

	channel  :AoS[_T_spectro_uv_channel] =  sp_property(coordinate1="1...N")
	""" Set of channels (detector or pixel of a camera)"""

	latency  :float =  sp_property(type="static",units="s",introduced_after_version="3.32.1")
	""" Upper bound of the delay between physical information received by the detector
		and data available on the real-time (RT) network."""
