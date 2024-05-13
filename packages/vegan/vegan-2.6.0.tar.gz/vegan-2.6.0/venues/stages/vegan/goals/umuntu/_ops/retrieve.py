
'''
	from vegan.goals.umuntu._ops.retrieve import retrieve_umutu_goal
	goal = retrieve_umutu_goal ({
		"region": region
	})
'''

from vegan.adventures.monetary.DB.vegan_tract.goals.retrieve_one import retrieve_one_goal

def retrieve_umutu_goal (packet):
	ingredient_doc = retrieve_one_goal ({
		"region": packet ["region"]
	})
	
	return ingredient_doc