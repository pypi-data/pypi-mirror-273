"""
  This module containes the _FyTok_ wrapper of IMAS/dd/transport_solver_numerics
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_identifier_dynamic_aos3,_T_core_radial_grid,_T_generic_grid_dynamic,_T_signal_flt_1d,_T_identifier,_T_b_tor_vacuum_1

class _E_transport_solver_numerics_bc_type(IntFlag):
	"""List of boundary condition types for 1D transport solvers	xpath: transport_solver_numerics/solver_1d/equation/boundary_condition/type	"""
  
	not_solved = 0
	"""Equation is not solved"""
  
	value = 1
	"""Boundary condition is the value of the equations primary quantity"""
  
	derivative_or_ip = 2
	"""Boundary condition is the radial derivative of the equations primary quantity,
		or the plasma current for the current diffusion equation"""
  
	e_folding_length_or_vloop = 3
	"""Boundary condition is the e-folding length of the equations primary quantity, or
		the loop voltage for the current diffusion equation"""
  
	flux = 4
	"""Boundary condition is the flux of the equations primary quantity"""
  
	combination = 5
	"""Boundary condition is a linear combination of radial derivative and value of the
		flux of the equations primary quantity, in the form a1.y-prime + a2.y = a3"""
  

class _E_transport_solver_numerics_computation_mode(IntFlag):
	"""List computation modes of transport equations	xpath: transport_solver_numerics/solver_1d/equation/computation_mode	"""
  
	static = 0
	"""Equation is not solved, no profile evolution"""
  
	interpretative = 1
	"""Equation is not solved, profile is evolved by interpolating from input objects"""
  
	predictive = 2
	"""Equation is solved, profile evolves"""
  

class _T_numerics_profiles_1d_derivatives_charge_state_d(SpTree):
	"""Quantities related to a given charge state, derivatives with respect to a given
		quantity"""

	temperature  :Expression  =  sp_property(coordinate1="../../../../grid/rho_tor_norm",units="eV",type="dynamic")
	""" Temperature"""

	density  :Expression  =  sp_property(coordinate1="../../../../grid/rho_tor_norm",units="m^-3",type="dynamic")
	""" Density (thermal+non-thermal)"""

	density_fast  :Expression  =  sp_property(coordinate1="../../../../grid/rho_tor_norm",units="m^-3",type="dynamic")
	""" Density of fast (non-thermal) particles"""

	pressure  :Expression  =  sp_property(coordinate1="../../../../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Pressure"""

	pressure_fast_perpendicular  :Expression  =  sp_property(coordinate1="../../../../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Fast (non-thermal) perpendicular pressure"""

	pressure_fast_parallel  :Expression  =  sp_property(coordinate1="../../../../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Fast (non-thermal) parallel pressure"""

	velocity_tor  :Expression  =  sp_property(coordinate1="../../../../grid/rho_tor_norm",units="m.s^-1",type="dynamic")
	""" Toroidal velocity"""

	velocity_pol  :Expression  =  sp_property(coordinate1="../../../../grid/rho_tor_norm",units="m.s^-1",type="dynamic")
	""" Poloidal velocity"""


class _T_numerics_profiles_1d_derivatives_ion_d(SpTree):
	"""Quantities related to an ion species, derivatives with respect to a given
		quantity"""

	temperature  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="eV",type="dynamic")
	""" Temperature (average over charge states when multiple charge states are
		considered)"""

	density  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="m^-3",type="dynamic")
	""" Density (thermal+non-thermal) (sum over charge states when multiple charge
		states are considered)"""

	density_fast  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="m^-3",type="dynamic")
	""" Density of fast (non-thermal) particles (sum over charge states when multiple
		charge states are considered)"""

	pressure  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Pressure (average over charge states when multiple charge states are considered)"""

	pressure_fast_perpendicular  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Fast (non-thermal) perpendicular pressure (average over charge states when
		multiple charge states are considered)"""

	pressure_fast_parallel  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Fast (non-thermal) parallel pressure (average over charge states when multiple
		charge states are considered)"""

	velocity_tor  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="m.s^-1",type="dynamic")
	""" Toroidal velocity (average over charge states when multiple charge states are
		considered)"""

	velocity_pol  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="m.s^-1",type="dynamic")
	""" Poloidal velocity (average over charge states when multiple charge states are
		considered)"""


class _T_numerics_profiles_1d_current_derivatives(SpTree):
	"""Derivatives of the current equation primary quantity"""

	d_dt  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="mixed",type="dynamic")
	""" Time derivative"""

	d_drho_tor_norm  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="mixed",type="dynamic")
	""" Derivative with respect to the normalised toroidal flux"""

	d2_drho_tor_norm2  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="mixed",type="dynamic")
	""" Second derivative with respect to the normalised toroidal flux"""

	d_drho_tor  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="mixed",type="dynamic")
	""" Derivative with respect to the toroidal flux"""

	d2_drho_tor2  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="mixed",type="dynamic")
	""" Second derivative with respect to the toroidal flux"""

	d_dt_cphi  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",type="dynamic",units="mixed")
	""" Derivative with respect to time, at constant toroidal flux"""

	d_dt_crho_tor_norm  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",type="dynamic",units="mixed")
	""" Derivative with respect to time, at constant normalised toroidal flux coordinate"""


class _T_numerics_profiles_1d_derivatives_depth5(SpTree):
	"""Derivatives of a transport equation primary quantity, depth 5 with respect to
		the 1D grid"""

	d_dt  :Expression  =  sp_property(coordinate1="../../../../../grid/rho_tor_norm",units="mixed",type="dynamic")
	""" Time derivative"""

	d_drho_tor_norm  :Expression  =  sp_property(coordinate1="../../../../../grid/rho_tor_norm",units="mixed",type="dynamic")
	""" Derivative with respect to the normalised toroidal flux"""

	d2_drho_tor_norm2  :Expression  =  sp_property(coordinate1="../../../../../grid/rho_tor_norm",units="mixed",type="dynamic")
	""" Second derivative with respect to the normalised toroidal flux"""

	d_drho_tor  :Expression  =  sp_property(coordinate1="../../../../../grid/rho_tor_norm",units="mixed",type="dynamic")
	""" Derivative with respect to the toroidal flux"""

	d2_drho_tor2  :Expression  =  sp_property(coordinate1="../../../../../grid/rho_tor_norm",units="mixed",type="dynamic")
	""" Second derivative with respect to the toroidal flux"""


class _T_numerics_profiles_1d_derivatives_depth4(SpTree):
	"""Derivatives of a transport equation primary quantity, depth 4 with respect to
		the 1D grid"""

	d_dt  :Expression  =  sp_property(coordinate1="../../../../grid/rho_tor_norm",units="mixed",type="dynamic")
	""" Time derivative"""

	d_drho_tor_norm  :Expression  =  sp_property(coordinate1="../../../../grid/rho_tor_norm",units="mixed",type="dynamic")
	""" Derivative with respect to the normalised toroidal flux"""

	d2_drho_tor_norm2  :Expression  =  sp_property(coordinate1="../../../../grid/rho_tor_norm",units="mixed",type="dynamic")
	""" Second derivative with respect to the normalised toroidal flux"""

	d_drho_tor  :Expression  =  sp_property(coordinate1="../../../../grid/rho_tor_norm",units="mixed",type="dynamic")
	""" Derivative with respect to the toroidal flux"""

	d2_drho_tor2  :Expression  =  sp_property(coordinate1="../../../../grid/rho_tor_norm",units="mixed",type="dynamic")
	""" Second derivative with respect to the toroidal flux"""


class _T_numerics_profiles_1d_derivatives_depth3(SpTree):
	"""Derivatives of a transport equation primary quantity, depth 3 with respect to
		the 1D grid"""

	d_dt  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="mixed",type="dynamic")
	""" Time derivative"""

	d_drho_tor_norm  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="mixed",type="dynamic")
	""" Derivative with respect to the normalised toroidal flux"""

	d2_drho_tor_norm2  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="mixed",type="dynamic")
	""" Second derivative with respect to the normalised toroidal flux"""

	d_drho_tor  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="mixed",type="dynamic")
	""" Derivative with respect to the toroidal flux"""

	d2_drho_tor2  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="mixed",type="dynamic")
	""" Second derivative with respect to the toroidal flux"""


class _T_numerics_profiles_1d_derivatives_electrons_d(SpTree):
	"""Quantities related to electrons, derivatives with respect to a given quantity"""

	temperature  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="eV",type="dynamic")
	""" Temperature"""

	density  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="m^-3",type="dynamic")
	""" Density (thermal+non-thermal)"""

	density_fast  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="m^-3",type="dynamic")
	""" Density of fast (non-thermal) particles"""

	pressure  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Pressure"""

	pressure_fast_perpendicular  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Fast (non-thermal) perpendicular pressure"""

	pressure_fast_parallel  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Fast (non-thermal) parallel pressure"""

	velocity_tor  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="m.s^-1",type="dynamic")
	""" Toroidal velocity"""

	velocity_pol  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="m.s^-1",type="dynamic")
	""" Poloidal velocity"""


class _T_numerics_profiles_1d_derivatives_total_ions(SpTree):
	"""Quantities related to total ion quantities, derivatives with respect to a given
		quantity"""

	n_i_total_over_n_e  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="-",type="dynamic")
	""" Ratio of total ion density (sum over species and charge states) over electron
		density. (thermal+non-thermal)"""

	pressure_ion_total  :Expression  =  sp_property(coordinate1="../../grid/rho_tor_norm",units="Pa",type="dynamic")
	""" Total thermal ion pressure"""


class _T_numerics_convergence_equations_single_delta(SpTree):
	"""Delta between two iterations of the solvers on a given transport equation"""

	value  :float =  sp_property(type="dynamic",units="-")
	""" Value of the relative deviation"""

	expression  :str =  sp_property(type="dynamic")
	""" Expression used by the solver to calculate the relative deviation"""


class _T_numerics_solver_1d_equation_control_float(SpTree):
	"""FLT0D for control parameters"""

	value  :float =  sp_property(units="mixed",type="dynamic")
	""" Value of the control parameter"""


class _T_numerics_solver_1d_equation_control_int(SpTree):
	"""INT0D for control parameters"""

	value  :int =  sp_property(type="dynamic")
	""" Value of the control parameter"""


class _T_numerics_solver_1d_equation_coefficient(SpTree):
	"""Coefficient for transport equation"""

	profile  :Expression  =  sp_property(units="mixed",type="dynamic",coordinate1="../../../grid/rho_tor_norm")
	""" Radial profile of the numerical coefficient"""


class _T_numerics_profiles_1d_derivatives_charge_state(SpTree):
	"""Quantities related to a given charge state"""

	z_min  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Minimum Z of the charge state bundle"""

	z_max  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Maximum Z of the charge state bundle"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying charge state (e.g. C+, C+2 , C+3, C+4, C+5, C+6, ...)"""

	vibrational_level  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Vibrational level (can be bundled)"""

	vibrational_mode  :str =  sp_property(type="dynamic")
	""" Vibrational mode of this state, e.g. _A_g_. Need to define, or adopt a standard
		nomenclature."""

	is_neutral  :int =  sp_property(type="dynamic")
	""" Flag specifying if this state corresponds to a neutral (1) or not (0)"""

	neutral_type  :_T_identifier_dynamic_aos3 =  sp_property()
	""" Neutral type (if the considered state is a neutral), in terms of energy. ID =1:
		cold; 2: thermal; 3: fast; 4: NBI"""

	electron_configuration  :str =  sp_property(type="dynamic")
	""" Configuration of atomic orbitals of this state, e.g. 1s2-2s1"""

	d_drho_tor_norm  :_T_numerics_profiles_1d_derivatives_charge_state_d =  sp_property()
	""" Derivatives with respect to the normalised toroidal flux"""

	d2_drho_tor_norm2  :_T_numerics_profiles_1d_derivatives_charge_state_d =  sp_property()
	""" Second derivatives with respect to the normalised toroidal flux"""

	d_dt  :_T_numerics_profiles_1d_derivatives_charge_state_d =  sp_property()
	""" Derivatives with respect to time"""


class _T_numerics_profiles_1d_derivatives_electrons(SpTree):
	"""Quantities related to electrons"""

	d_drho_tor_norm  :_T_numerics_profiles_1d_derivatives_electrons_d =  sp_property()
	""" Derivatives with respect to the normalised toroidal flux"""

	d2_drho_tor_norm2  :_T_numerics_profiles_1d_derivatives_electrons_d =  sp_property()
	""" Second derivatives with respect to the normalised toroidal flux"""

	d_dt  :_T_numerics_profiles_1d_derivatives_electrons_d =  sp_property()
	""" Derivatives with respect to time"""


class _T_numerics_restart(TimeSlice):
	"""Description of a restart file"""

	names  :List[str] =  sp_property(coordinate1="1...N",type="dynamic")
	""" Names of the restart files"""

	descriptions  :List[str] =  sp_property(coordinate1="../names",type="dynamic")
	""" Descriptions of the restart files"""


class _T_numerics_bc_1d_current_new(SpTree):
	"""Boundary conditions for the current diffusion equation"""

	identifier  :_T_identifier_dynamic_aos3 =  sp_property(coordinate1="../../../grid/rho_tor_norm",units="eV",type="dynamic")
	""" Identifier of the boundary condition type. ID = 1: poloidal flux; 2: ip; 3: loop
		voltage; 4: undefined; 5: generic boundary condition y expressed as a1y'+a2y=a3.
		6: equation not solved;"""

	value  :array_type =  sp_property(units="mixed",type="dynamic",coordinate1="1...3")
	""" Value of the boundary condition. For ID = 1 to 3, only the first position in the
		vector is used. For ID = 5, all three positions are used, meaning respectively
		a1, a2, a3."""

	rho_tor_norm  :float =  sp_property(units="-",type="dynamic")
	""" Position, in normalised toroidal flux, at which the boundary condition is
		imposed. Outside this position, the value of the data are considered to be
		prescribed."""

	rho_tor  :float =  sp_property(units="m",type="dynamic")
	""" Position, in toroidal flux, at which the boundary condition is imposed. Outside
		this position, the value of the data are considered to be prescribed."""


class _T_numerics_bc_1d_current(SpTree):
	"""Boundary conditions for the current diffusion equation"""

	identifier  :_T_identifier_dynamic_aos3 =  sp_property(units="eV")
	""" Identifier of the boundary condition type. ID = 1: poloidal flux; 2: ip; 3: loop
		voltage; 4: undefined; 5: generic boundary condition y expressed as a1y'+a2y=a3.
		6: equation not solved;"""

	value  :array_type =  sp_property(units="mixed",type="dynamic",coordinate1="1...3")
	""" Value of the boundary condition. For ID = 1 to 3, only the first position in the
		vector is used. For ID = 5, all three positions are used, meaning respectively
		a1, a2, a3."""

	rho_tor_norm  :float =  sp_property(units="-",type="dynamic")
	""" Position, in normalised toroidal flux, at which the boundary condition is
		imposed. Outside this position, the value of the data are considered to be
		prescribed."""


class _T_numerics_bc_ggd_current(SpTree):
	"""Boundary conditions for the current diffusion equation"""

	identifier  :_T_identifier_dynamic_aos3 =  sp_property()
	""" Identifier of the boundary condition type. List of options TBD."""

	grid_index  :int =  sp_property(type="dynamic")
	""" Index of the grid used to represent this quantity"""

	grid_subset_index  :int =  sp_property(type="dynamic")
	""" Index of the grid subset the data is provided on"""

	values  :array_type =  sp_property(type="dynamic",coordinate1="1...N",coordinate2="1...N",units="mixed")
	""" List of vector components, one list per element in the grid subset. First
		dimenstion: element index. Second dimension: vector component index (for ID = 1
		to 3, only the first position in the vector is used. For ID = 5, all three
		positions are used, meaning respectively a1, a2, a3)"""


class _T_numerics_bc_ggd_bc(SpTree):
	"""Boundary conditions for a given transport equation"""

	identifier  :_T_identifier_dynamic_aos3 =  sp_property(units="eV")
	""" Identifier of the boundary condition type. List of options TBD."""

	grid_index  :int =  sp_property(type="dynamic")
	""" Index of the grid used to represent this quantity"""

	grid_subset_index  :int =  sp_property(type="dynamic")
	""" Index of the grid subset the data is provided on"""

	values  :array_type =  sp_property(type="dynamic",coordinate1="1...N",coordinate2="1...N",units="mixed")
	""" List of vector components, one list per element in the grid subset. First
		dimenstion: element index. Second dimension: vector component index (for ID = 1
		to 3, only the first position in the vector is used. For ID = 5, all three
		positions are used, meaning respectively a1, a2, a3)"""


class _T_numerics_bc_1d_bc(SpTree):
	"""Boundary conditions for a given transport equation"""

	identifier  :_T_identifier_dynamic_aos3 =  sp_property(units="eV")
	""" Identifier of the boundary condition type. ID = 1: value of the field y; 2:
		radial derivative of the field (-dy/drho_tor); 3: scale length of the field
		y/(-dy/drho_tor); 4: flux; 5: generic boundary condition y expressed as
		a1y'+a2y=a3. 6: equation not solved;"""

	value  :array_type =  sp_property(units="mixed",type="dynamic",coordinate1="1...3")
	""" Value of the boundary condition. For ID = 1 to 4, only the first position in the
		vector is used. For ID = 5, all three positions are used, meaning respectively
		a1, a2, a3."""

	rho_tor_norm  :float =  sp_property(units="-",type="dynamic")
	""" Position, in normalised toroidal flux, at which the boundary condition is
		imposed. Outside this position, the value of the data are considered to be
		prescribed."""


class _T_numerics_convergence_equations_single(SpTree):
	"""Convergence details of a given transport equation"""

	iterations_n  :int =  sp_property(type="dynamic")
	""" Number of iterations carried out in the convergence loop"""

	delta_relative  :_T_numerics_convergence_equations_single_delta =  sp_property()
	""" Relative deviation on the primary quantity of the transport equation between the
		present and the previous iteration of the solver"""


class _T_numerics_solver_1d_equation_control_parameters(SpTree):
	"""Solver-specific input or output quantities"""

	integer0d  :AoS[_T_numerics_solver_1d_equation_control_int] =  sp_property(coordinate1="1...N")
	""" Set of integer type scalar control parameters"""

	real0d  :AoS[_T_numerics_solver_1d_equation_control_float] =  sp_property(coordinate1="1...N")
	""" Set of real type scalar control parameters"""


class _T_numerics_solver_1d_equation_primary(SpTree):
	"""Profile and derivatives a the primary quantity for a 1D transport equation"""

	identifier  :_T_identifier_dynamic_aos3 =  sp_property()
	""" Identifier of the primary quantity of the transport equation. The description
		node contains the path to the quantity in the physics IDS (example:
		core_profiles/profiles_1d/ion(1)/density)"""

	ion_index  :int =  sp_property(type="dynamic")
	""" If the primary quantity is related to a ion species, index of the corresponding
		species in the core_profiles/profiles_1d/ion array"""

	neutral_index  :int =  sp_property(type="dynamic")
	""" If the primary quantity is related to a neutral species, index of the
		corresponding species in the core_profiles/profiles_1d/neutral array"""

	state_index  :int =  sp_property(type="dynamic")
	""" If the primary quantity is related to a particular state (of an ion or a neutral
		species), index of the corresponding state in the core_profiles/profiles_1d/ion
		(or neutral)/state array"""

	profile  :Expression  =  sp_property(units="mixed",type="dynamic",coordinate1="../../../grid/rho_tor_norm")
	""" Profile of the primary quantity"""

	d_dr  :Expression  =  sp_property(units="mixed",type="dynamic",coordinate1="../../../grid/rho_tor_norm")
	""" Radial derivative with respect to the primary coordinate"""

	d2_dr2  :Expression  =  sp_property(units="mixed",type="dynamic",coordinate1="../../../grid/rho_tor_norm")
	""" Second order radial derivative with respect to the primary coordinate"""

	d_dt  :Expression  =  sp_property(units="mixed",type="dynamic",coordinate1="../../../grid/rho_tor_norm")
	""" Time derivative"""

	d_dt_cphi  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",type="dynamic",units="mixed")
	""" Derivative with respect to time, at constant toroidal flux (for current
		diffusion equation)"""

	d_dt_cr  :Expression  =  sp_property(coordinate1="../../../grid/rho_tor_norm",type="dynamic",units="mixed")
	""" Derivative with respect to time, at constant primary coordinate coordinate (for
		current diffusion equation)"""


class _T_numerics_solver_1d_equation_bc(SpTree):
	"""Boundary conditions for a 1D transport equation"""

	type  :_E_transport_solver_numerics_bc_type =  sp_property(doc_identifier="transport_solver_numerics/transport_solver_numerics_bc_type.xml")
	""" Boundary condition type"""

	value  :array_type =  sp_property(units="mixed",type="dynamic",coordinate1="1...3")
	""" Value of the boundary condition. For type/index = 1 to 3, only the first
		position in the vector is used. For type/index = 5, all three positions are
		used, meaning respectively a1, a2, a3."""

	position  :float =  sp_property(units="mixed",type="dynamic")
	""" Position, in terms of the primary coordinate, at which the boundary condition is
		imposed. Outside this position, the value of the data are considered to be
		prescribed (in case of a single boundary condition)."""


class _T_numerics_profiles_1d_derivatives_ion(SpTree):
	"""Quantities related to an ion species"""

	a  :float =  sp_property(units="Atomic Mass Unit",type="dynamic")
	""" Mass of atom"""

	z_ion  :float =  sp_property(type="dynamic",units="Elementary Charge Unit")
	""" Ion charge (of the dominant ionisation state; lumped ions are allowed)"""

	z_n  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Nuclear charge"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying ion (e.g. H+, D+, T+, He+2, C+, ...)"""

	d_drho_tor_norm  :_T_numerics_profiles_1d_derivatives_ion_d =  sp_property()
	""" Derivatives with respect to the normalised toroidal flux"""

	d2_drho_tor_norm2  :_T_numerics_profiles_1d_derivatives_ion_d =  sp_property()
	""" Second derivatives with respect to the normalised toroidal flux"""

	d_dt  :_T_numerics_profiles_1d_derivatives_ion_d =  sp_property()
	""" Derivatives with respect to time"""

	multiple_states_flag  :int =  sp_property(type="dynamic")
	""" Multiple state calculation flag : 0-Only one state is considered; 1-Multiple
		states are considered and are described in the state structure"""

	state  :AoS[_T_numerics_profiles_1d_derivatives_charge_state] =  sp_property(coordinate1="1...N_charge_states")
	""" Quantities related to the different states of the species (ionisation, energy,
		excitation, ...)"""


class _T_numerics_bc_1d_electrons(SpTree):
	"""Boundary conditions for the electron related transport equations"""

	particles  :_T_numerics_bc_1d_bc =  sp_property(units="m^-3.s^-1")
	""" Boundary condition for the electron density equation (density if ID = 1)"""

	energy  :_T_numerics_bc_1d_bc =  sp_property(units="W.m^-3")
	""" Boundary condition for the electron energy equation (temperature if ID = 1)"""


class _T_numerics_bc_ggd_electrons(SpTree):
	"""Boundary conditions for the electron related transport equations"""

	particles  :AoS[_T_numerics_bc_ggd_bc] =  sp_property(coordinate1="1...N",units="m^-3.s^-1")
	""" Boundary condition for the electron density equation (density if ID = 1), on
		various grid subsets"""

	energy  :AoS[_T_numerics_bc_ggd_bc] =  sp_property(coordinate1="1...N",units="W.m^-3")
	""" Boundary condition for the electron energy equation (temperature if ID = 1), on
		various grid subsets"""


class _T_numerics_bc_1d_ion_charge_state(SpTree):
	"""Boundary conditions for a given charge state related transport equations"""

	z_min  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Minimum Z of the charge state bundle"""

	z_max  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Maximum Z of the charge state bundle"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying charge state (e.g. C+, C+2 , C+3, C+4, C+5, C+6, ...)"""

	vibrational_level  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Vibrational level (can be bundled)"""

	vibrational_mode  :str =  sp_property(type="dynamic")
	""" Vibrational mode of this state, e.g. _A_g_. Need to define, or adopt a standard
		nomenclature."""

	is_neutral  :int =  sp_property(type="dynamic")
	""" Flag specifying if this state corresponds to a neutral (1) or not (0)"""

	neutral_type  :_T_identifier_dynamic_aos3 =  sp_property()
	""" Neutral type (if the considered state is a neutral), in terms of energy. ID =1:
		cold; 2: thermal; 3: fast; 4: NBI"""

	electron_configuration  :str =  sp_property(type="dynamic")
	""" Configuration of atomic orbitals of this state, e.g. 1s2-2s1"""

	particles  :_T_numerics_bc_1d_bc =  sp_property(units="m^-3.s^-1")
	""" Boundary condition for the charge state density equation (density if ID = 1)"""

	energy  :_T_numerics_bc_1d_bc =  sp_property(units="W.m^-3")
	""" Boundary condition for the charge state energy equation (temperature if ID = 1)"""


class _T_numerics_bc_ggd_ion_charge_state(SpTree):
	"""Boundary conditions for a given charge state related transport equations"""

	z_min  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Minimum Z of the charge state bundle"""

	z_max  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Maximum Z of the charge state bundle"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying charge state (e.g. C+, C+2 , C+3, C+4, C+5, C+6, ...)"""

	vibrational_level  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Vibrational level (can be bundled)"""

	vibrational_mode  :str =  sp_property(type="dynamic")
	""" Vibrational mode of this state, e.g. _A_g_. Need to define, or adopt a standard
		nomenclature."""

	is_neutral  :int =  sp_property(type="dynamic")
	""" Flag specifying if this state corresponds to a neutral (1) or not (0)"""

	neutral_type  :_T_identifier_dynamic_aos3 =  sp_property()
	""" Neutral type (if the considered state is a neutral), in terms of energy. ID =1:
		cold; 2: thermal; 3: fast; 4: NBI"""

	electron_configuration  :str =  sp_property(type="dynamic")
	""" Configuration of atomic orbitals of this state, e.g. 1s2-2s1"""

	particles  :AoS[_T_numerics_bc_ggd_bc] =  sp_property(coordinate1="1...N",units="m^-3.s^-1")
	""" Boundary condition for the charge state density equation (density if ID = 1), on
		various grid subsets"""

	energy  :AoS[_T_numerics_bc_ggd_bc] =  sp_property(coordinate1="1...N",units="W.m^-3")
	""" Boundary condition for the charge state energy equation (temperature if ID = 1),
		on various grid subsets"""


class _T_numerics_convergence_equations_ion_charge_state(SpTree):
	"""Boundary conditions for a given charge state related transport equations"""

	z_min  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Minimum Z of the charge state bundle"""

	z_max  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Maximum Z of the charge state bundle"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying charge state (e.g. C+, C+2 , C+3, C+4, C+5, C+6, ...)"""

	vibrational_level  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Vibrational level (can be bundled)"""

	vibrational_mode  :str =  sp_property(type="dynamic")
	""" Vibrational mode of this state, e.g. _A_g_. Need to define, or adopt a standard
		nomenclature."""

	is_neutral  :int =  sp_property(type="dynamic")
	""" Flag specifying if this state corresponds to a neutral (1) or not (0)"""

	neutral_type  :_T_identifier_dynamic_aos3 =  sp_property()
	""" Neutral type (if the considered state is a neutral), in terms of energy. ID =1:
		cold; 2: thermal; 3: fast; 4: NBI"""

	electron_configuration  :str =  sp_property(type="dynamic")
	""" Configuration of atomic orbitals of this state, e.g. 1s2-2s1"""

	particles  :_T_numerics_convergence_equations_single =  sp_property(units="m^-3.s^-1")
	""" Convergence details of the charge state density equation"""

	energy  :_T_numerics_convergence_equations_single =  sp_property(units="W.m^-3")
	""" Convergence details of the charge state energy equation"""


class _T_numerics_convergence_equations_electrons(SpTree):
	"""Convergence details for the electron related equations"""

	particles  :_T_numerics_convergence_equations_single =  sp_property(units="m^-3.s^-1")
	""" Convergence details of the electron density equation"""

	energy  :_T_numerics_convergence_equations_single =  sp_property(units="W.m^-3")
	""" Convergence details of the electron energy equation"""


class _T_numerics_solver_1d_equation(SpTree):
	"""Numeric of a given 1D transport equation"""

	primary_quantity  :_T_numerics_solver_1d_equation_primary =  sp_property()
	""" Profile and derivatives of the primary quantity of the transport equation"""

	computation_mode  :_E_transport_solver_numerics_computation_mode =  sp_property(doc_identifier="transport_solver_numerics/transport_solver_numerics_computation_mode.xml")
	""" Computation mode for this equation"""

	boundary_condition  :AoS[_T_numerics_solver_1d_equation_bc] =  sp_property(coordinate1="1...N")
	""" Set of boundary conditions of the transport equation"""

	coefficient  :AoS[_T_numerics_solver_1d_equation_coefficient] =  sp_property(coordinate1="1...N")
	""" Set of numerical coefficients involved in the transport equation"""

	convergence  :_T_numerics_convergence_equations_single =  sp_property()
	""" Convergence details"""


class _T_numerics_profiles_1d_derivatives(TimeSlice):
	"""Radial profiles derivatives for a given time slice"""

	grid  :_T_core_radial_grid =  sp_property()
	""" Radial grid"""

	electrons  :_T_numerics_profiles_1d_derivatives_electrons =  sp_property()
	""" Quantities related to the electrons"""

	ion  :AoS[_T_numerics_profiles_1d_derivatives_ion] =  sp_property(coordinate1="1...N")
	""" Quantities related to the different ion species"""

	d_drho_tor_norm  :_T_numerics_profiles_1d_derivatives_total_ions =  sp_property()
	""" Derivatives of total ion quantities with respect to the normalised toroidal flux"""

	d2_drho_tor_norm2  :_T_numerics_profiles_1d_derivatives_total_ions =  sp_property()
	""" Second derivatives of total ion quantities with respect to the normalised
		toroidal flux"""

	d_dt  :_T_numerics_profiles_1d_derivatives_total_ions =  sp_property()
	""" Derivatives of total ion quantities with respect to time"""

	dpsi_dt  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",type="dynamic",units="V")
	""" Derivative of the poloidal flux profile with respect to time"""

	dpsi_dt_cphi  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",type="dynamic",units="V")
	""" Derivative of the poloidal flux profile with respect to time, at constant
		toroidal flux"""

	dpsi_dt_crho_tor_norm  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",type="dynamic",units="V")
	""" Derivative of the poloidal flux profile with respect to time, at constant
		normalised toroidal flux coordinate"""

	drho_tor_dt  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",type="dynamic",units="m.s^-1")
	""" Partial derivative of the toroidal flux coordinate profile with respect to time"""

	d_dvolume_drho_tor_dt  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",type="dynamic",units="m^2.s^-1")
	""" Partial derivative with respect to time of the derivative of the volume with
		respect to the toroidal flux coordinate"""

	dpsi_drho_tor  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",type="dynamic",units="Wb.m^-1")
	""" Derivative of the poloidal flux profile with respect to the toroidal flux
		coordinate"""

	d2psi_drho_tor2  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",type="dynamic",units="Wb.m^-2")
	""" Second derivative of the poloidal flux profile with respect to the toroidal flux
		coordinate"""


class _T_numerics_bc_1d_ion(SpTree):
	"""Boundary conditions for a given ion species related transport equations"""

	a  :float =  sp_property(units="Atomic Mass Unit",type="dynamic")
	""" Mass of atom"""

	z_ion  :float =  sp_property(type="dynamic",units="Elementary Charge Unit")
	""" Ion charge (of the dominant ionisation state; lumped ions are allowed)"""

	z_n  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Nuclear charge"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying ion (e.g. H+, D+, T+, He+2, C+, ...)"""

	particles  :_T_numerics_bc_1d_bc =  sp_property(units="m^-3.s^-1")
	""" Boundary condition for the ion density equation (density if ID = 1)"""

	energy  :_T_numerics_bc_1d_bc =  sp_property(units="W.m^-3")
	""" Boundary condition for the ion energy equation (temperature if ID = 1)"""

	multiple_states_flag  :int =  sp_property(type="dynamic")
	""" Multiple states calculation flag : 0-Only one state is considered; 1-Multiple
		states are considered and are described in the state structure"""

	state  :AoS[_T_numerics_bc_1d_ion_charge_state] =  sp_property(coordinate1="1...N")
	""" Quantities related to the different states of the species (ionisation, energy,
		excitation, ...)"""


class _T_numerics_bc_ggd_ion(SpTree):
	"""Boundary conditions for a given ion species related transport equations"""

	a  :float =  sp_property(units="Atomic Mass Unit",type="dynamic")
	""" Mass of atom"""

	z_ion  :float =  sp_property(type="dynamic",units="Elementary Charge Unit")
	""" Ion charge (of the dominant ionisation state; lumped ions are allowed)"""

	z_n  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Nuclear charge"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying ion (e.g. H+, D+, T+, He+2, C+, ...)"""

	particles  :AoS[_T_numerics_bc_ggd_bc] =  sp_property(coordinate1="1...N",units="m^-3.s^-1")
	""" Boundary condition for the ion density equation (density if ID = 1), on various
		grid subsets"""

	energy  :AoS[_T_numerics_bc_ggd_bc] =  sp_property(coordinate1="1...N",units="W.m^-3")
	""" Boundary condition for the ion energy equation (temperature if ID = 1), on
		various grid subsets"""

	multiple_states_flag  :int =  sp_property(type="dynamic")
	""" Multiple states calculation flag : 0-Only one state is considered; 1-Multiple
		states are considered and are described in the state structure"""

	state  :AoS[_T_numerics_bc_ggd_ion_charge_state] =  sp_property(coordinate1="1...N")
	""" Quantities related to the different states of the species (ionisation, energy,
		excitation, ...)"""


class _T_numerics_convergence_equations_ion(SpTree):
	"""Convergence details of a given ion species related transport equations"""

	a  :float =  sp_property(units="Atomic Mass Unit",type="dynamic")
	""" Mass of atom"""

	z_ion  :float =  sp_property(type="dynamic",units="Elementary Charge Unit")
	""" Ion charge (of the dominant ionisation state; lumped ions are allowed)"""

	z_n  :float =  sp_property(units="Elementary Charge Unit",type="dynamic")
	""" Nuclear charge"""

	label  :str =  sp_property(type="dynamic")
	""" String identifying ion (e.g. H+, D+, T+, He+2, C+, ...)"""

	particles  :_T_numerics_convergence_equations_single =  sp_property(units="m^-3.s^-1")
	""" Convergence details of the ion density equation"""

	energy  :_T_numerics_convergence_equations_single =  sp_property(units="W.m^-3")
	""" Convergence details of the ion energy equation"""

	multiple_states_flag  :int =  sp_property(type="dynamic")
	""" Multiple state calculation flag : 0-Only one state is considered; 1-Multiple
		states are considered and are described in the state structure"""

	state  :AoS[_T_numerics_convergence_equations_ion_charge_state] =  sp_property(coordinate1="1...N")
	""" Convergence details of the related to the different states transport equations"""


class _T_numerics_solver_1d(TimeSlice):
	"""Numerics related to 1D radial solver for a given time slice"""

	grid  :_T_core_radial_grid =  sp_property()
	""" Radial grid"""

	equation  :AoS[_T_numerics_solver_1d_equation] =  sp_property(coordinate1="1...N")
	""" Set of transport equations"""

	control_parameters  :_T_numerics_solver_1d_equation_control_parameters =  sp_property()
	""" Solver-specific input or output quantities"""

	drho_tor_dt  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",type="dynamic",units="m.s^-1")
	""" Partial derivative of the toroidal flux coordinate profile with respect to time"""

	d_dvolume_drho_tor_dt  :Expression  =  sp_property(coordinate1="../grid/rho_tor_norm",type="dynamic",units="m^2.s^-1")
	""" Partial derivative with respect to time of the derivative of the volume with
		respect to the toroidal flux coordinate"""


class _T_numerics_bc_1d(TimeSlice):
	"""Boundary conditions of radial transport equations for a given time slice"""

	current  :_T_numerics_bc_1d_current =  sp_property()
	""" Boundary condition for the current diffusion equation."""

	electrons  :_T_numerics_bc_1d_electrons =  sp_property()
	""" Quantities related to the electrons"""

	ion  :AoS[_T_numerics_bc_1d_ion] =  sp_property(coordinate1="1...N")
	""" Quantities related to the different ion species"""

	energy_ion_total  :_T_numerics_bc_1d_bc =  sp_property(units="W.m^-3")
	""" Boundary condition for the ion total (sum over ion species) energy equation
		(temperature if ID = 1)"""

	momentum_tor  :_T_numerics_bc_1d_bc =  sp_property(units="kg.m.s^-1")
	""" Boundary condition for the total plasma toroidal momentum equation (summed over
		ion species and electrons) (momentum if ID = 1)"""


class _T_numerics_bc_ggd(TimeSlice):
	"""Boundary conditions of radial transport equations for a given time slice"""

	grid  :_T_generic_grid_dynamic =  sp_property()
	""" Grid description"""

	current  :AoS[_T_numerics_bc_ggd_current] =  sp_property(coordinate1="1...N")
	""" Boundary condition for the current diffusion equation, on various grid subsets"""

	electrons  :_T_numerics_bc_ggd_electrons =  sp_property()
	""" Quantities related to the electrons"""

	ion  :AoS[_T_numerics_bc_ggd_ion] =  sp_property(coordinate1="1...N")
	""" Quantities related to the different ion species"""


class _T_numerics_convergence_equation(TimeSlice):
	"""Convergence details of a given transport equation"""

	current  :_T_numerics_convergence_equations_single =  sp_property()
	""" Convergence details of the current diffusion equation"""

	electrons  :_T_numerics_convergence_equations_electrons =  sp_property()
	""" Quantities related to the electrons"""

	ion  :AoS[_T_numerics_convergence_equations_ion] =  sp_property(coordinate1="1...N")
	""" Quantities related to the different ion species"""

	energy_ion_total  :_T_numerics_convergence_equations_single =  sp_property(units="W.m^-3")
	""" Convergence details of the ion total (sum over ion species) energy equation"""


class _T_numerics_convergence(SpTree):
	"""Convergence details"""

	time_step  :Signal =  sp_property(units="s")
	""" Internal time step used by the transport solver (assuming all transport
		equations are solved with the same time step)"""

	equations  :TimeSeriesAoS[_T_numerics_convergence_equation] =  sp_property(coordinate1="time",type="dynamic")
	""" Convergence details of the transport equations, for various time slices"""


class _T_transport_solver_numerics(IDS):
	"""Numerical quantities used by transport solvers and convergence details
	lifecycle_status: alpha
	lifecycle_version: 3.1.0
	lifecycle_last_change: 3.22.0"""

	dd_version="v3_38_1_dirty"
	ids_name="transport_solver_numerics"

	time_step  :Signal =  sp_property(units="s")
	""" Internal time step used by the transport solver (assuming all transport
		equations are solved with the same time step)"""

	time_step_average  :Signal =  sp_property(units="s")
	""" Average internal time step used by the transport solver between the previous and
		the current time stored for this quantity (assuming all transport equations are
		solved with the same time step)"""

	time_step_min  :Signal =  sp_property(units="s")
	""" Minimum internal time step used by the transport solver between the previous and
		the current time stored for this quantity (assuming all transport equations are
		solved with the same time step)"""

	solver  :_T_identifier =  sp_property()
	""" Solver identifier"""

	primary_coordinate  :_T_identifier =  sp_property()
	""" Primary coordinate system with which the transport equations are solved. For a
		1D transport solver: index = 1 means rho_tor_norm; 2 = rho_tor."""

	solver_1d  :TimeSeriesAoS[_T_numerics_solver_1d] =  sp_property(coordinate1="time",type="dynamic",cocos_alias="IDSPATH",cocos_replace="transport_solver_numerics.solver_1d{i}")
	""" Numerics related to 1D radial solver, for various time slices."""

	derivatives_1d  :TimeSeriesAoS[_T_numerics_profiles_1d_derivatives] =  sp_property(coordinate1="time",type="dynamic",cocos_alias="IDSPATH",cocos_replace="transport_solver_numerics.derivatives_1d{i}")
	""" Radial profiles derivatives for various time slices. To be removed when the
		solver_1d structure is finalized."""

	boundary_conditions_1d  :TimeSeriesAoS[_T_numerics_bc_1d] =  sp_property(coordinate1="time",type="dynamic")
	""" Boundary conditions of the radial transport equations for various time slices.
		To be removed when the solver_1d structure is finalized."""

	boundary_conditions_ggd  :TimeSeriesAoS[_T_numerics_bc_ggd] =  sp_property(coordinate1="time",type="dynamic")
	""" Boundary conditions of the transport equations, provided on the GGD, for various
		time slices"""

	convergence  :_T_numerics_convergence =  sp_property()
	""" Convergence details To be removed when the solver_1d structure is finalized."""

	vacuum_toroidal_field  :_T_b_tor_vacuum_1 =  sp_property(cocos_alias="IDSPATH",cocos_replace="transport_solver_numerics.vacuum_toroidal_field")
	""" Characteristics of the vacuum toroidal field (used in rho_tor definition and in
		the normalization of current densities)"""

	restart_files  :TimeSeriesAoS[_T_numerics_restart] =  sp_property(coordinate1="time",type="dynamic")
	""" Set of code-specific restart files for a given time slice. These files are
		managed by a physical application to ensure its restart during long simulations"""
