"""
  This module containes the _FyTok_ wrapper of IMAS/dd/summary
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_identifier_static,_T_entry_tag
from .utilities import _E_materials
from .utilities import _E_midplane_identifier

class _T_summary_dynamic_flt_1d_root_parent_2(SpTree):
	"""Summary dynamic FLT_1D + source information, time at the root of the IDS and
		units as parent level 2"""

	value  :Expression  =  sp_property(type="dynamic",units="as_parent_level_2",coordinate1="/time")
	""" Value"""

	source  :str =  sp_property(type="constant")
	""" Source of the data (any comment describing the origin of the data : code, path
		to diagnostic signals, processing method, ...)"""


class _T_summary_dynamic_flt_2d_fraction_2(SpTree):
	"""Summary dynamic FL2_1D + source information, time at the root of the IDS, first
		dimension 1...3 (beam fractions)"""

	value  :array_type =  sp_property(type="dynamic",units="as_parent",coordinate1="1...3",coordinate2="/time")
	""" Value"""

	source  :str =  sp_property(type="constant")
	""" Source of the data (any comment describing the origin of the data : code, path
		to diagnostic signals, processing method, ...)"""


class _T_summary_dynamic_flt_1d_root(SpTree):
	"""Summary dynamic FLT_1D + source information, time at the root of the IDS"""

	value  :Expression  =  sp_property(type="dynamic",units="as_parent",coordinate1="/time")
	""" Value"""

	source  :str =  sp_property(type="constant")
	""" Source of the data (any comment describing the origin of the data : code, path
		to diagnostic signals, processing method, ...)"""


class _T_summary_static_flt_0d(SpTree):
	"""Summary static FLT_0D + source information"""

	value  :float =  sp_property(type="static",units="as_parent")
	""" Value"""

	source  :str =  sp_property(type="constant")
	""" Source of the data (any comment describing the origin of the data : code, path
		to diagnostic signals, processing method, ...)"""


class _T_summary_static_int_0d(SpTree):
	"""Summary static INT_0D + source information"""

	value  :int =  sp_property(type="static")
	""" Value"""

	source  :str =  sp_property(type="constant")
	""" Source of the data (any comment describing the origin of the data : code, path
		to diagnostic signals, processing method, ...)"""


class _T_summary_static_str_0d(SpTree):
	"""Summary static STR_0D + source information"""

	value  :str =  sp_property(type="static")
	""" Value"""

	source  :str =  sp_property(type="constant")
	""" Source of the data (any comment describing the origin of the data : code, path
		to diagnostic signals, processing method, ...)"""


class _T_summary_constant_int_0d(SpTree):
	"""Summary constant INT_0D + source information"""

	value  :int =  sp_property(type="constant")
	""" Value"""

	source  :str =  sp_property(type="constant")
	""" Source of the data (any comment describing the origin of the data : code, path
		to diagnostic signals, processing method, ...)"""


class _T_summary_constant_flt_0d(SpTree):
	"""Summary constant FLT_0D + source information"""

	value  :float =  sp_property(type="constant",units="as_parent")
	""" Value"""

	source  :str =  sp_property(type="constant")
	""" Source of the data (any comment describing the origin of the data : code, path
		to diagnostic signals, processing method, ...)"""


class _T_summary_constant_flt_0d_2(SpTree):
	"""Summary constant FLT_0D + source information, units as parent level 2"""

	value  :float =  sp_property(type="constant",units="as_parent_level_2")
	""" Value"""

	source  :str =  sp_property(type="constant")
	""" Source of the data (any comment describing the origin of the data : code, path
		to diagnostic signals, processing method, ...)"""


class _T_summary_constant_str_0d(SpTree):
	"""Summary constant STR_0D + source information"""

	value  :str =  sp_property(type="constant")
	""" Value"""

	source  :str =  sp_property(type="constant")
	""" Source of the data (any comment describing the origin of the data : code, path
		to diagnostic signals, processing method, ...)"""


class _T_summary_rz1d_dynamic(SpTree):
	"""Structure for R, Z positions (1D, dynamic) + source information"""

	r  :Expression  =  sp_property(units="m",type="dynamic",coordinate1="/time")
	""" Major radius"""

	z  :Expression  =  sp_property(units="m",type="dynamic",coordinate1="/time")
	""" Height"""

	source  :str =  sp_property(type="constant")
	""" Source of the data (any comment describing the origin of the data : code, path
		to diagnostic signals, processing method, ...)"""


class _T_summary_dynamic_int_1d_root(SpTree):
	"""Summary dynamic INT_1D + source information, time at the root of the IDS"""

	value  :array_type =  sp_property(type="dynamic",coordinate1="/time")
	""" Value"""

	source  :str =  sp_property(type="constant")
	""" Source of the data (any comment describing the origin of the data : code, path
		to diagnostic signals, processing method, ...)"""


class _T_summary_local_position_r_z(SpTree):
	"""Radial position at which physics quantities are evaluated, including an R,Z
		position"""

	rho_tor_norm  :Expression  =  sp_property(type="dynamic",coordinate1="../../../../time",units="-")
	""" Normalised toroidal flux coordinate. The normalizing value for rho_tor_norm, is
		the toroidal flux coordinate at the equilibrium boundary (LCFS or 99.x % of the
		LCFS in case of a fixed boundary equilibium calculation, see
		time_slice/boundary/b_flux_pol_norm in the equilibrium IDS)"""

	rho_tor  :Expression  =  sp_property(type="dynamic",coordinate1="../../../../time",units="m")
	""" Toroidal flux coordinate. rho_tor = sqrt(b_flux_tor/(pi*b0)) ~
		sqrt(pi*r^2*b0/(pi*b0)) ~ r [m]. The toroidal field used in its definition is
		indicated under global_quantities/b0"""

	psi  :Expression  =  sp_property(coordinate1="../../../../time",units="Wb",type="dynamic")
	""" Poloidal magnetic flux"""

	r  :Expression  =  sp_property(coordinate1="../../../../time",units="m",type="dynamic")
	""" Major radius"""

	z  :Expression  =  sp_property(coordinate1="../../../../time",units="m",type="dynamic")
	""" Height"""


class _T_summary_local_position(SpTree):
	"""Radial position at which physics quantities are evaluated"""

	rho_tor_norm  :Expression  =  sp_property(type="dynamic",coordinate1="../../../../time",units="-")
	""" Normalised toroidal flux coordinate. The normalizing value for rho_tor_norm, is
		the toroidal flux coordinate at the equilibrium boundary (LCFS or 99.x % of the
		LCFS in case of a fixed boundary equilibium calculation, see
		time_slice/boundary/b_flux_pol_norm in the equilibrium IDS)"""

	rho_tor  :Expression  =  sp_property(type="dynamic",coordinate1="../../../../time",units="m")
	""" Toroidal flux coordinate. rho_tor = sqrt(b_flux_tor/(pi*b0)) ~
		sqrt(pi*r^2*b0/(pi*b0)) ~ r [m]. The toroidal field used in its definition is
		indicated under global_quantities/b0"""

	psi  :Expression  =  sp_property(coordinate1="../../../../time",units="Wb",type="dynamic",cocos_label_transformation="psi_like",cocos_transformation_expression=".fact_psi",cocos_leaf_name_aos_indices="IDSPATH.position.psi")
	""" Poloidal magnetic flux"""


class _T_summary_rzphi0d_static(SpTree):
	"""Structure for R, Z, Phi positions (0D, static) + source information"""

	r  :_T_summary_static_flt_0d =  sp_property(units="m")
	""" Major radius"""

	z  :_T_summary_static_flt_0d =  sp_property(units="m")
	""" Height"""

	phi  :_T_summary_static_flt_0d =  sp_property(units="rad")
	""" Toroidal angle"""


class _T_summary_species_tor_angle(SpTree):
	"""List of ion species used in summary with tor_angle cocos transform"""

	hydrogen  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property(cocos_label_transformation="tor_angle_like",cocos_transformation_expression=".sigma_rphiz_eff",cocos_leaf_name_aos_indices="IDSPATH.velocity_tor.hydrogen.value")
	""" Hydrogen (H)"""

	deuterium  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property(cocos_label_transformation="tor_angle_like",cocos_transformation_expression=".sigma_rphiz_eff",cocos_leaf_name_aos_indices="IDSPATH.velocity_tor.deuterium.value")
	""" Deuterium (D)"""

	tritium  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property(cocos_label_transformation="tor_angle_like",cocos_transformation_expression=".sigma_rphiz_eff",cocos_leaf_name_aos_indices="IDSPATH.velocity_tor.tritium.value")
	""" Tritium (T)"""

	helium_3  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property(cocos_label_transformation="tor_angle_like",cocos_transformation_expression=".sigma_rphiz_eff",cocos_leaf_name_aos_indices="IDSPATH.velocity_tor.helium_3.value")
	""" Helium isotope with 3 nucleons (3He)"""

	helium_4  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property(cocos_label_transformation="tor_angle_like",cocos_transformation_expression=".sigma_rphiz_eff",cocos_leaf_name_aos_indices="IDSPATH.velocity_tor.helium_4.value")
	""" Helium isotope with 4 nucleons (4He)"""

	beryllium  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property(cocos_label_transformation="tor_angle_like",cocos_transformation_expression=".sigma_rphiz_eff",cocos_leaf_name_aos_indices="IDSPATH.velocity_tor.beryllium.value")
	""" Beryllium (Be)"""

	lithium  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property(cocos_label_transformation="tor_angle_like",cocos_transformation_expression=".sigma_rphiz_eff",cocos_leaf_name_aos_indices="IDSPATH.velocity_tor.lithium.value")
	""" Lithium (Li)"""

	carbon  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property(cocos_label_transformation="tor_angle_like",cocos_transformation_expression=".sigma_rphiz_eff",cocos_leaf_name_aos_indices="IDSPATH.velocity_tor.carbon.value")
	""" Carbon (C)"""

	nitrogen  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property(cocos_label_transformation="tor_angle_like",cocos_transformation_expression=".sigma_rphiz_eff",cocos_leaf_name_aos_indices="IDSPATH.velocity_tor.nitrogen.value")
	""" Nitrogen (N)"""

	neon  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property(cocos_label_transformation="tor_angle_like",cocos_transformation_expression=".sigma_rphiz_eff",cocos_leaf_name_aos_indices="IDSPATH.velocity_tor.neon.value")
	""" Neon (Ne)"""

	argon  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property(cocos_label_transformation="tor_angle_like",cocos_transformation_expression=".sigma_rphiz_eff",cocos_leaf_name_aos_indices="IDSPATH.velocity_tor.argon.value")
	""" Argon (Ar)"""

	xenon  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property(cocos_label_transformation="tor_angle_like",cocos_transformation_expression=".sigma_rphiz_eff",cocos_leaf_name_aos_indices="IDSPATH.velocity_tor.xenon.value")
	""" Xenon (Xe)"""

	oxygen  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property(cocos_label_transformation="tor_angle_like",cocos_transformation_expression=".sigma_rphiz_eff",cocos_leaf_name_aos_indices="IDSPATH.velocity_tor.oxygen.value")
	""" Oxygen (O)"""

	tungsten  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property(cocos_label_transformation="tor_angle_like",cocos_transformation_expression=".sigma_rphiz_eff",cocos_leaf_name_aos_indices="IDSPATH.velocity_tor.tungsten.value")
	""" Tungsten (W)"""

	iron  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property(cocos_label_transformation="tor_angle_like",cocos_transformation_expression=".sigma_rphiz_eff",cocos_leaf_name_aos_indices="IDSPATH.velocity_tor.iron.value")
	""" Iron (Fe)"""

	krypton  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property(cocos_label_transformation="tor_angle_like",cocos_transformation_expression=".sigma_rphiz_eff",cocos_leaf_name_aos_indices="IDSPATH.velocity_tor.krypton.value")
	""" Krypton (Kr)"""


class _T_summary_species(SpTree):
	"""List of ion species used in summary"""

	hydrogen  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Hydrogen (H)"""

	deuterium  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Deuterium (D)"""

	tritium  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Tritium (T)"""

	helium_3  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Helium isotope with 3 nucleons (3He)"""

	helium_4  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Helium isotope with 4 nucleons (4He)"""

	beryllium  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Beryllium (Be)"""

	lithium  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Lithium (Li)"""

	carbon  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Carbon (C)"""

	nitrogen  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Nitrogen (N)"""

	neon  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Neon (Ne)"""

	argon  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Argon (Ar)"""

	xenon  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Xenon (Xe)"""

	oxygen  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Oxygen (O)"""

	tungsten  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Tungsten (W)"""

	iron  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Iron (Fe)"""

	krypton  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Krypton (Kr)"""


class _T_summary_gas_injection_accumulated(SpTree):
	"""List of accumulated ion species and other related quantities within volume
		enclosed by first wall contour"""

	total  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Total accumulated injected gas (sum over species)"""

	midplane  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Accumulated gas injected from all valves located near the equatorial midplane"""

	top  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Accumulated gas injected from all valves located near the top of the vacuum
		chamber"""

	bottom  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Accumulated gas injected from all valves located near near the bottom of the
		vacuum chamber"""

	hydrogen  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Hydrogen"""

	deuterium  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Deuterium"""

	tritium  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Tritium"""

	helium_3  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Helium isotope with 3 nucleons"""

	helium_4  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Helium isotope with 4 nucleons"""

	impurity_seeding  :_T_summary_constant_int_0d =  sp_property()
	""" Flag set to 1 if any gas other than H, D, T, He is puffed during the pulse, 0
		otherwise"""

	beryllium  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Beryllium"""

	lithium  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Lithium"""

	carbon  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Carbon"""

	oxygen  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Oxygen"""

	nitrogen  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Nitrogen"""

	neon  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Neon"""

	argon  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Argon"""

	xenon  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Xenon"""

	krypton  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Krypton"""

	methane  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Methane (CH4)"""

	methane_carbon_13  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Methane (CH4 with carbon 13)"""

	methane_deuterated  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Deuterated methane (CD4)"""

	silane  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Silane (SiH4)"""

	ethylene  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Ethylene (C2H4)"""

	ethane  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Ethane (C2H6)"""

	propane  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Propane (C3H8)"""

	ammonia  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Ammonia (NH3)"""

	ammonia_deuterated  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Deuterated ammonia (ND3)"""


class _T_summary_gas_injection_prefill(SpTree):
	"""List of accumulated ion species during the prefill (constant)"""

	total  :_T_summary_constant_flt_0d_2 =  sp_property()
	""" Total accumulated injected gas (sum over species)"""

	midplane  :_T_summary_constant_flt_0d_2 =  sp_property()
	""" Accumulated gas injected from all valves located near the equatorial midplane"""

	top  :_T_summary_constant_flt_0d_2 =  sp_property()
	""" Accumulated gas injected from all valves located near the top of the vacuum
		chamber"""

	bottom  :_T_summary_constant_flt_0d_2 =  sp_property()
	""" Accumulated gas injected from all valves located near near the bottom of the
		vacuum chamber"""

	hydrogen  :_T_summary_constant_flt_0d_2 =  sp_property()
	""" Hydrogen"""

	deuterium  :_T_summary_constant_flt_0d_2 =  sp_property()
	""" Deuterium"""

	tritium  :_T_summary_constant_flt_0d_2 =  sp_property()
	""" Tritium"""

	helium_3  :_T_summary_constant_flt_0d_2 =  sp_property()
	""" Helium isotope with 3 nucleons"""

	helium_4  :_T_summary_constant_flt_0d_2 =  sp_property()
	""" Helium isotope with 4 nucleons"""

	impurity_seeding  :_T_summary_constant_int_0d =  sp_property()
	""" Flag set to 1 if any gas other than H, D, T, He is puffed during the prefill, 0
		otherwise"""

	beryllium  :_T_summary_constant_flt_0d_2 =  sp_property()
	""" Beryllium"""

	lithium  :_T_summary_constant_flt_0d_2 =  sp_property()
	""" Lithium"""

	carbon  :_T_summary_constant_flt_0d_2 =  sp_property()
	""" Carbon"""

	oxygen  :_T_summary_constant_flt_0d_2 =  sp_property()
	""" Oxygen"""

	nitrogen  :_T_summary_constant_flt_0d_2 =  sp_property()
	""" Nitrogen"""

	neon  :_T_summary_constant_flt_0d_2 =  sp_property()
	""" Neon"""

	argon  :_T_summary_constant_flt_0d_2 =  sp_property()
	""" Argon"""

	xenon  :_T_summary_constant_flt_0d_2 =  sp_property()
	""" Xenon"""

	krypton  :_T_summary_constant_flt_0d_2 =  sp_property()
	""" Krypton"""

	methane  :_T_summary_constant_flt_0d_2 =  sp_property()
	""" Methane (CH4)"""

	methane_carbon_13  :_T_summary_constant_flt_0d_2 =  sp_property()
	""" Methane (CH4 with carbon 13)"""

	methane_deuterated  :_T_summary_constant_flt_0d_2 =  sp_property()
	""" Deuterated methane (CD4)"""

	silane  :_T_summary_constant_flt_0d_2 =  sp_property()
	""" Silane (SiH4)"""

	ethylene  :_T_summary_constant_flt_0d_2 =  sp_property()
	""" Ethylene (C2H4)"""

	ethane  :_T_summary_constant_flt_0d_2 =  sp_property()
	""" Ethane (C2H6)"""

	propane  :_T_summary_constant_flt_0d =  sp_property()
	""" Propane (C3H8)"""

	ammonia  :_T_summary_constant_flt_0d_2 =  sp_property()
	""" Ammonia (NH3)"""

	ammonia_deuterated  :_T_summary_constant_flt_0d_2 =  sp_property()
	""" Deuterated ammonia (ND3)"""


class _T_summary_gas_injection(SpTree):
	"""List of ion species and other gas injection related quantities"""

	total  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Total gas injection rate (sum over species)"""

	midplane  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Gas injection rate from all valves located near the equatorial midplane"""

	top  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Gas injection rate from all valves located near the top of the vaccuum chamber"""

	bottom  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Gas injection rate from all valves located near near the bottom of the vaccuum
		chamber"""

	hydrogen  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Hydrogen"""

	deuterium  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Deuterium"""

	tritium  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Tritium"""

	helium_3  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Helium isotope with 3 nucleons"""

	helium_4  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Helium isotope with 4 nucleons"""

	impurity_seeding  :_T_summary_constant_int_0d =  sp_property()
	""" Flag set to 1 if any gas other than H, D, T, He is puffed during the pulse, 0
		otherwise"""

	beryllium  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Beryllium"""

	lithium  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Lithium"""

	carbon  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Carbon"""

	oxygen  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Oxygen"""

	nitrogen  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Nitrogen"""

	neon  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Neon"""

	argon  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Argon"""

	xenon  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Xenon"""

	krypton  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Krypton"""

	methane  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Methane (CH4)"""

	methane_carbon_13  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Methane (CH4 with carbon 13)"""

	methane_deuterated  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Deuterated methane (CD4)"""

	silane  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Silane (SiH4)"""

	ethylene  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Ethylene (C2H4)"""

	ethane  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Ethane (C2H6)"""

	propane  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Propane (C3H8)"""

	ammonia  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Ammonia (NH3)"""

	ammonia_deuterated  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Deuterated ammonia (ND3)"""


class _T_summary_plasma_composition_species(SpTree):
	"""Description of simple species (elements) without declaration of their ionisation
		state"""

	a  :_T_summary_constant_flt_0d =  sp_property(units="Atomic Mass Unit")
	""" Mass of atom"""

	z_n  :_T_summary_constant_flt_0d =  sp_property(units="Elementary Charge Unit")
	""" Nuclear charge"""

	label  :_T_summary_constant_str_0d =  sp_property()
	""" String identifying the species (e.g. H, D, T, ...)"""


class _T_summary_local_quantities_stellerator(SpTree):
	"""Set of local quantities for stellerators"""

	effective_helical_ripple  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Effective helical ripple for 1/nu neoclassical regime (see [Beidler, C. D., and
		W. N. G. Hitchon, 1994, Plasma Phys. Control. Fusion 35, 317])"""

	plateau_factor  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Plateau factor, as defined in equation (25) of reference [Stroth U. et al 1998
		Plasma Phys. Control. Fusion 40 1551]"""

	iota  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Rotational transform (1/q)"""


class _T_summary_pedestal_fit_stability_method(SpTree):
	"""MHD stability analysis of the pedestal (for a given method for calculating the
		bootstrap current)"""

	alpha_critical  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Critical normalized pressure gradient determined with self-consistent runs with
		an MHD stability code. Details of the method for scanning parameters in the
		series of runs must be described in the 'source' node"""

	alpha_ratio  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Ratio of alpha_critical over alpha_experimental"""

	t_e_pedestal_top_critical  :_T_summary_dynamic_flt_1d_root =  sp_property(units="eV")
	""" Critical electron temperature at pedestal top determined with self-consistent
		runs with an MHD stability code. Details of the method for scanning parameters
		in the series of runs must be described in the 'source' node"""


class _T_summary_pedestal_fit_linear_te(SpTree):
	"""Quantities related to linear fit of pedestal profiles for a given physical
		quantity (temperature)"""

	pedestal_height  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Pedestal height"""

	pedestal_width  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Pedestal full width in normalised poloidal flux"""

	pedestal_position  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Pedestal position in normalised poloidal flux"""

	offset  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Offset of the parent quantity in the SOL"""

	d_dpsi_norm  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Core slope of the parent quantity"""

	d_dpsi_norm_max  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Maximum gradient of the parent quantity (with respect to the normalised poloidal
		flux) in the pedestal"""


class _T_summary_pedestal_fit_te(SpTree):
	"""Quantities related to a generic fit of pedestal profiles for a given physical
		quantity (temperature)"""

	pedestal_height  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Pedestal height"""

	pedestal_width  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Pedestal full width in normalised poloidal flux"""

	pedestal_position  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Pedestal position in normalised poloidal flux"""

	offset  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Offset of the parent quantity in the SOL"""

	d_dpsi_norm  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Core slope of the parent quantity"""

	d_dpsi_norm_max  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Maximum gradient of the parent quantity (with respect to the normalised poloidal
		flux) in the pedestal"""

	d_dpsi_norm_max_position  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Position (in terms of normalised poloidal flux) of the maximum gradient of the
		parent quantity in the pedestal"""


class _T_summary_pedestal_fit_linear_ne(SpTree):
	"""Quantities related to linear fit of pedestal profiles for a given physical
		quantity (density or pressure)"""

	separatrix  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Value at separatrix"""

	pedestal_height  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Pedestal height"""

	pedestal_width  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Pedestal full width in normalised poloidal flux"""

	pedestal_position  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Pedestal position in normalised poloidal flux"""

	offset  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Offset of the parent quantity in the SOL"""

	d_dpsi_norm  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Core slope of the parent quantity"""

	d_dpsi_norm_max  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Maximum gradient of the parent quantity (with respect to the normalised poloidal
		flux) in the pedestal"""


class _T_summary_pedestal_fit_ne(SpTree):
	"""Quantities related to a generic fit of pedestal profiles for a given physical
		quantity (density or pressure)"""

	separatrix  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Value at separatrix"""

	pedestal_height  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Pedestal height"""

	pedestal_width  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Pedestal full width in normalised poloidal flux"""

	pedestal_position  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Pedestal position in normalised poloidal flux"""

	offset  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Offset of the parent quantity in the SOL"""

	d_dpsi_norm  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Core slope of the parent quantity"""

	d_dpsi_norm_max  :_T_summary_dynamic_flt_1d_root_parent_2 =  sp_property()
	""" Maximum gradient of the parent quantity (with respect to the normalised poloidal
		flux) in the pedestal"""

	d_dpsi_norm_max_position  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Position (in terms of normalised poloidal flux) of the maximum gradient of the
		parent quantity in the pedestal"""


class _T_summary_sol(SpTree):
	"""Scrape-Off-Layer characteristics"""

	t_e_decay_length  :_T_summary_dynamic_flt_1d_root =  sp_property(units="m")
	""" Electron temperature radial decay length inv(grad Te/Te)"""

	t_i_average_decay_length  :_T_summary_dynamic_flt_1d_root =  sp_property(units="m")
	""" Ion temperature (average over ion species) radial decay length inv(grad Ti/Ti)"""

	n_e_decay_length  :_T_summary_dynamic_flt_1d_root =  sp_property(units="m")
	""" Electron density radial decay length inv(grad ne/ne)"""

	n_i_total_decay_length  :_T_summary_dynamic_flt_1d_root =  sp_property(units="m")
	""" Ion density radial decay length inv(grad ni/ni)"""

	heat_flux_e_decay_length  :_T_summary_dynamic_flt_1d_root =  sp_property(units="m")
	""" Electron heat flux radial decay length inv(grad qe/qe)"""

	heat_flux_i_decay_length  :_T_summary_dynamic_flt_1d_root =  sp_property(units="m")
	""" Ion heat flux radial decay length inv(grad qi/qi)"""

	power_radiated  :_T_summary_dynamic_flt_1d_root =  sp_property(units="W")
	""" Power radiated from the SOL"""

	pressure_neutral  :_T_summary_dynamic_flt_1d_root =  sp_property(units="Pa")
	""" Neutral pressure in the SOL"""


class _T_summary_elms(SpTree):
	"""Edge Localized Modes related quantities"""

	frequency  :_T_summary_dynamic_flt_1d_root =  sp_property(units="Hz")
	""" ELMs frequency"""

	type  :_T_summary_dynamic_int_1d_root =  sp_property()
	""" ELMs type (I, II, III, ...)"""


class _T_summary_pellets(SpTree):
	"""Pellet related quantities"""

	occurrence  :_T_summary_constant_int_0d =  sp_property(units="Hz")
	""" Flag set to 1 if there is any pellet injected during the pulse, 0 otherwise"""


class _T_summary_boundary(SpTree):
	"""Geometry of the plasma boundary"""

	type  :_T_summary_dynamic_int_1d_root =  sp_property()
	""" 0 (limiter), 1 (diverted), 11 (LSN), 12 (USN), 13 (DN), 14 (snowflake)"""

	geometric_axis_r  :_T_summary_dynamic_flt_1d_root =  sp_property(units="m")
	""" R position of the geometric axis (defined as (Rmax+Rmin) / 2 of the boundary)"""

	geometric_axis_z  :_T_summary_dynamic_flt_1d_root =  sp_property(units="m")
	""" Z position of the geometric axis (defined as (Zmax+Zmin) / 2 of the boundary)"""

	magnetic_axis_r  :_T_summary_dynamic_flt_1d_root =  sp_property(units="m")
	""" R position of the magnetic axis"""

	magnetic_axis_z  :_T_summary_dynamic_flt_1d_root =  sp_property(units="m")
	""" Z position of the magnetic axis"""

	minor_radius  :_T_summary_dynamic_flt_1d_root =  sp_property(units="m")
	""" Minor radius of the plasma boundary (defined as (Rmax-Rmin) / 2 of the boundary)"""

	elongation  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Elongation of the plasma boundary"""

	triangularity_upper  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Upper triangularity of the plasma boundary"""

	triangularity_lower  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Lower triangularity of the plasma boundary"""

	strike_point_inner_r  :_T_summary_dynamic_flt_1d_root =  sp_property(units="m")
	""" R position of the inner strike point"""

	strike_point_inner_z  :_T_summary_dynamic_flt_1d_root =  sp_property(units="m")
	""" Z position of the inner strike point"""

	strike_point_outer_r  :_T_summary_dynamic_flt_1d_root =  sp_property(units="m")
	""" R position of the outer strike point"""

	strike_point_outer_z  :_T_summary_dynamic_flt_1d_root =  sp_property(units="m")
	""" Z position of the outer strike point"""

	strike_point_configuration  :_T_summary_constant_str_0d =  sp_property()
	""" String describing the configuration of the strike points (constant, may need to
		become dynamic when available)"""

	gap_limiter_wall  :_T_summary_dynamic_flt_1d_root =  sp_property(units="m")
	""" Distance between the separatrix and the nearest limiter or wall element"""

	distance_inner_outer_separatrices  :_T_summary_dynamic_flt_1d_root =  sp_property(units="m")
	""" Distance between the inner and outer separatrices, in the major radius
		direction, at the plasma outboard and at the height corresponding to the maximum
		R for the inner separatrix."""

	x_point_main  :_T_summary_rz1d_dynamic =  sp_property()
	""" RZ position of the main X-point"""


class _T_summary_rmp(SpTree):
	"""Resonant magnetic perturbations related quantities"""

	occurrence  :_T_summary_constant_int_0d =  sp_property(units="Hz")
	""" Flag set to 1 if resonant magnetic perturbations are used during the pulse, 0
		otherwise"""


class _T_summary_kicks(SpTree):
	"""Vertical kicks"""

	occurrence  :_T_summary_constant_int_0d =  sp_property(units="Hz")
	""" Flag set to 1 if vertical kicks of the plasma position are used during the
		pulse, 0 otherwise"""


class _T_summary_global_quantities(SpTree):
	"""Various global quantities calculated from the fields solved in the transport
		equations and from the Derived Profiles"""

	ip  :_T_summary_dynamic_flt_1d_root =  sp_property(units="A",cocos_label_transformation="ip_like",cocos_transformation_expression=".sigma_ip_eff",cocos_leaf_name_aos_indices="summary.global_quantities.ip.value")
	""" Total plasma current (toroidal component). Positive sign means anti-clockwise
		when viewed from above."""

	current_non_inductive  :_T_summary_dynamic_flt_1d_root =  sp_property(units="A",cocos_label_transformation="ip_like",cocos_transformation_expression=".sigma_ip_eff",cocos_leaf_name_aos_indices="summary.global_quantities.current_non_inductive.value")
	""" Total non-inductive current (toroidal component). Positive sign means
		anti-clockwise when viewed from above."""

	current_bootstrap  :_T_summary_dynamic_flt_1d_root =  sp_property(units="A",cocos_label_transformation="ip_like",cocos_transformation_expression=".sigma_ip_eff",cocos_leaf_name_aos_indices="summary.global_quantities.current_bootstrap.value")
	""" Bootstrap current (toroidal component). Positive sign means anti-clockwise when
		viewed from above."""

	current_ohm  :_T_summary_dynamic_flt_1d_root =  sp_property(units="A",cocos_label_transformation="ip_like",cocos_transformation_expression=".sigma_ip_eff",cocos_leaf_name_aos_indices="summary.global_quantities.current_ohm")
	""" Ohmic current (toroidal component). Positive sign means anti-clockwise when
		viewed from above."""

	current_alignment  :_T_summary_dynamic_flt_1d_root =  sp_property(units="A")
	""" Figure of merit of the alignment of the current profile sources, defined in the
		following reference:
		http://iopscience.iop.org/article/10.1088/0029-5515/43/7/318"""

	v_loop  :_T_summary_dynamic_flt_1d_root =  sp_property(units="V",cocos_label_transformation="ip_like",cocos_transformation_expression=".sigma_ip_eff",cocos_leaf_name_aos_indices="summary.global_quantities.v_loop.value")
	""" LCFS loop voltage (positive value drives positive ohmic current that flows
		anti-clockwise when viewed from above)"""

	li  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Internal inductance. The li_3 definition is used, i.e. li_3 = 2/R0/mu0^2/Ip^2 *
		int(Bp^2 dV)."""

	li_mhd  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Internal inductance as determined by an equilibrium reconstruction code. Use
		this only when the li node above is used for another estimation method and there
		is a need to store a second value of li (determined by an equilibrium
		reconstruction code). The li_3 definition is used, i.e. li_3 = 2/R0/mu0^2/Ip^2 *
		int(Bp^2 dV)."""

	beta_tor  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Toroidal beta, defined as the volume-averaged total perpendicular pressure
		divided by (B0^2/(2*mu0)), i.e. beta_toroidal = 2 mu0 int(p dV) / V / B0^2"""

	beta_tor_mhd  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Toroidal beta, using the pressure determined by an equilibrium reconstruction
		code"""

	beta_tor_norm  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Normalised toroidal beta, defined as 100 * beta_tor * a[m] * B0 [T] / ip [MA]"""

	beta_tor_norm_mhd  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Normalised toroidal beta, using the pressure determined by an equilibrium
		reconstruction code"""

	beta_tor_thermal_norm  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Normalised toroidal beta from thermal pressure only, defined as 100 *
		beta_tor_thermal * a[m] * B0 [T] / ip [MA]"""

	beta_pol  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Poloidal beta. Defined as betap = 4 int(p dV) / [R_0 * mu_0 * Ip^2]"""

	beta_pol_mhd  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Poloidal beta estimated from the pressure determined by an equilibrium
		reconstruction code. Defined as betap = 4 int(p dV) / [R_0 * mu_0 * Ip^2]"""

	energy_diamagnetic  :_T_summary_dynamic_flt_1d_root =  sp_property(units="J")
	""" Plasma diamagnetic energy content = 3/2 * integral over the plasma volume of the
		total perpendicular pressure"""

	denergy_diamagnetic_dt  :_T_summary_dynamic_flt_1d_root =  sp_property(units="W")
	""" Time derivative of the diamagnetic plasma energy content"""

	energy_total  :_T_summary_dynamic_flt_1d_root =  sp_property(units="J")
	""" Plasma energy content = 3/2 * integral over the plasma volume of the total
		kinetic pressure"""

	energy_mhd  :_T_summary_dynamic_flt_1d_root =  sp_property(units="J")
	""" Plasma energy content = 3/2 * integral over the plasma volume of the total
		kinetic pressure (pressure determined by an equilibrium reconstruction code)"""

	energy_thermal  :_T_summary_dynamic_flt_1d_root =  sp_property(units="J")
	""" Thermal plasma energy content = 3/2 * integral over the plasma volume of the
		thermal pressure"""

	energy_ion_total_thermal  :_T_summary_dynamic_flt_1d_root =  sp_property(units="J")
	""" Thermal ion plasma energy content (sum over the ion species) = 3/2 * integral
		over the plasma volume of the thermal ion pressure"""

	energy_electrons_thermal  :_T_summary_dynamic_flt_1d_root =  sp_property(units="J")
	""" Thermal electron plasma energy content = 3/2 * integral over the plasma volume
		of the thermal electron pressure"""

	denergy_thermal_dt  :_T_summary_dynamic_flt_1d_root =  sp_property(units="W")
	""" Time derivative of the thermal plasma energy content"""

	energy_b_field_pol  :_T_summary_dynamic_flt_1d_root =  sp_property(units="J")
	""" Poloidal magnetic plasma energy content = 1/(2.mu0) * integral over the plasma
		volume of b_field_pol^2"""

	energy_fast_perpendicular  :_T_summary_dynamic_flt_1d_root =  sp_property(units="J")
	""" Fast particles perpendicular energy content = 3/2 * integral over the plasma
		volume of the fast perpendicular pressure"""

	energy_fast_parallel  :_T_summary_dynamic_flt_1d_root =  sp_property(units="J")
	""" Fast particles parallel energy content = 3/2 * integral over the plasma volume
		of the fast parallel pressure"""

	volume  :_T_summary_dynamic_flt_1d_root =  sp_property(units="m^3")
	""" Volume of the confined plasma"""

	h_mode  :_T_summary_dynamic_int_1d_root =  sp_property()
	""" H-mode flag: 0 when the plasma is in L-mode and 1 when in H-mode"""

	r0  :_T_summary_constant_flt_0d =  sp_property(units="m")
	""" Reference major radius where the vacuum toroidal magnetic field is given
		(usually a fixed position such as the middle of the vessel at the equatorial
		midplane)"""

	b0  :_T_summary_dynamic_flt_1d_root =  sp_property(units="T",cocos_label_transformation="b0_like",cocos_transformation_expression=".sigma_b0_eff",cocos_leaf_name_aos_indices="summary.global_quantities.b0.value")
	""" Vacuum toroidal field at R0. Positive sign means anti-clockwise when viewed from
		above. The product R0B0 must be consistent with the b_tor_vacuum_r field of the
		tf IDS."""

	fusion_gain  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Fusion gain : ratio of the power provided by fusion reactions to the auxiliary
		power needed to heat the plasma. Often noted as Q in the litterature."""

	h_98  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Energy confinement time enhancement factor over the IPB98(y,2) scaling"""

	tau_energy  :_T_summary_dynamic_flt_1d_root =  sp_property(units="s")
	""" Energy confinement time"""

	tau_helium  :_T_summary_dynamic_flt_1d_root =  sp_property(units="s")
	""" Helium confinement time"""

	tau_resistive  :_T_summary_dynamic_flt_1d_root =  sp_property(units="s")
	""" Current diffusion characteristic time"""

	tau_energy_98  :_T_summary_dynamic_flt_1d_root =  sp_property(units="s")
	""" Energy confinement time estimated from the IPB98(y,2) scaling"""

	ratio_tau_helium_fuel  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Ratio of Helium confinement time to fuel confinement time"""

	resistance  :_T_summary_dynamic_flt_1d_root =  sp_property(units="ohm")
	""" Plasma electric resistance"""

	q_95  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-",cocos_label_transformation="q_like",cocos_transformation_expression=".fact_q",cocos_leaf_name_aos_indices="summary.global_quantities.q_95.value")
	""" q at the 95% poloidal flux surface (IMAS uses COCOS=11: only positive when
		toroidal current and magnetic field are in same direction)"""

	power_ohm  :_T_summary_dynamic_flt_1d_root =  sp_property(units="W")
	""" Ohmic power"""

	power_steady  :_T_summary_dynamic_flt_1d_root =  sp_property(units="W")
	""" Total power coupled to the plasma minus dW/dt (correcting from transient energy
		content)"""

	power_radiated  :_T_summary_dynamic_flt_1d_root =  sp_property(units="W")
	""" Total radiated power"""

	power_radiated_inside_lcfs  :_T_summary_dynamic_flt_1d_root =  sp_property(units="W")
	""" Radiated power from the plasma inside the Last Closed Flux Surface"""

	power_radiated_outside_lcfs  :_T_summary_dynamic_flt_1d_root =  sp_property(units="W")
	""" Radiated power from the plasma outside the Last Closed Flux Surface"""

	power_line  :_T_summary_dynamic_flt_1d_root =  sp_property(units="W")
	""" Radiated power from line radiation"""

	power_bremsstrahlung  :_T_summary_dynamic_flt_1d_root =  sp_property(units="W")
	""" Radiated power from Bremsstrahlung"""

	power_synchrotron  :_T_summary_dynamic_flt_1d_root =  sp_property(units="W")
	""" Radiated power from synchrotron radiation"""

	power_loss  :_T_summary_dynamic_flt_1d_root =  sp_property(units="W")
	""" Power through separatrix"""

	greenwald_fraction  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Greenwald fraction =line_average/n_e/value divided by
		(global_quantities/ip/value *1e6 * pi * minor_radius^2)"""

	fusion_fluence  :_T_summary_dynamic_flt_1d_root =  sp_property(units="J")
	""" Fusion fluence : power provided by fusion reactions, integrated over time since
		the beginning of the pulse"""

	psi_external_average  :_T_summary_dynamic_flt_1d_root =  sp_property(units="Wb",introduced_after_version="3.36.0")
	""" Average (over the plasma poloidal cross section) plasma poloidal magnetic flux
		produced by all toroidal loops (active coils and passive loops) but the plasma,
		given by the following formula : int(psi_loops.j_tor.dS) / Ip"""


class _T_summary_neutron_reaction(SpTree):
	"""Neutron fluxes per reaction
	lifecycle_status: obsolescent
	lifecycle_version: 3.34.0"""

	total  :_T_summary_dynamic_flt_1d_root =  sp_property(units="Hz")
	""" Total neutron flux coming from this reaction"""

	thermal  :_T_summary_dynamic_flt_1d_root =  sp_property(units="Hz")
	""" Neutron flux coming from thermal plasma"""

	beam_thermal  :_T_summary_dynamic_flt_1d_root =  sp_property(units="Hz")
	""" Neutron flux coming from NBI beam - plasma reactions"""

	beam_beam  :_T_summary_dynamic_flt_1d_root =  sp_property(units="Hz")
	""" Neutron flux coming from NBI beam self reactions"""


class _T_summary_neutron_rates_reaction(SpTree):
	"""Neutron rates per reaction"""

	total  :_T_summary_dynamic_flt_1d_root =  sp_property(units="Hz")
	""" Total neutron rate coming from this reaction"""

	thermal  :_T_summary_dynamic_flt_1d_root =  sp_property(units="Hz")
	""" Neutron rate coming from thermal plasma"""

	beam_thermal  :_T_summary_dynamic_flt_1d_root =  sp_property(units="Hz")
	""" Neutron rate coming from NBI beam - plasma reactions"""

	beam_beam  :_T_summary_dynamic_flt_1d_root =  sp_property(units="Hz")
	""" Neutron rate coming from NBI beam self reactions"""


class _T_summary_runaways(SpTree):
	"""Runaway electrons"""

	particles  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Number of runaway electrons"""

	current  :_T_summary_dynamic_flt_1d_root =  sp_property(units="A")
	""" Parallel current driven by the runaway electrons"""


class _T_summary_h_cd_ec(SpTree):
	"""ECRH/CD related parameters"""

	frequency  :_T_summary_dynamic_flt_1d_root =  sp_property(units="Hz")
	""" ECRH frequency"""

	position  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Position of the maximum of the ECRH power deposition, in rho_tor_norm"""

	polarisation  :_T_summary_dynamic_int_1d_root =  sp_property()
	""" Polarisation of the ECRH waves (0 = O mode, 1 = X mode)"""

	harmonic  :_T_summary_dynamic_int_1d_root =  sp_property()
	""" Harmonic number of the absorbed ECRH waves"""

	angle_tor  :_T_summary_dynamic_flt_1d_root =  sp_property(units="rad",cocos_label_transformation="tor_angle_like",cocos_transformation_expression=".sigma_rphiz_eff",cocos_leaf_name_aos_indices="summary.heating_current_drive.ec{i}.angle_tor.value")
	""" Toroidal angle of ECRH at resonance"""

	angle_pol  :_T_summary_dynamic_flt_1d_root =  sp_property(units="rad")
	""" Poloidal angle of ECRH at resonance"""

	power  :_T_summary_dynamic_flt_1d_root =  sp_property(units="W")
	""" Electron cyclotron heating power coupled to the plasma from this launcher"""

	power_launched  :_T_summary_dynamic_flt_1d_root =  sp_property(units="W")
	""" Electron cyclotron heating power launched into the vacuum vessel from this
		launcher"""

	current  :_T_summary_dynamic_flt_1d_root =  sp_property(units="A",cocos_label_transformation="ip_like",cocos_transformation_expression=".sigma_ip_eff",cocos_leaf_name_aos_indices="summary.heating_current_drive.ec{i}.current.value")
	""" Parallel current driven by EC waves"""

	energy_fast  :_T_summary_dynamic_flt_1d_root =  sp_property(units="J")
	""" Fast particle energy content driven by EC waves"""


class _T_summary_h_cd_lh(SpTree):
	"""LHCD related parameters"""

	frequency  :_T_summary_dynamic_flt_1d_root =  sp_property(units="Hz")
	""" LH wave frequency"""

	position  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Position of the maximum of the LH power deposition, in rho_tor_norm"""

	n_parallel  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Main parallel refractive index of LH waves at launch"""

	power  :_T_summary_dynamic_flt_1d_root =  sp_property(units="W")
	""" LH heating power coupled to the plasma from this launcher"""

	power_launched  :_T_summary_dynamic_flt_1d_root =  sp_property(units="W")
	""" LH heating power launched into the vacuum vessel from this launcher"""

	current  :_T_summary_dynamic_flt_1d_root =  sp_property(units="A",cocos_label_transformation="ip_like",cocos_transformation_expression=".sigma_ip_eff",cocos_leaf_name_aos_indices="summary.heating_current_drive.lh{i}.current.value")
	""" Parallel current driven by LH waves"""

	energy_fast  :_T_summary_dynamic_flt_1d_root =  sp_property(units="J")
	""" Fast particle energy content driven by LH waves"""


class _T_summary_h_cd_ic(SpTree):
	"""ICRH related parameters"""

	frequency  :_T_summary_dynamic_flt_1d_root =  sp_property(units="Hz")
	""" ICRH frequency"""

	position  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Position of the maximum of the ICRH power deposition, in rho_tor_norm"""

	n_tor  :_T_summary_dynamic_int_1d_root =  sp_property()
	""" Main toroidal mode number of IC waves"""

	k_perpendicular  :_T_summary_dynamic_flt_1d_root =  sp_property(units="m^-1")
	""" Main perpendicular wave number of IC waves"""

	e_field_plus_minus_ratio  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Average E+/E- power ratio of IC waves"""

	harmonic  :_T_summary_dynamic_int_1d_root =  sp_property()
	""" Harmonic number of the absorbed ICRH waves"""

	phase  :_T_summary_dynamic_flt_1d_root =  sp_property(units="rad")
	""" Phase between straps"""

	power  :_T_summary_dynamic_flt_1d_root =  sp_property(units="W")
	""" IC heating power coupled to the plasma from this launcher"""

	power_launched  :_T_summary_dynamic_flt_1d_root =  sp_property(units="W")
	""" IC heating power launched into the vacuum vessel from this launcher"""

	current  :_T_summary_dynamic_flt_1d_root =  sp_property(units="A",cocos_label_transformation="ip_like",cocos_transformation_expression=".sigma_ip_eff",cocos_leaf_name_aos_indices="summary.heating_current_drive.ic{i}.current.value")
	""" Parallel current driven by IC waves"""

	energy_fast  :_T_summary_dynamic_flt_1d_root =  sp_property(units="J")
	""" Fast particle energy content driven by IC waves"""


class _T_summary_disruption(SpTree):
	"""Disruption related parameters"""

	time  :_T_summary_constant_flt_0d =  sp_property(units="s")
	""" Time of the disruption"""

	time_radiated_power_max  :_T_summary_constant_flt_0d =  sp_property(units="s")
	""" Time of maximum radiated power, relative to the time of the disruption"""

	time_half_ip  :_T_summary_constant_flt_0d =  sp_property(units="s")
	""" Time at which the plasma current has fallen to half of the initial current at
		the start of the disruption, relative to the time of the disruption"""

	vertical_displacement  :_T_summary_constant_int_0d =  sp_property(units="s")
	""" Direction of the plasma vertical displacement just before the disruption 1
		(upwards) / 0 (no displacement)/ -1 (downwards)"""

	mitigation_valve  :_T_summary_constant_int_0d =  sp_property()
	""" Flag indicating whether any disruption mitigation valve has been used (1) or
		none (0)"""


class _T_summary_wall(SpTree):
	"""Wall characteristics"""

	material  :_E_materials =  sp_property(doc_identifier="utilities/materials_identifier.xml")
	""" Wall material"""

	evaporation  :_T_summary_static_str_0d =  sp_property()
	""" Chemical formula of the evaporated material or gas used to cover the vaccum
		vessel wall. NONE for no evaporation."""


class _T_summary_limiter(SpTree):
	"""Limiter characteristics"""

	material  :_E_materials =  sp_property(doc_identifier="utilities/materials_identifier.xml")
	""" Limiter material"""


class _T_summary_local_quantities_r_z(SpTree):
	"""Set of local quantities, including an R,Z position"""

	position  :_T_summary_local_position_r_z =  sp_property()
	""" Radial position at which physics quantities are evaluated"""

	t_e  :_T_summary_dynamic_flt_1d_root =  sp_property(units="eV")
	""" Electron temperature"""

	t_i_average  :_T_summary_dynamic_flt_1d_root =  sp_property(units="eV")
	""" Ion temperature (average over ion species)"""

	n_e  :_T_summary_dynamic_flt_1d_root =  sp_property(units="m^-3")
	""" Electron density"""

	n_i  :_T_summary_species =  sp_property(units="m^-3")
	""" Ion density per species"""

	n_i_total  :_T_summary_dynamic_flt_1d_root =  sp_property(units="m^-3")
	""" Total ion density (sum over species)"""

	zeff  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Effective charge"""

	momentum_tor  :_T_summary_dynamic_flt_1d_root =  sp_property(units="kg.m.s^-1",cocos_label_transformation="tor_angle_like",cocos_transformation_expression=".sigma_rphiz_eff",cocos_leaf_name_aos_indices="IDSPATH.momentum_tor.value")
	""" Total plasma toroidal momentum, summed over ion species and electrons"""

	velocity_tor  :_T_summary_species_tor_angle =  sp_property(units="m.s^-1")
	""" Ion toroidal rotation velocity, per species"""

	q  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-",cocos_label_transformation="q_like",cocos_transformation_expression=".fact_q",cocos_leaf_name_aos_indices="IDSPATH.q.value")
	""" Safety factor (IMAS uses COCOS=11: only positive when toroidal current and
		magnetic field are in same direction)"""

	magnetic_shear  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Magnetic shear, defined as rho_tor/q . dq/drho_tor"""

	b_field  :_T_summary_dynamic_flt_1d_root =  sp_property(units="T",cocos_label_transformation="b0_like",cocos_transformation_expression=".sigma_b0_eff",cocos_leaf_name_aos_indices="IDSPATH.b_field.value")
	""" Magnetic field"""

	e_field_parallel  :_T_summary_dynamic_flt_1d_root =  sp_property(units="V.m^-1",cocos_label_transformation="ip_like",cocos_transformation_expression=".sigma_ip_eff",cocos_leaf_name_aos_indices="IDSPATH.e_field_parallel.value")
	""" Average on the magnetic surface of (e_field.b_field) / B0, where B0 is
		global_quantities/b0/value"""


class _T_summary_local_quantities_no_position_name(SpTree):
	"""Set of local quantities without radial position, for localisations outside the
		LCFS, with a name"""

	name  :_T_summary_static_str_0d =  sp_property()
	""" Name of the limiter or divertor plate. Standard names are : LI (resp. LO) for
		lower inner (resp. outer) plates; UI (resp. UO) for upper inner (resp. outer)
		plates."""

	t_e  :_T_summary_dynamic_flt_1d_root =  sp_property(units="eV")
	""" Electron temperature"""

	t_i_average  :_T_summary_dynamic_flt_1d_root =  sp_property(units="eV")
	""" Ion temperature (average over ion species)"""

	n_e  :_T_summary_dynamic_flt_1d_root =  sp_property(units="m^-3")
	""" Electron density"""

	n_i  :_T_summary_species =  sp_property(units="m^-3")
	""" Ion density per species"""

	n_i_total  :_T_summary_dynamic_flt_1d_root =  sp_property(units="m^-3")
	""" Total ion density (sum over species)"""

	zeff  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Effective charge"""

	flux_expansion  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-",url="divertors/flux_expansion.png")
	""" Magnetic flux expansion as defined by Stangeby : ratio between the poloidal
		field at the midplane separatrix and the poloidal field at the strike-point see
		formula attached, where u means upstream (midplane separatrix) and t means at
		divertor target (downstream)."""

	power_flux_peak  :_T_summary_dynamic_flt_1d_root =  sp_property(units="W.m^-2")
	""" Peak power flux on the divertor target or limiter surface"""


class _T_summary_local_quantities(SpTree):
	"""Set of local quantities"""

	position  :_T_summary_local_position =  sp_property()
	""" Radial position at which physics quantities are evaluated"""

	t_e  :_T_summary_dynamic_flt_1d_root =  sp_property(units="eV")
	""" Electron temperature"""

	t_i_average  :_T_summary_dynamic_flt_1d_root =  sp_property(units="eV")
	""" Ion temperature (average over ion species)"""

	n_e  :_T_summary_dynamic_flt_1d_root =  sp_property(units="m^-3")
	""" Electron density"""

	n_i  :_T_summary_species =  sp_property(units="m^-3")
	""" Ion density per species"""

	n_i_total  :_T_summary_dynamic_flt_1d_root =  sp_property(units="m^-3")
	""" Total ion density (sum over species)"""

	zeff  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Effective charge"""

	momentum_tor  :_T_summary_dynamic_flt_1d_root =  sp_property(units="kg.m.s^-1",cocos_label_transformation="tor_angle_like",cocos_transformation_expression=".sigma_rphiz_eff",cocos_leaf_name_aos_indices="IDSPATH.momentum_tor.value")
	""" Total plasma toroidal momentum, summed over ion species and electrons"""

	velocity_tor  :_T_summary_species_tor_angle =  sp_property(units="m.s^-1")
	""" Ion toroidal rotation velocity, per species"""

	q  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-",cocos_label_transformation="q_like",cocos_transformation_expression=".fact_q",cocos_leaf_name_aos_indices="IDSPATH.q.value")
	""" Safety factor"""

	magnetic_shear  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Magnetic shear, defined as rho_tor/q . dq/drho_tor"""

	e_field_parallel  :_T_summary_dynamic_flt_1d_root =  sp_property(units="V.m^-1",cocos_label_transformation="ip_like",cocos_transformation_expression=".sigma_ip_eff",cocos_leaf_name_aos_indices="IDSPATH.e_field_parallel.value")
	""" Average on the magnetic surface of (e_field.b_field) / B0, where B0 is
		global_quantities/b0/value"""


class _T_summary_pedestal_fit_stability(SpTree):
	"""MHD stability analysis of the pedestal (for a given fit of the profiles)"""

	alpha_experimental  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Experimental normalized pressure gradient reconstructed by an MHD stability code
		(with assumptions on the ion pressure). See definition in [Miller PoP 5
		(1998),973,Eq. 42]"""

	bootstrap_current_sauter  :_T_summary_pedestal_fit_stability_method =  sp_property()
	""" MHD calculations of the critical alpha parameter using the Sauter formula for
		the calculation of the bootstrap current, from Phys. Plasmas 6 (1999) 2834"""

	bootstrap_current_hager  :_T_summary_pedestal_fit_stability_method =  sp_property()
	""" MHD calculations of the critical alpha parameter using the Hager formula for the
		calculation of the bootstrap current, from Phys. Plasmas 23 (2016) 042503"""


class _T_summary_pedestal_fit_linear(SpTree):
	"""Quantities related to linear fit of pedestal profiles"""

	n_e  :_T_summary_pedestal_fit_linear_ne =  sp_property(units="m^-3")
	""" Electron density related quantities"""

	t_e  :_T_summary_pedestal_fit_linear_te =  sp_property(units="eV")
	""" Electron temperature related quantities"""

	pressure_electron  :_T_summary_pedestal_fit_ne =  sp_property(units="Pa")
	""" Electron pressure related quantities"""

	energy_thermal_pedestal_electron  :_T_summary_dynamic_flt_1d_root =  sp_property(units="J")
	""" Pedestal stored thermal energy for electrons"""

	energy_thermal_pedestal_ion  :_T_summary_dynamic_flt_1d_root =  sp_property(units="J")
	""" Pedestal stored thermal energy for ions"""

	volume_inside_pedestal  :_T_summary_dynamic_flt_1d_root =  sp_property(units="m^-3")
	""" Plasma volume enclosed between the magnetic axis and the top of the pedestal"""

	beta_pol_pedestal_top_electron_average  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Poloidal beta at pressure pedestal top for electrons using the flux surface
		average magnetic poloidal field"""

	beta_pol_pedestal_top_electron_lfs  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Poloidal beta at pressure pedestal top for electrons using the low field side
		magnetic poloidal field"""

	beta_pol_pedestal_top_electron_hfs  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Poloidal beta at pressure pedestal top for electrons using the high field side
		magnetic poloidal field"""

	nustar_pedestal_top_electron  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Normalised collisionality at pressure pedestal top for electrons"""

	rhostar_pedestal_top_electron_lfs  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Normalised Larmor radius at pressure pedestal top for electrons using the low
		field side magnetic field (important for spherical tokamaks)"""

	rhostar_pedestal_top_electron_hfs  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Normalised Larmor radius at pressure pedestal top for electrons using the high
		field side magnetic field (important for spherical tokamaks)"""

	rhostar_pedestal_top_electron_magnetic_axis  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Normalised Larmor radius at pressure pedestal top for electrons using the
		magnetic field on the magnetic axis (definition used in most tokamak literature)"""

	b_field_pol_pedestal_top_average  :_T_summary_dynamic_flt_1d_root =  sp_property(units="T")
	""" Poloidal field calculated at the position of the pressure pedestal top (as
		determined by the fit) and averaged over the flux surface"""

	b_field_pol_pedestal_top_hfs  :_T_summary_dynamic_flt_1d_root =  sp_property(units="T")
	""" Poloidal field calculated at the position of the pressure pedestal top (as
		determined by the fit) on the high field side"""

	b_field_pol_pedestal_top_lfs  :_T_summary_dynamic_flt_1d_root =  sp_property(units="T")
	""" Poloidal field calculated at the position of the pressure pedestal top (as
		determined by the fit) on the low field side"""

	b_field_pedestal_top_hfs  :_T_summary_dynamic_flt_1d_root =  sp_property(units="T")
	""" Total magnetic field calculated at the position of the pressure pedestal top (as
		determined by the fit) on the high field side"""

	b_field_pedestal_top_lfs  :_T_summary_dynamic_flt_1d_root =  sp_property(units="T")
	""" Total magnetic field calculated at the position of the pressure pedestal top (as
		determined by the fit) on the low field side"""

	b_field_tor_pedestal_top_hfs  :_T_summary_dynamic_flt_1d_root =  sp_property(units="T",cocos_label_transformation="b0_like",cocos_transformation_expression=".sigma_b0_eff",cocos_leaf_name_aos_indices="summary.pedestal_fits.linear.b_field_tor_pedestal_top_hfs.value")
	""" Toroidal field calculated at the position of the pressure pedestal top (as
		determined by the fit) on the high field side"""

	b_field_tor_pedestal_top_lfs  :_T_summary_dynamic_flt_1d_root =  sp_property(units="T",cocos_label_transformation="b0_like",cocos_transformation_expression=".sigma_b0_eff",cocos_leaf_name_aos_indices="summary.pedestal_fits.linear.b_field_tor_pedestal_top_lfs.value")
	""" Toroidal field calculated at the position of the pressure pedestal top (as
		determined by the fit) on the low field side"""

	coulomb_factor_pedestal_top  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Coulomb factor log(lambda) at the position of the pressure pedestal top (as
		determined by the fit)"""

	parameters  :array_type =  sp_property(type="constant",units="mixed",coordinate1="1...5")
	""" Parameters of the fit"""


class _T_summary_average_quantities(SpTree):
	"""Set of average quantities"""

	t_e  :_T_summary_dynamic_flt_1d_root =  sp_property(units="eV")
	""" Electron temperature"""

	t_i_average  :_T_summary_dynamic_flt_1d_root =  sp_property(units="eV")
	""" Ion temperature (average over ion species)"""

	n_e  :_T_summary_dynamic_flt_1d_root =  sp_property(units="m^-3")
	""" Electron density"""

	dn_e_dt  :_T_summary_dynamic_flt_1d_root =  sp_property(units="m^-3.s-1")
	""" Time derivative of the electron density"""

	n_i  :_T_summary_species =  sp_property(units="m^-3")
	""" Ion density per species"""

	n_i_total  :_T_summary_dynamic_flt_1d_root =  sp_property(units="m^-3")
	""" Total ion density (sum over species)"""

	zeff  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Effective charge"""

	meff_hydrogenic  :_T_summary_dynamic_flt_1d_root =  sp_property(units="amu")
	""" Effective mass of the hydrogenic species (MH. nH+MD.nD+MT.nT)/(nH+nD+nT)"""

	isotope_fraction_hydrogen  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Fraction of hydrogen density among the hydrogenic species (nH/(nH+nD+nT))"""


class _T_summary_neutron(SpTree):
	"""Description of neutron fluxes
	lifecycle_status: obsolescent
	lifecycle_version: 3.34.0"""

	total  :_T_summary_dynamic_flt_1d_root =  sp_property(units="Hz")
	""" Total neutron flux from all reactions"""

	thermal  :_T_summary_dynamic_flt_1d_root =  sp_property(units="Hz")
	""" Neutron flux from all plasma thermal reactions"""

	dd  :_T_summary_neutron_reaction =  sp_property(catalogue_name="suffix")
	""" Neutron fluxes from DD reactions"""

	dt  :_T_summary_neutron_reaction =  sp_property(catalogue_name="suffix")
	""" Neutron fluxes from DT reactions"""

	tt  :_T_summary_neutron_reaction =  sp_property(catalogue_name="suffix")
	""" Neutron fluxes from TT reactions"""


class _T_summary_neutron_rates(SpTree):
	"""Description of neutron rates"""

	total  :_T_summary_dynamic_flt_1d_root =  sp_property(units="Hz")
	""" Total neutron rate from all reactions"""

	thermal  :_T_summary_dynamic_flt_1d_root =  sp_property(units="Hz")
	""" Neutron rate from all plasma thermal reactions"""

	dd  :_T_summary_neutron_rates_reaction =  sp_property(catalogue_name="suffix")
	""" Neutron rates from DD reactions"""

	dt  :_T_summary_neutron_rates_reaction =  sp_property(catalogue_name="suffix")
	""" Neutron rates from DT reactions"""

	tt  :_T_summary_neutron_rates_reaction =  sp_property(catalogue_name="suffix")
	""" Neutron rates from TT reactions"""


class _T_summary_h_cd_nbi(SpTree):
	"""NBI unit"""

	species  :_T_summary_plasma_composition_species =  sp_property()
	""" Injected species"""

	power  :_T_summary_dynamic_flt_1d_root =  sp_property(units="W")
	""" NBI power coupled to the plasma by this unit (i.e. without shine-through and
		fast ion losses)"""

	power_launched  :_T_summary_dynamic_flt_1d_root =  sp_property(units="W")
	""" NBI power launched into the vacuum vessel from this unit"""

	current  :_T_summary_dynamic_flt_1d_root =  sp_property(units="A",cocos_label_transformation="ip_like",cocos_transformation_expression=".sigma_ip_eff",cocos_leaf_name_aos_indices="summary.heating_current_drive.nbi{i}.current.value")
	""" Parallel current driven by this NBI unit"""

	position  :_T_summary_rzphi0d_static =  sp_property()
	""" R, Z, Phi position of the NBI unit centre"""

	tangency_radius  :_T_summary_static_flt_0d =  sp_property(units="m")
	""" Tangency radius (major radius where the central line of a NBI unit is tangent to
		a circle around the torus)"""

	angle  :_T_summary_static_flt_0d =  sp_property(units="rad")
	""" Angle of inclination between a beamlet at the centre of the injection unit
		surface and the horizontal plane"""

	direction  :_T_summary_static_int_0d =  sp_property()
	""" Direction of the beam seen from above the torus: -1 = clockwise; 1 = counter
		clockwise"""

	energy  :_T_summary_dynamic_flt_1d_root =  sp_property(units="eV")
	""" Full energy of the injected species (acceleration of a single atom)"""

	beam_current_fraction  :_T_summary_dynamic_flt_2d_fraction_2 =  sp_property(units="-")
	""" Fractions of beam current distributed among the different energies, the first
		index corresponds to the fast neutrals energy (1:full, 2: half, 3: one third)"""

	beam_power_fraction  :_T_summary_dynamic_flt_2d_fraction_2 =  sp_property(units="-")
	""" Fractions of beam power distributed among the different energies, the first
		index corresponds to the fast neutrals energy (1:full, 2: half, 3: one third)"""


class _T_summary_pedestal_fit(SpTree):
	"""Quantities related to generic fit of pedestal profiles"""

	n_e  :_T_summary_pedestal_fit_ne =  sp_property(units="m^-3")
	""" Electron density related quantities"""

	t_e  :_T_summary_pedestal_fit_te =  sp_property(units="eV")
	""" Electron temperature related quantities"""

	pressure_electron  :_T_summary_pedestal_fit_ne =  sp_property(units="Pa")
	""" Electron pressure related quantities"""

	energy_thermal_pedestal_electron  :_T_summary_dynamic_flt_1d_root =  sp_property(units="J")
	""" Pedestal stored thermal energy for electrons"""

	energy_thermal_pedestal_ion  :_T_summary_dynamic_flt_1d_root =  sp_property(units="J")
	""" Pedestal stored thermal energy for ions"""

	volume_inside_pedestal  :_T_summary_dynamic_flt_1d_root =  sp_property(units="m^-3")
	""" Plasma volume enclosed between the magnetic axis and the top of the pedestal"""

	alpha_electron_pedestal_max  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Maximum value in the pedestal of the alpha parameter for electron pressure (see
		[Miller PoP 5 (1998),973,Eq. 42])"""

	alpha_electron_pedestal_max_position  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Position in normalised poloidal flux of the maximum value in the pedestal of the
		alpha parameter for electron pressure (see [Miller PoP 5 (1998),973,Eq. 42])"""

	beta_pol_pedestal_top_electron_average  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Poloidal beta at pressure pedestal top for electrons using the flux surface
		average magnetic poloidal field"""

	beta_pol_pedestal_top_electron_lfs  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Poloidal beta at pedestal top for electrons using the low field side magnetic
		poloidal field"""

	beta_pol_pedestal_top_electron_hfs  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Poloidal beta at pressure pedestal top for electrons using the high field side
		magnetic poloidal field"""

	nustar_pedestal_top_electron  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Normalised collisionality at pressure pedestal top for electrons"""

	rhostar_pedestal_top_electron_lfs  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Normalised Larmor radius at pressure pedestal top for electrons using the low
		field side magnetic field (important for spherical tokamaks)"""

	rhostar_pedestal_top_electron_hfs  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Normalised Larmor radius at pressure pedestal top for electrons using the high
		field side magnetic field (important for spherical tokamaks)"""

	rhostar_pedestal_top_electron_magnetic_axis  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Normalised Larmor radius at pressure pedestal top for electrons using the
		magnetic field on the magnetic axis (definition used in most tokamak
		litterature)"""

	b_field_pol_pedestal_top_average  :_T_summary_dynamic_flt_1d_root =  sp_property(units="T")
	""" Poloidal field calculated at the position of the pressure pedestal top (as
		determined by the fit) and averaged over the flux surface"""

	b_field_pol_pedestal_top_hfs  :_T_summary_dynamic_flt_1d_root =  sp_property(units="T")
	""" Poloidal field calculated at the position of the pressure pedestal top (as
		determined by the fit) on the high field side"""

	b_field_pol_pedestal_top_lfs  :_T_summary_dynamic_flt_1d_root =  sp_property(units="T")
	""" Poloidal field calculated at the position of the pressure pedestal top (as
		determined by the fit) on the low field side"""

	b_field_pedestal_top_hfs  :_T_summary_dynamic_flt_1d_root =  sp_property(units="T")
	""" Total magnetic field calculated at the position of the pressure pedestal top (as
		determined by the fit) on the high field side"""

	b_field_pedestal_top_lfs  :_T_summary_dynamic_flt_1d_root =  sp_property(units="T")
	""" Total magnetic field calculated at the position of the pressure pedestal top (as
		determined by the fit) on the low field side"""

	b_field_tor_pedestal_top_hfs  :_T_summary_dynamic_flt_1d_root =  sp_property(units="T",cocos_label_transformation="b0_like",cocos_transformation_expression=".sigma_b0_eff",cocos_leaf_name_aos_indices="summary.pedestal_fits.mtanh.b_field_tor_pedestal_top_hfs.value")
	""" Toroidal field calculated at the position of the pressure pedestal top (as
		determined by the fit) on the high field side"""

	b_field_tor_pedestal_top_lfs  :_T_summary_dynamic_flt_1d_root =  sp_property(units="T",cocos_label_transformation="b0_like",cocos_transformation_expression=".sigma_b0_eff",cocos_leaf_name_aos_indices="summary.pedestal_fits.mtanh.b_field_tor_pedestal_top_lfs.value")
	""" Toroidal field calculated at the position of the pressure pedestal top (as
		determined by the fit) on the low field side"""

	coulomb_factor_pedestal_top  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Coulomb factor log(lambda) at the position of the pressure pedestal top (as
		determined by the fit)"""

	stability  :_T_summary_pedestal_fit_stability =  sp_property()
	""" MHD stability analysis of the pedestal (for this fit of the profiles)"""

	parameters  :array_type =  sp_property(type="constant",units="mixed",coordinate1="1...5")
	""" Parameters of the fit"""


class _T_summary_local(SpTree):
	"""Set of locations"""

	magnetic_axis  :_T_summary_local_quantities_r_z =  sp_property(catalogue_name="suffix",cocos_alias="IDSPATH",cocos_replace="summary.local.magnetic_axis")
	""" Parameters at magnetic axis"""

	separatrix  :_T_summary_local_quantities =  sp_property(catalogue_name="suffix",cocos_alias="IDSPATH",cocos_replace="summary.local.separatrix")
	""" Parameters at separatrix (intersection of the separatrix and the outboard
		midplane)"""

	separatrix_average  :_T_summary_local_quantities =  sp_property(catalogue_name="suffix",cocos_alias="IDSPATH",cocos_replace="summary.local.separatrix_average",introduced_after_version="3.36.0")
	""" Flux surface averaged parameters at separatrix (flux-surface average over the
		entire core-SOL boundary separatrix)"""

	pedestal  :_T_summary_local_quantities =  sp_property(catalogue_name="suffix",cocos_alias="IDSPATH",cocos_replace="summary.local.pedestal")
	""" Parameters at pedestal top"""

	itb  :_T_summary_local_quantities =  sp_property(catalogue_name="suffix",cocos_alias="IDSPATH",cocos_replace="summary.local.itb")
	""" Parameters at internal transport barrier"""

	limiter  :_T_summary_local_quantities_no_position_name =  sp_property()
	""" Parameters at the limiter tangency point"""

	divertor_target  :AoS[_T_summary_local_quantities_no_position_name] =  sp_property(catalogue_name="suffix",coordinate1="1...N",introduced_after_version="3.34.0",change_nbc_version="3.35.0",change_nbc_description="aos_renamed",change_nbc_previous_name="divertor_plate")
	""" Parameters at a divertor target"""

	r_eff_norm_2_3  :_T_summary_local_quantities_stellerator =  sp_property()
	""" Parameters at r_eff_norm = 2/3, where r_eff_norm is the stellarator effective
		minor radius normalised to its value at the last closed flux surface"""


class _T_summary_fusion(SpTree):
	"""Fusion reactions"""

	power  :_T_summary_dynamic_flt_1d_root =  sp_property(units="W")
	""" Power coupled to the plasma by fusion reactions"""

	current  :_T_summary_dynamic_flt_1d_root =  sp_property(units="A",cocos_label_transformation="ip_like",cocos_transformation_expression=".sigma_ip_eff",cocos_leaf_name_aos_indices="summary.fusion.current.value")
	""" Parallel current driven by this fusion reactions"""

	neutron_rates  :_T_summary_neutron_rates =  sp_property(change_nbc_version="3.34.0",change_nbc_description="structure_renamed",change_nbc_previous_name="neutron_fluxes",introduced_after_version="3.33.0")
	""" Neutron rates from various reactions"""

	neutron_power_total  :_T_summary_dynamic_flt_1d_root =  sp_property(units="W")
	""" Total neutron power (from all reactions). Sum over each type of reaction (DD,
		DT, TT for thermal, beam-plasma, beam-beam, etc.) of the neutron production rate
		times the average neutron birth energy"""


class _T_summary_h_cd(SpTree):
	"""Heating and current drive related parameters"""

	ec  :AoS[_T_summary_h_cd_ec] =  sp_property(catalogue_name="suffix",coordinate1="1...N")
	""" Set of ECRH/ECCD launchers"""

	nbi  :AoS[_T_summary_h_cd_nbi] =  sp_property(catalogue_name="suffix",coordinate1="1...N")
	""" Set of NBI units"""

	ic  :AoS[_T_summary_h_cd_ic] =  sp_property(catalogue_name="suffix",coordinate1="1...N")
	""" Set of ICRH launchers"""

	lh  :AoS[_T_summary_h_cd_lh] =  sp_property(catalogue_name="suffix",coordinate1="1...N")
	""" Set of LHCD launchers"""

	power_ec  :_T_summary_dynamic_flt_1d_root =  sp_property(units="W")
	""" Total EC power coupled to the plasma"""

	power_launched_ec  :_T_summary_dynamic_flt_1d_root =  sp_property(units="W")
	""" Total EC power launched from EC launchers into the vacuum vessel"""

	power_nbi  :_T_summary_dynamic_flt_1d_root =  sp_property(units="W")
	""" Total NBI power coupled to the plasma"""

	power_launched_nbi  :_T_summary_dynamic_flt_1d_root =  sp_property(units="W")
	""" Total NBI power launched from neutral beam injectors into the vacuum vessel"""

	power_launched_nbi_co_injected_ratio  :_T_summary_dynamic_flt_1d_root =  sp_property(units="-")
	""" Ratio of co-injected beam launched power to total NBI launched power. Is set to
		1 for purely perpendicular injection"""

	power_ic  :_T_summary_dynamic_flt_1d_root =  sp_property(units="W")
	""" Total IC power coupled to the plasma"""

	power_launched_ic  :_T_summary_dynamic_flt_1d_root =  sp_property(units="W")
	""" Total IC power launched from IC antennas into the vacuum vessel"""

	power_lh  :_T_summary_dynamic_flt_1d_root =  sp_property(units="W")
	""" Total LH power coupled to the plasma"""

	power_launched_lh  :_T_summary_dynamic_flt_1d_root =  sp_property(units="W")
	""" Total LH power launched from LH antennas into the vacuum vessel"""

	power_additional  :_T_summary_dynamic_flt_1d_root =  sp_property(units="W")
	""" Total additional external power (NBI+EC+IC+LH, without ohmic) coupled to the
		plasma"""


class _T_summary_pedestal_fits(SpTree):
	"""Quantities derived from specific fits of pedestal profiles, typically used in
		the Pedestal Database"""

	mtanh  :_T_summary_pedestal_fit =  sp_property(catalogue_name="suffix")
	""" Quantities related to _mtanh_ fit"""

	linear  :_T_summary_pedestal_fit_linear =  sp_property(catalogue_name="suffix")
	""" Quantities related to linear fit"""


class _T_summary(IDS):
	"""Summary of physics quantities from a simulation or an experiment. Dynamic
		quantities are either taken at given time slices (indicated in the _time_
		vector) or time-averaged over an interval (in such case the _time_width_ of the
		interval is indicated and the _time_ vector represents the end of each time
		interval).
	lifecycle_status: active
	lifecycle_version: 3.22.0
	lifecycle_last_change: 3.38.0"""

	dd_version="v3_38_1_dirty"
	ids_name="summary"

	tag  :_T_entry_tag =  sp_property()
	""" Tag qualifying this data entry (or a list of data entries)"""

	configuration  :_T_summary_static_str_0d =  sp_property()
	""" Device configuration (the content may be device-specific)"""

	magnetic_shear_flag  :_T_summary_static_int_0d =  sp_property()
	""" Magnetic field shear indicator for stellarators: 0 for shearless stellarators
		(W7-A, W7-AS, W7-X); 1, otherwise. See [Stroth U. et al 1996 Nucl. Fusion 36
		1063]"""

	stationary_phase_flag  :_T_summary_dynamic_int_1d_root =  sp_property()
	""" This flag is set to one if the pulse is in a stationary phase from the point of
		the of the energy content (if the time derivative of the energy dW/dt can be
		neglected when calculating tau_E as W/(P_abs-dW/dt).)"""

	midplane  :_E_midplane_identifier =  sp_property(doc_identifier="utilities/midplane_identifier.xml",introduced_after_version="3.32.1")
	""" Choice of midplane definition (use the lowest index number if more than one
		value is relevant)"""

	global_quantities  :_T_summary_global_quantities =  sp_property()
	""" Various global quantities derived from the profiles"""

	local  :_T_summary_local =  sp_property()
	""" Plasma parameter values at different locations"""

	boundary  :_T_summary_boundary =  sp_property()
	""" Description of the plasma boundary"""

	pedestal_fits  :_T_summary_pedestal_fits =  sp_property(url="summary/pedestal_fits_definitions.pdf")
	""" Quantities derived from specific fits of pedestal profiles, typically used in
		the Pedestal Database."""

	line_average  :_T_summary_average_quantities =  sp_property()
	""" Line average plasma parameters"""

	volume_average  :_T_summary_average_quantities =  sp_property()
	""" Volume average plasma parameters"""

	disruption  :_T_summary_disruption =  sp_property()
	""" Disruption characteristics, if the pulse is terminated by a disruption"""

	elms  :_T_summary_elms =  sp_property()
	""" Edge Localized Modes related quantities"""

	fusion  :_T_summary_fusion =  sp_property()
	""" Fusion reactions"""

	gas_injection_rates  :_T_summary_gas_injection =  sp_property(units="electrons.s^-1")
	""" Gas injection rates in equivalent electrons.s^-1"""

	gas_injection_accumulated  :_T_summary_gas_injection_accumulated =  sp_property(units="electrons",introduced_after_version="3.36.0")
	""" Accumulated injected gas since the plasma breakdown in equivalent electrons"""

	gas_injection_prefill  :_T_summary_gas_injection_prefill =  sp_property(units="electrons",introduced_after_version="3.37.2")
	""" Accumulated injected gas during the prefill in equivalent electrons"""

	heating_current_drive  :_T_summary_h_cd =  sp_property()
	""" Heating and current drive parameters"""

	kicks  :_T_summary_kicks =  sp_property()
	""" Vertical kicks of the plasma position"""

	pellets  :_T_summary_pellets =  sp_property()
	""" Pellet related quantities"""

	rmps  :_T_summary_rmp =  sp_property()
	""" Resonant magnetic perturbations related quantities"""

	runaways  :_T_summary_runaways =  sp_property()
	""" Runaway electrons"""

	scrape_off_layer  :_T_summary_sol =  sp_property()
	""" Scrape-Off-Layer (SOL) characteristics"""

	wall  :_T_summary_wall =  sp_property()
	""" Wall characteristics"""

	limiter  :_T_summary_limiter =  sp_property()
	""" Limiter characteristics"""

	time_breakdown  :_T_summary_constant_flt_0d =  sp_property(units="s",introduced_after_version="3.36.0")
	""" Time of the plasma breakdown"""

	plasma_duration  :_T_summary_constant_flt_0d =  sp_property(units="s",introduced_after_version="3.36.0")
	""" Duration of existence of a confined plasma during the pulse"""

	time_width  :Expression  =  sp_property(type="dynamic",units="s",coordinate1="../time")
	""" In case the time-dependent quantities of this IDS are averaged over a time
		interval, this node is the width of this time interval (empty otherwise). By
		convention, the time interval starts at time-time_width and ends at time."""
