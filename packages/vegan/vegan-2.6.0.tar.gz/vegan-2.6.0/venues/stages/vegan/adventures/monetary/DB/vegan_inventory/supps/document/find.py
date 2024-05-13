







'''
	from vegan.adventures.monetary.DB.vegan_inventory.supps.document.find import find_supp
	find_supp ({
		"filter": {
			"nature.identity.FDC ID": ""
		}
	})
'''



from vegan._essence import retrieve_essence
from vegan.adventures.monetary.DB.vegan_inventory.connect import connect_to_vegan_inventory
from vegan.besties.supp_NIH.nature_v2._ops.retrieve import retrieve_parsed_NIH_supp
	
import ships.modules.exceptions.parse as parse_exception



	
'''
	DSLD_ID = "",
	affiliates = [],
	goodness_certifications = []
'''
def find_supp (packet):
	filter = packet ["filter"]

	supp = None

	try:
		[ driver, vegan_inventory_DB ] = connect_to_vegan_inventory ()
		collection = vegan_inventory_DB ["supp"]
	except Exception as E:
		print ("supp collection connect:", E)
		raise Exception (E)
	
	try:	
		essence = retrieve_essence ()
		supp = collection.find_one (filter, {"_id": 0});
		
	except Exception as E:
		print (parse_exception.now (E))
		raise Exception (E)
		
	try:
		driver.close ()
	except Exception as E:
		print (parse_exception.now (E))
		print ("supp collection disconnect exception:", E)	
		
	return supp;








