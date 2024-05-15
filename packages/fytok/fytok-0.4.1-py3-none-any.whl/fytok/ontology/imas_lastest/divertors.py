"""
  This module containes the _FyTok_ wrapper of IMAS/dd/divertors
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_rzphi1d_static,_T_signal_flt_1d,_T_identifier_static
from .utilities import _E_midplane_identifier

class _T_divertor_target_two_point_model(TimeSlice):
	"""Two point model for a given divertor target"""

	t_e_target  :float =  sp_property(type="dynamic",units="eV")
	""" Electron temperature at divertor target"""

	n_e_target  :float =  sp_property(type="dynamic",units="m^-3")
	""" Electron density at divertor target"""

	sol_heat_decay_length  :float =  sp_property(type="dynamic",units="m")
	""" Heat flux decay length in SOL at divertor entrance, mapped to the mid-plane,
		this is the lambda_q parameter defined in reference T. Eich et al, Nucl. Fusion
		53 (2013) 093031"""

	sol_heat_spreading_length  :float =  sp_property(type="dynamic",units="m")
	""" Heat flux spreading length in SOL at equatorial mid-plane, this is the S power
		spreading parameter defined in reference T. Eich et al, Nucl. Fusion 53 (2013)
		093031. Relevant only for attached plasmas."""


class _T_divertor_target_tile(SpTree):
	"""Divertor tile description"""

	name  :str =  sp_property(type="static")
	""" Name of the tile"""

	identifier  :str =  sp_property(type="static")
	""" Alphanumeric identifier of tile"""

	surface_outline  :_T_rzphi1d_static =  sp_property()
	""" Outline of the tile surface facing the plasma"""

	surface_area  :float =  sp_property(type="static",units="m^2")
	""" Area of the tile surface facing the plasma"""

	current_incident  :Signal =  sp_property(units="A")
	""" Total current incident on this tile"""

	shunt_index  :int =  sp_property(type="static")
	""" If the tile carries a measurement shunt, index of that shunt (in the magnetics
		IDS shunt array)"""


class _T_divertor_target(SpTree):
	"""Divertor target description"""

	name  :str =  sp_property(type="static")
	""" Name of the target"""

	identifier  :str =  sp_property(type="static")
	""" Alphanumeric identifier of target"""

	heat_flux_steady_limit_max  :float =  sp_property(type="static",units="W.m^-2")
	""" Maximum steady state heat flux allowed on divertor target surface (engineering
		design limit)"""

	temperature_limit_max  :float =  sp_property(type="static",units="K")
	""" Maximum surface target temperature allowed to prevent damage (melting,
		recrystallization, sublimation, etc...)"""

	t_e_target_sputtering_limit_max  :float =  sp_property(type="static",units="eV")
	""" Maximum plasma temperature allowed on the divertor target to avoid excessive
		sputtering"""

	power_flux_peak  :Signal =  sp_property(units="W.m^-2")
	""" Peak power flux on the divertor target surface"""

	flux_expansion  :Signal =  sp_property(units="-",url="divertors/flux_expansion.png")
	""" Magnetic flux expansion as defined by Stangeby : ratio between the poloidal
		field at the midplane separatrix and the poloidal field at the strike-point see
		formula attached, where u means upstream (midplane separatrix) and t means at
		divertor target (downstream)."""

	two_point_model  :TimeSeriesAoS[_T_divertor_target_two_point_model] =  sp_property(coordinate1="time",type="dynamic")
	""" Description of SOL according to the two point model, the downstream point being
		on this target, for various time slices"""

	tilt_angle_pol  :Signal =  sp_property(units="rad")
	""" Angle between field lines projected in poloidal plane and target, measured
		clockwise from the target to the projected field lines"""

	extension_r  :float =  sp_property(type="static",units="m")
	""" Target length projected on the major radius axis"""

	extension_z  :float =  sp_property(type="static",units="m")
	""" Target length projected on the height axis"""

	wetted_area  :Signal =  sp_property(units="m^2")
	""" Wetted area of the target, defined by the SOL heat flux decay length (lambda_q)
		mapped to the target using flux expansion and spreading factor and the target
		toroidal circumference. In other words, this is the area getting heat flux from
		the maximum value down to one e-fold decay."""

	power_incident_fraction  :Signal =  sp_property(units="-")
	""" Power fraction incident on the target (normalized to the total power incident on
		the divertor)"""

	power_incident  :Signal =  sp_property(units="W")
	""" Total power incident on this target. This power is split in the various physical
		categories listed below"""

	power_conducted  :Signal =  sp_property(units="W")
	""" Power conducted by the plasma on this divertor target"""

	power_convected  :Signal =  sp_property(units="W")
	""" Power convected by the plasma on this divertor target"""

	power_radiated  :Signal =  sp_property(units="W")
	""" Net radiated power on this divertor target (incident - reflected)"""

	power_black_body  :Signal =  sp_property(units="W")
	""" Black body radiated power emitted from this divertor target (emissivity is
		included)"""

	power_neutrals  :Signal =  sp_property(units="W")
	""" Net power from neutrals on this divertor target (positive means power is
		deposited on the target)"""

	power_recombination_plasma  :Signal =  sp_property(units="W")
	""" Power deposited on this divertor target due to recombination of plasma ions"""

	power_recombination_neutrals  :Signal =  sp_property(units="W")
	""" Power deposited on this divertor target due to recombination of neutrals into a
		ground state (e.g. molecules)"""

	power_currents  :Signal =  sp_property(units="W")
	""" Power deposited on this divertor target due to electric currents (positive means
		power is deposited on the target)"""

	current_incident  :Signal =  sp_property(units="A",introduced_after_version="3.32.1")
	""" Total current incident on this target"""

	tile  :AoS[_T_divertor_target_tile] =  sp_property(coordinate1="1...N",introduced_after_version="3.32.1")
	""" Set of divertor tiles belonging to this target"""


class _T_divertor(SpTree):
	"""Divertor description"""

	name  :str =  sp_property(type="static")
	""" Name of the divertor"""

	identifier  :str =  sp_property(type="static")
	""" Alphanumeric identifier of divertor"""

	target  :AoS[_T_divertor_target] =  sp_property(coordinate1="1...N")
	""" Set of divertor targets"""

	wetted_area  :Signal =  sp_property(units="m^2")
	""" Wetted area of the divertor (sum over all targets)"""

	power_incident  :Signal =  sp_property(units="W")
	""" Total power incident on the divertor (sum over all targets). This power is split
		in the various physical categories listed below"""

	power_conducted  :Signal =  sp_property(units="W")
	""" Power conducted by the plasma on the divertor targets (sum over all targets)"""

	power_convected  :Signal =  sp_property(units="W")
	""" Power convected by the plasma on the divertor targets (sum over all targets)"""

	power_radiated  :Signal =  sp_property(units="W")
	""" Net radiated power on the divertor targets (incident - reflected) (sum over all
		targets)"""

	power_black_body  :Signal =  sp_property(units="W")
	""" Black body radiated power emitted from the divertor targets (emissivity is
		included) (sum over all targets)"""

	power_neutrals  :Signal =  sp_property(units="W")
	""" Net power from neutrals on the divertor targets (positive means power is
		deposited on the target) (sum over all targets)"""

	power_recombination_plasma  :Signal =  sp_property(units="W")
	""" Power deposited on the divertor targets due to recombination of plasma ions (sum
		over all targets)"""

	power_recombination_neutrals  :Signal =  sp_property(units="W")
	""" Power deposited on the divertor targets due to recombination of neutrals into a
		ground state (e.g. molecules) (sum over all targets)"""

	power_currents  :Signal =  sp_property(units="W")
	""" Power deposited on the divertor targets due to electric currents (positive means
		power is deposited on the target) (sum over all targets)"""

	particle_flux_recycled_total  :Signal =  sp_property(units="s^-1")
	""" Total recycled particle flux from the divertor (in equivalent electrons)"""

	current_incident  :Signal =  sp_property(units="A",introduced_after_version="3.32.1")
	""" Total current incident on this divertor"""


class _T_divertors(IDS):
	"""Description of divertors
	lifecycle_status: alpha
	lifecycle_version: 3.31.0
	lifecycle_last_change: 3.33.0"""

	dd_version="v3_38_1_dirty"
	ids_name="divertors"

	midplane  :_E_midplane_identifier =  sp_property(doc_identifier="utilities/midplane_identifier.xml",introduced_after_version="3.32.1")
	""" Choice of midplane definition (use the lowest index number if more than one
		value is relevant)"""

	divertor  :AoS[_T_divertor] =  sp_property(coordinate1="1...N")
	""" Set of divertors"""
