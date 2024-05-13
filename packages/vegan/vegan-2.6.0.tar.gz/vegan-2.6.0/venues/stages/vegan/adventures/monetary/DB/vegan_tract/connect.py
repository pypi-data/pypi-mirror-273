
'''	
	from vegan.adventures.monetary.DB.vegan_tract.connect import connect_to_vegan_tract
	[ driver, vegan_tract_DB ] = connect_to_vegan_tract ()
	driver.close ()
'''

'''
	from vegan.adventures.monetary.DB.vegan_tract.connect import connect_to_vegan_tract
	essential_nutrients_collection = connect_to_vegan_tract () ["essential_nutrients"]	
	essential_nutrients_collection.disconnect ()
'''


'''
	from vegan.adventures.monetary.DB.vegan_tract.connect import connect_to_vegan_tract
	cautionary_ingredients_collection = connect_to_vegan_tract () ["cautionary_ingredients"]	
	cautionary_ingredients_collection.disconnect ()
'''

from vegan.adventures.monetary.moves.URL.retrieve import retreive_monetary_URL
from vegan._essence import retrieve_essence
	
import pymongo

def connect_to_vegan_tract ():
	essence = retrieve_essence ()
	
	#ingredients_DB_name = essence ["monetary"] ["aliases"] ["vegan_tract"]
	ingredients_DB_name = essence ["monetary"] ["databases"] ["vegan_tract"] ["alias"]
	
	monetary_URL = retreive_monetary_URL ()

	driver = pymongo.MongoClient (monetary_URL)

	return [
		driver,
		driver [ ingredients_DB_name ]
	]