

'''
	from vegan.adventures.monetary.DB.vegan_inventory._treasures._indexes.drop_and_create import drop_and_create_treasures_indexes
	drop_and_create_treasures_indexes ({
		"collection": "foods"
	})
'''



from vegan.adventures.alerting.parse_exception import parse_exception
from vegan.adventures.alerting import activate_alert
from vegan.adventures.monetary.DB.vegan_inventory.connect import connect_to_vegan_inventory
	
	
def drop_and_create_treasures_indexes (packet):
	collection_name = packet ["collection"]

	[ driver, vegan_inventory_DB ] = connect_to_vegan_inventory ()
	the_collection = vegan_inventory_DB [ collection_name ]

	try:
		proceeds = the_collection.drop_indexes ()
	except Exception as E:
		activate_alert ("emergency", {
			"exception": parse_exception (E)
		})
		
	proceeds = the_collection.create_index ( 
		[( "nature.identity.UPC", 1 )],
		name = "name = nature.identity.UPC"
	)
	
	activate_alert ("info", {
		"proceeds of index create": proceeds
	}, mode = "pprint")
	
	driver.close ()