"""
  This module containes the _FyTok_ wrapper of IMAS/dd/dataset_fair
  Generate at 2023-10-17T11:53:10.881387+08:00
  FyTok (rev: 0.0.0) 
 
"""

from ...modules.Utilities import *

    

class _T_dataset_fair(IDS):
	"""FAIR metadata related to the dataset, providing inforrmation on licensing,
		annotations, references using this dataset, versioning and validity, provenance.
		This IDS is using Dublin Core metadata standard whenever possible
	lifecycle_status: alpha
	lifecycle_version: 3.30.0
	lifecycle_last_change: 3.30.0"""

	dd_version="v3_38_1_dirty"
	ids_name="dataset_fair"

	identifier  :str =  sp_property(type="constant")
	""" Persistent identifier allowing to cite this data in a public and persistent way,
		should be provided as HTTP URIs"""

	replaces  :str =  sp_property(type="constant")
	""" Persistent identifier referencing the previous version of this data"""

	is_replaced_by  :str =  sp_property(type="constant")
	""" Persistent identifier referencing the new version of this data (replacing the
		present version)"""

	valid  :str =  sp_property(type="constant")
	""" Date range during which the data is or was valid. Expressed as
		YYYY-MM-DD/YYYY-MM-DD, where the former (resp. latter) date is the data at which
		the data started (resp. ceased) to be valid. If the data is still valid, the
		slash should still be present, i.e. indicate the validity start date with
		YYYY-MM-DD/. If the data ceased being valid but there is no information on the
		validity start date, indicate /YYYY-MM-DD."""

	rights_holder  :str =  sp_property(type="constant")
	""" The organisation owning or managing rights over this data"""

	license  :str =  sp_property(type="constant")
	""" License(s) under which the data is made available (license description or, more
		convenient, publicly accessible URL pointing to the full license text)"""

	is_referenced_by  :List[str] =  sp_property(type="constant",coordinate1="1...N")
	""" List of documents (e.g. publications) or datasets making use of this data entry
		(e.g. PIDs of other datasets using this data entry as input)"""
