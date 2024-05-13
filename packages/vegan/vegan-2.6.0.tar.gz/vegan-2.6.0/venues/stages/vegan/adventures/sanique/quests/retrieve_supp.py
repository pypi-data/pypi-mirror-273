
import law_dictionary

from vegan.adventures.monetary.DB.vegan_inventory.supps.document.find import find_supp

def retrieve_supp_quest (packet):


	freight = packet ["freight"]
	
	report_freight = law_dictionary.check (
		return_obstacle_if_not_legit = True,
		allow_extra_fields = True,
		laws = {
			"filters": {
				"required": True,
				"type": dict
			}
		},
		dictionary = freight 
	)
	if (report_freight ["advance"] != True):
		return {
			"label": "unfinished",
			"freight": {
				"obstacle": report_freight,
				"obstacle number": 2
			}
		}
		
	filters = freight ["filters"]
	report_filters = law_dictionary.check (
		return_obstacle_if_not_legit = True,
		allow_extra_fields = True,
		laws = {
			"emblem": {
				"required": True,
				"type": str
			}
		},
		dictionary = filters 
	)
	if (report_filters ["advance"] != True):
		return {
			"label": "unfinished",
			"freight": {
				"obstacle": report_filters,
				"obstacle number": 3
			}
		}
	

	try:
		if ("emblem" in filters):
			filters ["emblem"] = int (filters ["emblem"])
	except Exception:	
		return {
			"label": "unfinished",
			"freight": {
				"description": "The emblem couldn't be converted to an integer.",
				"obstacle number": 4
			}
		}
	

	supp = find_supp ({
		"filter": filters
	})
	
	
	return {
		"label": "finished",
		"freight": supp
	}