"""
  This module containes the _FyTok_ wrapper of IMAS/dd/spectrometer_x_ray_crystal
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_identifier_static,_T_rzphi0d_static,_T_xyz0d_static,_T_x1x21d_static,_T_line_of_sight_2points,_T_rzphi1d_static,_T_detector_aperture,_T_curved_object,_T_filter_window,_T_camera_geometry
from .utilities import _E_spectrometer_x_reflector_geometry
from .utilities import _E_spectrometer_x_reflector_geometry
from .utilities import _E_materials

class _E_spectro_x_instrument_function(IntFlag):
	"""Translation table for instrument function for X ray crystal spectrometer	xpath: 	"""
  
	explicit = 1
	"""Explicit values, use the values node"""
  
	gaussian = 2
	"""Gaussian : use parameters intensity, centre, and sigma"""
  
	lorentzian = 3
	"""Lorentzian : use parameters intensity, centre, and scale"""
  
	voigt = 4
	"""Voigt : use parameters intensity, centre, sigma, and scale"""
  

class _E_spectrometer_x_reflector_geometry(IntFlag):
	"""Crystal mesh type	xpath: 	"""
  
	hexagonal = 1
	"""Hexagonal mesh"""
  
	cubic = 2
	"""Cubic mesh"""
  

class _T_spectrometer_x_ray_crystal_flt_2d_time_1(SpTree):
	"""Similar to a signal (FLT_2D) but with time base one level above"""

	data  :array_type =  sp_property(type="dynamic",units="as_parent",coordinate1="1...N",coordinate2="../../time",utilities_aoscontext="yes")
	""" Data"""

	validity_timed  :array_type =  sp_property(type="dynamic",coordinate1="../../time",utilities_aoscontext="yes")
	""" Indicator of the validity of the data for each time slice. 0: valid from
		automated processing, 1: valid and certified by the diagnostic RO; - 1 means
		problem identified in the data processing (request verification by the
		diagnostic RO), -2: invalid data, should not be used (values lower than -2 have
		a code-specific meaning detailing the origin of their invalidity)"""

	validity  :int =  sp_property(type="constant")
	""" Indicator of the validity of the data for the whole acquisition period. 0: valid
		from automated processing, 1: valid and certified by the diagnostic RO; - 1
		means problem identified in the data processing (request verification by the
		diagnostic RO), -2: invalid data, should not be used (values lower than -2 have
		a code-specific meaning detailing the origin of their invalidity)"""


class _T_spectrometer_x_ray_crystal_instrument_function(SpTree):
	"""Instrument function"""

	wavelengths  :array_type =  sp_property(type="static",units="m",coordinate1="1...N")
	""" Array of wavelengths on which the instrument function is defined"""

	values  :array_type =  sp_property(units="sr.m",type="static",coordinate1="1...N",coordinate1_same_as="../../wavelength_frames",coordinate2="../../z_frames",coordinate3="../wavelengths")
	""" Explicit instrument function values for the detector. When multiplied by the
		line-integrated emission spectrum in photons/second/sr/m/m^2 received on a pixel
		of the detector, gives the detector pixel output in counts/seconds."""

	type  :_E_spectro_x_instrument_function =  sp_property(doc_identifier="spectrometer_x_ray_crystal/spectro_x_instrument_function_identifier.xml")
	""" Instrument function type"""

	intensity  :array_type =  sp_property(type="static",units="m",coordinate1="../../z_frames",coordinate2="../wavelengths")
	""" Scaling factor for the instrument function such that convolving the instrument
		function with an emission spectrum gives the counts per second on the detector"""

	centre  :array_type =  sp_property(type="static",units="m",coordinate1="../../z_frames",coordinate2="../wavelengths")
	""" Centre (in terms of absolute wavelength) of instrument function"""

	sigma  :array_type =  sp_property(type="static",units="m",coordinate1="../../z_frames",coordinate2="../wavelengths")
	""" Standard deviation of Gaussian instrument function"""

	scale  :array_type =  sp_property(type="static",units="m",coordinate1="../../z_frames",coordinate2="../wavelengths")
	""" Scale of Lorentzian instrument function (full width at half height)"""


class _T_spectrometer_x_ray_crystal_crystal(SpTree):
	"""Characteristics of the crystal used, extension of the generic description of a
		small plane or curved object (crystal, reflector, ...)"""

	identifier  :str =  sp_property(type="static")
	""" ID of the object"""

	geometry_type  :_E_spectrometer_x_reflector_geometry =  sp_property(doc_identifier="utilities/curved_object_geometry_identifier.xml")
	""" Geometry of the object contour. Note that there is some flexibility in the
		choice of the local coordinate system (X1,X2,X3). The data provider should
		choose the most convenient coordinate system for the object, respecting the
		definitions of (X1,X2,X3) indicated below."""

	curvature_type  :_E_spectrometer_x_reflector_geometry =  sp_property(doc_identifier="utilities/curved_object_curvature_identifier.xml")
	""" Curvature of the object."""

	material  :_E_materials =  sp_property(doc_identifier="utilities/materials_identifier.xml")
	""" Material of the object"""

	centre  :_T_rzphi0d_static =  sp_property()
	""" Coordinates of the origin of the local coordinate system (X1,X2,X3) describing
		the object. This origin is located within the object area and should be the
		middle point of the object surface. If geometry_type=2, it's the centre of the
		circular object. If geometry_type=3, it's the centre of the rectangular object."""

	radius  :float =  sp_property(type="static",units="m")
	""" Radius of the circle, used only if geometry_type/index = 2"""

	x1_unit_vector  :_T_xyz0d_static =  sp_property(url="utilities/detector_aperture_coordinates.svg")
	""" Components of the X1 direction unit vector in the (X,Y,Z) coordinate system,
		where X is the major radius axis for phi = 0, Y is the major radius axis for phi
		= pi/2, and Z is the height axis. The X1 vector is more horizontal than X2 (has
		a smaller abs(Z) component) and oriented in the positive phi direction
		(counter-clockwise when viewing from above)."""

	x2_unit_vector  :_T_xyz0d_static =  sp_property(url="utilities/detector_aperture_coordinates.svg")
	""" Components of the X2 direction unit vector in the (X,Y,Z) coordinate system,
		where X is the major radius axis for phi = 0, Y is the major radius axis for phi
		= pi/2, and Z is the height axis. The X2 axis is orthonormal so that uX2 = uX3 x
		uX1."""

	x3_unit_vector  :_T_xyz0d_static =  sp_property(url="utilities/detector_aperture_coordinates.svg")
	""" Components of the X3 direction unit vector in the (X,Y,Z) coordinate system,
		where X is the major radius axis for phi = 0, Y is the major radius axis for phi
		= pi/2, and Z is the height axis. The X3 axis is normal to the object surface
		and oriented towards the plasma."""

	x1_width  :float =  sp_property(type="static",units="m")
	""" Full width of the object in the X1 direction, used only if geometry_type/index =
		3"""

	x2_width  :float =  sp_property(type="static",units="m")
	""" Full width of the object in the X2 direction, used only if geometry_type/index =
		3"""

	outline  :_T_x1x21d_static =  sp_property()
	""" Irregular outline of the object in the (X1, X2) coordinate system, used only if
		geometry_type/index=1. Do NOT repeat the first point."""

	x1_curvature  :float =  sp_property(type="static",units="m")
	""" Radius of curvature in the X1 direction, to be filled only for
		curvature_type/index = 2, 4 or 5"""

	x2_curvature  :float =  sp_property(type="static",units="m")
	""" Radius of curvature in the X2 direction, to be filled only for
		curvature_type/index = 3 or 5"""

	surface  :float =  sp_property(type="static",units="m^2")
	""" Surface of the object, derived from the above geometric data"""

	wavelength_bragg  :float =  sp_property(type="static",units="m")
	""" Bragg wavelength of the crystal"""

	angle_bragg  :float =  sp_property(type="static",units="rad")
	""" Bragg angle of the crystal"""

	thickness  :float =  sp_property(type="static",units="m",introduced_after_version="3.34.0")
	""" Thickness of the crystal"""

	cut  :List[int] =  sp_property(type="static",coordinate1="1...N",introduced_after_version="3.34.0")
	""" Miller indices characterizing the cut of the crystal (can be of length 3 or 4)"""

	mesh_type  :_E_spectrometer_x_reflector_geometry =  sp_property(doc_identifier="spectrometer_x_ray_crystal/crystal_mesh_identifier.xml",introduced_after_version="3.34.0")
	""" Crystal mesh type"""


class _T_spectrometer_x_ray_crystal_bin(SpTree):
	"""Binning scheme (binning done in the vertical direction)"""

	z_pixel_range  :array_type =  sp_property(type="static",coordinate1="1..2")
	""" Vertical pixel index range indicating the corresponding binned detector area"""

	wavelength  :array_type =  sp_property(type="static",coordinate1="1...N",coordinate1_same_as="../../wavelength_frames",units="m")
	""" Wavelength of incoming photons on each horizontal pixel of this bin."""

	line_of_sight  :_T_line_of_sight_2points =  sp_property()
	""" Description of the line of sight from the crystal to the plasma for this bin,
		defined by two points"""


class _T_spectrometer_x_ray_crystal_frame(TimeSlice):
	"""Frame of a camera"""

	counts_n  :array_type =  sp_property(units="-",type="dynamic",coordinate1="1...N",coordinate1_same_as="../../wavelength_frames",coordinate2="../../z_frames",introduced_after_version="3.34.0")
	""" Number of counts detected on each pixel of the frame during one exposure time"""

	counts_bin_n  :array_type =  sp_property(units="-",type="dynamic",coordinate1="1...N",coordinate1_same_as="../../wavelength_frames",coordinate2="../../bin",introduced_after_version="3.35.0")
	""" Number of counts detected on each pixel/bin of the binned frame during one
		exposure time"""


class _T_spectrometer_x_ray_crystal_proxy(SpTree):
	"""X-ray crystal spectrometer profile proxy"""

	lines_of_sight_second_point  :_T_rzphi1d_static =  sp_property()
	""" For each profile point, a line of sight is defined by a first point given by the
		centre of the crystal and a second point described here."""

	lines_of_sight_rho_tor_norm  :_T_spectrometer_x_ray_crystal_flt_2d_time_1 =  sp_property(units="-",coordinate1="../lines_of_sight_second_point/r")
	""" Shortest distance in rho_tor_norm between lines of sight and magnetic axis,
		signed with following convention : positive (resp. negative) means the point of
		shortest distance is above (resp. below) the magnetic axis"""

	t_i  :_T_spectrometer_x_ray_crystal_flt_2d_time_1 =  sp_property(units="eV",coordinate1="../lines_of_sight_second_point/r")
	""" Ion temperature (estimated from a spectral fit directly on the output
		line-integrated signal, without tomographic inversion)"""

	t_e  :_T_spectrometer_x_ray_crystal_flt_2d_time_1 =  sp_property(units="eV",coordinate1="../lines_of_sight_second_point/r")
	""" Electron temperature (estimated from a spectral fit directly on the output
		line-integrated signal, without tomographic inversion)"""

	velocity_tor  :_T_spectrometer_x_ray_crystal_flt_2d_time_1 =  sp_property(units="m.s^-1",coordinate1="../lines_of_sight_second_point/r")
	""" Toroidal velocity (estimated from a spectral fit directly on the output
		line-integrated signal, without tomographic inversion)"""

	time  :array_type =  sp_property(coordinate1="1...N",type="dynamic",units="s")
	""" Timebase for the dynamic nodes of this probe located at this level of the IDS
		structure"""


class _T_spectrometer_x_ray_crystal_channel(SpTree):
	"""X-crystal spectrometer channel"""

	exposure_time  :float =  sp_property(type="static",units="s")
	""" Exposure time of the measurement"""

	energy_bound_lower  :array_type =  sp_property(type="static",units="eV",coordinate1="1...N",coordinate1_same_as="../wavelength_frames",coordinate2="../z_frames")
	""" Lower energy bound for the photon detection, for each pixel (horizontal,
		vertical)"""

	energy_bound_upper  :array_type =  sp_property(type="static",units="eV",coordinate1="1...N",coordinate1_same_as="../wavelength_frames",coordinate2="../z_frames")
	""" Upper energy bound for the photon detection, for each pixel (horizontal,
		vertical)"""

	aperture  :DetectorAperture =  sp_property()
	""" Collimating aperture"""

	reflector  :AoS[_T_curved_object] =  sp_property(coordinate1="1...N")
	""" Set of reflectors (optional) reflecting the light coming from the plasma towards
		the crystal. If empty, means that the plasma light directly arrives on the
		crystal."""

	crystal  :_T_spectrometer_x_ray_crystal_crystal =  sp_property()
	""" Characteristics of the crystal used"""

	filter_window  :AoS[_T_filter_window] =  sp_property(coordinate1="1...N")
	""" Set of filter windows"""

	camera  :_T_camera_geometry =  sp_property()
	""" Characteristics of the camera used"""

	z_frames  :array_type =  sp_property(type="static",coordinate1="1...N",units="m")
	""" Height of the observed zone at the focal plane in the plasma, corresponding to
		the vertical dimension of the frame"""

	wavelength_frames  :array_type =  sp_property(type="static",coordinate1="1...N",coordinate2="../z_frames",units="m")
	""" Wavelength of incoming photons on each pixel of the frames, mainly varying
		accross the horizontal dimension of the frame. However a 2D map of the
		wavelength is given since it is not constant vertically due to the elliptical
		curvature of the photon iso-surfaces"""

	bin  :AoS[_T_spectrometer_x_ray_crystal_bin] =  sp_property(coordinate1="1...N",introduced_after_version="3.35.0")
	""" Set of bins (binning in the vertical dimension) defined to increase the signal
		to noise ratio of the spectra"""

	frame  :TimeSeriesAoS[_T_spectrometer_x_ray_crystal_frame] =  sp_property(coordinate1="time",type="dynamic")
	""" Set of frames"""

	energies  :array_type =  sp_property(type="static",units="eV",coordinate1="1...N",introduced_after_version="3.34.0")
	""" Array of energy values for tabulation of the detection efficiency"""

	detection_efficiency  :array_type =  sp_property(type="static",units="-",coordinate1="../energies",introduced_after_version="3.34.0")
	""" Probability of detection of a photon impacting the detector as a function of its
		energy"""

	profiles_line_integrated  :_T_spectrometer_x_ray_crystal_proxy =  sp_property(introduced_after_version="3.34.0")
	""" Profiles proxies are given in the vertical direction of the detector. They are
		estimated directly from the camera, without tomographic inversion. Binning is
		allowed so the number of profile points may be lower than the length of
		z_frames. Physical quantities deduced from the measured spectra are given for
		each profile point. They correspond to the spectra integrated along lines of
		sight, defined by a first point given by the centre of the crystal and a second
		point (depending on the profile point) described below."""

	instrument_function  :_T_spectrometer_x_ray_crystal_instrument_function =  sp_property(introduced_after_version="3.34.0")
	""" Instrument function, i.e. response of the detector to a monochromatic emission
		passing through the spectrometer. The resulting image on the detector will be a
		2-D distribution of pixel values, for each wavelength. It can be given as
		explicit values for each detector pixel (values node) or as a parametric
		function of wavelength (described by the other nodes)"""


class _T_spectrometer_x_ray_crystal(IDS):
	"""X-crystal spectrometer diagnostic
	lifecycle_status: alpha
	lifecycle_version: 3.26.0
	lifecycle_last_change: 3.36.0"""

	dd_version="v3_38_1_dirty"
	ids_name="spectrometer_x_ray_crystal"

	channel  :AoS[_T_spectrometer_x_ray_crystal_channel] =  sp_property(coordinate1="1...N",introduced_after_version="3.33.0")
	""" Measurement channel, composed of a camera, a crystal, and (optional) a set of
		reflectors. The light coming from the plasma passes through the (optional) set
		of reflectors, then the crystal and arrives at the camera"""

	latency  :float =  sp_property(type="static",units="s",introduced_after_version="3.32.1")
	""" Upper bound of the delay between physical information received by the detector
		and data available on the real-time (RT) network."""
