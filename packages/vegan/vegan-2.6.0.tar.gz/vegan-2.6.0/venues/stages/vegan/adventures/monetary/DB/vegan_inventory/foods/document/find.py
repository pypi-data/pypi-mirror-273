




'''
	from vegan.adventures.monetary.DB.vegan_inventory.foods.document.find import find_food
	find_food ({
		"filter": {
			"nature.identity.FDC ID": ""
		}
	})
'''



from vegan._essence import retrieve_essence
from vegan.adventures.monetary.DB.vegan_inventory.connect import connect_to_vegan_inventory
from vegan.besties.food_USDA.nature_v2._ops.retrieve import retrieve_parsed_USDA_food
	
import ships.modules.exceptions.parse as parse_exception



	
'''
	FDC_ID = "",
	affiliates = [],
	goodness_certifications = []
'''
def find_food (packet):
	filter = packet ["filter"]

	food = None

	try:
		[ driver, vegan_inventory_DB ] = connect_to_vegan_inventory ()
		food_collection = vegan_inventory_DB ["food"]
	except Exception as E:
		print ("food collection connect:", E)
		raise Exception (E)
	
	try:	
		essence = retrieve_essence ()
		USDA_food_pass = essence ['USDA'] ['food']

		food = food_collection.find_one (filter, {"_id": 0});
		
	except Exception as E:
		print (parse_exception.now (E))
		raise Exception (E)
		
	try:
		driver.close ()
	except Exception as E:
		print (parse_exception.now (E))
		print ("food collection disconnect exception:", E)	
		
	return food;








