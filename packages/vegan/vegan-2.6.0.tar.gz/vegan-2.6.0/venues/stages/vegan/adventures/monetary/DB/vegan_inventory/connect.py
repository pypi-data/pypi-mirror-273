


'''	
	from vegan.adventures.monetary.DB.vegan_inventory.connect import connect_to_vegan_inventory
	[ driver, vegan_inventory_DB ] = connect_to_vegan_inventory ()
	driver.close ()
'''

'''
	from vegan.adventures.monetary.DB.vegan_inventory.connect import connect_to_vegan_inventory
	[ driver, vegan_inventory_DB ] = connect_to_vegan_inventory ()
	foods_collection = vegan_inventory_DB ["foods"]	
	foods_collection.close ()
'''




from vegan.adventures.monetary.moves.URL.retrieve import retreive_monetary_URL
from vegan._essence import retrieve_essence
	
import pymongo

def connect_to_vegan_inventory ():
	essence = retrieve_essence ()
	
	ingredients_DB_name = essence ["monetary"] ["databases"] ["vegan_inventory"] ["alias"]
	
	monetary_URL = retreive_monetary_URL ()

	driver = pymongo.MongoClient (monetary_URL)

	return [
		driver,
		driver [ ingredients_DB_name ]
	]