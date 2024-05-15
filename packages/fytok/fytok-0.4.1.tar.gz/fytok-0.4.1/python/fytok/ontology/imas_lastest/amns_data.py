"""
  This module containes the _FyTok_ wrapper of IMAS/dd/amns_data
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    
from .utilities import _T_plasma_composition_neutral_element_constant,_T_identifier

class _T_amns_data_data_entry(SpTree):
	"""Definition of a given AMNS data entry"""

	description  :str =  sp_property(type="static")
	""" Description of this data entry"""

	shot  :int =  sp_property(type="static")
	""" Shot number = Mass*1000+Nuclear_charge"""

	run  :int =  sp_property(type="static")
	""" Which run number is the active run number for this version"""


class _T_amns_data_process_charge_state(SpTree):
	"""Process tables for a given charge state. Only one table is used for that
		process, defined by process(:)/table_dimension"""

	label  :str =  sp_property(type="static")
	""" String identifying charge state (e.g. C+, C+2 , C+3, C+4, C+5, C+6, ...)"""

	z_min  :float =  sp_property(units="Elementary Charge Unit",type="static")
	""" Minimum Z of the charge state bundle"""

	z_max  :float =  sp_property(units="Elementary Charge Unit",type="static")
	""" Maximum Z of the charge state bundle (equal to z_min if no bundle)"""

	table_0d  :float =  sp_property(type="static",units="units given by process(:)/results_units")
	""" 0D table describing the process data"""

	table_1d  :array_type =  sp_property(type="static",units="units given by process(i1)/results_units",coordinate1="../../../coordinate_system(process(i1)/coordinate_index)/coordinate(1)")
	""" 1D table describing the process data"""

	table_2d  :array_type =  sp_property(type="static",units="units given by process(i1)/results_units",coordinate1="../../../coordinate_system(process(i1)/coordinate_index)/coordinate(1)",coordinate2="../../../coordinate_system(process(i1)/coordinate_index)/coordinate(2)")
	""" 2D table describing the process data"""

	table_3d  :array_type =  sp_property(type="static",units="units given by process(:)/results_units",coordinate1="../../../coordinate_system(process(i1)/coordinate_index)/coordinate(1)",coordinate2="../../../coordinate_system(process(i1)/coordinate_index)/coordinate(2)",coordinate3="../../../coordinate_system(process(i1)/coordinate_index)/coordinate(3)")
	""" 3D table describing the process data"""

	table_4d  :array_type =  sp_property(type="static",units="units given by process(i1)/results_units",coordinate1="../../../coordinate_system(process(i1)/coordinate_index)/coordinate(1)",coordinate2="../../../coordinate_system(process(i1)/coordinate_index)/coordinate(2)",coordinate3="../../../coordinate_system(process(i1)/coordinate_index)/coordinate(3)",coordinate4="../../../coordinate_system(process(i1)/coordinate_index)/coordinate(4)")
	""" 4D table describing the process data"""

	table_5d  :array_type =  sp_property(type="static",units="units given by process(i1)/results_units",coordinate1="../../../coordinate_system(process(i1)/coordinate_index)/coordinate(1)",coordinate2="../../../coordinate_system(process(i1)/coordinate_index)/coordinate(2)",coordinate3="../../../coordinate_system(process(i1)/coordinate_index)/coordinate(3)",coordinate4="../../../coordinate_system(process(i1)/coordinate_index)/coordinate(4)",coordinate5="../../../coordinate_system(process(i1)/coordinate_index)/coordinate(5)")
	""" 5D table describing the process data"""

	table_6d  :array_type =  sp_property(type="static",units="units given by process(i1)/results_units",coordinate1="../../../coordinate_system(process(i1)/coordinate_index)/coordinate(1)",coordinate2="../../../coordinate_system(process(i1)/coordinate_index)/coordinate(2)",coordinate3="../../../coordinate_system(process(i1)/coordinate_index)/coordinate(3)",coordinate4="../../../coordinate_system(process(i1)/coordinate_index)/coordinate(4)",coordinate5="../../../coordinate_system(process(i1)/coordinate_index)/coordinate(5)",coordinate6="../../../coordinate_system(process(i1)/coordinate_index)/coordinate(6)")
	""" 6D table describing the process data"""


class _T_amns_data_coordinate_system_coordinate(SpTree):
	"""Description of a coordinate for atomic data tables. Can be either a range of
		real values or a set of discrete values (if interp_type=0)"""

	label  :str =  sp_property(type="static")
	""" Description of coordinate (e.g. _Electron temperature_)"""

	values  :array_type =  sp_property(units="units given by coordinate_system(:)/coordinate(:)/units",coordinate1="1...N",type="static")
	""" Coordinate values"""

	interpolation_type  :int =  sp_property(type="static")
	""" Interpolation strategy in this coordinate direction. Integer flag: 0=discrete
		(no interpolation); 1=linear; ..."""

	extrapolation_type  :array_type =  sp_property(coordinate1="1...2",type="static")
	""" Extrapolation strategy when leaving the domain. The first value of the vector
		describes the behaviour at lower bound, the second describes the at upper bound.
		Possible values: 0=none, report error; 1=boundary value; 2=linear extrapolation"""

	value_labels  :List[str] =  sp_property(coordinate1="../values",type="static")
	""" String description of discrete coordinate values (if interpolation_type=0).
		E.g., for spectroscopic lines, the spectroscopic description of the transition."""

	units  :str =  sp_property(type="static")
	""" Units of coordinate (e.g. eV)"""

	transformation  :int =  sp_property(type="static")
	""" Coordinate transformation applied to coordinate values stored in coord. Integer
		flag: 0=none; 1=log10; 2=ln"""

	spacing  :int =  sp_property(type="static")
	""" Flag for specific coordinate spacing (for optimization purposes). Integer flag:
		0=undefined; 1=uniform; ..."""


class _T_amns_data_release(SpTree):
	"""Definition of a given release of an AMNS data release"""

	description  :str =  sp_property(type="static")
	""" Description of this release"""

	date  :str =  sp_property(type="static")
	""" Date of this release"""

	data_entry  :AoS[_T_amns_data_data_entry] =  sp_property(coordinate1="1...N")
	""" For this release, list of each data item (i.e. shot/run pair containing the
		actual data) included in this release"""


class _T_amns_data_process_reactant(SpTree):
	"""Process reactant or product definition"""

	label  :str =  sp_property(type="static")
	""" String identifying reaction participant (e.g. _D_, _e_, _W_, _CD4_, _photon_,
		_n_)"""

	element  :AoS[_T_plasma_composition_neutral_element_constant] =  sp_property(coordinate1="1...N")
	""" List of elements forming the atom (in such case, this array should be of size 1)
		or molecule. Mass of atom and nuclear charge should be set to 0 for photons and
		electrons. The mass of atom shouldn't be set for an atomic process that is not
		isotope dependent."""

	role  :_T_identifier =  sp_property()
	""" Identifier for the role of this paricipant in the reaction. For surface
		reactions distinguish between projectile and wall."""

	mass  :float =  sp_property(units="Atomic Mass Unit",type="static")
	""" Mass of the participant"""

	charge  :float =  sp_property(units="-",type="static")
	""" Charge number of the participant"""

	relative_charge  :int =  sp_property(type="static")
	""" This is a flag indicating that charges are absolute (if set to 0), relative (if
		1) or irrelevant (-1); relative would be used to categorize the ionization
		reactions from i to i+1 for all charge states; in the case of bundles, the +1
		relative indicates the next bundle"""

	multiplicity  :float =  sp_property(units="-",type="static")
	""" Multiplicity in the reaction"""

	metastable  :List[int] =  sp_property(coordinate1="1...N",type="static")
	""" An array identifying the metastable; if zero-length, then not a metastable; if
		of length 1, then the value indicates the electronic level for the metastable
		(mostly used for atoms/ions); if of length 2, then the 1st would indicate the
		electronic level and the second the vibrational level for the metastable (mostly
		used for molecules and molecular ions); if of length 3, then the 1st would
		indicate the electronic level, the second the vibrational level and the third
		the rotational level for the metastable (mostly used for molecules and molecular
		ions)"""

	metastable_label  :str =  sp_property(type="static")
	""" Label identifying in text form the metastable"""


class _T_amns_data_coordinate_system(SpTree):
	"""Description of a coordinate system for atomic data tables"""

	coordinate  :AoS[_T_amns_data_coordinate_system_coordinate] =  sp_property(coordinate1="1...N")
	""" Set of coordinates for that coordinate system. A coordinate an be either a range
		of real values or a set of discrete values (if interpolation_type=0)"""


class _T_amns_data_process(SpTree):
	"""Definition of a process and its data"""

	source  :str =  sp_property(type="static")
	""" Filename or subroutine name used to provide this data"""

	provider  :str =  sp_property(type="static")
	""" Name of the person in charge of producing this data"""

	citation  :str =  sp_property(type="static")
	""" Reference to publication(s)"""

	label  :str =  sp_property(type="static")
	""" String identifying the process (e.g. EI, RC, ...)"""

	reactants  :AoS[_T_amns_data_process_reactant] =  sp_property(coordinate1="1...N")
	""" Set of reactants involved in this process"""

	products  :AoS[_T_amns_data_process_reactant] =  sp_property(coordinate1="1...N")
	""" Set of products resulting of this process"""

	table_dimension  :int =  sp_property(type="static")
	""" Table dimensionality of the process (1 to 6), valid for all charge states.
		Indicates which of the tables is filled (below the charge_state node)"""

	coordinate_index  :int =  sp_property(type="static")
	""" Index in tables_coord, specifying what coordinate systems to use for this
		process (valid for all tables)"""

	result_label  :str =  sp_property(type="static")
	""" Description of the process result (rate, cross section, sputtering yield, ...)"""

	result_units  :str =  sp_property(type="static")
	""" Units of the process result"""

	result_transformation  :int =  sp_property(type="static")
	""" Transformation of the process result. Integer flag: 0=no transformation; 1=10^;
		2=exp()"""

	charge_state  :AoS[_T_amns_data_process_charge_state] =  sp_property(coordinate1="1...N")
	""" Process tables for a set of charge states. Only one table is used for that
		process, defined by process(:)/table_dimension"""


class _T_amns_data(IDS):
	"""Atomic, molecular, nuclear and surface physics data. Each occurrence contains
		the data for a given element (nuclear charge), describing various physical
		processes. For each process, data tables are organized by charge states. The
		coordinate system used by the data tables is described under the
		coordinate_system node.
	lifecycle_status: alpha
	lifecycle_version: 3.0.0
	lifecycle_last_change: 3.21.0"""

	dd_version="v3_38_1_dirty"
	ids_name="amns_data"

	z_n  :float =  sp_property(units="Elementary Charge Unit",type="static")
	""" Nuclear charge"""

	a  :float =  sp_property(units="Atomic Mass Unit",type="static")
	""" Mass of atom"""

	process  :AoS[_T_amns_data_process] =  sp_property(coordinate1="1...N")
	""" Description and data for a set of physical processes."""

	coordinate_system  :AoS[_T_amns_data_coordinate_system] =  sp_property(coordinate1="1...N")
	""" Array of possible coordinate systems for process tables"""

	release  :AoS[_T_amns_data_release] =  sp_property(coordinate1="1...N")
	""" List of available releases of the AMNS data; each element contains information
		about the AMNS data that is included in the release. This part of the IDS is
		filled and stored only into shot/run=0/1, playing the role of a catalogue."""
