"""
  This module containes the _FyTok_ wrapper of IMAS/dd/charge_exchange
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_signal_flt_1d,_T_signal_flt_2d,_T_identifier,_T_rzphi1d_dynamic_aos1,_T_detector_aperture,_T_identifier_static

class _T_charge_exchange_channel_processed_line(SpTree):
	"""Description of a processed spectral line"""

	label  :str =  sp_property(type="constant")
	""" String identifying the processed spectral line: Spectroscopy notation emitting
		element (e.g. D I, Be IV, W I, C VI), transition - if known - between round
		brackets (e.g. (3-2) ) and indication type of charge exchange - if applicable -
		between square brackets (e.g. [ACX] or [PCX]). Example for beryllium active
		charge exchange line at 468.5 nm: 'Be IV (8-6) [ACX]'. Example for impact
		excitation tungsten line coming from the plasma edge: 'W I'"""

	wavelength_central  :float =  sp_property(type="constant",units="m")
	""" Unshifted central wavelength of the processed spectral line"""

	radiance  :Signal =  sp_property(units="m^-2.s^-1.sr^-1")
	""" Calibrated, background subtracted radiance (integrated over the spectrum for
		this line)"""

	intensity  :Signal =  sp_property(units="(photonelectrons).s^-1")
	""" Non-calibrated intensity (integrated over the spectrum for this line), i.e.
		number of photoelectrons detected by unit time, taking into account electronic
		gain compensation and channels relative calibration"""

	width  :Signal =  sp_property(units="m")
	""" Full width at Half Maximum (FWHM) of the emission line"""

	shift  :Signal =  sp_property(units="m")
	""" Shift of the emission line wavelength with respected to the unshifted cental
		wavelength (e.g. Doppler shift)"""


class _T_charge_exchange_channel_ion_fast(SpTree):
	"""Charge exchange channel: fast ion CX quantities"""

	a  :float =  sp_property(units="Atomic Mass Unit",type="constant")
	""" Mass of atom of the fast ion"""

	z_ion  :float =  sp_property(type="constant",units="Elementary Charge Unit")
	""" Fast ion charge"""

	z_n  :float =  sp_property(units="Elementary Charge Unit",type="constant")
	""" Nuclear charge of the fast ion"""

	label  :str =  sp_property(type="constant")
	""" String identifying the fast ion (e.g. H+, D+, T+, He+2, C+6, ...)"""

	transition_wavelength  :float =  sp_property(type="constant",units="m")
	""" Unshifted wavelength of the fast ion charge exchange transition"""

	radiance  :Signal =  sp_property(units="(photons) m^-2.s^-1.sr^-1")
	""" Calibrated radiance of the fast ion charge exchange spectrum assuming the shape
		is pre-defined (e.g. by the Fokker-Planck slowing-down function). Note: radiance
		is integrated over the sightline crossing the neutral beam"""

	radiance_spectral_method  :_T_identifier =  sp_property()
	""" Description of the method used to reconstruct the fast ion charge exchange
		spectrum (e.g. what pre-defined slowing-down and source functions used)"""


class _T_charge_exchange_channel_ion(SpTree):
	"""Charge exchange channel for a given ion species"""

	a  :float =  sp_property(units="Atomic Mass Unit",type="constant")
	""" Mass of atom of the ion"""

	z_ion  :float =  sp_property(type="constant",units="Elementary Charge Unit")
	""" Ion charge"""

	z_n  :float =  sp_property(units="Elementary Charge Unit",type="constant")
	""" Nuclear charge"""

	label  :str =  sp_property(type="constant")
	""" String identifying the ion (e.g. H+, D+, T+, He+2, C+6, ...)"""

	t_i  :Signal =  sp_property(units="eV")
	""" Ion temperature at the channel measurement point"""

	t_i_method  :_T_identifier =  sp_property()
	""" Description of the method used to derive the ion temperature"""

	velocity_tor  :Signal =  sp_property(units="m.s^-1")
	""" Toroidal velocity of the ion (oriented counter-clockwise when seen from above)
		at the channel measurement point"""

	velocity_tor_method  :_T_identifier =  sp_property()
	""" Description of the method used to reconstruct the ion toroidal velocity"""

	velocity_pol  :Signal =  sp_property(units="m.s^-1")
	""" Poloidal velocity of the ion (oriented clockwise when seen from front on the
		right side of the tokamak axi-symmetry axis) at the channel measurement point"""

	velocity_pol_method  :_T_identifier =  sp_property()
	""" Description of the method used to reconstruct the ion poloidal velocity"""

	n_i_over_n_e  :Signal =  sp_property(units="-")
	""" Ion concentration (ratio of the ion density over the electron density) at the
		channel measurement point"""

	n_i_over_n_e_method  :_T_identifier =  sp_property()
	""" Description of the method used to derive the ion concentration"""


class _T_charge_exchange_channel_bes(SpTree):
	"""Charge exchange channel - BES parameters"""

	a  :float =  sp_property(units="Atomic Mass Unit",type="constant")
	""" Mass of atom of the diagnostic neutral beam particle"""

	z_ion  :float =  sp_property(type="constant",units="Elementary Charge Unit")
	""" Ion charge of the diagnostic neutral beam particle"""

	z_n  :float =  sp_property(units="Elementary Charge Unit",type="constant")
	""" Nuclear charge of the diagnostic neutral beam particle"""

	label  :str =  sp_property(type="constant")
	""" String identifying the diagnostic neutral beam particle"""

	transition_wavelength  :float =  sp_property(type="constant",units="m")
	""" Unshifted wavelength of the BES transition"""

	doppler_shift  :Signal =  sp_property(units="m")
	""" Doppler shift due to the diagnostic neutral beam particle velocity"""

	lorentz_shift  :Signal =  sp_property(units="m")
	""" Lorentz shift due to the Lorentz electric field (vxB) in the frame of the
		diagnostic neutral beam particles moving with a velocity v across the magnetic
		field B"""

	radiances  :SignalND =  sp_property(units="(photons) m^-2.s^-1.sr^-1",coordinate1="1...9",coordinate2="time")
	""" Calibrated intensities of the 9 splitted lines (Stark effect due to Lorentz
		electric field). Note: radiances are integrated over the sightline crossing the
		neutral beam"""


class _T_charge_exchange_channel_spectrum(SpTree):
	"""CX spectrum observed via a grating"""

	grating  :float =  sp_property(type="static",units="m^-1")
	""" Number of grating lines per unit length"""

	slit_width  :float =  sp_property(type="static",units="m")
	""" Width of the slit (placed in the object focal plane)"""

	instrument_function  :array_type =  sp_property(type="static",units="m",coordinate1="1...2",coordinate2="1...N")
	""" Array of Gaussian widths and amplitudes which as a sum make up the instrument
		fuction. IF(lambda) = sum( instrument_function(1,i)/sqrt(2 * pi *
		instrument_function(2,i)^2 ) * exp( -lambda^2/(2 * instrument_function(2,i)^2) )
		),whereby sum( instrument_function(1,i) ) = 1"""

	exposure_time  :float =  sp_property(type="constant",units="s")
	""" Exposure time"""

	wavelengths  :array_type =  sp_property(type="constant",units="m",coordinate1="1...N")
	""" Measured wavelengths"""

	intensity_spectrum  :SignalND =  sp_property(units="(photoelectrons).s^-1",coordinate1="../wavelengths",coordinate2="time")
	""" Intensity spectrum (not calibrated), i.e. number of photoelectrons detected by
		unit time by a wavelength pixel of the channel, taking into account electronic
		gain compensation and channels relative calibration"""

	radiance_spectral  :SignalND =  sp_property(units="(photons) m^-2.s^-1.sr^-1.m^-1",coordinate1="../wavelengths",coordinate2="time")
	""" Calibrated spectral radiance (radiance per unit wavelength)"""

	processed_line  :AoS[_T_charge_exchange_channel_processed_line] =  sp_property(coordinate1="1...N")
	""" Set of processed spectral lines"""

	radiance_calibration  :array_type =  sp_property(type="static",units="m^-3.sr^-1",coordinate1="../wavelengths")
	""" Radiance calibration"""

	radiance_calibration_date  :str =  sp_property(type="static")
	""" Date of the radiance calibration (yyyy_mm_dd)"""

	wavelength_calibration_date  :str =  sp_property(type="static")
	""" Date of the wavelength calibration (yyyy_mm_dd)"""

	radiance_continuum  :SignalND =  sp_property(coordinate1="../wavelengths",coordinate2="time",units="m^-2.s^-1.sr^-1.m^-1")
	""" Calibrated continuum intensity in the middle of the spectrum per unit wavelength"""


class _T_charge_exchange_channel(SpTree):
	"""Charge exchange channel"""

	name  :str =  sp_property(type="static")
	""" Name of the channel"""

	identifier  :str =  sp_property(type="static")
	""" ID of the channel"""

	position  :_T_rzphi1d_dynamic_aos1 =  sp_property()
	""" Position of the measurements"""

	t_i_average  :Signal =  sp_property(units="eV")
	""" Ion temperature (averaged on charge states and ion species) at the channel
		measurement point"""

	t_i_average_method  :_T_identifier =  sp_property()
	""" Description of the method used to reconstruct the average ion temperature"""

	zeff  :Signal =  sp_property(units="-")
	""" Local ionic effective charge at the channel measurement point"""

	zeff_method  :_T_identifier =  sp_property()
	""" Description of the method used to reconstruct the local effective charge"""

	zeff_line_average  :Signal =  sp_property(units="-")
	""" Ionic effective charge, line average along the channel line-of-sight"""

	zeff_line_average_method  :_T_identifier =  sp_property()
	""" Description of the method used to reconstruct the line average effective charge"""

	momentum_tor  :Signal =  sp_property(units="kg.m^-1.s^-1")
	""" Total plasma toroidal momentum, summed over ion species and electrons weighted
		by their density and major radius, i.e. sum_over_species(n*R*m*Vphi), at the
		channel measurement point"""

	momentum_tor_method  :_T_identifier =  sp_property()
	""" Description of the method used to reconstruct the total plasma toroidal momentum"""

	ion  :AoS[_T_charge_exchange_channel_ion] =  sp_property(coordinate1="1...N")
	""" Physical quantities related to ion species and charge stage (H+, D+, T+, He+2,
		Li+3, Be+4, C+6, N+7, O+8, Ne+10, Si+14, Ar+16 or Ar+18) derived from the
		measured charge exchange emission of each species, at the position of the
		measurement"""

	bes  :_T_charge_exchange_channel_bes =  sp_property()
	""" Derived Beam Emission Spectroscopy (BES) parameters"""

	ion_fast  :AoS[_T_charge_exchange_channel_ion_fast] =  sp_property(coordinate1="1...N")
	""" Derived Fast Ion Charge eXchange (FICX) parameters"""

	spectrum  :AoS[_T_charge_exchange_channel_spectrum] =  sp_property(coordinate1="1...N")
	""" Set of spectra obtained by various gratings"""


class _T_charge_exchange(IDS):
	"""Charge exchange spectroscopy diagnostic
	lifecycle_status: alpha
	lifecycle_version: 3.0.4
	lifecycle_last_change: 3.33.0"""

	dd_version="v3_38_1_dirty"
	ids_name="charge_exchange"

	aperture  :DetectorAperture =  sp_property()
	""" Description of the collimating aperture of the diagnostic, relevant to all
		lines-of-sight (channels)"""

	etendue  :float =  sp_property(type="static",units="m^2.str")
	""" Etendue (geometric extent) of the optical system"""

	etendue_method  :_T_identifier_static =  sp_property()
	""" Method used to calculate the etendue. Index = 0 : exact calculation with a 4D
		integral; 1 : approximation with first order formula (detector surface times
		solid angle subtended by the apertures); 2 : other methods"""

	channel  :AoS[_T_charge_exchange_channel] =  sp_property(coordinate1="1...N")
	""" Set of channels (lines-of-sight). The line-of-sight is defined by the centre of
		the collimating aperture and the position of the measurements."""

	latency  :float =  sp_property(type="static",units="s",introduced_after_version="3.32.1")
	""" Upper bound of the delay between physical information received by the detector
		and data available on the real-time (RT) network."""
