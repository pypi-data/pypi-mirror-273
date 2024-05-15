"""
  This module containes the _FyTok_ wrapper of IMAS/dd/spectrometer_visible
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_geometry_matrix_emission,_T_signal_flt_1d,_T_rzphi1d_static,_T_plasma_composition_neutral_element_constant,_T_identifier,_T_rzphi0d_dynamic_aos3,_T_signal_flt_2d,_T_identifier_static,_T_detector_aperture,_T_line_of_sight_2points,_T_signal_int_1d

class _E_spectrometer_visible_method(IntFlag):
	"""Fitting method used to calculate isotope ratios	xpath: 	"""
  
	multi_gaussian = 1
	"""Multi-gaussian fitting"""
  
	exp_times_multi_gaussian = 2
	"""Experimental signal multiplied by multi-gaussian ratio"""
  

class _T_spectro_vis_geometry_matrix_interpolated(SpTree):
	"""Interpolated geometry matrix"""

	r  :array_type =  sp_property(type="constant",units="m",coordinate1="1...N")
	""" Major radius of interpolation knots"""

	z  :array_type =  sp_property(type="constant",units="m",coordinate1="../r")
	""" Height of interpolation knots"""

	phi  :array_type =  sp_property(type="constant",units="rad",coordinate1="../r")
	""" Toroidal angle (oriented counter-clockwise when viewing from above) of
		interpolation knots"""

	data  :array_type =  sp_property(type="constant",coordinate1="../r",units="m^-2")
	""" Interpolated Ray Transfer Matrix (RTM, or geometry matrix), which provides
		transformation of the reflected light from each interpolation knot to the
		receiver (detector or head of an optic fibre). When convolving with an emission
		profile, the values must be interpolated to the emission grid and multiplied by
		the volume of the grid cells. The interpolated matrix is given on an array of
		interpolation knots of coordinates r, z and phi"""


class _T_spectro_vis_geometry_matrix_step2(SpTree):
	"""Geometry matrix of the detector"""

	data  :array_type =  sp_property(type="static",coordinate1="1...N",units="m")
	""" The Ray Transfer Matrix (RTM, or geometry matrix) here provides transformation
		of the signal from each individual unit light source (voxel) to the receiver
		(detector or head of an optic fibre). The emission profile has
		[photons.m^-3.s^-1.sr^-1] units and radiance signal has
		[photons.m^-2.s^-1.sr^-1] units. So the RTM has [m] units. This data is stored
		in a sparse form, i.e. the array contains only the non-zero element of the Ray
		transfer matrix. The voxel index corresponding to an element of this array can
		be found in voxel_indices"""

	voxel_indices  :array_type =  sp_property(type="static",coordinate1="../data")
	""" List of voxel indices (defined in the voxel map) used in the sparse data array"""


class _T_spectro_vis_channel_wavelength_calibration(SpTree):
	"""Wavelength calibration"""

	offset  :float =  sp_property(type="static",units="m")
	""" Offset"""

	gain  :float =  sp_property(type="static",units="m")
	""" Gain"""


class _T_detector_image_circular(SpTree):
	"""Description of circular or elliptic observation cones"""

	radius  :float =  sp_property(type="static",units="m")
	""" Radius of the circle"""

	ellipticity  :float =  sp_property(type="static",units="-")
	""" Ellipticity"""


class _T_spectro_vis_geometry_matrix(SpTree):
	"""Geometry matrix of the detector"""

	with_reflections  :_T_spectro_vis_geometry_matrix_step2 =  sp_property(introduced_after_version="3.37.2")
	""" Geometry matrix with reflections"""

	without_reflections  :_T_spectro_vis_geometry_matrix_step2 =  sp_property(introduced_after_version="3.37.2")
	""" Geometry matrix without reflections"""

	interpolated  :_T_spectro_vis_geometry_matrix_interpolated =  sp_property(introduced_after_version="3.37.2")
	""" Interpolated geometry matrix for reflected light"""

	voxel_map  :array_type =  sp_property(type="static",coordinate1="../emission_grid/dim1",coordinate2="../emission_grid/dim2",coordinate3="../emission_grid/dim3")
	""" Voxel map for geometry matrix. The cells with same number are merged in the
		computation into a single emission source meta-cell (the voxel). Cells with
		number -1 are excluded. Voxel count starts from 0."""

	voxels_n  :int =  sp_property(type="static",introduced_after_version="3.37.2")
	""" Number of voxels defined in the voxel_map."""

	emission_grid  :_T_geometry_matrix_emission =  sp_property()
	""" Grid defining the light emission cells"""


class _T_spectro_vis_channel_processed_line(SpTree):
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


class _T_spectro_vis_channel_light_collection(SpTree):
	"""Emission weights for various points"""

	values  :array_type =  sp_property(type="static",units="-",coordinate1="../positions/r")
	""" Values of the light collection efficiencies"""

	positions  :_T_rzphi1d_static =  sp_property()
	""" List of positions for which the light collection efficiencies are provided"""


class _T_detector_image(SpTree):
	"""Description of the observation volume of the detector or detector pixel at the
		focal plane of the optical system. This is basically the image of the detector
		pixel on the focal plane"""

	geometry_type  :int =  sp_property(Type="static")
	""" Type of geometry used to describe the image (1:'outline', 2:'circular')"""

	outline  :_T_rzphi1d_static =  sp_property()
	""" Coordinates of the points shaping the polygon of the image"""

	circular  :_T_detector_image_circular =  sp_property()
	""" Description of circular or elliptic image"""


class _T_spectro_vis_channel_isotopes_isotope(SpTree):
	"""Isotope ratio"""

	element  :AoS[_T_plasma_composition_neutral_element_constant] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom or molecule"""

	label  :str =  sp_property(type="constant")
	""" String identifying the species (H, D, T, He3, He4)"""

	density_ratio  :Expression  =  sp_property(type="dynamic",units="-",coordinate1="../time")
	""" Ratio of the density of neutrals of this isotope over the summed neutral
		densities of all other isotopes described in the ../isotope array"""

	cold_neutrals_fraction  :Expression  =  sp_property(type="dynamic",units="-",coordinate1="../time")
	""" Fraction of cold neutrals for this isotope
		(n_cold_neutrals/(n_cold_neutrals+n_hot_neutrals))"""

	hot_neutrals_fraction  :Expression  =  sp_property(type="dynamic",units="-",coordinate1="../time")
	""" Fraction of hot neutrals for this isotope
		(n_hot_neutrals/(n_cold_neutrals+n_hot_neutrals))"""

	cold_neutrals_temperature  :Expression  =  sp_property(type="dynamic",units="eV",coordinate1="../time")
	""" Temperature of cold neutrals for this isotope"""

	hot_neutrals_temperature  :Expression  =  sp_property(type="dynamic",units="eV",coordinate1="../time")
	""" Temperature of hot neutrals for this isotope"""

	time  :array_type =  sp_property(type="dynamic",units="s",coordinate1="1...N")
	""" Timebase for dynamic quantities at this level of the data structure"""


class _T_spectro_vis_channel_polarization(SpTree):
	"""Physics quantities measured from polarized light spectroscopy"""

	e_field_lh_r  :Expression  =  sp_property(units="V.m^-1",type="dynamic",coordinate1="../time")
	""" Lower Hybrid electric field component in the major radius direction"""

	e_field_lh_z  :Expression  =  sp_property(units="V.m^-1",type="dynamic",coordinate1="../time")
	""" Lower Hybrid electric field component in the vertical direction"""

	e_field_lh_tor  :Expression  =  sp_property(units="V.m^-1",type="dynamic",coordinate1="../time")
	""" Lower Hybrid electric field component in the toroidal direction"""

	b_field_modulus  :Expression  =  sp_property(units="T",type="dynamic",coordinate1="../time")
	""" Modulus of the magnetic field (always positive, irrespective of the sign
		convention for the B-field direction), obtained from Zeeman effect fit"""

	n_e  :Expression  =  sp_property(units="m^-3",type="dynamic",coordinate1="../time")
	""" Electron density, obtained from Stark broadening fit"""

	temperature_cold_neutrals  :Expression  =  sp_property(units="eV",type="dynamic",coordinate1="../time")
	""" Fit of cold neutrals temperature"""

	temperature_hot_neutrals  :Expression  =  sp_property(units="eV",type="dynamic",coordinate1="../time")
	""" Fit of hot neutrals temperature"""

	velocity_cold_neutrals  :Expression  =  sp_property(units="m.s^-1",type="dynamic",coordinate1="../time")
	""" Projection of the cold neutral velocity along the line of sight, positive when
		going from first point to second point of the line of sight"""

	velocity_hot_neutrals  :Expression  =  sp_property(units="m.s^-1",type="dynamic",coordinate1="../time")
	""" Projection of the hot neutral velocity along the line of sight, positive when
		going from first point to second point of the line of sight"""

	time  :array_type =  sp_property(type="dynamic",units="s",coordinate1="1...N")
	""" Timebase for dynamic quantities at this level of the data structure"""


class _T_spectro_vis_channel_resolution(TimeSlice):
	"""In case of active spectroscopy, spatial resolution of the measurement"""

	centre  :_T_rzphi0d_dynamic_aos3 =  sp_property()
	""" Position of the centre of the spatially resolved zone"""

	width  :_T_rzphi0d_dynamic_aos3 =  sp_property()
	""" Full width of the spatially resolved zone in the R, Z and phi directions"""


class _T_spectro_vis_channel_filter(SpTree):
	"""Filter spectrometer"""

	processed_lines  :array_type =  sp_property(type="constant",units="m",coordinate1="1...N")
	""" Central wavelength of the processed lines"""

	line_labels  :List[str] =  sp_property(type="constant",coordinate1="../processed_lines")
	""" String identifying the processed line. To avoid ambiguities, the following
		syntax is used : element with ionization state_wavelength in Angstrom (e.g.
		WI_4000)"""

	line_radiances  :SignalND =  sp_property(units="m^-2.s^-1.sr^-1",coordinate1="../processed_lines (coordinate1 of the 'data' child)")
	""" Calibrated, background subtracted line integrals"""

	line_radiances_adjusted  :SignalND =  sp_property(units="m^-2.s^-1.sr^-1",coordinate1="../processed_lines (coordinate1 of the 'data' child)")
	""" Calibrated, background subtracted line integrals, adjusted as if the line was
		centred at the peak responsivity of the system (for this line)"""

	line_power_radiances  :SignalND =  sp_property(units="W.m^-2.sr^-1",coordinate1="../processed_lines (coordinate1 of the 'data' child)")
	""" Calibrated, background subtracted power radiances"""

	raw_lines  :array_type =  sp_property(type="constant",units="m",coordinate1="1...N")
	""" Central wavelength of the raw lines"""

	output_voltage  :SignalND =  sp_property(units="V",coordinate1="../raw_lines (coordinate1 of the 'data' child)")
	""" Raw voltage output of the whole acquisition chain for each raw line"""

	photoelectric_voltage  :SignalND =  sp_property(units="V",coordinate1="../raw_lines (coordinate1 of the 'data' child)")
	""" Gain corrected and background subtracted voltage for each raw line"""

	photon_count  :SignalND =  sp_property(units="s^-1",coordinate1="../raw_lines (coordinate1 of the 'data' child)")
	""" Detected photon count for each raw line"""

	line_intensities  :SignalND =  sp_property(units="m^-2.s^-1.sr^-1",coordinate1="../raw_lines (coordinate1 of the 'data' child)")
	""" Line gross integral intensities"""

	calibrated_lines  :array_type =  sp_property(type="constant",units="m",coordinate1="1...N")
	""" Central wavelength of the calibrated lines"""

	calibrated_line_integrals  :SignalND =  sp_property(units="m^-2.s^-1.sr^-1",coordinate1="../calibrated_lines (coordinate1 of the 'data' child)")
	""" Calibrated line gross areas integrals"""

	exposure_time  :float =  sp_property(type="constant",units="s")
	""" Exposure time"""

	radiance_calibration  :float =  sp_property(type="static",units="m^-2.sr^-1")
	""" Radiance calibration"""

	radiance_calibration_date  :str =  sp_property(type="static")
	""" Date of the radiance calibration (yyyy_mm_dd)"""


class _T_spectro_vis_channel_isotopes(SpTree):
	"""Isotope ratios and related information"""

	validity_timed  :array_type =  sp_property(type="dynamic",coordinate1="../time")
	""" Indicator of the validity of the isotope ratios as a function of time (0 means
		valid, negative values mean non-valid)"""

	validity  :int =  sp_property(type="static")
	""" Indicator of the validity of the isotope ratios for the whole acquisition period
		(0 means valid, negative values mean non-valid)"""

	signal_to_noise  :Expression  =  sp_property(type="dynamic",units="dB",coordinate1="../time")
	""" Log10 of the ratio of the powers in two bands, one with the spectral lines of
		interest (signal) the other without spectral lines (noise)."""

	method  :_E_spectrometer_visible_method =  sp_property(doc_identifier="spectrometer_visible/spectrometer_visible_method_identifier.xml")
	""" Fitting method used to calculate isotope ratios"""

	isotope  :AoS[_T_spectro_vis_channel_isotopes_isotope] =  sp_property(coordinate1="1...N")
	""" Set of isotopes"""

	time  :array_type =  sp_property(type="dynamic",units="s",coordinate1="1...N")
	""" Timebase for dynamic quantities at this level of the data structure"""


class _T_spectro_vis_channel_grating(SpTree):
	"""Grating spectrometer"""

	grating  :float =  sp_property(type="static",units="m^-1")
	""" Number of grating lines per unit length"""

	slit_width  :float =  sp_property(type="static",units="m")
	""" Width of the slit (placed in the object focal plane)"""

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

	processed_line  :AoS[_T_spectro_vis_channel_processed_line] =  sp_property(coordinate1="1...N")
	""" Set of processed spectral lines"""

	radiance_calibration  :array_type =  sp_property(type="static",units="m^-3.sr^-1",coordinate1="../wavelengths")
	""" Radiance calibration"""

	radiance_calibration_date  :str =  sp_property(type="static")
	""" Date of the radiance calibration (yyyy_mm_dd)"""

	wavelength_calibration  :_T_spectro_vis_channel_wavelength_calibration =  sp_property()
	""" Wavelength calibration data. The wavelength is obtained from the pixel index k
		by: wavelength = k * gain + offset. k is starting from 1."""

	wavelength_calibration_date  :str =  sp_property(type="static")
	""" Date of the wavelength calibration (yyyy_mm_dd)"""

	instrument_function  :array_type =  sp_property(type="static",units="m",coordinate1="1...2",coordinate2="1...N",introduced_after_version="3.36.0")
	""" Array of Gaussian widths and amplitudes which as a sum make up the instrument
		function. The instrument function is the shape that would be measured by a
		grating spectrometer if perfectly monochromatic line emission would be used as
		input. F(lambda) = 1 / sqrt (2*pi) * sum( instrument_function(1,i) /
		instrument_function(2,i) ) * exp( -lambda^2 / (2 * instrument_function(2,i)^2) )
		), whereby sum( instrument_function(1,i) ) = 1"""


class _T_spectro_vis_channel(SpTree):
	"""Visible spectroscopy channel"""

	name  :str =  sp_property(type="static")
	""" Name of the channel"""

	object_observed  :str =  sp_property(type="static")
	""" Main object observed by the channel"""

	type  :_T_identifier_static =  sp_property()
	""" Type of spectrometer the channel is connected to (index=1: grating, 2: filter)"""

	detector  :DetectorAperture =  sp_property()
	""" Detector description"""

	aperture  :AoS[DetectorAperture] =  sp_property(coordinate1="1...N")
	""" Description of a set of collimating apertures"""

	etendue  :float =  sp_property(type="static",units="m^2.str")
	""" Etendue (geometric extent) of the channel's optical system"""

	etendue_method  :_T_identifier_static =  sp_property()
	""" Method used to calculate the etendue. Index = 0 : exact calculation with a 4D
		integral; 1 : approximation with first order formula (detector surface times
		solid angle subtended by the apertures); 2 : other methods"""

	line_of_sight  :_T_line_of_sight_2points =  sp_property()
	""" Description of the line of sight of the channel, given by 2 points"""

	detector_image  :_T_detector_image =  sp_property()
	""" Image of the detector or pixel on the focal plane of the optical system"""

	fibre_image  :_T_detector_image =  sp_property()
	""" Image of the optical fibre on the focal plane of the optical system"""

	light_collection_efficiencies  :_T_spectro_vis_channel_light_collection =  sp_property()
	""" Light collection efficiencies (fraction of the local emission detected by the
		optical system) for a list of points defining regions of interest. To be used
		for non-pinhole optics."""

	active_spatial_resolution  :TimeSeriesAoS[_T_spectro_vis_channel_resolution] =  sp_property(coordinate1="time",type="dynamic")
	""" In case of active spectroscopy, describes the spatial resolution of the
		measurement, calculated as a convolution of the atomic smearing, magnetic and
		beam geometry smearing and detector projection, for a set of time slices"""

	polarizer  :DetectorAperture =  sp_property()
	""" Polarizer description"""

	polarizer_active  :int =  sp_property(type="static")
	""" Indicator of whether a polarizer is present and active in the optical system
		(set to 1 in this case, set to 0 or leave empty ottherwise)"""

	grating_spectrometer  :_T_spectro_vis_channel_grating =  sp_property()
	""" Quantities measured by the channel if connected to a grating spectrometer"""

	filter_spectrometer  :_T_spectro_vis_channel_filter =  sp_property()
	""" Quantities measured by the channel if connected to a filter spectrometer"""

	validity_timed  :Signal =  sp_property()
	""" Indicator of the validity of the channel as a function of time (0 means valid,
		negative values mean non-valid)"""

	validity  :int =  sp_property(type="static")
	""" Indicator of the validity of the channel for the whole acquisition period (0
		means valid, negative values mean non-valid)"""

	isotope_ratios  :_T_spectro_vis_channel_isotopes =  sp_property()
	""" Isotope ratios and related information"""

	polarization_spectroscopy  :_T_spectro_vis_channel_polarization =  sp_property()
	""" Physics quantities measured from polarized light spectroscopy"""

	geometry_matrix  :_T_spectro_vis_geometry_matrix =  sp_property()
	""" Description of geometry matrix (ray transfer matrix)"""


class _T_spectrometer_visible(IDS):
	"""Spectrometer in visible light range diagnostic
	lifecycle_status: alpha
	lifecycle_version: 3.3.1
	lifecycle_last_change: 3.38.0"""

	dd_version="v3_38_1_dirty"
	ids_name="spectrometer_visible"

	detector_layout  :str =  sp_property(type="static")
	""" Layout of the detector grid employed. Ex: '4x16', '4x32', '1x18'"""

	channel  :AoS[_T_spectro_vis_channel] =  sp_property(coordinate1="1...N")
	""" Set of channels (detector or pixel of a camera)"""

	latency  :float =  sp_property(type="static",units="s",introduced_after_version="3.32.1")
	""" Upper bound of the delay between physical information received by the detector
		and data available on the real-time (RT) network."""
