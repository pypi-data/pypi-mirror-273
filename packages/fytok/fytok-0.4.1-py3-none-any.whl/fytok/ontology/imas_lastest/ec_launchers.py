"""
  This module containes the _FyTok_ wrapper of IMAS/dd/ec_launchers
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_signal_flt_1d

class _T_ec_launchers_launching_position(SpTree):
	"""Structure for R, Z, Phi positions and min max values of R (1D, dynamic within a
		type 1 array of structure and with a common time base at the same level)"""

	r  :Expression  =  sp_property(type="dynamic",units="m",coordinate1="../../time")
	""" Major radius"""

	r_limit_min  :float =  sp_property(type="static",units="m",introduced_after_version="3.32.1")
	""" Major radius lower limit for the system"""

	r_limit_max  :float =  sp_property(type="static",units="m",introduced_after_version="3.32.1")
	""" Major radius upper limit for the system"""

	z  :Expression  =  sp_property(type="dynamic",units="m",coordinate1="../../time")
	""" Height"""

	phi  :Expression  =  sp_property(type="dynamic",units="rad",coordinate1="../../time")
	""" Toroidal angle"""


class _T_ec_launchers_beam_spot(SpTree):
	"""Spot ellipse characteristics"""

	size  :array_type =  sp_property(type="dynamic",coordinate1="1...2",coordinate2="../../time",units="m")
	""" Size of the spot ellipse"""

	angle  :Expression  =  sp_property(type="dynamic",coordinate1="../../time",units="rad")
	""" Rotation angle for the spot ellipse"""


class _T_ec_launchers_beam_phase(SpTree):
	"""Phase ellipse characteristics"""

	curvature  :array_type =  sp_property(type="dynamic",coordinate1="1...2",coordinate2="../../time",units="m^-1")
	""" Inverse curvature radii for the phase ellipse, positive/negative for
		divergent/convergent beams"""

	angle  :Expression  =  sp_property(units="rad",type="dynamic",coordinate1="../../time")
	""" Rotation angle for the phase ellipse"""


class _T_ec_launchers_beam(SpTree):
	"""Electron Cyclotron beam"""

	name  :str =  sp_property(type="static")
	""" Beam name"""

	identifier  :str =  sp_property(type="static")
	""" Beam identifier"""

	frequency  :Signal =  sp_property(units="Hz")
	""" Frequency"""

	power_launched  :Signal =  sp_property(units="W")
	""" Beam power launched into the vacuum vessel"""

	mode  :int =  sp_property(type="constant")
	""" Identifier for the main plasma wave mode excited by the EC beam. For the
		ordinary mode (O-mode), mode=1. For the extraordinary mode (X-mode), mode=-1"""

	launching_position  :_T_ec_launchers_launching_position =  sp_property()
	""" Launching position of the beam"""

	steering_angle_pol  :Expression  =  sp_property(type="dynamic",units="rad",coordinate1="../time")
	""" Steering angle of the EC beam in the R,Z plane (from the -R axis towards the -Z
		axis), angle_pol=atan2(-k_Z,-k_R), where k_Z and k_R are the Z and R components
		of the mean wave vector in the EC beam"""

	steering_angle_tor  :Expression  =  sp_property(type="dynamic",units="rad",coordinate1="../time",cocos_label_transformation="tor_angle_like",cocos_transformation_expression=".sigma_rphiz_eff",cocos_leaf_name_aos_indices="ec_launchers.launcher{i}.steering_angle_tor.data")
	""" Steering angle of the EC beam away from the poloidal plane that is increasing
		towards the positive phi axis, angle_tor=arcsin(k_phi/k), where k_phi is the
		component of the wave vector in the phi direction and k is the length of the
		wave vector. Here the term wave vector refers to the mean wave vector in the EC
		beam"""

	spot  :_T_ec_launchers_beam_spot =  sp_property()
	""" Spot ellipse characteristics"""

	phase  :_T_ec_launchers_beam_phase =  sp_property()
	""" Phase ellipse characteristics"""

	time  :array_type =  sp_property(units="s",type="dynamic",coordinate1="1...N")
	""" Time base used for position, angle, spot and phase quantities"""


class _T_ec_launchers(IDS):
	"""Launchers for heating and current drive in the electron cyclotron (EC)
		frequencies.
	lifecycle_status: alpha
	lifecycle_version: 3.7.0
	lifecycle_last_change: 3.37.0"""

	dd_version="v3_38_1_dirty"
	ids_name="ec_launchers"

	beam  :AoS[_T_ec_launchers_beam] =  sp_property(coordinate1="1...N",introduced_after_version="3.36.0")
	""" Set of Electron Cyclotron beams"""

	latency  :float =  sp_property(type="static",units="s",introduced_after_version="3.32.1")
	""" Upper bound of the delay between input command received from the RT network and
		actuator starting to react. Applies globally to the system described by this IDS
		unless specific latencies (e.g. channel-specific or antenna-specific) are
		provided at a deeper level in the IDS structure."""
