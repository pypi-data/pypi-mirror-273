"""
  This module containes the _FyTok_ wrapper of IMAS/dd/nbi
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_rzphi0d_dynamic_aos3,_T_rzphi1d_static,_T_rzphi0d_static,_T_plasma_composition_species,_T_signal_flt_1d,_T_signal_flt_2d,_T_detector_aperture

class _T_nbi_unit_beamlets_group_divergence(SpTree):
	"""Describes a divergence component of a group of beamlets"""

	particles_fraction  :float =  sp_property(type="static",units="-")
	""" Fraction of injected particles in the component"""

	vertical  :float =  sp_property(type="static",units="rad")
	""" The vertical beamlet divergence of the component. Here the divergence is defined
		for Gaussian beams as the angel where the beam density is reduced by a factor
		1/e compared to the maximum density. For non-Gaussian beams the divergence is
		sqrt(2)*mean((x-mean(x))**2), where x is the angle and the mean should be
		performed over the beam density, P(x): mean(y)=int(y*P(x)*dx)."""

	horizontal  :float =  sp_property(type="static",units="rad")
	""" The horiztonal beamlet divergence of the component. Here the divergence is
		defined for Gaussian beams as the angel where the beam density is reduced by a
		factor 1/e compared to the maximum density. For non-Gaussian beams the
		divergence is sqrt(2)*mean((x-mean(x))**2), where x is the angle and the mean
		should be performed over the beam density, P(x): mean(y)=int(y*P(x)*dx)."""


class _T_nbi_unit_beamlets_group_focus(SpTree):
	"""Describes of a group of beamlets is focused"""

	focal_length_horizontal  :float =  sp_property(type="static",units="m")
	""" Horizontal focal length along the beam line, i.e. the point along the centre of
		the beamlet-group where the beamlet-group has its minimum horizontal width"""

	focal_length_vertical  :float =  sp_property(type="static",units="m")
	""" Vertical focal length along the beam line, i.e. the point along the centre of
		the beamlet-group where the beamlet-group has its minimum vertical width"""

	width_min_horizontal  :float =  sp_property(type="static",units="m")
	""" The horizontal width of the beamlets group at the at the horizontal focal point"""

	width_min_vertical  :float =  sp_property(type="static",units="m")
	""" The vertical width of the beamlets group at the at the vertical focal point"""


class _T_nbi_unit_beamlets_group_tilting(TimeSlice):
	"""Variation of position, tangency radius and angle in case of dynamic beam
		tilting, for a given time slice"""

	delta_position  :_T_rzphi0d_dynamic_aos3 =  sp_property()
	""" Variation of the position of the beamlet group centre"""

	delta_tangency_radius  :float =  sp_property(type="dynamic",units="m")
	""" Variation of the tangency radius (major radius where the central line of a NBI
		unit is tangent to a circle around the torus)"""

	delta_angle  :float =  sp_property(type="dynamic",units="rad")
	""" Variation of the angle of inclination between a beamlet at the centre of the
		injection unit surface and the horiontal plane"""


class _T_nbi_unit_beamlets_group_beamlets(SpTree):
	"""Detailed information on beamlets"""

	positions  :_T_rzphi1d_static =  sp_property(cocos_label_transformation="tor_angle_like",cocos_transformation_expression=".sigma_rphiz_eff",cocos_leaf_name_aos_indices="nbi.unit{i}.beamlets_group{j}.beamlets.positions.phi")
	""" Position of each beamlet"""

	tangency_radii  :array_type =  sp_property(type="static",units="m",coordinate1="../positions/r")
	""" Tangency radius (major radius where the central line of a beamlet is tangent to
		a circle around the torus), for each beamlet"""

	angles  :array_type =  sp_property(type="static",units="rad",coordinate1="../positions/r")
	""" Angle of inclination between a line at the centre of a beamlet and the
		horizontal plane, for each beamlet"""

	power_fractions  :array_type =  sp_property(type="static",units="-",coordinate1="../positions/r")
	""" Fraction of power of a unit injected by each beamlet"""


class _T_nbi_unit_beamlets_group(SpTree):
	"""Group of beamlets"""

	position  :_T_rzphi0d_static =  sp_property(cocos_label_transformation="tor_angle_like",cocos_transformation_expression=".sigma_rphiz_eff",cocos_leaf_name_aos_indices="nbi.unit{i}.beamlets_group{j}.position.phi")
	""" R, Z, Phi position of the beamlet group centre"""

	tangency_radius  :float =  sp_property(type="static",units="m")
	""" Tangency radius (major radius where the central line of a NBI unit is tangent to
		a circle around the torus)"""

	angle  :float =  sp_property(type="static",units="rad")
	""" Angle of inclination between a beamlet at the centre of the injection unit
		surface and the horiontal plane"""

	tilting  :TimeSeriesAoS[_T_nbi_unit_beamlets_group_tilting] =  sp_property(coordinate1="time",type="dynamic")
	""" In case of dynamic beam tilting (i.e. during the pulse), e.g. for some Beam
		Emission Spectroscopy use cases, variations of position, tangency radius and
		angle with respect to their static value, for various time slices"""

	direction  :int =  sp_property(type="static",cocos_label_transformation="tor_angle_like",cocos_transformation_expression=".sigma_rphiz_eff",cocos_leaf_name_aos_indices="nbi.unit{i}.beamlets_group{j}.direction")
	""" Direction of the beam seen from above the torus: -1 = clockwise; 1 = counter
		clockwise"""

	width_horizontal  :float =  sp_property(type="static",units="m")
	""" Horizontal width of the beam group at the injection unit surface (or grounded
		grid)"""

	width_vertical  :float =  sp_property(type="static",units="m")
	""" Vertical width of the beam group at the injection unit surface (or grounded
		grid)"""

	focus  :_T_nbi_unit_beamlets_group_focus =  sp_property()
	""" Describes how the beamlet group is focused"""

	divergence_component  :AoS[_T_nbi_unit_beamlets_group_divergence] =  sp_property(coordinate1="1...N")
	""" Detailed information on beamlet divergence. Divergence is described as a
		superposition of Gaussian components with amplitide _particles_fraction_ and
		vertical/horizontal divergence. Note that for positive ion NBI the divergence is
		well described by a single Gaussian"""

	beamlets  :_T_nbi_unit_beamlets_group_beamlets =  sp_property()
	""" Detailed information on beamlets"""


class _T_nbi_unit(SpTree):
	"""NBI unit"""

	name  :str =  sp_property(type="static")
	""" Name of the NBI unit"""

	identifier  :str =  sp_property(type="static")
	""" ID of the NBI unit"""

	species  :_T_plasma_composition_species =  sp_property()
	""" Injected species"""

	power_launched  :Signal =  sp_property(units="W")
	""" Power launched from this unit into the vacuum vessel"""

	energy  :Signal =  sp_property(units="eV")
	""" Full energy of the injected species (acceleration of a single atom)"""

	beam_current_fraction  :SignalND =  sp_property(coordinate1="1...3",coordinate2="time",units="-")
	""" Fractions of beam current distributed among the different energies, the first
		index corresponds to the fast neutrals energy (1:full, 2: half, 3: one third)"""

	beam_power_fraction  :SignalND =  sp_property(coordinate1="1...3",coordinate2="time",units="-")
	""" Fractions of beam power distributed among the different energies, the first
		index corresponds to the fast neutrals energy (1:full, 2: half, 3: one third)"""

	beamlets_group  :AoS[_T_nbi_unit_beamlets_group] =  sp_property(coordinate1="1...N")
	""" Group of beamlets with common vertical and horizontal focal point. If there are
		no common focal points, then select small groups of beamlets such that a focal
		point description of the beamlets group provides a fair description"""

	source  :DetectorAperture =  sp_property()
	""" Description of the surface of the ion source from which the beam is extracted"""

	aperture  :AoS[DetectorAperture] =  sp_property(coordinate1="1...N")
	""" Description of a set of collimating apertures through which the beam is launched"""


class _T_nbi(IDS):
	"""Neutral Beam Injection systems and description of the fast neutrals that arrive
		into the torus
	lifecycle_status: alpha
	lifecycle_version: 3.0.4
	lifecycle_last_change: 3.33.0"""

	dd_version="v3_38_1_dirty"
	ids_name="nbi"

	unit  :AoS[_T_nbi_unit] =  sp_property(coordinate1="1...N")
	""" The NBI system is described as a set of units of which the power can be
		controlled individually."""

	latency  :float =  sp_property(type="static",units="s",introduced_after_version="3.32.1")
	""" Upper bound of the delay between input command received from the RT network and
		actuator starting to react. Applies globally to the system described by this IDS
		unless specific latencies (e.g. channel-specific or antenna-specific) are
		provided at a deeper level in the IDS structure."""
