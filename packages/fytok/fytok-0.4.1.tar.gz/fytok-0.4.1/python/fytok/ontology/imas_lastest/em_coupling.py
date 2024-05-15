"""
  This module containes the _FyTok_ wrapper of IMAS/dd/em_coupling
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    

class _T_em_coupling(IDS):
	"""Description of the axisymmetric mutual electromagnetics; does not include
		non-axisymmetric coil systems; the convention is Quantity_Sensor_Source
	lifecycle_status: alpha
	lifecycle_version: 3.0.0
	lifecycle_last_change: 3.0.0"""

	dd_version="v3_38_1_dirty"
	ids_name="em_coupling"

	mutual_active_active  :array_type =  sp_property(type="static",units="H",coordinate1="../active_coils",coordinate2="../active_coils")
	""" Mutual inductance coupling from active coils to active coils"""

	mutual_passive_active  :array_type =  sp_property(Type="static",units="H",coordinate1="../passive_loops",coordinate2="../active_coils")
	""" Mutual inductance coupling from active coils to passive loops"""

	mutual_loops_active  :array_type =  sp_property(type="static",units="H",coordinate1="../flux_loops",coordinate2="../active_coils")
	""" Mutual inductance coupling from active coils to poloidal flux loops"""

	field_probes_active  :array_type =  sp_property(type="static",units="T/A",coordinate1="../poloidal_probes",coordinate2="../active_coils")
	""" Poloidal field coupling from active coils to poloidal field probes"""

	mutual_passive_passive  :array_type =  sp_property(type="static",units="H",coordinate1="../passive_loops",coordinate2="../passive_loops")
	""" Mutual inductance coupling from passive loops to passive loops"""

	mutual_loops_passive  :array_type =  sp_property(type="static",units="H",coordinate1="../flux_loops",coordinate2="../passive_loops")
	""" Mutual inductance coupling from passive loops to poloidal flux loops"""

	field_probes_passive  :array_type =  sp_property(type="static",units="T/A",coordinate1="../poloidal_probes",coordinate2="../passive_loops")
	""" Poloidal field coupling from passive loops to poloidal field probes"""

	mutual_grid_grid  :array_type =  sp_property(type="static",units="H",coordinate1="../grid_points",coordinate2="../grid_points")
	""" Mutual inductance from equilibrium grid to itself"""

	mutual_grid_active  :array_type =  sp_property(type="static",units="H",coordinate1="../grid_points",coordinate2="../active_coils")
	""" Mutual inductance coupling from active coils to equilibrium grid"""

	mutual_grid_passive  :array_type =  sp_property(type="static",units="H",coordinate1="../grid_points",coordinate2="../passive_loops")
	""" Mutual inductance coupling from passive loops to equilibrium grid"""

	field_probes_grid  :array_type =  sp_property(type="static",units="T/A",coordinate1="../poloidal_probes",coordinate2="../grid_points")
	""" Poloidal field coupling from equilibrium grid to poloidal field probes"""

	mutual_loops_grid  :array_type =  sp_property(type="static",units="H",coordinate1="../flux_loops",coordinate2="../grid_points")
	""" Mutual inductance from equilibrium grid to poloidal flux loops"""

	active_coils  :List[str] =  sp_property(type="static",coordinate1="IDS:pf_active/coil")
	""" List of the names of the active PF+CS coils"""

	passive_loops  :List[str] =  sp_property(type="static",coordinate1="IDS:pf_passive/loop")
	""" List of the names of the passive loops"""

	poloidal_probes  :List[str] =  sp_property(type="static",coordinate1="IDS:magnetics/bpol_probe")
	""" List of the names of poloidal field probes"""

	flux_loops  :List[str] =  sp_property(type="static",coordinate1="IDS:magnetics/flux_loop")
	""" List of the names of the axisymmetric flux loops"""

	grid_points  :List[str] =  sp_property(type="constant",coordinate1="1...N")
	""" List of the names of the plasma region grid points"""
